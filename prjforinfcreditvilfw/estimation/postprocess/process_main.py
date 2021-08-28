'''
Created on Aug 14, 2018

@author: fan

GIVEN ESTIMATION RESULTS PROCESSING

Compare estimation results from many initial values and different estimation methods

Same data, same objective. Using AWS

- data structure:
  + the csv results include period_dict_key
  + moments do not have priod_dict_key appended
  + the data moments are in a nested dict where each period_dict_key has a dict with regular moment keys
- so, given the panda file that includes the top N*2 number of Results
  + loop over the list of period_dict_keys
  + within each loop, grab out the subset of raws from panda that is for this period
  + within each loop, grab out the nested moment keys
  + now these share the same keys
- output:
  + perhaps easiest thing is to generate two csv files
  + each column and row the same as saved main csv files
  + include only key moments columns
  + add a row for data
  + add a column to distinguish between data moment and simu moments
  + which subset of moments to include?
    - all that is in the initial csv file, but order columns so that:
      - first column = time key
      - second column = data or model
      - next set = the moments that exist in model and data
        + perhaps include mean and variance both.
      - next set = all other moments.
  + results from both periods should be compiled together into one CSV, that is the one to save

'''

import logging
import numpy as np
# import pandas.io.combine as pd_combine
import pyfan.panda.inout.combine as pd_combine

