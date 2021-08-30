'''

@author: fan
'''

import logging
import pyfan.amto.json.json as support_json

import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.hardcode.str_periodkey as hardcode_periodkey
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def param2str_groups_esti_Fxc(gen_type=0, periods_key_list=[1, 2]):
    """
    Fixed Informal borrow across periods, allow other parameters to shift
    """

    periods_keys_dict = hardcode_periodkey.region_time_dict()

    if (gen_type == 0):
        list_policy_FinXc = []
    elif (gen_type == 1):
        list_policy_FinXc = ['BNI_BORR_P']
    else:
        raise ('bad')

    for key, vals in periods_keys_dict.items():
        if (vals[1] in periods_key_list):
            cur_suffix = hardcode_periodkey.peristr(period=vals[1])

            #             list_policy_Fxc = ['data__A_params_mu' + cur_suffix,
            #                                'data__A_params_sd' + cur_suffix,
            #                                'BNF_SAVE_P' + cur_suffix,
            #                                'BNF_BORR_P' + cur_suffix,
            #                                'BNI_LEND_P' + cur_suffix,]

            list_policy_Fxc = ['BNF_SAVE_P' + cur_suffix,
                               'BNF_BORR_P' + cur_suffix,
                               'BNI_LEND_P' + cur_suffix, ]

            if (gen_type == 0):
                list_policy_Fxc = list_policy_Fxc + ['BNI_BORR_P' + cur_suffix]
            elif (gen_type == 1):
                pass
            else:
                raise ('bad')

            list_policy_Kap = ['kappa' + cur_suffix]
            list_policy_FinXc = list_policy_FinXc + list_policy_Fxc + list_policy_Kap

    return list_policy_FinXc


