'''
Created on Apr 8, 2018
@author: fan
'''

import copy
import os.path

import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

import analyze.analyzesteady as analyzesteady
import estimation.estimate_objective as estiobjective
import estimation.moments.momcomp as moments
import estimation.postprocess.jsoncsv.gen_agg_csv_from_json as gen_csvaggjson
import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.paraminstpreset as param_inst_preset
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.hardcode.str_estimation as hardcode_estimation
import projectsupport.hardcode.str_periodkey as hardcode_periodkey
import projectsupport.systemsupport as proj_sys_sup
import soluequi.param_loop as soluequipartial

logger = logging.getLogger(__name__)


def estimate_objective_multiperiods(
        params_esti, param_esti_group_key_list,
        moments_type=['a', '20180724_test'], use_states_data=False, use_likelihood=False,
        combo_type='', param_combo='',
        compesti_specs=None,
        ge=False, multiprocess=False,
        graph_list=None,
        save_directory='estisubdirectory',
        logger=None,
        **kwargs):
    """
    
    Examples
    --------
    import estimation.estimate_objective_multiperiods as estiobjmulti    
    """
    if (logger is not None):
        logger.info(f'{params_esti=}')
        logger.info(f'{param_esti_group_key_list=}')

    period_keys_esti_set = kwargs['period_keys_esti_set']

    '''
    A, Estimation moments and moment match groups    
    '''
    moments_type = compesti_specs['moments_type']
    momsets_type = compesti_specs['momsets_type']
    moments_data, momsets, momsets_graphing = moments.get_moments_momsets(moments_type, momsets_type)

    '''
    B1. Collect moments across periods
    '''
    param_dict_moments_list = []

    '''
    B2a, loop over periods    
    '''
    param_inst = param_inst_preset.get_param_inst_preset_combo(param_combo)

    '''
    B2c, estimate actually solving model
    '''
    esti_obj_sum = 0
    paramstr_dict = paramloopstr.param2str()
    for period in period_keys_esti_set:

        '''
        B2b, estimate with multivariate polynomial approximation
        '''
        try_this = True
        if compesti_specs['memory'] == '517' or compesti_specs['bl_mpoly_approx']:
            '''
            this is: fargate_mpoly_1vcpu, compute_specs:l278
            Only save top results in panda csv, otherwise saving too many things
            '''
            panda_df_save_best = True
            s3_status = False

            '''
            Generate param_dict_moments
            '''
            simu_moments_output = mpoly_predict_moment(param_esti_group_key_list,
                                                       params_esti,
                                                       period,
                                                       combo_type, param_combo,
                                                       compesti_specs,
                                                       logger)

            '''
            Generate param_dict_moments
            '''
            file_save_suffix = param_combo['file_save_suffix']
            json_directory = proj_sys_sup.get_paths(save_directory, sub_folder_name='json')

            integrated = False
            if ('_ITG_' in combo_type[1]):
                integrated = True

            file_save_suffix = file_save_suffix + '_' + \
                               proj_sys_sup.save_suffix_time(2) + \
                               proj_hardcode_filename.file_suffix(
                                   equilibrium=ge, integrated=integrated)['exo_or_endo_graph_row_select']

            # export_json file saved later, do not save here, file conflict otherwise
            export_json = False

            '''
            Update param_inst
            '''
            for param_ctr, param_esti_group_key in enumerate(param_esti_group_key_list):
                param_val = params_esti[param_ctr]
                param_inst = paramloopstr.update_param_inst(param_inst, param_esti_group_key, param_val)

            '''
            Predict Moments Again
            '''
            param_dict_moments = analyzesteady.gen_param_dict_moment(param_inst,
                                                                     simu_moments_output,
                                                                     file_save_suffix,
                                                                     json_directory,
                                                                     export_json=export_json)

        else:
            '''
            Save all results! Not simulating this that many times fully, need to keep all
            '''
            panda_df_save_best = False
            s3_status = True

            '''
            B3. Get all potential period specific keys, and what these keys should translate to
            in terms of standard simulation parameters
            '''
            period_keys, period_keys_trans = paramloopstr.period_vars(period=period,
                                                                      param_esti_group_key_list=param_esti_group_key_list)

            '''
            B4. Replace the string name of the estimation key by their translated normal simulation
            key. If do not replace, the estimationkey with the period suffix has no impact on simulation. 
            By replacing, the value in estimation key with period suffix is now associated with the standard
            non-period specific version of the key.
            '''
            param_esti_group_key_list_copy = copy.deepcopy(param_esti_group_key_list)
            params_esti_copy = copy.deepcopy(params_esti)
            for period_key_ctr, period_key in enumerate(period_keys):

                '''
                not_found_period_key_in_esti:
                this means if period key not found in esti, still need to add them to 
                param_esti and key_list because need to update the non-period specific key
                with period specific values.
                '''
                not_found_period_key_in_esti = True
                for param_ctr, param_esti in enumerate(param_esti_group_key_list):
                    param_key = paramloopstr.param_type_param_name(param_group_key=param_esti,
                                                                   return_param_key=True)
                    if (param_key == period_key):
                        not_found_period_key_in_esti = False
                        param_type_param_name = paramstr_dict[period_keys_trans[period_key_ctr]][1]
                        param_esti_group_key_list_copy.append(param_type_param_name)
                        params_esti_copy = np.append(params_esti_copy, params_esti[param_ctr])

                '''
                If not estimating region specific var, still update
                '''
                if (not_found_period_key_in_esti):

                    param_type_param_name = paramstr_dict[period_keys_trans[period_key_ctr]][1]
                    param_val, __, __ = \
                        paramloopstr.get_current_init_param_values(paramstr_dict[period_key][1], param_inst)

                    if (param_val is not None):
                        '''
                        only none for: data__A_params_mu_ce9901', 'data__A_params_sd_ce9901
                            these parameters when estimating without integration do not exist
                        '''
                        param_esti_group_key_list_copy.append(param_type_param_name)
                        params_esti_copy = np.append(params_esti_copy, param_val)

            '''
            B5. Solve now period specific model with period specific parameter
            '''
            return_type = 'combo_list_results'
            combo_list_results = estiobjective.estimate_objective(
                params_esti_copy, param_esti_group_key_list_copy,
                moments_type=moments_type, use_states_data=use_states_data, use_likelihood=use_likelihood,
                combo_type=combo_type, param_combo=param_combo,
                compesti_specs=compesti_specs,
                return_type=return_type,
                ge=ge, multiprocess=multiprocess,
                graph_list=graph_list,
                save_directory=save_directory,
                logger=logger)

            '''
            B6. Get moments data
            '''
            wgtJ_out_dict = combo_list_results['wgtJ_out_dict']
            simu_moments_output = wgtJ_out_dict['simu_moments_output']
            param_dict_moments = wgtJ_out_dict['param_dict_moments']

        '''
        B7. Compare model and data moments to generate estimation objective when there are
        multiple periods
            - period specific data
            - compare
        '''
        dictkey = paramloopstr.peristr(period=period, action='dictkey')
        moments_data_cur_period = moments_data[dictkey]
        moments_dict = moments.compare_moments_direct(model_moments=simu_moments_output,
                                                      moments_data=moments_data_cur_period,
                                                      momsets=momsets,
                                                      momsets_graphing=momsets_graphing)
        simu_moments_output['esti_obj'] = moments_dict

        '''
        B8. Update param_dict with moments and keys with simu_moments_output
        '''
        param_dict_moments.update(simu_moments_output)

        '''
        B9. Append to Moments Collection
        '''
        param_dict_moments_list.append(param_dict_moments)

        '''
        B10. Overall Objective
        '''
        esti_obj_sum = esti_obj_sum + moments_dict['main_obj']

    '''
    C0. Replace Existing json Files
        add current moment and overall moment to each json
    '''
    for ctr, period in enumerate(period_keys_esti_set):
        '''
        C1. Refresh, Resave Json File
        '''
        period_dictkey = paramloopstr.peristr(period=period, action='dictkey')
        param_dict_moments = param_dict_moments_list[ctr]

        param_dict_moments['esti_obj']['main_allperiods_obj'] = esti_obj_sum
        param_dict_moments['period_dictkey'] = period_dictkey

        json_directory = param_dict_moments['json_directory']
        json_file_name = param_dict_moments['json_file_name']

        '''
        s3=False, do not push json to s3, csv at the end is enough. 
        this doubles mpoly ec2 estimate time potentially. 
        '''
        proj_sys_sup.save_json(json_directory + json_file_name,
                               param_dict_moments, replace=True,
                               s3=s3_status)

    obj = esti_obj_sum

    combo_list = [param_combo]
    compute_specs = compesti_specs

    '''
    Exit if reach max, the function below will raise an exception
    '''
    integrated = False
    if ('_ITG_' in combo_type[1]):
        integrated = True
    exo_or_endo_json_search = proj_hardcode_filename.file_suffix(equilibrium=ge, integrated=integrated)[
        'exo_or_endo_json_search']
    save_directory_dict = {}
    save_directory_dict['json'] = proj_sys_sup.get_paths(save_directory, sub_folder_name='json')
    save_directory_dict['img_main'] = save_directory
    save_directory_dict['csv'] = save_directory
    export_agg_json_csv = soluequipartial.export_agg_json_or_not(graph_list,
                                                                 compute_specs,
                                                                 save_directory_dict,
                                                                 combo_type,
                                                                 exo_or_endo_json_search)

    if (export_agg_json_csv == 'EXCEPTION') or (export_agg_json_csv) == True:
        compute_specs = compesti_specs
        gen_csvaggjson.gen_agg_csv_from_json(combo_type, param_combo,
                                             ge, compute_specs,
                                             save_directory_dict,
                                             graph_list,
                                             panda_df_save_best)
    if export_agg_json_csv == 'EXCEPTION':
        raise Exception("Max Iteration Allowed Reached. estimate_objective_multiperiod")

    return obj


