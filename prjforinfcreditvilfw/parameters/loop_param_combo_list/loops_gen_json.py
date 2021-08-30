'''

@author: fan

Same outcome as loops_gen, but now can be based on json file

import parameters.loop_param_combo_list.loops_gen_json as paramloop_json
'''

from copy import deepcopy

import itertools
import logging
import pyfan.amto.json.json as support_json
import pyfan.panda.inout.readexport as readexport

import parameters.dist.a_dist as param_dist_a
import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.loop_param_combo_list.loop_values as paramspecs
import parameters.minmax.a_minmax as param_minmax_a
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def combo_list_auto(combo_type=None,
                    compesti_specs=None,
                    grid_f='a', grid_t='20180607',
                    esti_f='a', esti_t='20180607',
                    data_f='a', data_t='20180607',
                    model_f='a', model_t='20180607',
                    interpolant_f='a', interpolant_t='20180607',
                    dist_f='a', dist_t='20180710',
                    minmax_f='a', minmax_t='20180801'):
    """
    Based on some base parameters, update single or a set of parameters. Generate
    a combo_list where each element is a different value along a grid of a single
    parameter, or each element is a combination of values from N different parameters
    along grid of values for each parameter. N could be 1

    The folder root is controlled by projectsupport.systemsupport.main_directory. Which is
    '/data/' on AMZN and is 'D:/repos/ThaiJMP' locally. Modify those inside there.

    Parameters
    ----------
    combo_type: list
        example input is,
        combo_type=["e","20201025x_esr_list_tKap_mlt_ce1a2",["esti_param.kappa_ce9901","esti_param.kappa_ce0209"],
        1,'C2E49M3S3'], the 3rd element is which sorted top ranked best estimate from mpoly to use. The final
        5th element, is the subfolder/file suffix from mpoly estimation, the mpoly result to use for this.
    compesti_specs: list
        This is the compestispec for the current new estimation, that will rely on
        some existing file for current best estimates.
    """

    # Where is the JSON file?
    bl_get_param_from_parametersjson = False
    if bl_get_param_from_parametersjson:
        # file_path: 'D:/repos/ThaiJMP\\esti\\e_20201025x_esr_tstN5_vig_list_tKap_mlt_ce1a2\\ce9901c1_C1E31M3S3_top_json.json'
        file_path = proj_hardcode_filename.get_path_to_top_json_parametersfolder(combo_type)
    else:
        # This is the updated method, result in main esti region specific folder
        # Results there during vig/cmd run naturally, during AWS run, the JSON top esti file uploaded to S3 and downloaded
        # to the docker container via invoke.run_estimate.invoke_estimate
        # 'D:/repos/ThaiJMP\\esti\\e_20201025x_esr_tstN5_vig_list_tKap_mlt_ce1a2\\'
        save_directory_main = compesti_specs['save_directory_main']
        file_path = proj_hardcode_filename.get_path_to_top_json(combo_type, main_folder_name=save_directory_main)

    json_dict_flat = proj_sys_sup.load_json(file_name_and_directory=file_path, keep_int=True)
    json_dict = readexport.unflatten_denormalize(dictionary=json_dict_flat)

    #     grid_param_len_k_start =  json_dict['grid_param']['len_k_start']

    grid_type = [grid_f, grid_t]
    esti_type = [esti_f, esti_t]
    data_type = [data_f, data_t]
    model_type = [model_f, model_t]
    interpolant_type = [interpolant_f, interpolant_t]
    dist_type = [dist_f, dist_t]

    minmax_type = [minmax_f, minmax_t]

    '''
    1. Get Vector Length, and if random or grid
    '''

    if 'param_grid_or_rand' in compesti_specs.keys():
        # If estimamting, compute spec has this key
        param_grid_or_rand = compesti_specs['param_grid_or_rand']
    else:
        # If simulating, compute_spec does not have this key
        param_grid_or_rand = 'grid'

    '''
    If under simulation, esti_param_vec_count key would not exist
    if under estimation, use esti_param_vec_count
    '''
    if 'esti_param_vec_count' in compesti_specs.keys():
        param_vec_count = compesti_specs['esti_param_vec_count']
    else:
        param_vec_count = compesti_specs['compute_param_vec_count']

    common_name = '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)'

    '''
    2. Collection list and get 3rd Element of combo_type
    '''
    param_name = ""
    param_list_coll = []
    param_type_coll = []
    param_name_coll = []
    param_shortname_col = []
    param_group_key_list = combo_type[2]
    if param_group_key_list is not None:
        for param_group_key in param_group_key_list:

            '''
            3. Decompose param_type and param_name
            '''
            param_shortname, param_type, param_name = paramloopstr.param_type_param_name(
                param_group_key=param_group_key)

            '''
            4. Get grid of parameter values
            '''
            if minmax_f == 'a':
                minmax_param, minmax_subtitle = param_minmax_a.param(minmax_type)
                if param_group_key in json_dict_flat:
                    if param_vec_count == 1:
                        # If here, solve/start estimation etc at single point
                        # This could be based on the estimated result from mpoly for a particular seed
                        minmax_param, minmax_subtitle = param_minmax_a.minmax_json_meanminmaxsame_fromfile(
                            json_dict_flat, param_group_key, minmax_param, minmax_subtitle)
                    else:
                        minmax_param, minmax_subtitle = param_minmax_a.minmax_json(json_dict_flat,
                                                                                   param_group_key,
                                                                                   minmax_param,
                                                                                   minmax_subtitle)

            param_list = paramspecs.gen_param_grid(param_type=param_type,
                                                   param_name=param_name,
                                                   minmax_param=minmax_param,
                                                   param_vec_count=param_vec_count,
                                                   param_grid_or_rand=param_grid_or_rand)

            '''
            5. Collect
            '''
            param_list_coll.append(param_list)
            param_type_coll.append(param_type)
            param_name_coll.append(param_name)
            param_shortname_col.append(param_shortname)

    '''
    6. All possible combinations of parameter values for simulation
    '''
    if (param_grid_or_rand == 'grid'):
        params_all_combinations = list(itertools.product(*param_list_coll))
    else:
        params_all_combinations = []
        for cur_ctr in range(param_vec_count):
            params_combinations = []
            for param_list in param_list_coll:
                params_combinations.append(param_list[cur_ctr])
            params_all_combinations.append(tuple(params_combinations))

    '''
    7. Loop over all combinations of parameters:
        if param_a = {1,2,3}
        and params_b = {3,4,5}
        then we have 9 combinations
    '''

    '''
    generate fixed ctr, so can pick subset
    '''
    params_all_combo_ctr_list = range(len(params_all_combinations))

    if combo_type[3] is not None:
        param_combo_select_ctr = int(combo_type[3])
        params_all_combinations = [params_all_combinations[param_combo_select_ctr]]
        params_all_combo_ctr_list = [params_all_combo_ctr_list[param_combo_select_ctr]]

    combo_list = []
    for param_combo_ctr, param_val_dict_combine_set in zip(params_all_combo_ctr_list, params_all_combinations):

        '''
        8a. Build up param_combo basic structure
        '''
        # here to make sure updates do not override initial across loops
        param_combo_dict = {'grid_type': grid_type,
                            'esti_type': esti_type,
                            'data_type': data_type,
                            'model_type': model_type,
                            'interpolant_type': interpolant_type,
                            'dist_type': dist_type,
                            'minmax_type': minmax_type}

        '''
        8c. Updating here all other parameters
        update all parameters here:
            parameters that participated in estimation?
            all esti_param?
            Develope a function that converst from the
            flat dict to actrual dict.
            do everything so that everything is fully consistent.
        '''

        '''
        Append to each, because 3rd element does not exist yet
        '''
        if ('grid_param' in json_dict):
            param_combo_dict['grid_type'].append(json_dict['grid_param'])
        if ('esti_param' in json_dict):
            param_combo_dict['esti_type'].append(json_dict['esti_param'])
        if ('data_param' in json_dict):
            param_combo_dict['data_type'].append(json_dict['data_param'])
        if ('model_option' in json_dict):
            param_combo_dict['model_type'].append(json_dict['model_option'])
        if ('interpolant' in json_dict):
            param_combo_dict['interpolant_type'].append(json_dict['interpolant'])

        '''
        Dealing with integration issues
        '''
        if ((dist_t is None) or (dist_t == 'NONE')):
            '''
            do not do distribution, regardless if estimation considered it and the parameter is in json_dict
            '''
            pass
        elif ('dist_param' in json_dict):
            '''
            This means estimation involved integration
            do not need to updated any parameters
            and we want to do integration for simulation
            '''
            param_combo_dict['dist_type'].append(json_dict['dist_param'])
        else:
            '''
            THis means we want to do simulation with itnegration
            but we did not do integration in estimation
            
            Do a little bit correction below, clearly, integrated version 
            can not keep same mean of the normal inside the exp. that would blow up more than it should            
            '''
            if dist_f == 'a':
                dist_param, dist_subtitle = param_dist_a.param(dist_type)

            if 'data_param' in json_dict:
                sd_impose = dist_param['data__A']['params']['sd']
                mean_esti_no_sd = json_dict['data_param']['A']
                dist_param['data__A']['params']['mu'] = mean_esti_no_sd - (sd_impose ** 2) / 2
                param_combo_dict['dist_type'].append(dist_param)

        '''
        8b. Loop over the different parameters for each combination
            Updating multiple parameters potentially
        '''
        base_str = ''
        file_save_suffix = ''
        for param_ctr, param_val_dict in enumerate(param_val_dict_combine_set):
            """
                initially had: param_type_update = {param_name:param_val_dict['use']}
                but this only allows one parameter to be updated, what if two?
            """
            param_type_update = param_val_dict['use']
            if (len(param_combo_dict[param_type_coll[param_ctr]]) == 2):
                # no third element add on dictionary yet
                param_combo_dict[param_type_coll[param_ctr]].append(param_type_update)
            else:
                # already have parameter add-on, add to current dict.
                param_combo_dict[param_type_coll[param_ctr]][2].update(param_type_update)
            # create full set of updates and parameters
            base_str += '{0:.{1}f}'.format(param_val_dict['base'], 4)

            file_save_suffix += '_' + param_shortname_col[param_ctr] + param_val_dict['str']

        '''
        8c. Generate full param_combo
        '''
        # must do a deep copy to make sure old param_combo_dict and new do not conflict
        param_combo_dict_cur = deepcopy(param_combo_dict)
        param_combo = {'param_update_dict': param_combo_dict_cur,
                       'title': param_name + '=' + base_str + ':' + common_name,
                       'combo_desc': 'Angeletos quick'}

        '''
        8d. Estimation add on
        '''
        param_combo_more_keys = ['esti_method',
                                 'moments_type', 'momsets_type',
                                 'esti_option_type', 'esti_func_type',
                                 'param_grid_or_rand', 'esti_param_vec_count']
        for param_combo_more_key in param_combo_more_keys:
            if (param_combo_more_key in compesti_specs.keys()):
                param_combo[param_combo_more_key] = compesti_specs[param_combo_more_key]

        '''
        8e. file_save_suffix, limit folder/file name length
        '''
        param_combo['param_combo_list_ctr_str'] = '_c' + str(param_combo_ctr)
        if (len(file_save_suffix) <= 60):
            '''
            also see IOSupport:63
            '''
            param_combo['file_save_suffix'] = '_c' + str(param_combo_ctr) + file_save_suffix[:45]
        else:
            shorter_str = ''.join([l for l in file_save_suffix if l not in ['a', 'e', 'i', 'o', 'u',
                                                                            'A', 'E', 'I', 'O', 'U']])
            param_combo['file_save_suffix'] = '_c' + str(param_combo_ctr) + shorter_str[:45]

        '''
        9. Add to combo_list
        '''
        combo_list.append(param_combo)

    # log
    support_json.jdump(combo_list, 'combo_list', logger=logger.info)

    return combo_list
