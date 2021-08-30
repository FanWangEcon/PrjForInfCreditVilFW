'''
@author: fan

Invokations with fixed costs
'''

import numpy as np

import parameters.loop_param_combo_list.loops_gen as paramloops
import parameters.loop_param_combo_list.loops_gen_json as paramloopsjson


def get_combo_list(combo_type=['b', '20180513a'], compesti_specs=None):
    module = combo_type[0]
    sub_type = combo_type[1]

    if (sub_type == '20180512'):
        """
        Somewhat wideish distribution, still just borrow save, now include
        informal lending fixed cost.
        """
        int_rate_counts = 5
        min_int = 1.00
        max_int = 1.25

        BNI_LEND_P_count = 10
        min_BNI_LEND_P = 0
        max_BNI_LEND_P = 8

        A = 0.25
        std = 0.75
        maxinter = 15

        interpolant_type = ['a', 11, {'maxinter': maxinter}]

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180512, {'std_eps': std, 'std_eps_E': std}],
                                    'esti_type': ['a', 20180512, {'BNI_LEND_P': BNI_LEND_P,
                                                                  'R_INFORM_SAVE': cur_rate,
                                                                  'R_INFORM_BORR': cur_rate}],
                                    'data_type': ['b', 20180512,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0, 'Year': 0}],
                                    'model_type': ['a', 1],
                                    'interpolant_type': interpolant_type}
                 ,
              'title': '(INF BORR+SAVE)+(0MIN)+(LOG,Angeletos)+i15+(R=' + str(int(cur_rate * 100)) + ',A=' + str(
                  A) + ',S=' + str(std) + ')'
                 , 'combo_desc': 'Angeletos, INF BORR ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(cur_rate * 100))
                 , 'file_save_suffix': '_r' + str(int(cur_rate * 100)) + 'ilf' + str(int(BNI_LEND_P * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)
             for BNI_LEND_P in np.linspace(min_BNI_LEND_P, max_BNI_LEND_P, num=BNI_LEND_P_count)]

    if (sub_type == '20180513a'):
        """
        Allow for borrow informal, and save formal and save informal
        """
        inf_rate = 1.10
        R_FORMAL_SAVE = 1.02
        BNI_LEND_P_count = 1
        min_BNI_LEND_P = 2
        max_BNI_LEND_P = 2

        BNF_SAVE_P = 0.5

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180513],
                                    'esti_type': ['a', 20180512,
                                                  {'BNI_LEND_P': BNI_LEND_P,
                                                   'BNF_SAVE_P': BNF_SAVE_P,
                                                   'R_INFORM_SAVE': inf_rate,
                                                   'R_INFORM_BORR': inf_rate,
                                                   'R_FORMAL_SAVE': R_FORMAL_SAVE}],
                                    'data_type': ['b', 20180513],
                                    'model_type': ['a', 20180513],
                                    'interpolant_type': ['a', 20180513]}
                 , 'title': '(IB+IS+FS)+(0MIN)+(LOG,Angeletos)+(R=' + str(int(inf_rate * 100)) +
                            ',ilf=' + str(int(BNI_LEND_P * 100)) + ',fsf=' + str(int(BNF_SAVE_P * 100)) + ')'
                 , 'combo_desc': 'Angeletos, INF BORR ZERO FIXED COSTS ZERO MIN BORR SAVE LOG' + str(
                    int(inf_rate * 100))
                 , 'file_save_suffix': '_r' + str(int(inf_rate * 100)) + 'ilf' + str(
                    int(BNI_LEND_P * 100)) + 'fsf' + str(int(BNF_SAVE_P * 100))}
             for BNI_LEND_P in np.linspace(min_BNI_LEND_P, max_BNI_LEND_P, num=BNI_LEND_P_count)]

    if (sub_type == '20180521_LENDFC'):
        """
        combo_type=['b', '20180521_LENDFC', 'esti_param.BNI_LEND_P']
        Allow for borrow informal, and save formal and save informal
        """

        inf_rate = 1.10
        R_FORMAL_SAVE = 1.02
        BNI_LEND_P_count = 5
        min_BNI_LEND_P = 0
        max_BNI_LEND_P = 5

        BNF_SAVE_P = 0.5

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180513],
                                    'esti_type': ['a', 201805160,
                                                  {'BNI_LEND_P': BNI_LEND_P,
                                                   'BNF_SAVE_P': BNF_SAVE_P,
                                                   'R_INFORM_SAVE': inf_rate,
                                                   'R_INFORM_BORR': inf_rate,
                                                   'R_FORMAL_SAVE': R_FORMAL_SAVE}],
                                    'data_type': ['b', 20180513],
                                    'model_type': ['a', 20180513],
                                    'interpolant_type': ['a', 20180513]}
                 , 'title': '(IB+IS+FS)+(0MIN)+(LOG,Angeletos)' + \
                            ',ilf=' + str(int(BNI_LEND_P * 100)) + \
                            ',fsf=' + str(int(BNF_SAVE_P * 100)) + ')'
                 , 'combo_desc': 'Angeletos, INF BORR ZERO FIXED COSTS ZERO MIN BORR SAVE LOG'
                 , 'file_save_suffix': '_ilf' + str(int(BNI_LEND_P * 100)) + 'fsf' + str(int(BNF_SAVE_P * 100))}
             for BNI_LEND_P in np.linspace(min_BNI_LEND_P, max_BNI_LEND_P, num=BNI_LEND_P_count)]

    if (sub_type == '20180613_basicJ5'):
        """
        Include 5 choice categories, allows me to do basic testing for mjall.py
        """

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20180607],
                                    'esti_type': ['a', 20180613],
                                    'data_type': ['a', 20180607],
                                    'model_type': ['a', 20180613],
                                    'interpolant_type': ['a', 20180607]}
                 , 'title': '(IB+FB,IS+FS,6)+(FC)+(LOG,Angeletos)'
                 , 'combo_desc': 'Angeletos, 5 cate, FIXED COSTS LOG'
                 , 'file_save_suffix': '_basic'}]

    if ("20180623_" in sub_type):
        """
        5 Choices
        """
        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f='a', grid_t='20180607',
            esti_f='a', esti_t='20180628',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180613',
            interpolant_f='a', interpolant_t='20180607')

    if (sub_type == '20180701_basicJ7'):
        """
        7 Choices testing testsolu
        """

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', '20180607'],
                                    'esti_type': ['a', '20180701'],
                                    'data_type': ['a', '20180607'],
                                    'model_type': ['a', '20180701'],
                                    'interpolant_type': ['a', '20180607']}
                 , 'title': '(IB+FB,IS+FS,6,joint)+(FC)+(LOG,Angeletos)'
                 , 'combo_desc': 'Angeletos, 7 cate, FIXED COSTS LOG'
                 , 'file_save_suffix': '_basic'}]

    if (sub_type == '20200804_basicJ7'):
        """
        7 Choices testing testsolu
        """

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', '20200804'],
                                    'esti_type': ['a', '20180701'],
                                    'data_type': ['a', '20180607'],
                                    'model_type': ['a', '20180701'],
                                    'interpolant_type': ['a', '20180607']}
                 , 'title': '(IB+FB,IS+FS,6,joint)+(FC)+(LOG,Angeletos)'
                 , 'combo_desc': 'Angeletos, 7 cate, FIXED COSTS LOG'
                 , 'file_save_suffix': '_basic'}]

    """
    DEBUG GROUPS
    """

    if ("debug_" in sub_type):

        # TEST 1
        if ("20180717debug_fcib" in sub_type):
            """
            fcib_BNI_BORR_P_0_r12000_A0_equitg
            """
            A = -1.5653705443525463
            R_inf = 1.20

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180628',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'BNI_BORR_P': 0}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'combo_desc': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'file_save_suffix': '_debug'}]

        # TEST 2
        if ("20180717debug_alpk" in sub_type):
            """
            equi_20180702_ITG_alpk_alpha_k_3666_r12000_A0_equitg_maxJ
            """
            A = -1.5653705443525463
            R_inf = 1.20

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180628',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'alpha_k': 0.36666666666666664}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'combo_desc': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'file_save_suffix': '_debug'}]

        # TEST 3
        if ("20180717debug_beta" in sub_type):
            """
            equi_20180702_ITG_beta_beta_9800_r12000_A0_equitg_maxJ
            """
            A = -1.5653705443525463
            R_inf = 1.20

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180628',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'beta': 0.98}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'combo_desc': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'file_save_suffix': '_debug'}]

        # TEST 4
        if ("20180717debug_depr" in sub_type):
            """
            equi_20180702_ITG_depr_K_DEPRECIATION_500_r11333_A0_equitg_maxJ
            """
            A = -1.5653705443525463
            R_inf = 1.1333333333333333

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180628',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'K_DEPRECIATION': 0.05}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'combo_desc': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'file_save_suffix': '_debug'}]

        # TEST 5
        if ("20180717debug_kapp" in sub_type):
            """
            equi_20180702_ITG_kapp_kappa_7000_r11333_A0_equitg_maxJ
            """
            A = -1.5653705443525463
            R_inf = 1.1333333333333333

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180628',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'kappa': 0.7}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'combo_desc': 'DEBUGGING--fcib_BNI_BORR_P_0_r12000_A0_equitg'
                     , 'file_save_suffix': '_debug'}]

        # TEST 6
        if ("20180916debug_Afcib" in sub_type):
            """
            failed to produce:
                s_20180829_ITG_I3_fcib_c2_fcib8076_A2613_exoitg_wgtJ.json
            generate this by itself to see where things went wrong
            """
            A = -0.15344410277866738
            BNI_BORR_P = 0.8076923076923077

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180815',
                                                      {'BNI_BORR_P': BNI_BORR_P}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--s_20180829_ITG_I3_fcib_c2_fcib8076_A2613_exoitg_wgtJ'
                     , 'combo_desc': 'DEBUGGING--s_20180829_ITG_I3_fcib_c2_fcib8076_A2613_exoitg_wgtJ'
                     , 'file_save_suffix': '_debug'}]

        # TEST 7
        if ("20180916debug_lgit" in sub_type):
            """
            failed to produce:
                low A and lgit
            generate this by itself to see where things went wrong
            """
            A = -0.4147801360881366
            logit_sd_scale = 0.75

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629'],
                                        'esti_type': ['a', '20180815',
                                                      {'logit_sd_scale': logit_sd_scale}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607']}
                     , 'title': 'DEBUGGING--lowAloglogitSD'
                     , 'combo_desc': 'DEBUGGING--lowAloglogitSD'
                     , 'file_save_suffix': '_debug'}]

        # TEST 8
        if ("20180917debug_lgitlowR" in sub_type):
            """
            failed to produce:
                low A and lgit
            generate this by itself to see where things went wrong
            """
            A = -0.4147801360881366
            logit_sd_scale = 0.75
            R_inf = 0.80

            combo_list = \
                [{'param_update_dict': {'grid_type': ['a', '20180629x'],
                                        'esti_type': ['a', '20180815',
                                                      {'R_INFORM_SAVE': R_inf,
                                                       'R_INFORM_BORR': R_inf,
                                                       'logit_sd_scale': logit_sd_scale}],
                                        'data_type': ['a', '20180607',
                                                      {'A': A}],
                                        'model_type': ['a', '20180701'],
                                        'interpolant_type': ['a', '20180607x']}
                     , 'title': 'DEBUGGING--lowAlowRloglogitSD'
                     , 'combo_desc': 'DEBUGGING--lowAlowRloglogitSD'
                     , 'file_save_suffix': '_debug'}]

    """
    MAIN RUN GROUPS
    """
    if ("20180702" in sub_type):

        if ("20180702x" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("20180702d" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180628',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t)
    """
    MAIN RUN GROUPS
    """
    main_type_str = '20180814'
    if ((main_type_str in sub_type) and ('JSON' not in sub_type)):
        '''
        interest rates for Central Second Period
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

    """
    2018-09-18 05:50:
        during 20180829, same program, had bugs:
            1. https://www.evernote.com/shard/s10/nl/1203171/415be2fb-4c51-4f0e-9160-7bed433e8ec9
            2. https://www.evernote.com/shard/s10/nl/1203171/c12f5534-199e-4707-8ea2-eeba5740a485
        after resolving these bugs, reran as 0916
        than expanded change minmax range, rerun as 0918
    """
    main_type_str_list = ['20180829', '20180916', '20180918']
    main_type_str_list = ['20180829', '20180918']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])
            and ('JSON' not in sub_type)):
        '''
        sizing
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
        Integration
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        '''
        min max range adjustments
        '''
        if ('20180829' in sub_type):
            minmax_t = '20180901'
        elif ('20180916' in sub_type):
            minmax_t = '20180901'
        elif ('20180918' in sub_type):
            minmax_t = '20180917'
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

    """
    Incorportating Estimation Results into Simulation:
        + to run counterfactuals based on estimates
    """
    main_type_str = 'JSON'
    if (main_type_str in sub_type):
        '''
        interest rates for Central Second Period
        these below don't matter, will be overriden
        '''
        if ("x_" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("d_" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
        else:
            dist_t = 'NONE'

        combo_list = paramloopsjson.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t='20180815',
            data_f='a', data_t='20180607',
            model_f='a', model_t='20180701',
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t='20180917')

    """
    2018-10-11 21:28
        Single Set of Parameter Invokation: 201810S, S for Single invoke
        Bench market simulation, based on benchmark parameters
        - 201810S_ITG
    """
    main_type_str = '201810S'
    if (main_type_str in sub_type):
        '''
        interest rates for Central Second Period
        these below don't matter, will be overriden
        '''
        if ("x_" in sub_type):
            grid_type = ['a', '20180629x']
            interpolant_type = ['a', '20180607x']
        elif ("d_" in sub_type):
            grid_type = ['a', '20180629d']
            interpolant_type = ['a', '20180607d']
        else:
            grid_type = ['a', '20180629']
            interpolant_type = ['a', '20180607']

        if ("_ITG_" in sub_type):
            dist_t = '20180716'
            if ("d_" in sub_type):
                dist_t = '20181013'
        else:
            dist_t = 'NONE'

        if ("_1j7" in sub_type):
            model_t = '20181011'
            esti_t = '20180607'
        elif ("_1ja7" in sub_type):
            '''
            _1j7 does not work, 1ja7 approximates 1j7 by making fixed cost very high for saving option
            '''
            model_t = '20181013j16'
            esti_t = '20181013simuinfFC'
        elif ("_2j127" in sub_type):
            model_t = '20181013j016'
            esti_t = '20181013simu'
        elif ("_5j12347" in sub_type):
            model_t = '20180613'
            esti_t = '20181013simuFC5j12347'
        elif ("_7jAll" in sub_type):
            model_t = '20180701'
            esti_t = '20181013simuFC5j12347'
        else:
            raise ('bad _j12347 etc not in sub_type')

        esti_add = {}
        if (main_type_str + '20A' in sub_type):
            '''
            adjust lgit to lower number, see effects
            '''
            esti_add = {'logit_sd_scale': 0.85}

        #         'data_type':['a', '20180701']
        combo_list = \
            [{'param_update_dict': {'grid_type': [grid_type[0], grid_type[1]],
                                    'esti_type': ['a', esti_t, esti_add],
                                    'data_type': ['a', '20180607'],
                                    'model_type': ['a', model_t],
                                    'interpolant_type': [interpolant_type[0], interpolant_type[1]],
                                    'dist_type': ['a', dist_t],
                                    'minmax_type': ['a', '20180917']}
                 , 'title': 'Benchmark'
                 , 'combo_desc': 'Benchmark'
                 , 'file_save_suffix': '_benchmark'}]

    """
    2018-10-24 16:20
    testing mean preserving variance
    """
    main_type_str_list = ['20181024']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):
        '''
        sizing
        '''
        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024x']
            interpolant_type = ['a', '20180607x']
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20181024']
            interpolant_type = ['a', '20180607']

        '''
        Integration
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20181025'
        else:
            dist_t = 'NONE'

        '''
        min max range adjustments
        '''
        if ('20181024' in sub_type):
            minmax_t = '20180901'
        else:
            raise ('bad')

        '''
        Which model
        '''
        if ("_1j7" in sub_type):
            model_t = '20181011'
            esti_t = '20180607'
        elif ("_1ja7" in sub_type):
            '''
            _1j7 does not work, 1ja7 approximates 1j7 by making fixed cost very high for saving option
            '''
            model_t = '20181013j16'
            esti_t = '20181013simuinfFC'
        elif ("_2j127" in sub_type):
            model_t = '20181013j016'
            esti_t = '20181021bench'
        elif ("_5j12347" in sub_type):
            model_t = '20180613'
            esti_t = '20181013simuFC5j12347'
        elif ("_7jAll" in sub_type):
            model_t = '20180701'
            esti_t = '20181013simuFC5j12347'
        else:
            raise ('bad _j12347 etc not in sub_type')

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t=esti_t,
            data_f='a', data_t='20181024',
            model_f='a', model_t=model_t,
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t=minmax_t)

    """
    2018-11-11 11:04
    Simulating T2 Main GE
    + after significant T2 simulations, picked a final one as main simulation
    """
    main_type_str_list = ['20181111']
    if (any([main_type_str in sub_type for main_type_str in main_type_str_list])):
        '''
        sizing
        '''
        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024x']
            interpolant_type = ['a', '20180607x']
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20181024']
            interpolant_type = ['a', '20180607']

        '''
        Integration
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20181025'
        else:
            dist_t = 'NONE'

        '''
        Which model
        '''
        if ("_1j7" in sub_type):
            model_t = '20181011'
            esti_t = '20180607'
        elif ("_1ja7" in sub_type):
            '''
            _1j7 does not work, 1ja7 approximates 1j7 by making fixed cost very high for saving option
            '''
            model_t = '20181013j16'
            esti_t = '20181013simuinfFC'
        elif ("_2j127" in sub_type):
            model_t = '20181013j016'
            esti_t = '20181021bench'
        elif ("_5j12347" in sub_type):
            model_t = '20180613'
            esti_t = '20181013simuFC5j12347'
        elif ("_7jAll" in sub_type):
            model_t = '20180701'
            esti_t = '20181013simuFC5j12347'
        else:
            raise ('bad _j12347 etc not in sub_type')

        if ('20181111a' in sub_type):
            lgit_grid = np.linspace(np.linspace(0.90, 1.1, 10)[5 - 1], np.linspace(0.80, 1.2, 10)[7 - 1], 10)
            kappa_grid = np.linspace(0.10, 0.90, 10)
            R_FORMAL_SAVE_grid = np.linspace(1.0, 1.050, 10)
            R_FORMAL_BORR_grid = np.linspace(1.033, 1.133, 10)
            BNF_BORR_P_grid = np.linspace(0, 3, 10)

            '''
            A: T2, GOOD SAVE, Panel Left, Row 2 column 3
                - https://www.evernote.com/shard/s10/nl/1203171/3358e600-4d49-4ed4-b47c-48f8bc0b1631
            '''
            esti_type_dict = {'logit_sd_scale': lgit_grid[3],
                              'BNI_BORR_P': 0.0,
                              'BNI_LEND_P': 3.0,
                              'BNF_BORR_P': BNF_BORR_P_grid[2],
                              'BNF_SAVE_P': 0.0,
                              'kappa': kappa_grid[7],
                              'R_FORMAL_BORR': R_FORMAL_BORR_grid[5],
                              'R_FORMAL_SAVE': R_FORMAL_SAVE_grid[9],
                              'R_INFORM_SAVE': 1.0992187500000001,
                              'R_INFORM_BORR': 1.0992187500000001}
            data__A_params_sd = {'epsA_frac_A': 0.15}
            esti_type_f = '20181021bench'
            dist_type_f = '20181025'

        if ('20181111b' in sub_type):
            '''
            very uneven, a little weird looking, more eve now
            '''
            esti_type_dict = {}
            #             esti_type_dict = {'logit_sd_scale': 1,
            #                               'BNI_BORR_P': 0.0,
            #                               'BNI_LEND_P': 2.0,
            #                               'BNF_BORR_P': BNF_BORR_P_grid[1],
            #                               'BNF_SAVE_P': 0.0,
            #                               'kappa': kappa_grid[7],
            #                               'R_FORMAL_BORR': R_FORMAL_BORR_grid[5],
            #                               'R_FORMAL_SAVE': R_FORMAL_SAVE_grid[3],
            #                               'R_INFORM_SAVE': 1.0992187500000001,
            #                               'R_INFORM_BORR': 1.0992187500000001}
            data__A_params_sd = {'epsA_frac_A': 0.15}
            esti_type_f = '20181013simuFC5j12347'
            dist_type_f = '20181025'

        if ('20181111c' in sub_type):
            '''
            change some parameters in ways I understand and see what happens
            '''
            lgit_grid = np.linspace(np.linspace(0.90, 1.1, 10)[5 - 1], np.linspace(0.80, 1.2, 10)[7 - 1], 10)
            kappa_grid = np.linspace(0.10, 0.90, 10)
            R_FORMAL_SAVE_grid = np.linspace(1.0, 1.050, 10)
            R_FORMAL_BORR_grid = np.linspace(1.033, 1.133, 10)
            BNF_BORR_P_grid = np.linspace(0, 3, 10)

            '''
            A: T2, GOOD SAVE, Panel Left, Row 2 column 3
                - https://www.evernote.com/shard/s10/nl/1203171/3358e600-4d49-4ed4-b47c-48f8bc0b1631
                but now modified to be more consistent with previous detailed simulation:
                    - 201810S
            '''
            esti_type_dict = {'rho': 1,
                              'logit_sd_scale': 1,
                              'BNI_BORR_P': 0.25,
                              'BNI_LEND_P': 1.5,
                              'BNF_BORR_P': BNF_BORR_P_grid[2],
                              'BNF_SAVE_P': 0.25,
                              'kappa': kappa_grid[2],
                              'R_FORMAL_BORR': R_FORMAL_BORR_grid[5],
                              'R_FORMAL_SAVE': R_FORMAL_SAVE_grid[4],
                              'R_INFORM_SAVE': 1.05,
                              'R_INFORM_BORR': 1.05}
            data__A_params_sd = {'epsA_frac_A': 0.15}
            esti_type_f = '20181021bench'
            dist_type_f = '20181025'

        combo_list = \
            [{'param_update_dict': {'grid_type': [grid_type[0], grid_type[1]],
                                    'esti_type': ['a', esti_type_f, esti_type_dict],
                                    'data_type': ['a', '20181024'],
                                    'model_type': ['a', model_t],
                                    'interpolant_type': [interpolant_type[0], interpolant_type[1]],
                                    'dist_type': ['a', dist_type_f, data__A_params_sd],
                                    'minmax_type': ['a', 'B181107']}  # B181021 already called
                 , 'title': 'Benchmarksimu'
                 , 'combo_desc': 'Benchmarksimu'
                 , 'file_save_suffix': '_bnchsimu'}]

    return combo_list
