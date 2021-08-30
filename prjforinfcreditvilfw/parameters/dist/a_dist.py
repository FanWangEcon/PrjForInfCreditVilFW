'''

@author: fan
'''
import numpy as np
from scipy.stats import norm

import parameters.loop_combo_type_list.param_str as paramloopstr


def param(param_type=1):
    """
    Distributional parameters

    dist_param below is nost a list of parameters, but a list of distributional variables.

    For each distributional variables, there are multiple parameters.

    Modified code so that distributional variables are allowed. Write here this way
    to make it easier to understand the role of distributional variables.

    When looping over parameters, loop over individual parameter for each variable with dots
    as below. Looping of variables themselves don't make sense.

    in param_str_names.py:
        paramstr_dict_dist = \
            {'esti__BNF_SAVE_P_params_max': ['_DmmfsMx', 'dist_param.esti__BNF_SAVE_P.params.max'],
             'data__A_params_mu':          ['_DAprdMu', 'dist_param.data__A.params.mu']}

    in param_loops.py:
        if(param_type == 'dist_type' and param_name == 'data__A.params.mu'):
            ...
        if(param_type == 'dist_type' and param_name == 'esti__BNF_SAVE_P.params.max'):
            ...
        all in terms of each parameter of the distributional variable.

    If there are multiple separate items dist_param dictionary below, that means
        we are integrating over each of the dimensions jointly, with independent
        distributions.
    """

    module = param_type[0]
    sub_type = str(param_type[1])
    #     grid_type = grid[2]
    #     grid_type = grid[3]

    subtitle = 'zeroFE'

    '''
    When updating parameters for estimation:

    '''

    if (sub_type == '20180710'):
        subtitle = 'test'
        dist_param = {
            # BudgetConsumption
            'esti__BNF_SAVE_P': {'method': 'uniform',
                                 'params': {'min': 1,
                                            'max': 2},
                                 'integrate': {'method': 'grid',
                                               'params': {'points': 8}}},
            'data__A': {'dist': 'normal',
                        'params': {'mu': 1,
                                   'sd': 2},
                        'integrate': {'method': 'grid',
                                      'params': {'points': 8}}},
        }

        dist_param_integrate_points = gen_dist_param_integrate_points_sample()

    if (sub_type == 'NONE'):
        subtitle = 'None'
        dist_param = {}

    if (sub_type == '20180716'):
        subtitle = 'coreA'

        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': 8}}
                        }

        dist_param = {'data__A': data__A_dict,
                      'data__A_mu' + paramloopstr.peristr(period=1): data__A_dict,
                      'data__A_mu' + paramloopstr.peristr(period=2): data__A_dict,
                      'data__A_mu' + paramloopstr.peristr(period=3): data__A_dict,
                      'data__A_mu' + paramloopstr.peristr(period=4): data__A_dict,
                      'data__A_sd' + paramloopstr.peristr(period=1): data__A_dict,
                      'data__A_sd' + paramloopstr.peristr(period=2): data__A_dict,
                      'data__A_sd' + paramloopstr.peristr(period=3): data__A_dict,
                      'data__A_sd' + paramloopstr.peristr(period=4): data__A_dict}

    if (sub_type == '20181013'):
        '''
        32 simulation points
        '''
        subtitle = 'coreA'

        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': 10}}
                        }
        dist_param = {'data__A': data__A_dict}

    if (sub_type == '20181025'):
        '''
        starting now, mu and sd ignored, only care about epsA_frac_A and epsA_std if those exist
        '''
        subtitle = 'coreA'

        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': 10}}
                        }

        '''
            angeletos etc, epsA_std: 0.5
            0.5 permanent risk? me, trying things out
            see below: def gen_mu_sigma() for how this works
            sd = 0.5*sqrt(0.5) \sim 0.35
        '''
        dist_param = {'data__A': data__A_dict,
                      'epsA_frac_A': 0.5,
                      'epsA_std': 0.5}

    if (sub_type == '20181111'):
        '''
        To match up with previous result:
            "std_eps_E": 0.75
            "mean_eps": 0,
        '''
        subtitle = 'coreA'
        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': 10}}
                        }

        '''
            angeletos etc, epsA_std: 0.5
            0.5 permanent risk? me, trying things out
            see below: def gen_mu_sigma() for how this works
            sd = 0.5*sqrt(0.5) \sim 0.35
            0.75/sqrt(0.5)
        '''
        dist_param = {'data__A': data__A_dict,
                      'epsA_frac_A': 0.5,
                      'epsA_std': 1}

    if (sub_type == '20181025'):
        '''
        starting now, mu and sd ignored, only care about epsA_frac_A and epsA_std if those exist
        '''
        subtitle = 'coreA'

        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': 10}}
                        }

        '''
            angeletos etc, epsA_std: 0.5
            0.5 permanent risk? me, trying things out
            see below: def gen_mu_sigma() for how this works
            sd = 0.5*sqrt(0.5) \sim 0.35
        '''
        dist_param = {'data__A': data__A_dict,
                      'epsA_frac_A': 0.5,
                      'epsA_std': 0.5}

    '''
    Accomandates:
        20181025x, 20181025d, 20181025
        20201025x, 20201025d, 20201025
    '''
    main_type_str_list = ['20181025', '20201025']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        subtitle = 'coreA'

        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            inter_points = 3
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            inter_points = 20
        else:
            inter_points = 12

        '''
            0.5 permanent risk? me, trying things out
            see below: def gen_mu_sigma() for how this works
            sd = 0.5*sqrt(0.5) \sim 0.35
        '''
        data__A_dict = {'dist': 'normal',
                        'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                                   'sd': 0.25},
                        'integrate': {'method': 'grid', 'params': {'points': inter_points}}
                        }
        dist_param = {'data__A': data__A_dict,
                      'epsA_frac_A': 0.5,
                      'epsA_std': 0.5}

    return dist_param, subtitle


