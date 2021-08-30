'''
@author: fan
'''


# from datashape.predicates import isscalar


def param(param_type=['a', 1]):
    """
    a_grid files are only for testing purposes

    Parameters
    ----------
    param_type: list
        = ['a', 1]
        could be longer, more and more
        param_type[0]: 'a' always7
        param_type = ['a', 1] : 1 state 1 choice
        param_type = ['a', 2] : 1 state 50 choice
        param_type = ['a', 3] : 20 state 50 choice
        param_type = ['a', 30]: 1 state 450 choice
        param_type = ['a', 31]: 3 state 1000 choice, broadcast_kron
        param_type = ['a', 32]: 3 state 1000 choice, broadcast
        param_type = ['a', 33]: 3 state 1000 choice, 1to1
        param_type = ['a', 41]: 1000 state 1000 choice, broadcast_kron
        param_type = ['a', 42]: 1000 state 1000 choice, broadcast
        param_type = ['a', 43]: 1000 state 1000 choice, 1to1
    """

    module = param_type[0]
    sub_type = str(param_type[1])

    # Update specific Parameters as a dictionary

    grid_param, subtitle = param_sub_type(sub_type)

    if (len(param_type) == 3):
        more_update = param_type[2]
        grid_param.update(more_update)

    return grid_param, subtitle