def param2str_groups_esti():
    """
    Examples
    --------
    import parameters.loop_combo_type_list.param_str_esti as paramstrnames
    list_all = paramstrnames.param2str_groups_esti()
    """

    '''
    Policy Parameters
    '''
    list_policy_Rsb = ['R_FORMAL_SAVE', 'R_FORMAL_BORR']

    list_policy_Fxc = ['BNF_SAVE_P', 'BNF_BORR_P',
                       'BNI_LEND_P', 'BNI_BORR_P']
    list_policy_Kap = ['kappa']

    list_policy_Fxc_1 = ['BNF_SAVE_P' + paramloopstr.peristr(period=1),
                         'BNF_BORR_P' + paramloopstr.peristr(period=1),
                         'BNI_LEND_P' + paramloopstr.peristr(period=1),
                         'BNI_BORR_P' + paramloopstr.peristr(period=1)]
    list_policy_Kap_1 = ['kappa' + paramloopstr.peristr(period=1)]
    list_policy_Fxc_2 = ['BNF_SAVE_P' + paramloopstr.peristr(period=2),
                         'BNF_BORR_P' + paramloopstr.peristr(period=2),
                         'BNI_LEND_P' + paramloopstr.peristr(period=2),
                         'BNI_BORR_P' + paramloopstr.peristr(period=2)]
    list_policy_Kap_2 = ['kappa' + paramloopstr.peristr(period=2)]
    list_policy_Fxc_3 = ['BNF_SAVE_P' + paramloopstr.peristr(period=3),
                         'BNF_BORR_P' + paramloopstr.peristr(period=3),
                         'BNI_LEND_P' + paramloopstr.peristr(period=3),
                         'BNI_BORR_P' + paramloopstr.peristr(period=3)]
    list_policy_Kap_3 = ['kappa' + paramloopstr.peristr(period=3)]
    list_policy_Fxc_4 = ['BNF_SAVE_P' + paramloopstr.peristr(period=4),
                         'BNF_BORR_P' + paramloopstr.peristr(period=4),
                         'BNI_LEND_P' + paramloopstr.peristr(period=4),
                         'BNI_BORR_P' + paramloopstr.peristr(period=4)]
    list_policy_Kap_4 = ['kappa' + paramloopstr.peristr(period=4)]

    '''
    Preference Parameters
    '''
    list_preference = ['rho', 'beta', 'logit_sd_scale']
    list_preference_rho = ['rho']

    '''
    Technology Parameters
    '''
    list_technology = ['alpha_k', 'A', 'std_eps', 'data__A_params_mu']
    list_technology = ['alpha_k', 'A', 'std_eps']
    list_technology = ['alpha_k', 'std_eps']
    list_technology = ['alpha_k', 'std_eps', 'K_DEPRECIATION']

    '''
    Distribution Parameters
    '''
    list_Adist_mu_sd = ['data__A_params_mu', 'data__A_params_sd']
    list_Adist_mu_1 = ['data__A_params_mu' + paramloopstr.peristr(period=1)]
    list_Adist_mu_2 = ['data__A_params_mu' + paramloopstr.peristr(period=2)]
    list_Adist_mu_3 = ['data__A_params_mu' + paramloopstr.peristr(period=3)]
    list_Adist_mu_4 = ['data__A_params_mu' + paramloopstr.peristr(period=4)]
    list_Adist_sd_1 = ['data__A_params_sd' + paramloopstr.peristr(period=1)]
    list_Adist_sd_2 = ['data__A_params_sd' + paramloopstr.peristr(period=2)]
    list_Adist_sd_3 = ['data__A_params_sd' + paramloopstr.peristr(period=3)]
    list_Adist_sd_4 = ['data__A_params_sd' + paramloopstr.peristr(period=4)]

    '''
    Cores estimation parameters jointly
    '''
    list_all_params = list_policy_Fxc + list_policy_Kap + list_preference + list_technology

    '''
    Just kappa, for testing
    '''
    list_Adist_1and2 = list_Adist_mu_1 + list_Adist_sd_1 + list_Adist_mu_2 + list_Adist_sd_2
    list_Adist_3and4 = list_Adist_mu_3 + list_Adist_sd_3 + list_Adist_mu_4 + list_Adist_sd_4
    list_Adist = list_Adist_1and2 + list_Adist_3and4

    '''
    Just Time Specific Coefficients
    '''
    list_tvars_1a2 = list_policy_Fxc_1 + list_policy_Fxc_2 + \
                     list_policy_Kap_1 + list_policy_Kap_2
    list_tvars_3a4 = list_policy_Fxc_3 + list_policy_Fxc_4 + \
                     list_policy_Kap_3 + list_policy_Kap_4
    list_tvars = list_tvars_1a2 + list_tvars_3a4

    '''
    Just Time Specific Coefficients and one preference parameter as well, 
    so that estimation test can cover time specific and non-time specific parameters both.
    '''
    list_tvarsb_1a2 = list_tvars_1a2 + list_preference_rho
    list_tvarsb_3a4 = list_tvars_3a4 + list_preference_rho
    list_tvarsb = list_tvars + list_preference_rho

    '''
    All parameters, with time specific coefficients
    '''
    list_tall_1a2 = list_tvars_1a2 + list_Adist_1and2 + list_preference + list_technology
    list_tall_3a4 = list_tvars_3a4 + list_Adist_3and4 + list_preference + list_technology
    list_tall = list_tvars_1a2 + list_tvars_3a4 + list_Adist_1and2 + list_Adist_3and4 + list_preference + list_technology

    '''
    '''
    list_Afx3_1a2 = param2str_groups_esti_Fxc(gen_type=1, periods_key_list=[1, 2]) + \
                    ['data__A_params_sd'] + list_Adist_mu_1 + list_Adist_mu_2 + \
                    list_preference + list_technology
    list_Afx3_3a4 = param2str_groups_esti_Fxc(gen_type=1, periods_key_list=[3, 4]) + \
                    ['data__A_params_sd'] + list_Adist_mu_3 + list_Adist_mu_4 + \
                    list_preference + list_technology

    '''
    Distributional Parameters
    '''
    list_tKap_1and2 = list_policy_Kap_1 + list_policy_Kap_2
    list_tKap_3and4 = list_policy_Kap_3 + list_policy_Kap_4
    list_tKap = list_tKap_1and2 + list_tKap_3and4

    '''Combine Lists'''
    region_time_suffix = hardstring.region_time_suffix()

    #     region_time_suffix['_ce1a2']
    #     region_time_suffix['_ne1a2']
    '''
    Afx3 = all fixed cost 3 time specific
    '''
    param_list_all = {'list_policy_Fxc': list_policy_Fxc,
                      'list_policy_Rsb': list_policy_Rsb,
                      'list_preference': list_preference,
                      'list_technology': list_technology,
                      'list_all_params': list_all_params,

                      'list_tall' + region_time_suffix['_all_ne1a1ce1a1'][0]: list_tall,
                      'list_tall' + region_time_suffix['_ce1a2'][0]: list_tall_1a2,
                      'list_tall' + region_time_suffix['_ne1a2'][0]: list_tall_3a4,

                      'list_Afx3' + region_time_suffix['_ce1a2'][0]: list_Afx3_1a2,
                      'list_Afx3' + region_time_suffix['_ne1a2'][0]: list_Afx3_3a4,

                      'list_tvars' + region_time_suffix['_all_ne1a1ce1a1'][0]: list_tvars,
                      'list_tvars' + region_time_suffix['_ce1a2'][0]: list_tvars_1a2,
                      'list_tvars' + region_time_suffix['_ne1a2'][0]: list_tvars_3a4,

                      'list_tKap' + region_time_suffix['_all_ne1a1ce1a1'][0]: list_tKap,
                      'list_tKap' + region_time_suffix['_ce1a2'][0]: list_tKap_1and2,
                      'list_tKap' + region_time_suffix['_ne1a2'][0]: list_tKap_3and4,

                      'list_Adist' + region_time_suffix['_all_ne1a1ce1a1'][0]: list_Adist,
                      'list_Adist' + region_time_suffix['_ce1a2'][0]: list_Adist_1and2,
                      'list_Adist' + region_time_suffix['_ne1a2'][0]: list_Adist_3and4,

                      'list_policy_Kap': list_policy_Kap,

                      'list_tvarsb' + region_time_suffix['_all_ne1a1ce1a1'][0]: list_tvarsb,
                      'list_tvarsb' + region_time_suffix['_ce1a2'][0]: list_tvarsb_1a2,
                      'list_tvarsb' + region_time_suffix['_ne1a2'][0]: list_tvarsb_3a4}

    return param_list_all


if __name__ == '__main__':
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    for gen_type in [0, 1]:
        for periods_key_list in [[1, 2], [3, 4]]:
            support_json.jdump(param2str_groups_esti_Fxc(gen_type, periods_key_list),
                               'param2str_groups_esti_Fxc()',
                               logger=logger.info)
