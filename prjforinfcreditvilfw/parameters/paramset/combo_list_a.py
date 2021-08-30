'''

@author: fan

Started apr3rd2018
'''

import numpy as np
import parameters.loop_param_combo_list.loops_gen as paramloops


def get_combo_list(combo_type=['a', '20180517_A', 'data_param.A'],
                   compesti_specs=None):
    """Testing Codes without fixed cost, just borrow and save
    
    Test Effects of Key parameters
    1. TFP
    2. R
    3. CRRA
    
    Test System Parameters
    1. VFI rounds
    2. Zoom in iteration rounds
    3. EV approximation method 
    4. Denser grid, geom vs linear grid     
    
    """

    module = combo_type[0]
    sub_type = combo_type[1]

    if (sub_type == '20180403a'):
        grid_type = ['a', 42]
        esti_type = ['a', 1]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 2]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': '(INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180404a'):
        'Loop over interest rates'

        int_rate_counts = 6
        min_int = 0.5
        max_int = 2.0

        grid_type = ['a', 42]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 2]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 1,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 ,
              'title': '(inf borr) + (inf save) + (0 bmin, 0 FC) + (log U) + (r=' + str(int(cur_rate * 100)) + ')'
                 ,
              'combo_desc': 'inf borr save zero fixed costs zero min borr save log ' + str(int(cur_rate * 100))
                 , 'file_save_suffix': '_r' + str(int(cur_rate * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180404b'):
        'Loop over interest rates'

        int_rate_counts = 6
        min_int = 1.0
        max_int = 1.5

        grid_type = ['a', 42]
        data_type = ['a']
        model_type = ['a', 2]
        interpolant_type = ['a', 2]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 2,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': '(for inf borr) + (for inf save) + (0 bmin, wth FC) + (log U) + (r=' + str(
                    int(cur_rate * 100)) + ')'
                 ,
              'combo_desc': 'four possible choices, no joint formal informal, has basic fixed costs structure, log U, ' + str(
                  int(cur_rate * 100))
                 , 'file_save_suffix': '_r' + str(int(cur_rate * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180417a'):
        """
        Grid Data, linear interpolation:
            also fix choice set to be bounded by soluvalue grid so that we are 
            interpolating, not extrapolating. 
            
        """

        grid_type = ['a', 42]
        esti_type = ['a', 1]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 11]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'G900, GridData, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'G900, GridData, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180418a'):
        """
        Increase choice grid:
            20180417a
            realized from:
                opticts_xcash_yktp_opti_ck_Ga42Ea1Ma1Ia2Da_20180418-190101-606225
            maybe people are choosing both assets as complements, but I did not
            have fine enough grid, and old grid structure was too weird.
            
            - linear spline, weird, does not increase                          
        """

        grid_type = ['a', 52]
        esti_type = ['a', 1]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 11]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'C9000, GridData, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'C9000, GridData, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180418b'):
        """
        20180418a except polynomial approximate
        """

        grid_type = ['a', 52]
        esti_type = ['a', 1]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 2]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'C9000, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'C9000, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180419a'):
        """
        20180419a except polynomial approximate, log utility, was not log before actually
        """

        grid_type = ['a', 42]
        esti_type = ['a', 3]
        data_type = ['a']
        model_type = ['a', 1]
        interpolant_type = ['a', 11]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'G900, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180501a'):
        """
        20180419a but now with denser choice grid:
            before we improve codes so that I have double grid search procedure. check does having 
            denser choice grid really improve anything?
            
            grid_type = ['a',42] to grid_type = ['a',62] 
        """

        grid_type = ['a', 62]  # len_choices: 9000
        esti_type = ['a', 3]  # log utility
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11]  # griddata, maxiter = 1

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'G900, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180506a'):
        """
        20180419a but now with denser choice grid:
            before we improve codes so that I have double grid search procedure. check does having 
            denser choice grid really improve anything?
            
            grid_type = ['a',20180506] meaning 900 choice points in total, 30 by 30 
        """

        grid_type = ['a', 20180506]  # len_choices: 9000
        esti_type = ['a', 3]  # log utility
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11]  # griddata, maxiter = 1

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'G900, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.15)'
                 , 'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': ''}]

    if (sub_type == '20180507'):
        """
        20180506a but now with more interest rates.  
        """

        grid_type = ['a', 20180506]  # len_choices: 9000
        esti_type = ['a', 3]  # log utility
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11]  # griddata, maxiter = 1

        int_rate_counts = 20
        min_int = 1.0
        max_int = 1.4

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 3,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': 'G900, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=' + str(
                    int(cur_rate * 100)) + ')'
                 , 'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_r' + str(int(cur_rate * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180508'):
        """
        20180506a solve at a greater number of VFI periods  
        """

        grid_type = ['a', 20180506]  # len_choices: 9000
        esti_type = ['a', 3, {'R_INFORM_SAVE': 1.05,
                              'R_INFORM_BORR': 1.05}]  # log utility
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        #         interpolant_type = ['a',11] # griddata, maxiter = 1

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': esti_type,
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': ['a', 11, {'maxinter': maxinter}]
                                    }
                 ,
              'title': 'G900, Poly, (INF BORR) + (INF SAVE) + (0 BMIN, 0 FC) + (LOG U) + (R=1.1) + uter=' + str(
                  maxinter) + ')'
                 ,
              'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(maxinter)
                 , 'file_save_suffix': '_iter' + str(maxinter)}
             for maxinter in [15]]

    #             ,3,4,5,10,20,40,80

    if (sub_type == '20180510'):
        """
        20180506a solve at a greater number of VFI periods  
        """
        int_rate_counts = 40
        min_int = 1.0
        max_int = 1.4

        grid_type = ['a', 20180506]  # len_choices: 9000
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11, {'maxinter': 15}]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 3,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG)+i15+(R=' + str(int(cur_rate * 100)) + ')'
                 , 'combo_desc': 'G900, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_i15r' + str(int(cur_rate * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180511'):
        """
        20180506a solve at a greater number of VFI periods  
        """
        int_rate_counts = 10
        min_int = 1.00
        max_int = 1.20

        grid_type = ['a', 20180511]  # len_choices: 9000
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11, {'maxinter': 15}]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 20180511,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': data_type,
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 , 'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,b=0.96)+i15+(R=' + str(int(cur_rate * 100)) + ')'
                 , 'combo_desc': 'b=0.96, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_i15r' + str(int(cur_rate * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180511b'):
        """
        20180506a solve at a greater number of VFI periods  
        """
        int_rate_counts = 3
        min_int = 1.00
        max_int = 1.20

        A_counts = 3
        min_A = 0.75
        max_A = 3.75

        grid_type = ['a', 20180511]  # len_choices: 9000
        data_type = ['a']  #
        model_type = ['a', 1]  # choice_set_list: [0,1]
        interpolant_type = ['a', 11, {'maxinter': 1}]

        combo_list = \
            [{'param_update_dict': {'grid_type': grid_type,
                                    'esti_type': ['a', 20180511,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': ['a',
                                                  {'A': A, 'Region': 0, 'Year': 0}],
                                    'model_type': model_type,
                                    'interpolant_type': interpolant_type}
                 ,
              'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,b=0.96)+i15+(R=' + str(int(cur_rate * 100)) + ',A=' + str(
                  A) + ')'
                 , 'combo_desc': 'b=0.96, Poly, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_i15r' + str(int(cur_rate * 100)) + 'A' + str(int(A * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)
             for A in np.linspace(min_A, max_A, A_counts)]

    if (sub_type == '20180512'):
        """
        20180506a solve at a greater number of VFI periods  
        """
        int_rate_counts = 5
        min_int = 0.95
        max_int = 1.05

        A_counts = 3
        min_A = -1
        max_A = 0.25
        A_counts = 1
        min_A = 0.25
        max_A = 0.25

        esp_count = 3
        min_eps = 0.1
        max_eps = 0.75
        esp_count = 1
        min_eps = 0.75
        max_eps = 0.75

        interpolant_type = ['a', 11, {'maxinter': 15}]

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180512, {'std_eps': std, 'std_eps_E': std}],
                                    'esti_type': ['a', 20180512,
                                                  {'R_INFORM_SAVE': cur_rate, 'R_INFORM_BORR': cur_rate}],
                                    'data_type': ['b', 20180512,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': interpolant_type}
                 ,
              'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i15+(R=' + str(
                  int(cur_rate * 100)) + ',A=' + str(
                  A) + ',S=' + str(std) + ')'
                 , 'combo_desc': 'Angeletos, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_i15r' + str(int(cur_rate * 100)) + 'A' + str(int(A * 100)) + 's' + str(
                    int(std * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)
             for A in np.linspace(min_A, max_A, A_counts)
             for std in np.linspace(min_eps, max_eps, esp_count)]

    if (sub_type == '20180512_bench_nofc_J2'):
        """
        20180512_bench_nofc benchmark kind of for no fixed costs  
        """
        int_rate_counts = 1
        min_int = 0.95
        max_int = 1.05

        A = 0.25
        std = 0.75

        interpolant_type = ['a', 11, {'maxinter': 15}]

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180512, {'std_eps': std, 'std_eps_E': std}],
                                    'esti_type': ['a', 20180512,
                                                  {'R_INFORM_SAVE': cur_rate, 'R_INFORM_BORR': cur_rate}],
                                    'data_type': ['b', 20180512,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': interpolant_type}
                 ,
              'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i15+(R=' + str(
                  int(cur_rate * 100)) + ',A=' + str(
                  A) + ',S=' + str(std) + ')'
                 , 'combo_desc': 'Angeletos, INF BORR SAVE ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_i15r' + str(int(cur_rate * 100)) + 'A' + str(int(A * 100)) + 's' + str(
                    int(std * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    if (sub_type == '20180512_bquick_nofc'):
        """
        20180512_bquick_nofc benchmark but quick 3 VFI, small grid, quick testing  
        """

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 201805160],
                                    'esti_type': ['a', 201805160],
                                    'data_type': ['b', 20180513],
                                    'model_type': ['a', 1],
                                    'interpolant_type': ['a', 201805160]}
                 , 'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.1),Small grid)'
                 , 'combo_desc': 'Angeletos quick', 'file_save_suffix': '_quicktest'}]

    if (sub_type == '20180512_mjalltest'):
        """
        20180512_mjalltest, tiny grid, for mjall, single or multi state testing
        after VFI, check results at very small subset  
        """

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 2018051617],
                                    'esti_type': ['a', 201805160],
                                    'data_type': ['b', 20180513],
                                    'model_type': ['a', 1],
                                    'interpolant_type': ['a', 201805160]}
                 , 'title': '(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.1),Small grid)'
                 , 'combo_desc': 'Angeletos quick', 'file_save_suffix': '_quicktest'}]

    if (sub_type == '20180517_quick'):
        """
        Came back to testing after realizing previous error with log(K)
        20180517_quick for quick testing  
        """

        std = 0.75
        A_counts = 3
        min_A = -0.65
        max_A = 0.35

        markov_points = 10
        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 201805160,
                                                  {'std_eps': std, 'std_eps_E': std,
                                                   'markov_points': markov_points}],
                                    'esti_type': ['a', 201805160],
                                    'data_type': ['b', 20180513,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': ['a', 20180513, {'maxinter': 1}]}
                 , 'title': 'A' + str(A) + ':(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.08))'
                 , 'combo_desc': 'Angeletos quick', 'file_save_suffix': '_A' + str(int(A * 1000))}
             for A in np.linspace(min_A, max_A, A_counts)]

    if (sub_type == '20180517_A'):
        """
        Effects of Different As on demand supply etc.  
        """

        std = 0.75
        A_counts = 5
        min_A = -0.65
        max_A = 0.35

        markov_points = 100
        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180513,
                                                  {'std_eps': std, 'std_eps_E': std,
                                                   'markov_points': markov_points}],
                                    'esti_type': ['a', 201805160],
                                    'data_type': ['b', 20180513,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': ['a', 20180513]}
                 , 'title': 'A' + str(A) + ':(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.08))'
                 , 'combo_desc': 'Angeletos quick', 'file_save_suffix': '_A' + str(int(A * 1000))}
             for A in np.linspace(min_A, max_A, A_counts)]

    if (sub_type == '20180529_A'):
        """
        same as 20180517_A except change interpolating method to forgegeom
        """

        std = 0.75
        A_counts = 5
        min_A = -0.65
        max_A = 0.35

        markov_points = 100
        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180513,
                                                  {'std_eps': std, 'std_eps_E': std,
                                                   'markov_points': markov_points}],
                                    'esti_type': ['a', 201805160],
                                    'data_type': ['b', 20180513,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': ['a', 20180529]}
                 , 'title': 'A' + str(A) + ':(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.08))'
                 , 'combo_desc': 'Angeletos quick', 'file_save_suffix': '_A' + str(int(A * 10000))}
             for A in np.linspace(min_A, max_A, A_counts)]

    if ("20180607_" in sub_type):
        """
        share common param_set_file and param_set_type
        """

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f='a', grid_t='20180607',
            esti_f='a', esti_t='20180607',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180607',
            interpolant_f='a', interpolant_t='20180607')

    return combo_list