def param_sub_type(sub_type):
    """
    """
    """
    Keys of Grid Param
    -------------------
    grid_zoom_rounds : int 
        0 to N, zooming in after VFI. If 'CEV_PROP_INCREASE' is not None, this is overridedn to be 0. 
        This leads to policy function that is inconsistent with value function results.    
    """
    subtitle = 'basic'
    grid_param = {

        'len_k_start': 1,

        'len_states': 1,
        'len_choices': 1,

        'len_shocks': 3,
        'len_eps': 3,
        'len_eps_E': 50,

        'shape_choice': {'type': '1to1', 'shape': 1, 'row': None, 'col': None},

        'max_kapital': 20,
        'min_kapital': 0,
        'mean_kapital': 25,
        'std_kapital': 2,

        'max_netborrsave': 40,
        'min_netborrsave': -25,
        'mean_netborrsave': -25,
        'std_netborrsave': 2,

        # minimal savings, multinomial if chosen given shock needs non-zero value
        'BNF_SAVE_P_startVal': 0,
        'BNF_BORR_P_startVal': -0,
        'BNI_LEND_P_startVal': 0,
        'BNI_BORR_P_startVal': -0,
    }

    if (sub_type == '1'):
        pass

    if (sub_type == '2'):
        """
        Invoking with 1 state only
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_choices': 50,
            'shape_choice': {'type': '1to1', 'shape': 50, 'row': None, 'col': None},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '3'):
        """
        20 states, will produce 4 by 5 k and b:
            see C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_states
        50 choices, will produce 10 by 5 choice grid:
            C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_policytics
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 2,
            'len_states': 4,
            'len_choices': 9,
            'len_shocks': 2,
            'len_eps': 2,
            'len_eps_E': 3,
            'shape_choice': {'type': 'broadcast', 'shape': [4, 9], 'row': 4, 'col': 9},
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '4'):
        """
        20 states, will produce 4 by 5 k and b:
            see C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_states
        50 choices, will produce 10 by 5 choice grid:
            C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_policytics
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 4,
            'len_states': 20,
            'len_choices': 50,
            'shape_choice': {'type': 'broadcast', 'shape': [20, 50], 'row': 20, 'col': 50},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '5'):
        """
        Invoking with 1000 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 1,
            'len_states': 1,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast', 'shape': [1, 1000], 'row': 1, 'col': 1},
        }

    if (sub_type == '30'):
        """
        Invoking with 1 state only
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_choices': 450,
            'shape_choice': {'type': 'broadcast_kron', 'shape': 450, 'row': None, 'col': None},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '31'):
        """
        Invoking with 3 states
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_states': 3,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast_kron', 'shape': 1000, 'row': None, 'col': None},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '32'):
        """
        Invoking with 3 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_states': 3,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast', 'shape': [3, 1000], 'row': 3, 'col': 1000},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '33'):
        """
        Invoking with 3 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_states': 3,
            'len_choices': 1000,
            'shape_choice': {'type': '1to1', 'shape': 3 * 1000, 'row': 3 * 1000, 'col': 1},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '41'):
        """
        Invoking with 1000 states
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 30,
            'len_states': 900,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast_kron', 'shape': 900, 'row': None, 'col': None},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '42' or sub_type == '142'):
        """
        Invoking with 1000 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 30,
            'len_states': 900,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast', 'shape': [900, 1000], 'row': 900, 'col': 1000},
        }
        if (sub_type == '142'):
            grid_param_update['len_eps'] = 1
        grid_param.update(grid_param_update)

    if (sub_type == '43'):
        """
        Invoking with 1000 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 30,
            'len_states': 900,
            'len_choices': 1000,
            'shape_choice': {'type': '1to1', 'shape': 900 * 1000, 'row': 900 * 1000, 'col': 1},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '52' or sub_type == '142'):
        """
        Invoking with 1000 states, different choices potentially per state
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 90,
            'len_states': 8100,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast', 'shape': [8100, 1000], 'row': 8100, 'col': 1000},
        }
        if (sub_type == '152'):
            grid_param_update['len_eps'] = 1
        grid_param.update(grid_param_update)

    if (sub_type == '62' or sub_type == '142'):
        """
        Invoking with 1000 states, 9000 choices
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 30,
            'len_states': 900,
            'len_choices': 9000,
            'shape_choice': {'type': 'broadcast', 'shape': [900, 9000], 'row': 900, 'col': 9000},
        }
        if (sub_type == '142'):
            grid_param_update['len_eps'] = 1
        grid_param.update(grid_param_update)

    if (sub_type == '20180506'):
        """
        Invoking with 1000 states, 900 choices, should have simple square root to get
        even K and B choices, same count along each of those two choice dimensions.
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180511'):
        """
        Invoking with 1000 states, 900 choices, should have simple square root to get
        even K and B choices, same count along each of those two choice dimensions.
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 1,
            'std_eps_E': 1,
            'max_kapital': 10,
            'max_netborrsave': 50,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180512'):
        """
        Angeletos
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.5,
            'std_eps_E': 0.5,
            'max_kapital': 50,
            'max_netborrsave': 50,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180513'):
        """
        Angeletos
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 50,
            'max_netborrsave': 50,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '201805160'):
        """
        Angeletos
        """
        subtitle = 'quick'
        grid_param_update = {
            'len_k_start': 15,
            'len_states': 225,
            'len_choices': 100,
            'shape_choice': {'type': 'broadcast', 'shape': [400, 100], 'row': 400, 'col': 100},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 20,
            'max_netborrsave': 50,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '2018051617'):
        """
        Angeletos
        """
        subtitle = 'quick3states'
        grid_param_update = {
            'len_k_start': 3,
            'len_states': 3,
            'len_choices': 1000,
            'shape_choice': {'type': 'broadcast', 'shape': [3, 1000], 'row': 3, 'col': 1000},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 20,
            'max_netborrsave': 50,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180607'):
        """
        Angeletos
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 50,
            'max_netborrsave': 50,
            'grid_zoom_rounds': 1,
            'markov_points': 200,
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180629d'):
        """
        Angeletos
        (23.6-5.2) = 10gb vfi and
        (31ish-5.2) = 26gb solu memory
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 120,
            'len_states': 14400,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [14400, 900], 'row': 14400, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 50,
            'max_netborrsave': 50,
            'grid_zoom_rounds': 3,
            'markov_points': 200,
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180629x'):
        """
        Angeletos: small run for testing purposes
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 20,
            'len_states': 400,
            'len_choices': 100,
            'shape_choice': {'type': 'broadcast', 'shape': [400, 100], 'row': 400, 'col': 100},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 50,
            'max_netborrsave': 50,
            'grid_zoom_rounds': 3,
            'markov_points': 50,
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    if (sub_type == '20180629'):
        """
        Angeletos
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': 50,
            'len_states': 2500,
            'len_choices': 900,
            'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
            'min_steady_coh': 0,
            'max_steady_coh': 50,
            'std_eps': 0.75,
            'std_eps_E': 0.75,
            'max_kapital': 50,
            'max_netborrsave': 50,
            'grid_zoom_rounds': 1,
            'markov_points': 200,
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    main_type_str_list = ['20181024', '20201025']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            len_k_start = 20
            len_states = 400
            len_choices = 100
            shape_choice = {'type': 'broadcast', 'shape': [400, 100], 'row': 400, 'col': 100}
            markov_points = 50
            len_eps_E = 50
            grid_zoom_rounds = 0
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            len_k_start = 120
            len_states = 14400
            len_choices = 900
            shape_choice = {'type': 'broadcast', 'shape': [14400, 900], 'row': 14400, 'col': 900}
            markov_points = 200
            len_eps_E = 75
            grid_zoom_rounds = 3
        else:
            len_k_start = 50
            len_states = 2500
            len_choices = 900
            shape_choice = {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900}
            markov_points = 200
            len_eps_E = 50
            grid_zoom_rounds = 1

        std = 0.5
        std_eps = std
        mean_eps = (-1) * ((std ** 2) / 2)
        std_eps_E = std
        mean_eps_E = mean_eps

        """
        Angeletos
        """
        subtitle = 'basic'
        grid_param_update = {
            'len_k_start': len_k_start,
            'len_states': len_states,
            'len_choices': len_choices,
            'shape_choice': shape_choice,
            'min_steady_coh': 0,
            'max_steady_coh': 50,

            'std_eps': std_eps,
            'mean_eps': mean_eps,
            'std_eps_E': std_eps_E,
            'mean_eps_E': mean_eps_E,

            'len_eps_E': len_eps_E,

            'max_kapital': 50,
            'max_netborrsave': 50,
            'grid_zoom_rounds': grid_zoom_rounds,
            'markov_points': markov_points,
            'BNF_SAVE_P_startVal': 0,
            'BNF_BORR_P_startVal': -0,
            'BNI_LEND_P_startVal': 0,
            'BNI_BORR_P_startVal': -0,
        }
        grid_param.update(grid_param_update)

    return grid_param, subtitle
