'''
@author: fan

provides lower and upper bounds parameters: provide minmax_f, minmax_t inputs for
gen_initial_params function:

    param_list_coll, param_type_coll, param_name_coll, param_shortname_col = \
        gen_initial_params(param_group_key_list, minmax_f, minmax_t, param_vec_count, param_grid_or_rand)

the actual parameter to loop over is provided from invoke by param_group_key_list.
'''

import random

import copy
import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.hardcode.string_shared as hardstring
import math

import numpy as np


def minmax_json_meanminmaxsame_fromfile(json_dict,
                                        param_group_key,
                                        minmax_param, subtitle):
    """minmax_json

    There is an existing JSON dictionary with parameter values. These parameter
    values might be from a particular estimation exercise's estimated results.

    We want to update the min/max bounds for simulating the parameter, so that min
    max are equal to the current parameter estimate.

    After ESR simulation finishes 3rd MPOLY step and there are best parameter, use
    this to grab out the best parameters simulate/estimate starting at those value. This
    min/max structure is used in order to re-use the loop_gen estimation/simulation existing
    structure.

    JSON file from mpoly have time specific estimates:
    > "esti_param.kappa": 0.25,
    > "esti_param.kappa_ce9901": 0.4503418023478664,
    > "esti_param.kappa_ce0209": 0.3428781419412163,

    In this file:
        param_name: looks like, kappa
        early_period_param: looks like, kappa_ne9901
        later_period_param: looks like, kappa_ne0209
    The idea is that I am looping over variables like: kappa
        that is what simulation understands, but the estimated parameter values
        are stored in kappa_ne9901, kappa_ne0209.
        so I use these two region/time specific parameters to update the min and max
        range for kappa, which allows kappa simulation now to follow estimated
        change in key policy parameters.
    """
    param_shortname, param_type, param_name = paramloopstr.param_type_param_name(param_group_key=param_group_key)

    # do not extend beyond current range. if at bound, do not go beyond bound.
    minmax_param[param_type][param_name][0] = json_dict[param_group_key]
    minmax_param[param_type][param_name][1] = json_dict[param_group_key]

    return minmax_param, subtitle


def minmax_json(json_dict,
                param_group_key,
                minmax_param, subtitle):
    """minmax_json
    In this file:
        param_name: looks like, kappa
        early_period_param: looks like, kappa_ne9901
        later_period_param: looks like, kappa_ne0209
    The idea is that I am looping over variables like: kappa
        that is what simulation understands, but the estimated parameter values
        are stored in kappa_ne9901, kappa_ne0209.
        so I use these two region/time specific parameters to update the min and max
        range for kappa, which allows kappa simulation now to follow estimated
        change in key policy parameters.
    """
    period_dictkey = json_dict[hardstring.moment_csv_strs()['period_dictkey'][1]]
    param_type_param, param_name = paramloopstr.param_type_param_name(param_group_key=param_group_key, split=True)
    param_shortname, param_type, param_name = paramloopstr.param_type_param_name(param_group_key=param_group_key)

    early_period_param, later_period_param = hardstring.region_time_next(cur_var=param_name,
                                                                         both_periods=True,
                                                                         period_dictkey=period_dictkey)
    curparam_9901 = json_dict[param_type_param][early_period_param]
    curparam_0209 = json_dict[param_type_param][later_period_param]

    '''
    Current Lower and Higher Parameters
    '''
    curparam_lowwer = min(curparam_9901, curparam_0209)
    curparam_higher = max(curparam_9901, curparam_0209)

    '''
    Paramter minmax non-estimated bounds
    '''
    param_min_esti_bound = minmax_param[param_type][param_name][0]
    param_max_esti_bound = minmax_param[param_type][param_name][1]

    curparam_expand_bin = (param_max_esti_bound - param_min_esti_bound) / 6
    if (math.isclose(curparam_9901, curparam_0209, rel_tol=1e-3, abs_tol=1e-3)):
        '''
        If too close:use default bin
        '''
        pass
    else:
        '''
        If further away
        '''
        curparam_gap = (curparam_higher - curparam_lowwer)
        '''
        Try to get a big enough gap, otherwise graphs not very interesting.
        '''
        curparam_expand_bin = max(curparam_gap / 6, curparam_expand_bin)

    # do not extend beyond current range. if at bound, do not go beyond bound.
    minmax_param[param_type][param_name][0] = max(curparam_lowwer - curparam_expand_bin, param_min_esti_bound)
    minmax_param[param_type][param_name][1] = min(curparam_higher + curparam_expand_bin, param_max_esti_bound)

    return minmax_param, subtitle


