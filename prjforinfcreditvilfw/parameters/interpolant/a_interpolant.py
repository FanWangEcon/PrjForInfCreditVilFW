'''
@author: fan
'''

import parameters.model.a_model as param_model_a

'''
Created on Jan 1, 2018

@author: fan
'''


def param(param_type=1):
    module = param_type[0]
    sub_type = str(param_type[1])

    bktp_geom_dict_null = param_model_a.choice_index_names()['bktp_geom_dict']

    if (sub_type == '2'):
        subtitle = 'polyquad2'
        interpolant = {
            'interp_type': ['polyquad', 'V_ONE', 'EV_TWO'],
            'V_coef': None,
            'EV_coef': None,
            'maxinter': 1
        }

    if (sub_type == '11'):
        subtitle = 'griddata'
        interpolant = {
            'interp_type': ['griddata'],
            'interp_type_option': {'method': 'linear'},
            'maxinter': 1,
            'interp_V_k_cash': {'V': None, 'k': None, 'cash': None},
            'interp_EV_k_b': {'EV': None, 'k': None, 'b': None}
        }

    if (sub_type == '20180513'):
        subtitle = 'griddata'
        interpolant = {
            'interp_type': ['griddata'],
            'interp_type_option': {'method': 'linear'},
            'maxinter': 15,
            'interp_V_k_cash': {'V': None, 'k': None, 'cash': None},
            'interp_EV_k_b': {'EV': None, 'k': None, 'b': None}
        }

    if (sub_type == '201805160'):
        subtitle = 'quick'
        interpolant = {
            'interp_type': ['griddata'],
            'interp_type_option': {'method': 'linear'},
            'maxinter': 2,
            'interp_V_k_cash': {'V': None, 'k': None, 'cash': None},
            'interp_EV_k_b': {'EV': None, 'k': None, 'b': None}
        }

    if (sub_type == '20180529'):
        #             'converge_condi':{'maxinter':15},
        subtitle = 'forgegeom'
        interpolant = {
            'interp_type': ['forgegeom'],
            'interp_type_option': {'method': 'linear'},
            'maxinter': 15,
            'econforge_interpolant': None,
            'interp_EV_k_b': {'B_Vepszr_square_max': None,
                              'B_Vepszr_square_min': None,
                              'K_Vepszr_square_max': None,
                              'K_Vepszr_square_min': None,
                              'start': 0,
                              'stop': 1,
                              'geom_ratio': 1.03},
            'bktp_geom': bktp_geom_dict_null,  # have to specify all possible
            'pre_save': True
        }
    #             'bktp_geom' only relevant for forgegeom_reuse

    '''
    Accomandates:
        20180607x, 20180607d, 20180607
        20201025x, 20201025d, 20201025
    '''
    main_type_str_list = ['20180607', '20201025']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        geom_ratio = 1.03
        subtitle = 'forgegeom'

        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            maxinter = 1000
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            maxinter = 1000
        else:
            maxinter = 1000

        interpolant = {
            'interp_type': ['forgegeom'],
            'interp_type_option': {'method': 'linear'},
            'maxinter': maxinter,
            'econforge_interpolant': None,
            'interp_EV_k_b': {'B_Vepszr_square_max': None,
                              'B_Vepszr_square_min': None,
                              'K_Vepszr_square_max': None,
                              'K_Vepszr_square_min': None,
                              'start': 0,
                              'stop': 1,
                              'geom_ratio': geom_ratio},
            'bktp_geom': bktp_geom_dict_null,  # have to specify all possible
            'pre_save': True
        }

    return interpolant, subtitle
