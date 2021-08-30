'''
@author: fan
'''

import logging
import pyfan.amto.json.json as support_json

import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def param_type_name_to_param_inst_attribute(param_type, reverse=False):
    """
    USE param_type_param_name BELOW

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    param_inst_attribute = paramloopstr.param_type_name_to_param_inst_attribute(param_type)
    """
    pass


def update_param_inst(param_inst, param_esti_group_key, param_val):
    """Decomposing the second element of the value in dictionary below

    update param_inst. 
    in mpoly estimate, update param_inst based on current estimate

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    param_inst = paramloopstr.update_param_inst(param_inst, param_esti_group_key, param_val)
    """

    param_shortname, param_type, param_name = param_type_param_name(param_group_key=param_esti_group_key)

    '''
    1. get param inst component
    '''
    if (param_type == 'esti_type'):
        param_inst_group = param_inst.esti_param
    if (param_type == 'grid_type'):
        param_inst_group = param_inst.grid_param
    if (param_type == 'interpolant_type'):
        param_inst_group = param_inst.interpolant
    if (param_type == 'dist_type'):
        param_inst_group = param_inst.dist_param
    if (param_type == 'data_type'):
        param_inst_group = param_inst.data_param

    '''
    2. update dictionary 
    '''
    if (len(param_inst_group) > 0):
        param_name_list = param_name.split('.')
        if (len(param_name_list) == 1):
            param_inst_group[param_name] = param_val
        elif (len(param_name_list) == 2):
            param_inst_group[param_name_list[0]][param_name_list[1]] = param_val
        elif (len(param_name_list) == 3):
            param_inst_group[param_name_list[0]][param_name_list[1]][param_name_list[2]] = param_val
        else:
            message = 'param_key_list:' + str(param_name_list) + ', too many dots, > 3, too nested'
            logger.debug(message)
            raise ValueError(message)
    else:
        '''
            if dist_type = {} for example, do not try to fill it
            only none for: data__A_params_mu_ce9901', 'data__A_params_sd_ce9901
                            these parameters when estimating without integration do not exist 
        '''
        param_val = None

    '''
    3. update param_inst
    '''
    if (param_type == 'esti_type'):
        param_inst.esti_param = param_inst_group
    if (param_type == 'grid_type'):
        param_inst.grid_param = param_inst_group
    if (param_type == 'interpolant_type'):
        param_inst.interpolant = param_inst_group
    if (param_type == 'dist_type'):
        param_inst.dist_param = param_inst_group
    if (param_type == 'data_type'):
        param_inst.data_param = param_inst_group

    return param_inst


def get_current_init_param_values(param_esti_group_key, param_inst):
    param_shortname, param_type, param_name = param_type_param_name(param_group_key=param_esti_group_key)
    if (param_type == 'esti_type'):
        param_inst_group = param_inst.esti_param
    if (param_type == 'grid_type'):
        param_inst_group = param_inst.grid_param
    if (param_type == 'interpolant_type'):
        param_inst_group = param_inst.interpolant
    if (param_type == 'dist_type'):
        param_inst_group = param_inst.dist_param
    if (param_type == 'data_type'):
        param_inst_group = param_inst.data_param

    '''This is if the key has nested tiers. Mainly for dist_param.'''
    if (len(param_inst_group) > 0):
        param_name_list = param_name.split('.')
        if (len(param_name_list) == 1):
            param_val = param_inst_group[param_name]
        elif (len(param_name_list) == 2):
            param_val = param_inst_group[param_name_list[0]][param_name_list[1]]
        elif (len(param_name_list) == 3):
            param_val = param_inst_group[param_name_list[0]][param_name_list[1]][param_name_list[2]]
        else:
            message = 'param_key_list:' + str(param_name_list) + ', too many dots, > 3, too nested'
            logger.debug(message)
            raise ValueError(message)
    else:
        '''
            if dist_type = {} for example, do not try to fill it
            only none for: data__A_params_mu_ce9901', 'data__A_params_sd_ce9901
                            these parameters when estimating without integration do not exist 
        '''
        param_val = None

    return param_val, param_type, param_name