def mpoly_predict_moment(param_esti_group_key_list, params_esti,
                         period_key,
                         combo_type, param_combo,
                         compesti_specs,
                         logger):
    """
    Check locally, EC2 or own computer if the file is there
    d_root = proj_sys_sup.s3_local_sync_folder()
    bucket_name = proj_sys_sup.s3_bucket_name()

    This assumes that there is already an mpoly file in the /data/ folder on EC2 or on something like
    G:/S3/thaijmp202010, or D:/repos/ThaiJMP locally.

    So on EC2, need to make sure the mpoly_reg_coef file is already uploaded into the docker container data
    folder.

    1. check if file is saved locally
    2. grab file from S3 if not saved locally
    3. load locally
    """
    if (logger is not None):
        logger.debug('combo_type:\n%s', combo_type)
        logger.info('param_combo:\n%s', param_combo)

    folder_file_name = proj_hardcode_filename.get_path_to_mpoly_reg_coef(
        combo_type, main_folder_name=compesti_specs['save_directory_main'])

    exist_local = False
    if (os.path.isfile(folder_file_name)):
        exist_local = True

    if (exist_local == False):
        '''
        2a. Load from S3 if not here, and save locally 
        '''
        proj_sys_sup.s3_download(local_download_to_directory_file=folder_file_name)

    '''
    3 load file
    '''
    if (logger is not None):
        logger.info('mpoly_reg_coef-folder_file_name:\n%s', folder_file_name)

    mpoly_reg_coef = proj_sys_sup.read_csv(csv_file_folder=folder_file_name)

    for ctr in np.arange(559 + 1):
        if (ctr == 0):
            cols_sorted = ['const']
        else:
            cols_sorted.append('x' + str(ctr))

    if (logger is not None):
        logger.debug('X linear names, param_group_key_list:\n%s', param_esti_group_key_list)
        logger.debug('X linear, params_esti:\n%s', params_esti)

    mpoly_coef_list = []
    counter = 0
    unique_periodkey = hardcode_periodkey.region_time_dict(True)[period_key]
    if (logger is not None):
        logger.info('unique_periodkey:\n%s', unique_periodkey)
    counter = counter + 1

    all_feasible_key_list = hardcode_periodkey.period_key_list()

    columns_rhs_dict = {}
    for param_ctr, columns in enumerate(param_esti_group_key_list):
        if (unique_periodkey in columns):
            '''
            Includes current relevant key
            '''
            columns_rhs_dict[columns] = params_esti[param_ctr]
        elif (any([key in columns for key in all_feasible_key_list])):
            '''
            Includes coefficients for other periods
            '''
            pass
        else:
            '''
            not time specific variables
            '''
            columns_rhs_dict[columns] = [params_esti[param_ctr]]

    if (logger is not None):
        logger.info('X linear dict, columns_rhs_dict:\n%s', columns_rhs_dict)

    # df_columns_rhs = pd.DataFrame(columns_rhs_dict, columns=columns_rhs_dict.keys())
    df_columns_rhs = pd.DataFrame(columns_rhs_dict, columns=columns_rhs_dict.keys(), index=[1])
    if (logger is not None):
        logger.info('X linear df, df_columns_rhs:\n%s', df_columns_rhs)

    poly = PolynomialFeatures(3)
    X = poly.fit_transform(df_columns_rhs)
    if (logger is not None):
        logger.info('X mpoly, X:\n%s', X)
        logger.info('X mpoly, X.shape:\n%s', X.shape)

    '''
    Get Mpoly coefficients
    '''
    period_dictkey = hardcode_estimation.esti_predict_moment_csv()['period_dictkey']['str']
    moment_lhs_str = hardcode_estimation.esti_predict_moment_csv()['moment_lhs']['str']
    cur_select = (mpoly_reg_coef[period_dictkey] == unique_periodkey)

    cols_sorted = [col for col in mpoly_reg_coef.columns if 'x' in col]
    cols_sorted.insert(0, 'const')

    mpoly_reg_coef_sorted_multiobj = mpoly_reg_coef[cur_select][cols_sorted]
    if (logger is not None):
        logger.info('beta mat mpoly shape, mpoly_reg_coef_sorted_multiobj.shape:\n%s',
                    mpoly_reg_coef_sorted_multiobj.shape)
        logger.info('beta mat mpoly, mpoly_reg_coef_sorted_multiobj.values:\n%s',
                    mpoly_reg_coef_sorted_multiobj.values)

    '''
    Predict Moments
    '''
    predict_obj = np.matmul(X, np.transpose(mpoly_reg_coef_sorted_multiobj.values))
    if (logger is not None):
        logger.debug('predict_obj:\n%s', predict_obj)

    '''
    Which moments were predicted? all rows that satisfied: mpoly_reg_coef[cur_select]
    '''
    moment_lhs = mpoly_reg_coef[cur_select][moment_lhs_str]
    if (logger is not None):
        logger.debug('moment_lhs:\n%s', list(moment_lhs.values))

    simu_moments_output = {}
    for ctr, cur_moment in enumerate(moment_lhs.values):
        simu_moments_output[cur_moment] = predict_obj[0, ctr]

    if (logger is not None):
        logger.info('x times beta, simu_moments_output:\n%s', simu_moments_output)

    return simu_moments_output