def gen_dist_param_integrate_points(dist_param):
    """Obtain distributional integration points and weights

    This is invoked parameters.paraminst.get_param_inst() after all param_inst
    parameters have been updated.

    Examples
    --------
    parameters.dist.a_dist.gen_dist_param_integrate_points()
    """

    if ('data__A' in dist_param):
        dist_param_integrate_points = gen_dist_param_integrate_points_A(dist_param)
    else:
        '''
        This means even though dist_param != {}, but does not contain
            dist_param['data_A'] key
        which means it contains data_A_ne0209 type region time specific key.
        This is invoked estimate.py:l79 for example 
        We do not need to generate the integration points at that spot. 
        In estimate_objective_multiperiods.py, will generate data_A key, and put values from
        data_A_ne0209 into there. which means when this function here
        is invoked again, we will have integration points. 
        '''
        dist_param_integrate_points = None

    return dist_param_integrate_points


def gen_mu_sigma(sigma=0.5, F=0.5, P=1):
    """Generate mean preserving component variance
    
    Examples
    --------
    import parameters.dist.a_dist as param_dist_a
    return_dict = param_dist_a.gen_mu_sigma(simga=sigma,F=F)    
    return_dict['mu_A']    
    return_dict['sigma_A']
    return_dict['mu_epsilon']
    return_dict['sigma_epsilon']    
    """
    # Return dict
    return_dict = {}

    # Means
    """
    So if I know the mu that I want, I can figure out what is the P I should have
    """
    mu = (np.log(P) / 2) - (sigma ** 2) / 4
    return_dict['mu_epsilon'] = mu
    return_dict['mu_A'] = mu

    # Standard Deviations
    return_dict['sigma_epsilon'] = sigma * np.sqrt(1 - F)
    return_dict['sigma_A'] = sigma * np.sqrt(F)

    # Return
    return return_dict