def param_type_param_name(param_group_key='esti_param.alpha_k', return_param_key=False, split=False):
    """Decomposing the second element of the value in dictionary below

    param_group_key = param_type_name: group = type, key = name

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    param_shortname, param_type, param_name = paramloopstr.param_type_param_name(param_group_key=param_group_key)
    """

    param_type = param_group_key.split(".")[0]
    if (param_type == 'interpolant'):
        param_type = 'interpolant_type'
    else:
        param_type = param_type.replace('_param', '_type')
    # this allows for fdots laters not be be broken for dist_param
    param_name = param_group_key[(param_group_key.index(".") + 1):]

    paramstr_dict = param2str()
    #     logger.warning('param_group_key:%s', param_group_key)
    for key, val_list in paramstr_dict.items():
        #         logger.warning('val_list[1]:%s', val_list[1].strip())
        if (val_list[1].strip() == param_group_key):
            param_shortname = val_list[0][1:]  # drop the starting dash
            param_key = key

    if (split):
        param_type_param = param_group_key.split(".")[0]
        return param_type_param, param_name
    elif (return_param_key):
        return param_key
    else:
        return param_shortname, param_type, param_name


def period_vars(period=1, param_esti_group_key_list=[]):
    """

    Parameters
    ----------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    cur_period_vars, cur_period_vars_trans = paramloopstr.period_vars(period=1)
    """
    paramstr_dict = param2str()
    equi_trans_dict = param_str_equi()

    cur_period_keys = []
    cur_period_keys_trans = []

    for paramstr_dict_key, paramstr_dict_val in paramstr_dict.items():

        period_str = peristr(period=period, action='str')
        period_suffix = period_str
        if ((period_suffix in paramstr_dict_key)
                and
                (paramstr_dict_val[1] in param_esti_group_key_list)):
            cur_period_keys.append(paramstr_dict_key)
            cur_period_keys_trans.append(equi_trans_dict[paramstr_dict_key][0])

    return cur_period_keys, cur_period_keys_trans


def peristr(period=None, action='str'):
    """Combined string of the two for command line invoke

    period string control

    import parameters.runspecs.estimate_specs as estispec
    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')
    compute_spec_key = spec_key_dict['compute_spec_key']
    esti_spec_key = spec_key_dict['esti_spec_key']

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    period_str = paramloopstr.peristr(period=0, action='period_name')
    periods = paramloopstr.peristr(action='list')
    """

    return hardstring.peristr(period=period, action=action)


def param_str_equi():
    period_list = peristr(action='list')

    equivalence_keys = {}

    for cur_period in period_list:
        equivalence_keys['BNF_SAVE_P' + peristr(period=cur_period)] = ['BNF_SAVE_P']
        equivalence_keys['BNI_LEND_P' + peristr(period=cur_period)] = ['BNI_LEND_P']
        equivalence_keys['BNF_BORR_P' + peristr(period=cur_period)] = ['BNF_BORR_P']
        equivalence_keys['BNI_BORR_P' + peristr(period=cur_period)] = ['BNI_BORR_P']
        equivalence_keys['kappa' + peristr(period=cur_period)] = ['kappa']

        equivalence_keys['R_INFORM_SAVE' + peristr(period=cur_period)] = ['R_INFORM_SAVE']
        equivalence_keys['R_INFORM_BORR' + peristr(period=cur_period)] = ['R_INFORM_BORR']
        equivalence_keys['R_FORMAL_BORR' + peristr(period=cur_period)] = ['R_FORMAL_BORR']
        equivalence_keys['R_FORMAL_SAVE' + peristr(period=cur_period)] = ['R_FORMAL_SAVE']

        equivalence_keys['data__A_params_mu' + peristr(period=cur_period)] = ['data__A_params_mu']
        equivalence_keys['data__A_params_sd' + peristr(period=cur_period)] = ['data__A_params_sd']

    return equivalence_keys