import analyze.analyzeequi as analyzeequi
import estimation.moments.momcomp as momcomp
import estimation.postprocess.jsoncsv.gen_predict_more_points as gen_predict
import estimation.postprocess.jsoncsv.gen_simu_params as gen_simu_params
import estimation.postprocess.jsoncsv.gen_top_estimates_df as top_estimate
import estimation.postprocess.jsoncsv.gen_update_objectiv as esti_update_obj
import estimation.postprocess.texdo.texdo_manage as gen_tex
import invoke.combo_type_list_wth_specs as paramcombospecs
import parameters.combo as paramcombo
import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def search_combine_indi_esti(paramstr_key_list,
                             combo_type_list_ab,
                             combo_type_list_date, esti_spec_key,
                             moment_key=0, momset_key=1,
                             exo_or_endo_graph_row_select='_exo_wgtJ',
                             image_save_name_prefix='AGG_ALLESTI_',
                             search_directory=None,
                             fils_search_str=None,
                             save_file_name=None,
                             save_panda_all=False,
                             return_current_panda_all=False,
                             save_panda_top=True,
                             return_panda_top=False,
                             graph_list=None,
                             **kwargs):
    """
    Parameters
    ----------
    save_panda_all: boolean
        if true, after searching through all estimation files from all subfolders,
        then combine them into a single panda file, and then save that panda file,
        which contains all subfolder estimation results. This is a large file potentially.
    save_panda_top: boolean
        if true, after searching through all estimation files from all subfolders,
        pick from panda the top results by current objective, and then save just the top
        results
    return_current_panda_all: boolean
        to save time in re-saving collecting from hundreds of individual estimation csvs.
        if this is true, return dcurrent panda_all, do not save.
        otherwise return new, update panda dataframe
    **kwargs :
        includes gn_invoke_set which can be speckey as well

    Examples
    --------
    import estimation.estimate_compare as esticomp
    """

    esti_obj_rank_tex_pdf = kwargs.get('esti_obj_rank_tex_pdf', 0)
    top_estimates_keep_count = kwargs.get('top_estimates_keep_count', 4)

    # get compute_spec_key if not available, use integer 1 as default, which is spec_key = 'ng_s_t'
    gn_invoke_set = kwargs.get('compute_spec_key', 1)

    '''
    1. Generate Requisite Input Parameters
    '''
    compute_spec_key, __, __, __, combo_type_list = \
        paramcombospecs.gen_combo_type_list(gn_invoke_set=gn_invoke_set,
                                            paramstr_key_list=paramstr_key_list,
                                            combo_type_list_ab=combo_type_list_ab,
                                            combo_type_list_date=combo_type_list_date)
    combo_type = combo_type_list[0]
    sub_folder_name = combo_type[0] + '_' + combo_type[1]
    compute_specs = computespec.compute_set(compute_spec_key)
    cur_esti_spec = estispec.estimate_set(esti_spec_key, moment_key=moment_key, momset_key=momset_key)
    compesti_specs = compute_specs.copy()
    compesti_specs.update(cur_esti_spec)
    compesti_short_name = hardstring.gen_compesti_short_name(compute_spec_key, esti_spec_key, moment_key,
                                                             momset_key)

    '''
    2. Get folder names if not specified
    '''
    if (search_directory is None):
        # This does not downloads, this just finds path
        # local remote folder name
        d_root = proj_sys_sup.s3_local_sync_folder()
        # Latest Bucket
        bucket_name = proj_sys_sup.s3_bucket_name()
        # This is the folder names on remote that are getting synced here
        d_submain = bucket_name + '/esti/'
        param_folder_name = sub_folder_name
        search_directory = d_root + d_submain + param_folder_name + '/'

    if (fils_search_str is None):
        file_search_str = '*/*.csv'

    '''
    3. Combine Individual subfolder estimation results into main dataframe folder
    '''
    if (save_file_name is None):
        save_file_name = sub_folder_name

    if (save_panda_all or return_current_panda_all):
        '''
        This either grabs out existing panda_all or saves a new one
        '''
        all_esti_df = pd_combine.search_combine(search_directory=search_directory,
                                                file_search_str=file_search_str,
                                                save_file_name=save_file_name,
                                                save_panda=save_panda_all,
                                                return_current=return_current_panda_all)
        '''
        Select only rows in all_esti_df that has the same compute and esti specs
        This allows for generating files that are specific to different steps of ESR process
        '''
        all_esti_df = all_esti_df.loc[all_esti_df['support_arg.compesti_short_name'] == compesti_short_name]

    else:
        '''
        If both of the two above rae false, that means we just need to grab out top_esti_df
        '''
        all_esti_df = None

    if 'thin' in esti_spec_key:

        '''
        Predict more points:
            - This is the initial algorithm I tried
            1. simulate the model at N points
            2. do polynomial regressions
            3. predict the model at N*M points
            4. find max
            - This does not work that well because the parameter space is massive, the N*M draws is simply still not enough at all.
            
        generates and saves *_mpoly_reg_coef.csv* files: 
            i.e.: e_20201025x_esr_tstN5_aws_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv
        '''
        # why is this set at 6400?
        param_vec_count = 6400
        param_vec_predict_count = 0
        save_file_main_lhsrhs = save_file_name + proj_hardcode_filename.sync_glob_esti_file_suffix(
            file_type='_main_lhsrhs')
        save_name_mpoly_reg_coef = save_file_name + proj_hardcode_filename.sync_glob_esti_file_suffix(
            file_type='_mpoly_reg_coef')
        df_simu_predict = gen_predict.gen_predict_obj(combo_type_list, all_esti_df,
                                                      minmax_f='a', minmax_t='20201025',
                                                      param_vec_count=param_vec_count,
                                                      param_vec_predict_count=param_vec_predict_count,
                                                      save_directory=search_directory,
                                                      save_main_name=save_file_main_lhsrhs,
                                                      save_name_mpoly_reg_coef=save_name_mpoly_reg_coef,
                                                      exo_or_endo_graph_row_select=exo_or_endo_graph_row_select)

        '''
        4A. Change the Moments to be matched up
        '''
        moments_type = cur_esti_spec['moments_type']
        momsets_type = cur_esti_spec['momsets_type']
        save_file_main_lhsrhsnew = save_file_name + proj_hardcode_filename.sync_glob_esti_file_suffix(
            file_type='_main_lhsrhs_new')
        all_esti_df_next = esti_update_obj.moments_regen(moments_type=moments_type,
                                                         momsets_type=momsets_type,
                                                         df_use=df_simu_predict,
                                                         save_directory=search_directory,
                                                         save_main_name=save_file_main_lhsrhsnew)
    elif 'mpoly' in esti_spec_key:
        '''
        mpoly estimation:
            - This is the results from many estimations, many approximated objective estimation using polynomials
            - The results here should be optimal points given initial positions
            - This is the end of Step 3 as described in estimation algorithm
        '''
        all_esti_df_next = all_esti_df[
            all_esti_df['file_save_suffix'].str.contains(exo_or_endo_graph_row_select) == True]

        datacheck = True
        if (datacheck):
            '''
            all_esti_df contains potentially:
                1. esti_test: Round 1 Simulation Results
                    + 24 (2 periods) rows? per simulation, most of all_esti_df is these
                2. esti_poly: Step 3 polynomial approximation estimation results
                    + 2 rows? Just the final round estimation result at convergence, 5% of all_esti_df results
                3. esti_poly and esti_test have different keys for support_arg.compesti_short_name
                    + C1E65M3S5 and C4E79M3S5 for example, just show what the counts are
            '''
            logger.info(all_esti_df_next[['support_arg.compesti_short_name']].groupby(
                ['support_arg.compesti_short_name']).size());
            logger.info(all_esti_df[['support_arg.compesti_short_name']].groupby(
                ['support_arg.compesti_short_name']).size());

    elif 'post' in esti_spec_key:
        # 4th step of ESR
        all_esti_df_next = all_esti_df[
            all_esti_df['file_save_suffix'].str.contains(exo_or_endo_graph_row_select) == True]
    else:
        raise NameError(f'{esti_spec_key=} does not contain thin, mpoly or post in name')

    '''
    4B. Find Top estimates, combine model with data, and save
    generates *top_datamodel_C2E4M3S3.csv* files:
        i.e. e_20201025x_esr_tstN5_aws_list_tKap_mlt_ce1a2_top_datamodel_C2E4M3S3.csv
    '''
    save_file_name_esti_top = save_file_name + proj_hardcode_filename.sync_glob_esti_file_suffix(
        file_type='_top_datamodel', compesti_short_name=compesti_short_name)
    save_file_name_esti_top_regress = save_file_name + proj_hardcode_filename.sync_glob_esti_file_suffix(
        file_type='_modelsimu_regress')
    top_esti_df = top_estimate.top_results_merge_moments_data(
        combo_type_list=combo_type_list,
        esti_specs=cur_esti_spec,
        all_esti_df=all_esti_df_next,
        top_estimates_keep_count=top_estimates_keep_count,
        search_directory=search_directory,
        save_file_name=save_file_name_esti_top,
        save_file_name_regress=save_file_name_esti_top_regress,
        multiperiod=True,
        save_panda_top=save_panda_top,
        return_panda_top=return_panda_top,
        exo_or_endo_graph_row_select=exo_or_endo_graph_row_select)

    '''
    5. Top estimates    
    '''
    obj_min_params_row = top_esti_df[combo_type[2]]
    obj_min_params = obj_min_params_row.to_json()
    proj_sys_sup.jdump(obj_min_params, 'obj_min_params', logger=logger.info, print_here=True)

    '''
    6. Moments at Top Estimates
    '''
    moments_type = cur_esti_spec['moments_type']
    momsets_type = cur_esti_spec['momsets_type']
    data_actual_dict, model_simu_dict, model_data_simu_dict = \
        momcomp.show_moments(moments_type, momsets_type, top_esti_df)

    proj_sys_sup.jdump(data_actual_dict, 'data_actual_dict', logger=logger.info, print_here=True)
    proj_sys_sup.jdump(model_simu_dict, 'model_simu_dict', logger=logger.info, print_here=True)
    proj_sys_sup.jdump(model_data_simu_dict, 'model_data_simu_dict', logger=logger.info, print_here=True)

    '''
    7. Generate store key outputs: 
        i.e.: DATASIMUPROBJ_C2E4M3S3.do, DATASIMUPROBJ_C2E4M3S3.tex, PARAMS_C2E4M3S3.do, PARAMS_C2E4M3S3.tex
    '''
    gen_tex.out2tex(top_esti_df, save_directory=search_directory,
                    esti_obj_rank=esti_obj_rank_tex_pdf, compesti_short_name=compesti_short_name)

    '''
    8. generates the TOP JSON files, generates the JSONs from excel, not from JSON Files
        i.e.: ce0209c1_C2E4M3S3_top_json.json
    '''
    gen_simu_params.gen_simu_params(top_esti_df, save_directory=search_directory,
                                    compesti_short_name=compesti_short_name,
                                    combo_type=combo_type)

    '''
    9. Graph etc
    '''
    moment_csv_strs = hardstring.moment_csv_strs()
    all_esti_df_next[moment_csv_strs['main_allperiods_obj'][1]] = \
        np.log(all_esti_df_next[moment_csv_strs['main_allperiods_obj'][1]])
    all_esti_df_next[moment_csv_strs['main_obj'][1]] = \
        np.log(all_esti_df_next[moment_csv_strs['main_obj'][1]])
    if (graph_list is None):
        pass

    else:
        '''
        Here, just getting 1 is enough, just need some simple strings
        '''
        compesti_specs['esti_param_vec_count'] = 1
        combo_list = paramcombo.get_combo(combo_type, compesti_specs)

        '''
        10. Subset of data based on period
        '''
        common_suffix = hardstring.region_time_suffix(True)
        if (common_suffix in moments_type[1]):
            all_esti_df_list = []
            periods = paramloopstr.peristr(action='list')
            for period in periods:
                period_dictkey = paramloopstr.peristr(period=period, action='dictkey')
                cur_condi = (all_esti_df_next['period_dictkey'] == period_dictkey)
                all_esti_df_sub = all_esti_df_next[cur_condi]
                if ('esti_mpoly' in esti_spec_key):
                    '''
                    mpoly estimation
                    '''
                    all_esti_df_sub = all_esti_df_sub[
                        all_esti_df_sub['support_arg.compesti_short_name'].str.contains('C1E65M3S5') == True]

                all_esti_df_list.append(all_esti_df_sub)
        else:
            all_esti_df_list = [all_esti_df_next]
            periods = [None]

        x_var_list = [moment_csv_strs['main_allperiods_obj'][1]] + [moment_csv_strs['main_obj'][1]] + combo_type[2]
        x_var_list = [moment_csv_strs['main_allperiods_obj'][1]] + [moment_csv_strs['main_obj'][1]]

        gen_graphs = False

        if (gen_graphs):
            for period, all_esti_df_next in zip(periods, all_esti_df_list):

                '''
                9. Generate Graphs
                '''
                select_r_equi = False
                title_display = save_file_name
                save_directory = {'img_main': search_directory}

                if (period is not None):
                    period_dictkey = paramloopstr.peristr(period=period, action='dictkey')
                    save_file_name_use = save_file_name + '_' + period_dictkey
                else:
                    save_file_name_use = save_file_name

                for x_var_override in x_var_list:
                    analyzeequi.equi_graph_main(combo_type, combo_list, compute_specs,
                                                jsons_panda_df=all_esti_df_next,
                                                exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                                select_r_equi=select_r_equi,
                                                save_directory=save_directory,
                                                image_save_name=save_file_name_use,
                                                title_display=title_display,
                                                graph_list=graph_list,
                                                x_var_override=x_var_override)


if __name__ == "__main__":
    paramstr_key_list = ['list_policy_Kap_1and2']
    combo_type_list_ab = 'c'
    combo_type_list_date = '20180814x'
    esti_spec_key = 'kap_m0_nld_m'
    search_directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation EC2/thaijmp201808j7itgesti/esti/c_20180814x_list_policy_Kap_1and2/'
    search_combine_indi_esti(paramstr_key_list,
                             combo_type_list_ab,
                             combo_type_list_date, esti_spec_key,
                             moment_key=0, momset_key=1,
                             exo_or_endo_graph_row_select='_exo_wgtJ',
                             image_save_name_prefix='AGG_ALLESTI_',
                             search_directory=search_directory,
                             fils_search_str=None,
                             save_file_name=None,
                             save_panda_all=True,
                             graph_list=None,
                             top_estimates_keep_count=5)
