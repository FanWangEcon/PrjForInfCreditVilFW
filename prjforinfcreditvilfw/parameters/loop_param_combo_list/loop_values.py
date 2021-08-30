'''

@author: fan
'''

import logging

logger = logging.getLogger(__name__)
import pyfan.amto.json.json as support_json

import numpy as np
import random


def gen_param_grid(param_type='data_type',
                   param_name='A',
                   minmax_param=None,
                   param_vec_count=4,
                   param_grid_or_rand=True):
    """
    min_v and max_v are values stored in this file, they can over-ride minmax_param
    supplied min_v and max_v if that is needed 
    
    Parameters
    ----------
    minmax_param: dict
        a nested dictionary from a_minmax.py 
    param_vec_count: int
        number of elements in parameter vector to output
    param_grid: boolean
        if param_grid is true, generate a grid for param_list
        if param_grid is false, generate a random vector based on min and max 
        
    Returns
    -------
    param_list: list    
        list (vector) of parameter values for a particular paramter
    
    """
    process_normal = True

    min_v, max_v, rseed = None, None, 123
    if (minmax_param is not None):
        if (param_name in minmax_param[param_type]):
            min_v = minmax_param[param_type][param_name][0]
            max_v = minmax_param[param_type][param_name][1]
            rseed = minmax_param[param_type][param_name][2]

    """
    SECTION: ESTI_TYPE, Group A, 2 Choices Only
    """
    if param_type == 'esti_type' and param_name == 'CEV_PROP_INCREASE':
        override = True
        if override or (min_v is None):
            # do noto use standard even grid, use uneven grid, denser at zero.
            process_normal = False
            # CEV change, consider minus 20 percent to + 20 percent
            max_v = 0.30
            min_v = -1 * max_v

            # param_vec_count = 11
            # one sided
            grid_powerspace_power = 3
            fl_a_max = 0.30
            fl_a_min = 0

            it_a_points = int(np.floor(param_vec_count / 2) + 1)

            ar_fl_cev_lvl_grid = np.zeros([it_a_points, 1])
            for i in range(1, it_a_points + 1):
                fl_cev_cur = fl_a_min + \
                             (fl_a_max - fl_a_min) * ((i - 1) / (it_a_points - 1)) ** grid_powerspace_power
                ar_fl_cev_lvl_grid[i - 1, 0] = fl_cev_cur

            # two-sided
            ar_fl_cev_lvl_grid = np.concatenate((ar_fl_cev_lvl_grid * -1, ar_fl_cev_lvl_grid))
            ar_fl_cev_lvl_grid = np.unique(np.sort(ar_fl_cev_lvl_grid))
            if (param_vec_count % 2) == 0:
                ar_fl_cev_lvl_grid = ar_fl_cev_lvl_grid[ar_fl_cev_lvl_grid != 0]
            print(ar_fl_cev_lvl_grid)

            # generate param_list
            param_list = []
            for fl_cev in ar_fl_cev_lvl_grid:
                param_list_cur = {'base': fl_cev,
                                  'use': {'CEV_PROP_INCREASE': fl_cev},
                                  'str': str(int(fl_cev * 10000))}
                param_list.append(param_list_cur)

    if (param_type == 'esti_type' and param_name == 'alpha_k'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.30, 0.50

    if (param_type == 'esti_type' and param_name == 'beta'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.78, 0.98

    if (param_type == 'esti_type' and param_name == 'K_DEPRECIATION'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.05, 0.17

    if (param_type == 'esti_type' and param_name == 'rho'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.25, 0.96

    if (param_type == 'esti_type' and param_name == 'logit_sd_scale'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.9, 1.1

    if (param_type == 'esti_type' and param_name == 'R_INFORM_SAVE'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 1.0, 1.20

        process_normal = False
        param_list = [
            {'base': R_INFORM_SAVE,
             'use': {'R_INFORM_SAVE': R_INFORM_SAVE,
                     'R_INFORM_BORR': R_INFORM_SAVE},
             'str': str(int(R_INFORM_SAVE * 10000))}
            for R_INFORM_SAVE in np.linspace(min_v, max_v, param_vec_count)]

    """
    SECTION: ESTI_TYPE, Group B, >2 choices, formal and informal
    """
    if (param_type == 'esti_type' and param_name == 'BNF_SAVE_P'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0, 1.5

    if (param_type == 'esti_type' and param_name == 'BNF_BORR_P'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0, 3.5

    if (param_type == 'esti_type' and param_name == 'BNI_LEND_P'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0, 3.5

    if (param_type == 'esti_type' and param_name == 'BNI_BORR_P'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0, 1.5

    if (param_type == 'esti_type' and param_name == 'kappa'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.10, 0.70

    if (param_type == 'esti_type' and param_name == 'R_FORMAL_SAVE'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.95, 1.05

    if (param_type == 'esti_type' and param_name == 'R_FORMAL_BORR'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.95, 1.05

    """
    SECTION: DATA_TYPE
    """
    if (param_type == 'data_type' and param_name == 'A'):
        process_normal = False
        override = False
        if (override or (min_v is None)):
            min_v = -0.65
            max_v = 0.35
        std = 0.75
        param_list = []
        param_list_val = process_rand_or_vec(param_grid_or_rand, param_vec_count, min_v, max_v, rseed)
        for A in param_list_val:
            if (A < 0):
                str_rep = str(int(np.abs(A - min_v) * 10000))
            else:
                str_rep = str(int(np.abs(A - min_v) * 10000))
            param_list_cur = {'base': A,
                              'use': {'A': A - ((std ** 2) / 2)},
                              'str': str_rep}
            param_list.append(param_list_cur)

    """
    SECTION: GRID_TYPE and INTERPOLANT
    Testing Solution Accuracy
    """
    if (param_type == 'grid_type'):
        if (param_type == 'grid_type' and param_name == 'BNF_SAVE_P_startVal'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = 0, 3
        elif (param_type == 'grid_type' and param_name == 'BNF_BORR_P_startVal'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = -0.0, -3.0
        elif (param_type == 'grid_type' and param_name == 'BNI_LEND_P_startVal'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = 0, 3
        elif (param_type == 'grid_type' and param_name == 'BNI_BORR_P_startVal'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = -0.0, -3.0
        else:
            process_normal, param_list = key_param_check_loops_grid_type(param_type, param_name,
                                                                         param_grid_or_rand,
                                                                         param_vec_count,
                                                                         min_v, max_v,
                                                                         rseed)

    """
    Interpolant
    """
    if (param_type == 'interpolant_type' and param_name == 'maxinter'):
        process_normal = False
        base_states_all = [5, 10, 15, 20] + [int(val) for val in np.arange(25, 55, 5)]

        param_list = [
            {'base': vfi_iter,
             'use': {'maxinter': vfi_iter},
             'str': str(int(vfi_iter))}
            for vfi_iter in get_subset(base_states_all, param_vec_count)]

    """
    SECTION: DIST_TYPE
    """
    if (param_type == 'dist_type'):

        if (param_type == 'dist_type' and param_name == 'epsA_frac_A'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = 0.35, 0.65
        elif (param_type == 'dist_type' and param_name == 'epsA_std'):
            override = False
            if (override or (min_v is None)):
                min_v, max_v = 0.35, 0.65
        else:
            process_normal, param_list = key_param_check_loops_dist_type(param_type, param_name,
                                                                         param_grid_or_rand,
                                                                         param_vec_count,
                                                                         min_v, max_v,
                                                                         rseed)

    '''
    Generates grid or random vector of parameter values
    '''
    if (process_normal):
        param_list_val = process_rand_or_vec(param_grid_or_rand, param_vec_count, min_v, max_v, rseed)
        if (param_grid_or_rand == 'rand'):
            param_list = [param_value_dict(val, param_name) for val in (param_list_val)]
        else:
            param_list = [param_value_dict(val, param_name) for val in np.sort(param_list_val)]

    return param_list


def process_rand_or_vec(param_grid_or_rand, param_vec_count, min_v, max_v, rseed):
    if (param_grid_or_rand == 'grid'):
        # generate a grid
        if (param_vec_count == 1):
            param_list_val = [(max_v - min_v) / 2]
        elif (param_vec_count == 2):
            param_list_val = [min_v, max_v]
        else:
            param_list_val = np.linspace(min_v, max_v, param_vec_count)
    elif (param_grid_or_rand == 'rand'):
        # generate a random vector, random.seed(rseed) is WRONG, need NP.RANDOM.SEED!
        np.random.seed(rseed)
        param_list_val = np.random.uniform(min_v, max_v, param_vec_count)
    else:
        raise ('not possible')

    return param_list_val


def param_value_dict(val, param_name):
    param_combo_update_dict = {'base': val,
                               'use': {param_name: val},
                               'str': str(int(val * 10000))}

    return param_combo_update_dict


def get_subset(base_states_all, param_vec_grid_count):
    """
    subset of large set
        base_states_small = [int(val**2) for val in np.arange(5, 30, 5)]
        base_states_large = [900, 1600, 2500, 3600, 4900]
        base_states_all = base_states_small + base_states_large
        [[base_states_all[int(cur)] 
          for cur in np.linspace(0, len(base_states_all)-1, param_vec_grid_count)] 
          for param_vec_grid_count in [1,2,3,4,5]]
    subset of smaller set:
    
        base_states_large = [900, 1600, 2500, 3600, 4900]
        base_states_all = [900, 1600, 2500, 3600, 4900]
        subset_list = [[base_states_all[int(cur)] 
          for cur in np.linspace(0, len(base_states_all)-1, param_vec_grid_count)] 
          for param_vec_grid_count in [1,2,3,4,5]]    
    
    """
    subset_list = [base_states_all[int(cur)]
                   for cur in
                   np.linspace(0, len(base_states_all) - 1, param_vec_grid_count)]

    subset_list_unique = np.unique(subset_list)

    return subset_list_unique


def key_param_check_loops_grid_type(param_type, param_name,
                                    param_grid_or_rand,
                                    param_vec_grid_count,
                                    min_v, max_v,
                                    r_seed):
    """
    SECTION: GRID_TYPE and INTERPOLANT
    Testing Solution Accuracy
    """
    process_normal = False
    if (param_type == 'grid_type' and param_name == 'len_states'):
        base_states_small = [int(val ** 2) for val in np.arange(5, 30, 5)]
        base_states_large = [900, 1600, 2500, 3600, 4900]
        base_states_all = base_states_small + base_states_large

        param_list = [
            {'base': len_states,
             'use': {'len_states': int(len_states),
                     'len_k_start': int(np.sqrt(len_states)),
                     'len_choices': 900,
                     'shape_choice': {'type': 'broadcast', 'shape': [int(len_states), 900], 'row': int(len_states),
                                      'col': 900}},
             'str': str(int(len_states))}
            for len_states in get_subset(base_states_all, param_vec_grid_count)]

    if (param_type == 'grid_type' and param_name == 'len_choices'):
        base_choices_small = [int(val ** 2) for val in np.arange(5, 30, 5)]
        base_states_all = base_choices_small + [900, 1225, 1600, 2025, 2500]

        param_list = [
            {'base': len_choices,
             'use': {'len_states': 2500,
                     'len_k_start': 50,
                     'len_choices': len_choices,
                     'shape_choice': {'type': 'broadcast', 'shape': [2500, len_choices], 'row': 2500,
                                      'col': len_choices}},
             'str': str(int(len_choices))}
            for len_choices in get_subset(base_states_all, param_vec_grid_count)]

    if (param_type == 'grid_type' and param_name == 'max_steady_coh'):
        base_states_all = [50, 60, 70, 80, 90, 100] + [int(val * 10) for val in np.arange(10, 50, 5)]
        param_list = [
            {'base': max_steady_coh,
             'use': {'markov_points': int(max_steady_coh / (50 / 200)),
                     'max_steady_coh': max_steady_coh,
                     'max_kapital': max_steady_coh,
                     'max_netborrsave': max_steady_coh},
             'str': str(int(max_steady_coh))}
            for max_steady_coh in get_subset(base_states_all, param_vec_grid_count)]

    if (param_type == 'grid_type' and param_name == 'markov_points'):
        base_states_all = [20, 30, 40, 50, 100, 150, 200, 300]

        param_list = [
            {'base': markov_points,
             'use': {'markov_points': markov_points},
             'str': str(int(markov_points))}
            for markov_points in get_subset(base_states_all, param_vec_grid_count)]

    if (param_type == 'grid_type' and param_name == 'std_eps'):
        override = False
        if (override or (min_v is None)):
            min_v, max_v = 0.2, 2.0

        base_states = process_rand_or_vec(param_grid_or_rand, param_vec_grid_count, min_v, max_v, r_seed)

        param_list = [
            {'base': std,
             'use': {'std_eps': std,
                     'mean_eps': (-1) * ((std ** 2) / 2),
                     'std_eps_E': std,
                     'mean_eps_E': (-1) * ((std ** 2) / 2)},
             'str': str(int(std * 100))} for std in base_states]

    return process_normal, param_list


def key_param_check_loops_dist_type(param_type, param_name,
                                    param_grid_or_rand,
                                    param_vec_count,
                                    min_v, max_v,
                                    rseed):
    """
    SECTION: GRID_TYPE and INTERPOLANT
    Testing Solution Accuracy
    """

    '''
    All other estimation parameters do not have nested dicts for storing values
        others use process_normal
    '''
    process_normal = False
    if (param_type == 'dist_type' and
            (('params.mu' in param_name)
             or
             ('params.sd' in param_name))):

        override = False
        if (override or (min_v is None)):
            min_v, max_v = -0.50, 0.50

        param_list = []
        param_list_val = process_rand_or_vec(param_grid_or_rand, param_vec_count, min_v, max_v, rseed)

        if (param_grid_or_rand == 'rand'):
            pass
        else:
            param_list_val = np.sort(param_list_val)

        for val in param_list_val:

            if (val < 0):
                str_rep = str(int(np.abs(val - min_v) * 10000))
            else:
                str_rep = str(int(np.abs(val - min_v) * 10000))

            data__A_regiondate = param_name.split('.')[0]

            '''
            fill just one value is fine actually
            '''
            A = 0.25
            std = 0.75
            fixed_sd = 0.25
            fixed_mu = A - ((std ** 2) / 2)
            if ('params.mu' in param_name):
                params_dict = {'mu': val,
                               'sd': fixed_sd}
            elif ('params.sd' in param_name):
                params_dict = {'mu': fixed_mu,
                               'sd': val}
            else:
                pass

            results = {'base': val,
                       'use': {data__A_regiondate: {'dist': 'normal',
                                                    'params': params_dict,
                                                    'integrate': {'method': 'grid',
                                                                  'params': {'points': 8}}}},
                       'str': str_rep}

            param_list.append(results)

    if (param_type == 'dist_type' and (param_name in 'esti__BNF_SAVE_P.params.max')):

        override = False
        if (override or (min_v is None)):
            min_v, max_v = 1.5, 2.5

        param_list = [{'base': val,
                       'use': {'esti__BNF_SAVE_P': {'dist': 'normal',
                                                    'params': {'min': 1,
                                                               'max': 2},
                                                    'integrate': {'method': 'grid',
                                                                  'params': {'points': 5}}}},
                       'str': str(int(val * 100))}
                      for val in np.linspace(min_v, max_v, param_vec_grid_count)]

    return process_normal, param_list


def test_cases():
    results = gen_param_grid()
    support_json.jdump(results, 'default grid', logger=logger.warning)

    import parameters.minmax.a_minmax as param_minmax_a
    minmax_param, minmax_subtitle = param_minmax_a.param(param_type=['a', '20180801'])
    results = gen_param_grid(param_type='grid_type', param_name='BNF_SAVE_P_startVal', minmax_param=minmax_param)
    support_json.jdump(results, 'grid_type change', logger=logger.warning)

    # Random parameter vector
    results = gen_param_grid(param_grid=False)
    support_json.jdump(results, 'random vector', logger=logger.warning)

    # Grid parameter vector 
    results = gen_param_grid(param_type='esti_type', param_name='alpha_k', param_grid=True)
    support_json.jdump(results, 'esti_type.alpha_k', logger=logger.warning)

    # A parameter that has no min or max, is not impacted by param_grid true or false
    results_true = gen_param_grid(param_type='interpolant_type', param_name='maxinter', param_grid=True)
    results_false = gen_param_grid(param_type='interpolant_type', param_name='maxinter', param_grid=False)
    support_json.jdump(results_true, 'interpolant_type.maxinter.truematter', logger=logger.warning)
    support_json.jdump(results_false, 'interpolant_type.maxinter.falsedontmatter', logger=logger.warning)


if __name__ == "__main__":
    test_cases()
