'''
@author: fan
'''


def get_all_param_default():
    """List most basic parametesr to invoke
    
    To invoke the program, what are the parameters needed, with these parameter set
    can invoke the main program and get results. 
    
    param_inst.esti_param: dictionary
        potential estimation parameter, and other parameters that directly enter 
        into model equations, even if never estimated, like interest rates.
        
    param_inst.data_param: dictionary
        data that enter as parameters, simulated possibly. Specificlaly for A now
        we want to solve for each A seprately, to save space, do not add that to
        main stateshockchoice mat, but keep as a parameter, then combine different
        A results together

    param_inst.grid_param: dictionary
        everything grid related, dimensions, min and max etc, sd etc, 
        some of the parameters here and the parameters for data and esti param
        might be difficult to classify        
    
    param_inst.model_option: dictionary
        model_options are key parameters that determine the type of model invoked
        like which type of future value is used, and everything else that 
        determine which functions to invoke in some sense. 
          
    param_inst.interpolant  
    interpolant['interp_solu']: dictionary
        solu_param are value function polynomial approximation coefficient type 
        things.
    
    param_inst.support_arg: dictionary
        everything else    
    """

    grid_param = {

        'len_k_start': 5,
        'len_states': 25,
        'len_shocks': 1,  # shock soluvalue
        'len_choices': 25,
        'len_choices_k': 5,
        'len_choices_b': 5,
        'shape_choice': {'type': 'broadcast_kron', 'shape': 25, 'row': None, 'col': None},

        'len_k_start': 9,
        'len_states': 81,
        'len_choices': 100,
        'len_shocks': 3,
        'len_eps': 3,
        'len_eps_E': 30,
        'shape_choice': {'type': 'broadcast', 'shape': [81, 100], 'row': 81, 'col': 100},

        'max_kapital': 20,
        'min_kapital': 0,
        'mean_kapital': 25,
        'std_kapital': 2,

        'max_netborrsave': 40,
        'min_netborrsave': -25,  # SEE LINE 173 #####################
        'mean_netborrsave': -25,
        'std_netborrsave': 2,

        'max_steady_coh': 25,
        'min_steady_coh': 0,

        'max_eps': +4,
        'min_eps': -4,
        'mean_eps': 0,
        'std_eps': 0.5,
        'len_eps': 1,
        'drawtype_eps': 1,  # 1 when solving, 2 when simulating
        'seed_eps': 1561,  # 1 when solving, 2 when simulating

        'max_eps_E': +4,
        'min_eps_E': -4,
        'mean_eps_E': 0,
        #         'std_eps_E':1,
        'len_eps_E': 1,

        # minimal savings, multinomial if chosen given shock needs non-zero value
        'BNF_SAVE_P_startVal': 0.5,
        'BNF_BORR_P_startVal': -1,
        'BNI_LEND_P_startVal': 3.0,
        'BNI_BORR_P_startVal': -2,

        # see solumain, this is how many times to zoom in. 
        'grid_zoom_rounds': 1,

        # see solusteady
        'markov_points': 200

    }

    grid_param['std_eps_E'] = grid_param['std_eps']

    data_param = {
        # LifeTimeUtility
        'A': 0.75,
        'mean_A': 0.75,
        'std_A': 0,
        'len_A': 1,

        'Region': 0,
        'Region_set': [0, 1],

        'Year': 0,
        'Year_set': [0, 1]
    }

    esti_param = {
        # BudgetConsumption
        'R_INFORM_SAVE': 1.10,
        'R_INFORM_BORR': 1.10,
        'R_FORMAL_SAVE': 1.02,
        'R_FORMAL_BORR': 1.06,
        'BNF_SAVE_P': 0,
        'BNF_BORR_P': 0,
        'BNI_LEND_P': 0,
        'BNI_BORR_P': 0,

        'R_AVG_INT': 1.05,  # used in future_loginf 
        'K_DEPRECIATION': 0.05,

        # PeriodUtility
        'rho': 0.15,

        # MultinomialLogitU
        'logit_sd_scale': 1,

        # ProductionFunction
        'alpha_k': 0.30,

        # TodayUtility
        'c_min_bound': 0.001,

        # LifeTimeUtility
        'beta': 0.90,

        # Borrowing Constraint
        'kappa': 0.25,
    }
    esti_param['R_INFORM'] = esti_param['R_INFORM_SAVE']
    grid_param['min_netborrsave'] = grid_param['max_kapital'] * (1 - esti_param['K_DEPRECIATION'])

    model_option = {
        'VFI_type': 'infinite',
        'choice_set_list': [0, 1],
        'simu_iter_periods': 20,
        'simu_indi_count': 100,
    }

    interpolant = {
        'interp_type': ['polyquad', 'V_ONE', 'EV_TWO'],
        'V_coef': None,
        'EV_coef': None,
        'maxinter': 1
    }

    support_arg = {
        'save_directory': 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/',
    }

    dist_param = {}

    return grid_param, data_param, esti_param, model_option, interpolant, dist_param, support_arg
