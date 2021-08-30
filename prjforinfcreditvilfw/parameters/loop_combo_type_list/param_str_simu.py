'''

@author: fan

import parameters.paramset.param_str_names as paramstrnames
'''


def param2str_groups_simu():
    """
    Examples
    --------
    import parameters.loop_param_combo_list.combo_type_list.param_str as paramloopstr
    list_all = paramstrnames.param2str_groups_simu()
    """

    list_esti = ['alpha_k', 'beta', 'K_DEPRECIATION',
                 'rho', 'R_INFORM_SAVE', 'logit_sd_scale',
                 'std_eps', 'A']

    list_solu = ['len_states', 'len_choices',
                 'max_steady_coh', 'markov_points',
                 'maxinter']

    # memr = regular memory
    list_memr = ['alpha_k', 'beta', 'K_DEPRECIATION',  # 3
                 'rho', 'R_INFORM_SAVE', 'logit_sd_scale',  # 6
                 'std_eps', 'A',  # 8
                 'max_steady_coh', 'markov_points',  # 10
                 'maxinter',  # 11
                 'R_FORMAL_SAVE', 'R_FORMAL_BORR',  # 13
                 'BNF_SAVE_P', 'BNF_BORR_P',  # 15
                 'BNI_LEND_P', 'BNI_BORR_P',  # 17
                 'BNF_SAVE_P_startVal', 'BNF_BORR_P_startVal',  # 19
                 'BNI_LEND_P_startVal', 'BNI_BORR_P_startVal',  # 21
                 'kappa']  # 22

    list_memr_esti = ['alpha_k', 'beta', 'K_DEPRECIATION',  # 3
                      'rho', 'R_INFORM_SAVE', 'logit_sd_scale',  # 6
                      'std_eps', 'A',  # 8
                      'R_FORMAL_SAVE', 'R_FORMAL_BORR',  # 13
                      'BNF_SAVE_P', 'BNF_BORR_P',  # 15
                      'BNI_LEND_P', 'BNI_BORR_P',  # 17
                      'kappa']  # 22

    # integration list 
    list_intg = list_memr + ['data__A_params_mu', 'data__A_params_sd']
    list_esti_intg = list_memr_esti + ['data__A_params_mu', 'data__A_params_sd']

    # 20 main parameters, created when had 20 fargate task allowances
    list_20mn = ['alpha_k', 'beta', 'K_DEPRECIATION',  # 3
                 'rho', 'R_INFORM_SAVE', 'logit_sd_scale',  # 6
                 'std_eps', 'A',  # 8
                 'max_steady_coh',  # 9
                 'R_FORMAL_SAVE', 'R_FORMAL_BORR',  # 11
                 'BNF_SAVE_P', 'BNF_BORR_P',  # 13
                 'BNI_LEND_P', 'BNI_BORR_P',  # 15
                 'BNF_SAVE_P_startVal', 'BNF_BORR_P_startVal',  # 17
                 'BNI_LEND_P_startVal', 'BNI_BORR_P_startVal',  # 19
                 'kappa']  # 20

    # parameters some grid values require very large memories
    list_larg = ['len_states', 'len_choices']

    '''Combine Lists'''
    param_list_all = {'list_esti': list_esti,
                      'list_solu': list_solu,
                      'list_reg_memory': list_memr,
                      'list_reg_memory_itg': list_intg,
                      'list_esti_memory_itg': list_esti_intg,
                      'list_reg_memory_main_20': list_20mn,
                      'list_big_memory': list_larg}

    return param_list_all
