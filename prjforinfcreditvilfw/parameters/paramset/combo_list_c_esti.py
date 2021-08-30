'''
@author: fan
'''

import numpy as np

import parameters.esti.a_esti as param_esti_a
import parameters.loop_param_combo_list.loops_gen as paramloops


def get_combo_list(combo_type=['c', '20180513a'],
                   compesti_specs=None):
    """
    Five key estimation related parameters:
        esti_method = None
        param_esti_list_key = None
        moment_type = None
        esti_option_type = None
        esti_func_type = None

    - specified as None at first
    - can be replaced by compesti_specs dictionary, specified in estimate_specs
    - if do not have compesti_specs, there are default estimate_specs associate with each sub_type
    """

    module = combo_type[0]
    sub_type = combo_type[1]

    """
    If compesti_specs specified from outside via estimate_specs.py
    """
    esti_method = None
    param_esti_list_key = None
    moments_type = None
    momsets_type = None
    esti_option_type = None
    esti_func_type = None
    esti_init_rand_seed = None
    esti_rand_count = None

    if ('esti_method' in compesti_specs.keys()):
        esti_method = compesti_specs['esti_method']
    if ('moments_type' in compesti_specs.keys()):
        moments_type = compesti_specs['moments_type']
    if ('momsets_type' in compesti_specs.keys()):
        momsets_type = compesti_specs['momsets_type']
    if ('esti_option_type' in compesti_specs.keys()):
        esti_option_type = compesti_specs['esti_option_type']
    if ('esti_func_type' in compesti_specs.keys()):
        esti_func_type = compesti_specs['esti_func_type']
    if ('param_grid_or_rand' in compesti_specs.keys()):
        param_grid_or_rand = compesti_specs['param_grid_or_rand']
    if ('esti_param_vec_count' in compesti_specs.keys()):
        esti_param_vec_count = compesti_specs['esti_param_vec_count']

    """
    Estimate groups
    """

    if ("20180723" in sub_type):

        '''
        Small, Dense or Normal
        '''
        if ("20180723x" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("20180723d" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        '''
        Integrate or not
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        # TEST 1: 20180723x_2312
        if ("_2312" in sub_type):
            """
            First Estimation Tester:
                do not need to specify, in fact, do not specify any parameters here
            """

            if (esti_method == None):
                esti_method = 'MomentsSimuStates'
            if (moments_type == None):
                moments_type = ['a', '20180805a']
            if (momsets_type == None):
                momsets_type = ['a', '20180805a']
            if (esti_option_type == None):
                esti_option_type = 2
            if (esti_func_type == None):
                esti_func_type = 'Nelder-Mead'
            if (param_grid_or_rand == None):
                param_grid_or_rand = 'rand'
            if (esti_param_vec_count == None):
                esti_param_vec_count = 1

            if (esti_init_rand_seed is None):
                kappa_init_fixed = 0.7
                kappa_init_list = [kappa_init_fixed]
            else:
                np.random.seed(esti_init_rand_seed)
                kappa_init_list = np.random.rand(esti_rand_count)

            rand_init_list = [{'kappa': kappa_init}
                              for kappa_init in (kappa_init_list)]

            combo_list = \
                [{'param_update_dict': {'grid_type': grid_type,
                                        'esti_type': ['a', '20180628',
                                                      {'kappa': cur_init['kappa']}],
                                        'data_type': ['a', '20180607'],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': interpolant_type,
                                        'dist_type': ['a', dist_t]}
                     , 'title': 'estimation basic tester'
                     , 'combo_desc': 'estimation basic tester'
                     , 'file_save_suffix': '_' + str(ctr)
                     , 'param_combo_list_ctr_str': '_c' + str(ctr)
                     , 'esti_method': esti_method
                     , 'param_esti_list_key': param_esti_list_key
                     , 'moments_type': moments_type
                     , 'momsets_type': momsets_type
                     , 'esti_option_type': esti_option_type
                     , 'esti_func_type': esti_func_type}
                 for ctr, cur_init in enumerate(rand_init_list)]

        # TEST 2: 20180723x_flex
        if ("_flex" in sub_type):
            '''2018-07-30 10:03
            second Estimation tester, test alpha_k. Perhaps Kappa has too little
            effects on probability. alpha_k, we know, has large effects on aggregates.
            '''

            if (esti_method == None):
                esti_method = 'MomentsSimuStates'
            if (moments_type == None):
                moments_type = ['a', '20180805a']
            if (momsets_type == None):
                momsets_type = ['a', '20180805a']
            if (esti_option_type == None):
                esti_option_type = 2
            if (esti_func_type == None):
                esti_func_type = 'L-BFGS-B'  # constrained optimization
            if (param_grid_or_rand == None):
                param_grid_or_rand = 'rand'
            if (esti_param_vec_count == None):
                esti_param_vec_count = 1

            '''
            Estimating parameter initial values
            '''
            esti_type = ['a', '20180628']
            alpha_k_base = param_esti_a.param(esti_type)[0]['alpha_k']
            if (esti_init_rand_seed is None):
                alpha_k_init_list = [alpha_k_base]
            else:
                np.random.seed(esti_init_rand_seed)
                alpha_k_init_list = (np.random.rand(esti_rand_count) - 0.5) / 10 + alpha_k_base

            rand_init_list = [{'alpha_k': kappa_init}
                              for kappa_init in (alpha_k_init_list)]

            combo_list = \
                [{'param_update_dict': {'grid_type': grid_type,
                                        'esti_type': [esti_type[0], esti_type[1],
                                                      {'alpha_k': cur_init['alpha_k']}],
                                        'data_type': ['a', '20180607'],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': interpolant_type,
                                        'dist_type': ['a', dist_t]}
                     , 'title': 'estimation basic tester 2'
                     , 'combo_desc': 'estimation basic tester 2'
                     , 'file_save_suffix': '_' + str(ctr)
                     , 'param_combo_list_ctr_str': '_c' + str(ctr)
                     , 'esti_method': esti_method
                     , 'moments_type': moments_type
                     , 'momsets_type': momsets_type
                     , 'esti_option_type': esti_option_type
                     , 'esti_func_type': esti_func_type}
                 for ctr, cur_init in enumerate(rand_init_list)]

    if ("20180801" in sub_type):

        '''
        Small, Dense or Normal
        '''
        if ("20180801x" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("20180801d" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        '''
        Integrate or not
        '''

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        if (compesti_specs['esti_method'] == None):
            compesti_specs['esti_method'] = 'MomentsSimuStates'

        if (compesti_specs['moments_type'] == None):
            compesti_specs['moments_type'] = ['a', '20180805a']

        if (compesti_specs['momsets_type'] == None):
            compesti_specs['momsets_type'] = ['a', '20180805b']

        if (compesti_specs['esti_option_type'] == None):
            compesti_specs['esti_option_type'] = 2

        if (compesti_specs['esti_func_type'] == None):
            compesti_specs['esti_func_type'] = 'L-BFGS-B'

        if (compesti_specs['param_grid_or_rand'] == None):
            compesti_specs['param_grid_or_rand'] = 'rand'

        if (compesti_specs['esti_param_vec_count'] == None):
            compesti_specs['esti_param_vec_count'] = 3

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180628',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t='20180801')

    if ("20180814" in sub_type):
        '''
        Updating estimation
            + interest rates for Central Second Period
        '''
        if ("20180814x" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("20180814d" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        '''
        Integrate or not
        '''

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180814',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t='20180801')

    main_type_str = '20180815'
    if (main_type_str in sub_type):
        '''
        Joint estimation of two periods with shared and not-shared parameters
        Period specific interest rates
        estimating different fixed cost and collateral parameters
        share preference and technology parameters
        '''
        if (main_type_str + "x" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif (main_type_str + "d" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        '''
        Integrate or not
        '''

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180815',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t='20180801')

    '''
    2018-09-01 12:15
    Wider min-max range for estimation several parameters
    Also now have 4 regions + times. Don't have to be in the same estimation though.
        20180901 switched to 0916:
            - major debug: 
                1. rhoo was not changing
                2. lgit was not working due to high and low values
            - but the _t below are the same
    
    '''
    main_type_str_list = ['20180901', '20180918', '20180925']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        '''
        Joint estimation of two periods with shared and not-shared parameters
        Period specific interest rates
        estimating different fixed cost and collateral parameters
        share preference and technology parameters
        '''
        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        '''
        Integrate or not
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        '''
        min max range adjustments
        '''
        if ('20180901' in sub_type):
            minmax_t = '20180901'
        elif ('20180918' in sub_type):
            minmax_t = '20180917'
        elif ('20180925' in sub_type):
            minmax_t = '20180925'
        else:
            raise ('bad')

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180815',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t=minmax_t)

    return combo_list