def param(param_type=1):
    """
    Parameters
    ----------
    type: list
        = ['a', 1]
        could be longer, more and more

    Returns
    -------
    min_max_param: dict
        for each dict key/value, for the value, which is a list,
            first position is,
                min
            second position is,
                max
            third position is,
                random seed (if a random vector will be generated)

    """
    module = param_type[0]
    sub_type = str(param_type[1])

    subtitle = 'zeroFE'

    '''
    Generate a long list of random integers
    '''
    random.seed(123)
    seeds = random.sample(range(100, 1000), 100)

    '''
    Set Defaults
    '''
    esti_type = {
        'alpha_k': [0.30, 0.50, seeds[0]],
        'beta': [0.78, 0.98, seeds[1]],
        'K_DEPRECIATION': [0.05, 0.17, seeds[2]],
        'rho': [0.25, 0.96, seeds[3]],
        'logit_sd_scale': [0.9, 1.1, seeds[4]],
        'R_INFORM_SAVE': [1.0, 1.20, seeds[5]],
        'R_FORMAL_SAVE': [0.95, 1.15, seeds[11]],
        'R_FORMAL_BORR': [0.95, 1.15, seeds[12]],
        'CEV_PROP_INCREASE': [-0.20, +0.20, seeds[61]],

        'BNF_SAVE_P': [0, 1.5, seeds[6]],
        'BNF_BORR_P': [0, 3.5, seeds[7]],
        'BNI_LEND_P': [0, 3.5, seeds[8]],
        'BNI_BORR_P': [0, 3.5, seeds[9]],
        'kappa': [0.10, 0.70, seeds[10]]
    }

    data_type = {
        'A': [-0.65, 0.35, seeds[13]]
    }

    grid_type = {
        'BNF_SAVE_P_startVal': [0, 3, seeds[14]],
        'BNF_BORR_P_startVal': [-0.0, -3.0, seeds[15]],
        'BNI_LEND_P_startVal': [0, 3, seeds[16]],
        'BNI_BORR_P_startVal': [-0.0, -3.0, seeds[17]],
        'std_eps': [0.2, 2.0, seeds[18]],
        'max_steady_coh': [50, 450, 9393],
        'markov_points': [20, 300, 9394]
    }

    dist_type = {
        'data__A.params.mu': [-0.50, 0.50, seeds[19]],
        'data__A.params.sd': [0.15, 0.35, seeds[20]],
        'esti__BNF_SAVE_P.params.max': [1.5, 2.5, seeds[21]],
        'epsA_frac_A': [0.05, 0.95, seeds[22]],
        'epsA_std': [0.2, 2.0, seeds[23]],
        'std_eps': [0.2, 2.0, seeds[24]],
    }

    if (sub_type == '20180801'):
        grid_type['BNF_SAVE_P_startVal'][1] = 4
        esti_type['alpha_k'][1] = 0.6

    if (sub_type == '20180829'):
        '''
        *Increase Bounds*
            - esti_param.alpha_k
                0.3
                this is the lower bound, *add to alpha_k* lower bound perhaps
            - what is the beta used in other models?
                could allow some flexibility here I think, does not have to be strict, *beta little flexible*
            - esti_param.logit_sd_scale: 1.105, 1.1
        '''
        esti_type['logit_sd_scale'][0] = 0.5
        esti_type['logit_sd_scale'][1] = 2.0
        esti_type['alpha_k'][0] = 0.15
        esti_type['alpha_k'][1] = 0.75
        esti_type['rho'][0] = 0.95
        esti_type['rho'][1] = 1.05

    if (sub_type == '20180901'):
        '''
        Ranges below have been tested (using invoking 20180829 above)
        hole around 1 for rho where things don't work
        '''
        esti_type['logit_sd_scale'][0] = 0.75
        esti_type['logit_sd_scale'][1] = 2.0
        esti_type['alpha_k'][0] = 0.15
        esti_type['alpha_k'][1] = 0.75
        esti_type['rho'][0] = 0.10
        esti_type['rho'][1] = 1.5
        '''
        Testing what happens if interest rate gets very high for informal saving borrowing
            things should go a little crazy, but code should not break
            code was breaking at very high NE interest rate 1.3 >
        '''
        esti_type['R_INFORM_SAVE'][0] = 0.90
        esti_type['R_INFORM_SAVE'][1] = 2.00
        '''
        2018-09-06 17:54 expand A range, bounded
        '''
        data_type['A'][0] = -0.65
        data_type['A'][1] = 1

    if (sub_type == '20180917'):
        '''
        Ranges below have been tested (using invoking 20180829 above)
        hole around 1 for rho where things don't work
        '''
        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 2.0
        esti_type['alpha_k'][0] = 0.15
        esti_type['alpha_k'][1] = 0.75

        '''
        weird too low rho, and extend risk-aversion to higher numbers
        '''
        esti_type['rho'][0] = 0.25
        esti_type['rho'][1] = 5.0  # 4 to 5 2018-09-18 05:43

        '''
        Testing what happens if interest rate gets very high for informal saving borrowing
            things should go a little crazy, but code should not break
            code was breaking at very high NE interest rate 1.3 >
        '''
        esti_type['R_INFORM_SAVE'][0] = 0.90
        esti_type['R_INFORM_SAVE'][1] = 2.00

        '''
        2018-09-06 17:54 expand A range, bounded
        '''
        data_type['A'][0] = -0.65
        data_type['A'][1] = 1

        '''
        2018-09-17 21:20 expand
        '''
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

        '''
        2018-09-18 05:42 expand
        '''
        dist_type['data__A.params.mu'][0] = -0.65
        dist_type['data__A.params.mu'][1] = 0.65

    if (sub_type == '20180925'):
        '''
        KT estimate rage for some parameters
        '''
        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 2.0
        esti_type['beta'][0] = 0.88
        esti_type['beta'][1] = 0.98

        esti_type['alpha_k'][0] = 0.15
        esti_type['alpha_k'][1] = 0.75

        '''
        weird too low rho, and extend risk-aversion to higher numbers
        '''
        esti_type['rho'][0] = 1.1
        esti_type['rho'][1] = 1.5  # 4 to 5 2018-09-18 05:43

        '''
        Testing what happens if interest rate gets very high for informal saving borrowing
            things should go a little crazy, but code should not break
            code was breaking at very high NE interest rate 1.3 >
        '''
        esti_type['R_INFORM_SAVE'][0] = 0.90
        esti_type['R_INFORM_SAVE'][1] = 2.00

        '''
        2018-09-06 17:54 expand A range, bounded
        '''
        data_type['A'][0] = -0.65
        data_type['A'][1] = 1

        '''
        2018-09-17 21:20 expand
        '''
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

        '''
        2018-09-18 05:42 expand
        '''
        dist_type['data__A.params.mu'][0] = -0.65
        dist_type['data__A.params.mu'][1] = 0.65

    if (sub_type == 'B181021'):
        '''
        For Benchmark simulation, all numbers easily divislbe by 10
        '''
        esti_type['BNI_LEND_P'][0] = 0
        esti_type['BNI_LEND_P'][1] = 3
        esti_type['BNI_BORR_P'][0] = 0
        esti_type['BNI_BORR_P'][1] = 3

        esti_type['BNF_SAVE_P'][0] = 0
        esti_type['BNF_SAVE_P'][1] = 3
        esti_type['BNF_BORR_P'][0] = 0
        esti_type['BNF_BORR_P'][1] = 3

        esti_type['R_FORMAL_SAVE'][0] = 1.0
        esti_type['R_FORMAL_SAVE'][1] = 1.05
        esti_type['R_FORMAL_BORR'][0] = 1.05
        esti_type['R_FORMAL_BORR'][1] = 1.15

        esti_type['kappa'][0] = 0
        esti_type['kappa'][1] = 0.9

        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 1.2
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

    if (sub_type == 'B181025'):
        '''
        Making Adjustments based on simulation experiences from B181021
            1. the FC formal borrow range should be smaller, at highest rate, weird rate
            2. collateral range wider
        '''
        esti_type['BNI_LEND_P'][0] = 0
        esti_type['BNI_LEND_P'][1] = 3
        esti_type['BNI_BORR_P'][0] = 0
        esti_type['BNI_BORR_P'][1] = 3

        esti_type['BNF_SAVE_P'][0] = 0
        esti_type['BNF_SAVE_P'][1] = 3
        esti_type['BNF_BORR_P'][0] = 0
        esti_type['BNF_BORR_P'][1] = 3

        esti_type['R_FORMAL_SAVE'][0] = 1.0
        esti_type['R_FORMAL_SAVE'][1] = 1.050
        esti_type['R_FORMAL_BORR'][0] = 1.033
        esti_type['R_FORMAL_BORR'][1] = 1.133

        esti_type['kappa'][0] = 0.10
        esti_type['kappa'][1] = 0.90

        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 1.2
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

    if ('B181104' in sub_type):
        '''
        Making Adjustments based on simulation experiences from B181021
            1. the FC formal borrow range should be smaller, at highest rate, weird rate
            2. collateral range wider
        '''
        esti_type['BNI_LEND_P'][0] = 0
        esti_type['BNI_LEND_P'][1] = 3.5
        esti_type['BNI_BORR_P'][0] = 0
        esti_type['BNI_BORR_P'][1] = 3.5

        esti_type['BNF_SAVE_P'][0] = 0
        esti_type['BNF_SAVE_P'][1] = 3.5
        esti_type['BNF_BORR_P'][0] = 0
        esti_type['BNF_BORR_P'][1] = 3.5

        esti_type['R_FORMAL_SAVE'][0] = 1.0
        esti_type['R_FORMAL_SAVE'][1] = 1.050
        esti_type['R_FORMAL_BORR'][0] = 1.033
        esti_type['R_FORMAL_BORR'][1] = 1.133

        esti_type['kappa'][0] = 0.10
        esti_type['kappa'][1] = 0.90

        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 1.2
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

        if (sub_type == 'B181104b'):
            esti_type['logit_sd_scale'][0] = 0.90
            esti_type['logit_sd_scale'][1] = 1.1

    if ('B181107' in sub_type):
        '''
        Making Adjustments based on simulation experiences from B181021
            1. the FC formal borrow range should be smaller, at highest rate, weird rate
            2. collateral range wider
        '''
        esti_type['BNI_LEND_P'][0] = 0
        esti_type['BNI_LEND_P'][1] = 3
        esti_type['BNI_BORR_P'][0] = 0
        esti_type['BNI_BORR_P'][1] = 3

        esti_type['BNF_SAVE_P'][0] = 0
        esti_type['BNF_SAVE_P'][1] = 3
        esti_type['BNF_BORR_P'][0] = 0
        esti_type['BNF_BORR_P'][1] = 3

        esti_type['R_FORMAL_SAVE'][0] = 1.0
        esti_type['R_FORMAL_SAVE'][1] = 1.050
        esti_type['R_FORMAL_BORR'][0] = 1.033
        esti_type['R_FORMAL_BORR'][1] = 1.133

        esti_type['kappa'][0] = 0.10
        esti_type['kappa'][1] = 0.90

        esti_type['logit_sd_scale'][0] = np.linspace(0.90, 1.1, 10)[5 - 1]
        esti_type['logit_sd_scale'][1] = np.linspace(0.80, 1.2, 10)[7 - 1]
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

    main_type_str_list = ['20201025', 'B181021']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):
        esti_type['BNI_LEND_P'][0] = 0
        esti_type['BNI_LEND_P'][1] = 3
        esti_type['BNI_BORR_P'][0] = 0
        esti_type['BNI_BORR_P'][1] = 3

        esti_type['BNF_SAVE_P'][0] = 0
        esti_type['BNF_SAVE_P'][1] = 3
        esti_type['BNF_BORR_P'][0] = 0
        esti_type['BNF_BORR_P'][1] = 3

        esti_type['R_FORMAL_SAVE'][0] = 1.0
        esti_type['R_FORMAL_SAVE'][1] = 1.05
        esti_type['R_FORMAL_BORR'][0] = 1.05
        esti_type['R_FORMAL_BORR'][1] = 1.15

        # kappa[0] > 0 important, makes formal borrowing category feasible, reduces bug
        esti_type['kappa'][0] = 0.1
        esti_type['kappa'][1] = 0.9

        esti_type['logit_sd_scale'][0] = 0.80
        esti_type['logit_sd_scale'][1] = 1.2
        dist_type['data__A.params.sd'][0] = 0.10
        dist_type['data__A.params.sd'][1] = 1.00

    '''
    Remember update process_main.py:L160 with latest sub_type
    '''

    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['BNF_SAVE_P'])
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['BNF_BORR_P'])
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['BNI_LEND_P'])
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['BNI_BORR_P'])
    esti_type['kappa' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['kappa'])
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['BNF_SAVE_P'])
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['BNF_BORR_P'])
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['BNI_LEND_P'])
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['BNI_BORR_P'])
    esti_type['kappa' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['kappa'])
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['BNF_SAVE_P'])
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['BNF_BORR_P'])
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['BNI_LEND_P'])
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['BNI_BORR_P'])
    esti_type['kappa' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['kappa'])
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['BNF_SAVE_P'])
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['BNF_BORR_P'])
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['BNI_LEND_P'])
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['BNI_BORR_P'])
    esti_type['kappa' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['kappa'])

    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=1)][2] = seeds[25]
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=1)][2] = seeds[26]
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=1)][2] = seeds[27]
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=1)][2] = seeds[28]
    esti_type['kappa' + paramloopstr.peristr(period=1)][2] = seeds[29]
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=2)][2] = seeds[30]
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=2)][2] = seeds[31]
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=2)][2] = seeds[32]
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=2)][2] = seeds[33]
    esti_type['kappa' + paramloopstr.peristr(period=2)][2] = seeds[34]
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=3)][2] = seeds[35]
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=3)][2] = seeds[36]
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=3)][2] = seeds[37]
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=3)][2] = seeds[38]
    esti_type['kappa' + paramloopstr.peristr(period=3)][2] = seeds[39]
    esti_type['BNF_SAVE_P' + paramloopstr.peristr(period=4)][2] = seeds[40]
    esti_type['BNF_BORR_P' + paramloopstr.peristr(period=4)][2] = seeds[41]
    esti_type['BNI_LEND_P' + paramloopstr.peristr(period=4)][2] = seeds[42]
    esti_type['BNI_BORR_P' + paramloopstr.peristr(period=4)][2] = seeds[43]
    esti_type['kappa' + paramloopstr.peristr(period=4)][2] = seeds[44]

    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['R_FORMAL_BORR'])
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=1)] = copy.deepcopy(esti_type['R_FORMAL_SAVE'])
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['R_FORMAL_BORR'])
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=2)] = copy.deepcopy(esti_type['R_FORMAL_SAVE'])
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['R_FORMAL_BORR'])
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=3)] = copy.deepcopy(esti_type['R_FORMAL_SAVE'])
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['R_FORMAL_BORR'])
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=4)] = copy.deepcopy(esti_type['R_FORMAL_SAVE'])

    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=1)][2] = seeds[45]
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=1)][2] = seeds[46]
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=2)][2] = seeds[47]
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=2)][2] = seeds[48]
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=3)][2] = seeds[49]
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=3)][2] = seeds[50]
    esti_type['R_FORMAL_BORR' + paramloopstr.peristr(period=4)][2] = seeds[51]
    esti_type['R_FORMAL_SAVE' + paramloopstr.peristr(period=4)][2] = seeds[52]

    dist_type['data__A_mu' + paramloopstr.peristr(period=1) + '.params.mu'] = copy.deepcopy(
        dist_type['data__A.params.mu'])
    dist_type['data__A_mu' + paramloopstr.peristr(period=2) + '.params.mu'] = copy.deepcopy(
        dist_type['data__A.params.mu'])
    dist_type['data__A_mu' + paramloopstr.peristr(period=3) + '.params.mu'] = copy.deepcopy(
        dist_type['data__A.params.mu'])
    dist_type['data__A_mu' + paramloopstr.peristr(period=4) + '.params.mu'] = copy.deepcopy(
        dist_type['data__A.params.mu'])

    dist_type['data__A_mu' + paramloopstr.peristr(period=1) + '.params.mu'][2] = seeds[53]
    dist_type['data__A_mu' + paramloopstr.peristr(period=2) + '.params.mu'][2] = seeds[54]
    dist_type['data__A_mu' + paramloopstr.peristr(period=3) + '.params.mu'][2] = seeds[55]
    dist_type['data__A_mu' + paramloopstr.peristr(period=4) + '.params.mu'][2] = seeds[56]

    dist_type['data__A_sd' + paramloopstr.peristr(period=1) + '.params.sd'] = copy.deepcopy(
        dist_type['data__A.params.sd'])
    dist_type['data__A_sd' + paramloopstr.peristr(period=2) + '.params.sd'] = copy.deepcopy(
        dist_type['data__A.params.sd'])
    dist_type['data__A_sd' + paramloopstr.peristr(period=3) + '.params.sd'] = copy.deepcopy(
        dist_type['data__A.params.sd'])
    dist_type['data__A_sd' + paramloopstr.peristr(period=4) + '.params.sd'] = copy.deepcopy(
        dist_type['data__A.params.sd'])

    dist_type['data__A_sd' + paramloopstr.peristr(period=1) + '.params.sd'][2] = seeds[57]
    dist_type['data__A_sd' + paramloopstr.peristr(period=2) + '.params.sd'][2] = seeds[58]
    dist_type['data__A_sd' + paramloopstr.peristr(period=3) + '.params.sd'][2] = seeds[59]
    dist_type['data__A_sd' + paramloopstr.peristr(period=4) + '.params.sd'][2] = seeds[60]

    minmax_param = {
        'esti_type': esti_type,
        'data_type': data_type,
        'grid_type': grid_type,
        'dist_type': dist_type
    }

    return minmax_param, subtitle