def param2str():
    """
    {param_key: [param_savestr, param_group.param_name]}
    {param_key: [param_savestr, param_group.param_name]}
    together second term is param_str_group_name
    together second term is param_group_name

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    paramstr_dict = paramloopstr.param2str()
    """

    # 7
    paramstr_dict_esti_param = \
        {'alpha_k': ['_alpk', 'esti_param.alpha_k'],
         'beta': ['_beta', 'esti_param.beta'],
         'K_DEPRECIATION': ['_depr', 'esti_param.K_DEPRECIATION'],
         'rho': ['_rhoo', 'esti_param.rho'],
         'logit_sd_scale': ['_lgit', 'esti_param.logit_sd_scale'],  # X2
         'CEV_PROP_INCREASE': ['_cev', 'esti_param.CEV_PROP_INCREASE'],  # proportional c increase

         'BNF_SAVE_P': ['_fcfs', 'esti_param.BNF_SAVE_P'],
         'BNF_BORR_P': ['_fcfb', 'esti_param.BNF_BORR_P'],
         'BNI_LEND_P': ['_fcil', 'esti_param.BNI_LEND_P'],
         'BNI_BORR_P': ['_fcib', 'esti_param.BNI_BORR_P'],
         'kappa': ['_kapp', 'esti_param.kappa'],

         'BNF_SAVE_P' + peristr(period=1): ['_fcfs' + peristr(period=1),
                                            'esti_param.BNF_SAVE_P' + peristr(period=1)],
         'BNF_BORR_P' + peristr(period=1): ['_fcfb' + peristr(period=1),
                                            'esti_param.BNF_BORR_P' + peristr(period=1)],
         'BNI_LEND_P' + peristr(period=1): ['_fcil' + peristr(period=1),
                                            'esti_param.BNI_LEND_P' + peristr(period=1)],
         'BNI_BORR_P' + peristr(period=1): ['_fcib' + peristr(period=1),
                                            'esti_param.BNI_BORR_P' + peristr(period=1)],
         'kappa' + peristr(period=1): ['_kapp' + peristr(period=1), 'esti_param.kappa' + peristr(period=1)],
         'BNF_SAVE_P' + peristr(period=2): ['_fcfs' + peristr(period=2),
                                            'esti_param.BNF_SAVE_P' + peristr(period=2)],
         'BNF_BORR_P' + peristr(period=2): ['_fcfb' + peristr(period=2),
                                            'esti_param.BNF_BORR_P' + peristr(period=2)],
         'BNI_LEND_P' + peristr(period=2): ['_fcil' + peristr(period=2),
                                            'esti_param.BNI_LEND_P' + peristr(period=2)],
         'BNI_BORR_P' + peristr(period=2): ['_fcib' + peristr(period=2),
                                            'esti_param.BNI_BORR_P' + peristr(period=2)],
         'kappa' + peristr(period=2): ['_kapp' + peristr(period=2), 'esti_param.kappa' + peristr(period=2)],
         'BNF_SAVE_P' + peristr(period=3): ['_fcfs' + peristr(period=3),
                                            'esti_param.BNF_SAVE_P' + peristr(period=3)],
         'BNF_BORR_P' + peristr(period=3): ['_fcfb' + peristr(period=3),
                                            'esti_param.BNF_BORR_P' + peristr(period=3)],
         'BNI_LEND_P' + peristr(period=3): ['_fcil' + peristr(period=3),
                                            'esti_param.BNI_LEND_P' + peristr(period=3)],
         'BNI_BORR_P' + peristr(period=3): ['_fcib' + peristr(period=3),
                                            'esti_param.BNI_BORR_P' + peristr(period=3)],
         'kappa' + peristr(period=3): ['_kapp' + peristr(period=3), 'esti_param.kappa' + peristr(period=3)],
         'BNF_SAVE_P' + peristr(period=4): ['_fcfs' + peristr(period=4),
                                            'esti_param.BNF_SAVE_P' + peristr(period=4)],
         'BNF_BORR_P' + peristr(period=4): ['_fcfb' + peristr(period=4),
                                            'esti_param.BNF_BORR_P' + peristr(period=4)],
         'BNI_LEND_P' + peristr(period=4): ['_fcil' + peristr(period=4),
                                            'esti_param.BNI_LEND_P' + peristr(period=4)],
         'BNI_BORR_P' + peristr(period=4): ['_fcib' + peristr(period=4),
                                            'esti_param.BNI_BORR_P' + peristr(period=4)],
         'kappa' + peristr(period=4): ['_kapp' + peristr(period=4), 'esti_param.kappa' + peristr(period=4)],

         'R_INFORM_SAVE': ['_rinfs', 'esti_param.R_INFORM_SAVE'],  # X2
         'R_INFORM_BORR': ['_rinfb', 'esti_param.R_INFORM_BORR'],  # X2
         'R_FORMAL_SAVE': ['_fsvR', 'esti_param.R_FORMAL_SAVE'],
         'R_FORMAL_BORR': ['_fbrR', 'esti_param.R_FORMAL_BORR'],

         'R_INFORM_SAVE' + peristr(period=1): ['_rinfs' + peristr(period=1),
                                               'esti_param.R_INFORM_SAVE' + peristr(period=1)],  # X2
         'R_INFORM_BORR' + peristr(period=1): ['_rinfb' + peristr(period=1),
                                               'esti_param.R_INFORM_BORR' + peristr(period=1)],  # X2
         'R_FORMAL_SAVE' + peristr(period=1): ['_fsvR' + peristr(period=1),
                                               'esti_param.R_FORMAL_SAVE' + peristr(period=1)],
         'R_FORMAL_BORR' + peristr(period=1): ['_fbrR' + peristr(period=1),
                                               'esti_param.R_FORMAL_BORR' + peristr(period=1)],

         'R_INFORM_SAVE' + peristr(period=2): ['_rinfs' + peristr(period=2),
                                               'esti_param.R_INFORM_SAVE' + peristr(period=2)],  # X2
         'R_INFORM_BORR' + peristr(period=2): ['_rinfb' + peristr(period=2),
                                               'esti_param.R_INFORM_BORR' + peristr(period=2)],  # X2
         'R_FORMAL_SAVE' + peristr(period=2): ['_fsvR' + peristr(period=2),
                                               'esti_param.R_FORMAL_SAVE' + peristr(period=2)],
         'R_FORMAL_BORR' + peristr(period=2): ['_fbrR' + peristr(period=2),
                                               'esti_param.R_FORMAL_BORR' + peristr(period=2)],

         'R_INFORM_SAVE' + peristr(period=3): ['_rinfs' + peristr(period=3),
                                               'esti_param.R_INFORM_SAVE' + peristr(period=3)],  # X2
         'R_INFORM_BORR' + peristr(period=3): ['_rinfb' + peristr(period=3),
                                               'esti_param.R_INFORM_BORR' + peristr(period=3)],  # X2
         'R_FORMAL_SAVE' + peristr(period=3): ['_fsvR' + peristr(period=3),
                                               'esti_param.R_FORMAL_SAVE' + peristr(period=3)],
         'R_FORMAL_BORR' + peristr(period=3): ['_fbrR' + peristr(period=3),
                                               'esti_param.R_FORMAL_BORR' + peristr(period=3)],

         'R_INFORM_SAVE' + peristr(period=4): ['_rinfs' + peristr(period=4),
                                               'esti_param.R_INFORM_SAVE' + peristr(period=4)],  # X2
         'R_INFORM_BORR' + peristr(period=4): ['_rinfb' + peristr(period=4),
                                               'esti_param.R_INFORM_BORR' + peristr(period=4)],  # X2
         'R_FORMAL_SAVE' + peristr(period=4): ['_fsvR' + peristr(period=4),
                                               'esti_param.R_FORMAL_SAVE' + peristr(period=4)],
         'R_FORMAL_BORR' + peristr(period=4): ['_fbrR' + peristr(period=4),
                                               'esti_param.R_FORMAL_BORR' + peristr(period=4)],

         }

    paramstr_dict_data_param = \
        {'A': ['_Aprd', 'data_param.A'],
         }

    # 5
    paramstr_dict_grid_param = \
        {'std_eps': ['_step', 'grid_param.std_eps'],  # X2
         'len_states': ['_lenstates', 'grid_param.len_states'],
         'len_choices': ['_lenchoice', 'grid_param.len_choices'],
         'max_steady_coh': ['_maxstdcoh', 'grid_param.max_steady_coh'],
         'markov_points': ['_markovpts', 'grid_param.markov_points'],
         'BNF_SAVE_P_startVal': ['_mmfs', 'grid_param.BNF_SAVE_P_startVal'],
         'BNF_BORR_P_startVal': ['_mmfb', 'grid_param.BNF_BORR_P_startVal'],  # X!2
         'BNI_LEND_P_startVal': ['_mmil', 'grid_param.BNI_LEND_P_startVal'],
         'BNI_BORR_P_startVal': ['_mmib', 'grid_param.BNI_BORR_P_startVal'],
         }

    # 1
    paramstr_dict_interpolant = \
        {'maxinter': ['_vfimaxitr', 'interpolant.maxinter']
         }

    # 2
    paramstr_dict_dist = \
        {'epsA_frac_A': ['_fA', 'dist_param.epsA_frac_A'],
         'epsA_std': ['_steAp', 'dist_param.epsA_std'],

         'esti__BNF_SAVE_P_params_max': ['_DmmfsMx', 'dist_param.esti__BNF_SAVE_P.params.max'],

         'data__A_params_mu': ['_DAprdMu', 'dist_param.data__A.params.mu'],

         'data__A_params_mu' + peristr(period=1): ['_DAprdMu' + peristr(period=1),
                                                   'dist_param.data__A_mu' + peristr(period=1) + '.params.mu'],
         'data__A_params_mu' + peristr(period=2): ['_DAprdMu' + peristr(period=2),
                                                   'dist_param.data__A_mu' + peristr(period=2) + '.params.mu'],
         'data__A_params_mu' + peristr(period=3): ['_DAprdMu' + peristr(period=3),
                                                   'dist_param.data__A_mu' + peristr(period=3) + '.params.mu'],
         'data__A_params_mu' + peristr(period=4): ['_DAprdMu' + peristr(period=4),
                                                   'dist_param.data__A_mu' + peristr(period=4) + '.params.mu'],

         'data__A_params_sd': ['_DAprdSd', 'dist_param.data__A.params.sd'],

         'data__A_params_sd' + peristr(period=1): ['_DAprdSd' + peristr(period=1),
                                                   'dist_param.data__A_sd' + peristr(period=1) + '.params.sd'],
         'data__A_params_sd' + peristr(period=2): ['_DAprdSd' + peristr(period=2),
                                                   'dist_param.data__A_sd' + peristr(period=2) + '.params.sd'],
         'data__A_params_sd' + peristr(period=3): ['_DAprdSd' + peristr(period=3),
                                                   'dist_param.data__A_sd' + peristr(period=3) + '.params.sd'],
         'data__A_params_sd' + peristr(period=4): ['_DAprdSd' + peristr(period=4),
                                                   'dist_param.data__A_sd' + peristr(period=4) + '.params.sd'],
         }

    # 13 together
    paramstr_dict = paramstr_dict_esti_param
    paramstr_dict.update(paramstr_dict_data_param)
    paramstr_dict.update(paramstr_dict_grid_param)
    paramstr_dict.update(paramstr_dict_interpolant)
    paramstr_dict.update(paramstr_dict_dist)

    return paramstr_dict


