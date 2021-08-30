'''

@author: fan

the idea is given these three inputs, generate what is needed to update
param_combo with the param combo dictionary structure: 
    param_combo = \
    {'param_update_dict':{'grid_type':['a', 20180607, {UPDATE DICT}],
                           'esti_type':['a', 20180613, {UPDATE DICT}],
                           'data_type':['b', 20180607, {UPDATE DICT}],
                           'model_type':['a',20180613, {UPDATE DICT}],
                           'interpolant_type': ['a',20180607, {UPDATE DICT}],
                           'dist_type': ['a',20180607, {UPDATE DICT}]}
    ,'title':'(IB+FB,IS+FS,6)+(FC)+(LOG,Angeletos)' +
                ',ilf='+str(int(BNI_LEND_P*100)) +',fsf='+str(int(BNF_SAVE_P*100))+')'
    ,'combo_desc':'Angeletos, 5 cate, FIXED COSTS  LOG'+str(int(inf_rate*100))
    ,'file_save_suffix':'maint'}


import parameters.loop_param_combo_list.loops_gen as paramloop

'''

from copy import deepcopy

import itertools
import logging
import pandas as pd
import pyfan.amto.json.json as support_json

import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.loop_param_combo_list.loop_values as paramspecs
import parameters.minmax.a_minmax as param_minmax_a
import projectsupport.hardcode.str_estimation as hardcode_estimation

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

    Could be used for simulation or estimation.

    Under simulation, assume ESTI_PARAM_VEC_COUNT does not exist, but COMPUTE_PARAM_VEC_COUNT
    does, that will determine the length of the COMBO_LIST generated. And unless PARAM_GRID_OR_RAND
    is specified, will assume PARAM_GRID_OR_RAND = 'GRID'. In estimation, PARAM_GRID_OR_RAND = 'RAND'
    is the case. These are keys specified in COMPESTI_SPECS. These different specs are
    set by how parameters.runspecs.get_compesti_specs.get_compesti_specs is called, the second
    element of the compspec input string.

    COMPUTE_PARAM_VEC_COUNT vs ESTI_PARAM_VEC_COUNT:
    - ESTI_PARAM_VEC_COUNT: if this is specified will be drawing parameters from within some min and max bounds, randomly.
    If len(combo_type[2]) > 1, will draw parameters jointly ESTI_PARAM_VEC_COUNT times.
    - COMPUTE_PARAM_VEC_COUNT: if ESTI_PARAM_VEC_COUNT key does not exist, then draw even ordered grid or meshed grid
    over multiple parameters. If len(combo_type[2]) > 1, total simulations is COMPUTE_PARAM_VEC_COUNT*len(combo_type[2]).


    There is an issue with having multiple parameters to jointly mesh loop over if they are
    grid parameters. states and choice grid can not be meshed due to the way they are
    defined. But simple normal parameters under esti can be easily mesh looped over.

    Parameters
    ----------
    combo_type: list
        looks like = ['a', '20180517_A', ['data_param.A']]
        3rd position could be a list with multiple parameters
    compesti_specs: dict
        Dictionary of estimation and simulation specifications.
    """

    logger.info('jdump combo_list_auto.locals()')
    support_json.jdump(locals(), 'combo_list_auto.locals()', logger=logger.info)

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
    if ('esti_param_vec_count' in compesti_specs.keys()):
        param_vec_count = compesti_specs['esti_param_vec_count']
    else:
        param_vec_count = compesti_specs['compute_param_vec_count']

    common_name = '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)'

    '''
    2. Collection list and get 3rd Element of combo_type
    '''
    # ls_string_A = ['c', '20180918']
    # ls_string_B = ['c', '20180918', None]
    # ls_string_C = ['c', '20180918', 'esti_param.alpha_k']
    if len(combo_type) <= 2:
        # Deals with situation A
        combo_type.append(['esti_param.alpha_k'])
    elif combo_type[2] is None:
        # Deals with situation B
        combo_type[2] = ['esti_param.alpha_k']
    else:
        # Situation C
        pass
    param_group_key_list = combo_type[2]
    logger.info('param_group_key_list:\n%s', param_group_key_list)

    param_list_coll, param_type_coll, param_name_coll, param_shortname_col = \
        gen_initial_params(param_group_key_list, minmax_f, minmax_t, param_vec_count, param_grid_or_rand)

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

    if len(combo_type) <= 3:
        # Deals with situation A
        combo_type.append(None)

    if combo_type[3] is not None:
        param_combo_select_ctr = int(combo_type[3])
        logger.info('len(params_all_combinations):%s', len(params_all_combinations))
        logger.info('param_combo_select_ctr:%s', param_combo_select_ctr)
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
                       'title': base_str + ':' + common_name,
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
            also see IOSupport:63     
        '''
        _c_param_combo_ctr = hardcode_estimation.estisimu_draw_counter_str(param_combo_ctr)
        param_combo[
            hardcode_estimation.string_estimation()['param_combo_list_ctr_str']['str']] = _c_param_combo_ctr
        if (len(file_save_suffix) <= 60):
            param_combo['file_save_suffix'] = _c_param_combo_ctr + file_save_suffix[:45]
        else:
            shorter_str = ''.join([l for l in file_save_suffix if l not in ['_', '0',
                                                                            'a', 'e', 'i', 'o', 'u',
                                                                            'A', 'E', 'I', 'O', 'U']])
            param_combo['file_save_suffix'] = _c_param_combo_ctr + shorter_str[:45]

        '''
        9. Add to combo_list
        '''
        combo_list.append(param_combo)

    # log
    support_json.jdump(combo_list, 'combo_list', logger=logger.info)

    return combo_list


def gen_initial_params(param_group_key_list, minmax_f, minmax_t, param_vec_count, param_grid_or_rand):
    """    
    Parameters
    ----------
    param_group_key_list: list
        this is normally just combo_type[2]
    
    Examples
    --------
    see test_parameters/test_loop_gen.py
    import parameters.loop_param_combo_list.loops_gen as paramloop
    combo_type = ''
    minmax_f = ''
    minmax_t = ''
    param_vec_count = 100
    param_grid_or_rand = 'grid'
    paramloop.gen_initial_params(combo_type, minmax_f, minmax_t, param_vec_count, param_grid_or_rand)
    """
    minmax_type = [minmax_f, minmax_t]

    param_list_coll = []
    param_type_coll = []
    param_name_coll = []
    param_shortname_col = []
    #     param_group_key_list = combo_type[2]
    for param_group_key in param_group_key_list:

        '''
        3. Decompose param_type and param_name
        '''
        param_shortname, param_type, param_name = paramloopstr.param_type_param_name(
            param_group_key=param_group_key)

        '''
        4. Get grid of parameter values
        '''
        if (minmax_f == 'a'):
            minmax_param, minmax_subtitle = param_minmax_a.param(minmax_type)

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

    return param_list_coll, param_type_coll, param_name_coll, param_shortname_col


def gen_initial_params_df(param_group_key_list, minmax_f, minmax_t, param_vec_count, param_grid_or_rand):
    param_list_coll, param_type_coll, param_name_coll, param_shortname_col = \
        gen_initial_params(param_group_key_list, minmax_f, minmax_t, param_vec_count, param_grid_or_rand)

    #     support_json.jdump(param_list_coll, 'param_list_coll', logger=logger.info)

    simu_param_dict = {}
    for ctr, param_group_key in enumerate(param_group_key_list):

        param_list = param_list_coll[ctr]
        param_base_list = []
        param_ctr_list = []
        for cur_ctr, param_dict in enumerate(param_list):
            param_val = param_dict['base']
            param_base_list.append(param_val)
            if (ctr == 0):
                _c_param_combo_ctr = hardcode_estimation.estisimu_draw_counter_str(cur_ctr)
                param_ctr_list.append(_c_param_combo_ctr)

        simu_param_dict[param_group_key] = param_base_list
        if (ctr == 0):
            simu_param_dict[
                hardcode_estimation.string_estimation()['param_combo_list_ctr_str']['str_full']] = param_ctr_list

    df_simu_params = pd.DataFrame(simu_param_dict, columns=simu_param_dict.keys())

    return df_simu_params