def gen_dist_param_integrate_points_A(dist_param):
    """generate dist_param_integrate_points, single parameter

    this is the core task, because I only have to integrate over productivity types
    """

    '''Single element'''
    data__A_dict = dist_param['data__A']
    mu_val = [v for k, v in data__A_dict['params'].items() if 'mu' in k]
    sd_val = [v for k, v in data__A_dict['params'].items() if 'sd' in k]

    #     if (dist_type_mu is None):
    dist_type_mu = mu_val[0]
    #     if (dist_type_sd is None):
    dist_type_sd = sd_val[0]

    dist_type_integrate_method = data__A_dict['integrate']['method']
    dist_type_integrate_points = data__A_dict['integrate']['params']['points']

    if (dist_type_integrate_method == 'grid'):
        min_quantile = 0.00
        max_quantile = 1.00

        quantile_brackets = np.linspace(min_quantile,
                                        max_quantile,
                                        dist_type_integrate_points + 1)

        param_value_weights = (quantile_brackets[1:] - quantile_brackets[:-1])
        quantile_brackets_points = (quantile_brackets[1:] + quantile_brackets[:-1]) / 2

        param_value_points = norm.ppf(quantile_brackets_points,
                                      loc=dist_type_mu,
                                      scale=dist_type_sd)

        # copied over from param_loops.py line 247
        min_v = np.min(param_value_points)
        param_save_suffixs = []
        param_descs = []
        for A in param_value_points:
            if (A < 0):
                str_rep = str(int(np.abs(A - min_v) * 10000))
            else:
                str_rep = str(int(np.abs(A - min_v) * 10000))
            param_save_suffixs.append(str_rep)
            param_descs.append('A=' + str(A))

        dist_param_integrate_points = \
            {'title_integrate_loop': 'Productivity Loop',
             'file_save_suffix_integrate_loop': '_A',
             'combo_desc_integrate_loop': 'Productivity',
             'param_types': ['data_type'],
             'param_names': ['A'],
             'param_values_keys': ['data_type_A'],
             'param_descs': param_descs,
             'param_save_suffixs': param_save_suffixs,
             'param_weights': param_value_weights,
             'param_values': {'data_type_A': param_value_points}}

    return dist_param_integrate_points


def gen_dist_param_integrate_points_sample():
    """from dist_param, generate intergate points

    dist_param has parameters that could shift, representing different mean and
    sd of different things.

    the integration program, simu_integrate_loop.py only wants:
        dist_param_integrate_points as shown below
        - this could be composed of N number of parameters for M sets of parameters
            values, of different param_types
        - any combinations of parameter values for the N number of parameters
        - different combinations could have whatever discretized weights

    """

    param_weights = np.array([0.3, 0.4, 0.3, 0.3, 0.4, 0.3, 0.3, 0.4, 0.3]) / 3.0

    dist_param_integrate_points = \
        {'title_integrate_loop': 'Fixed Cost Prod Joint',
         'file_save_suffix_integrate_loop': '_ABNF',
         'combo_desc_integrate_loop': 'info info info',
         'param_types': ['data_type', 'esti_type'],
         'param_names': ['A', 'BNF_SAVE_P'],
         'param_values_keys': ['data_type_A', 'esti_type_BNF_SAVE_P'],
         'param_descs': ['p11', 'p12', 'p13',
                         'p21', 'p22', 'p23',
                         'p31', 'p32', 'p33'],
         'param_save_suffixs': ['p11', 'p12', 'p13',
                                'p21', 'p22', 'p23',
                                'p31', 'p32', 'p33'],
         'param_weights': param_weights,
         'param_values': {'data_type_A': [0.5, 0.6, 0.7, 0.5, 0.6, 0.7, 0.5, 0.6, 0.7],
                          'esti_type_BNF_SAVE_P': [1, 1, 1, 2, 2, 2, 3, 3, 3]}}

    return dist_param_integrate_points