def test_cases():
    cur_period_keys, cur_period_keys_trans = period_vars(period=1)
    support_json.jdump(cur_period_keys, 'cur_period_keys 1', logger=logger.warning)
    support_json.jdump(cur_period_keys_trans, 'cur_period_keys_trans 1', logger=logger.warning)

    cur_period_keys, cur_period_keys_trans = period_vars(period=2)
    support_json.jdump(cur_period_keys, 'cur_period_keys 2', logger=logger.warning)
    support_json.jdump(cur_period_keys_trans, 'cur_period_keys_trans 2', logger=logger.warning)

    cur_period_keys, cur_period_keys_trans = period_vars(period=3)
    support_json.jdump(cur_period_keys, 'cur_period_keys 3', logger=logger.warning)
    support_json.jdump(cur_period_keys_trans, 'cur_period_keys_trans 3', logger=logger.warning)

    cur_period_keys, cur_period_keys_trans = period_vars(period=4)
    support_json.jdump(cur_period_keys, 'cur_period_keys 4', logger=logger.warning)
    support_json.jdump(cur_period_keys_trans, 'cur_period_keys_trans 4', logger=logger.warning)

    paramstr_dict = param2str()
    support_json.jdump(paramstr_dict, 'paramstr_dict', logger=logger.warning)


if __name__ == "__main__":
    test_cases()
