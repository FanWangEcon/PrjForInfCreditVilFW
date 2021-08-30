'''

@author: fan
'''

import parameters.loop_combo_type_list.param_str as paramloopstr


def param(param_type=1):
    """
    Parameters
    ----------
    type: list
        = ['a', 1]
        could be longer, more and more

    """

    module = param_type[0]
    sub_type = str(param_type[1])

    subtitle = 'zeroFE'
    esti_param = {'R_INFORM_SAVE': 1.15, 'R_INFORM_BORR': 1.15, 'R_FORMAL_SAVE': 1.02, 'R_FORMAL_BORR': 1.05,
                  'R_AVG_INT': 1.10, 'BNF_SAVE_P': 0, 'BNF_BORR_P': 0, 'BNI_LEND_P': 0, 'BNI_BORR_P': 0,
                  'CEV_PROP_INCREASE': 0.00}

    # 2021-01-08 10:58, add consumption share change as a parameter

    if (sub_type == '1'):
        pass

    if (sub_type == '2'):
        subtitle = 'basicFE'
        esti_param = {
            # BudgetConsumption
            'R_INFORM_SAVE': 1.15,
            'R_INFORM_BORR': 1.15,
            'R_FORMAL_SAVE': 1.02,
            'R_FORMAL_BORR': 1.06,
            'R_AVG_INT': 1.10,  # used in future_loginf
            'BNF_SAVE_P': 0.5,
            'BNF_BORR_P': 3,
            'BNI_LEND_P': 5,
            'BNI_BORR_P': 1.5,
        }

    if (sub_type == '3'):
        """log utility"""
        esti_param['rho'] = 1

    if (sub_type == '20180511'):
        """log utility + 0.96 beta"""
        '''people not saving enough, see if they save more now'''
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96

    if (sub_type == '20180512'):
        """log utility + 0.96 beta"""
        '''people not saving enough, see if they save more now'''
        '''Copy as many parameters as possible from Angeletos'''
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.3
        esti_param['K_DEPRECIATION'] = 0.08

    if (sub_type == '201805160'):
        """log utility + 0.96 beta"""
        '''people not saving enough, see if they save more now'''
        '''Copy as many parameters as possible from Angeletos'''
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.08
        esti_param['R_INFORM_SAVE'] = 1.08
        esti_param['R_INFORM_BORR'] = 1.08

    if (sub_type == '20180607'):
        """log utility + 0.96 beta"""
        '''people not saving enough, see if they save more now'''
        '''Copy as many parameters as possible from Angeletos'''
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.08
        esti_param['R_INFORM_SAVE'] = 1.02
        esti_param['R_INFORM_BORR'] = 1.02
        esti_param['logit_sd_scale'] = 1

    if (sub_type == '20180613'):
        """
        Same as 20180607 except R informal, 1.08 more realistic,
        doable with more choice categories
        """
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.08
        esti_param['R_INFORM_SAVE'] = 1.08
        esti_param['R_INFORM_BORR'] = 1.08
        esti_param['logit_sd_scale'] = 1

        esti_param['BNF_SAVE_P'] = 0.5
        esti_param['BNF_BORR_P'] = 1.5
        esti_param['BNI_LEND_P'] = 2.5
        esti_param['BNI_BORR_P'] = 1

        esti_param['kappa'] = 0.25

    if (sub_type == '20180628'):
        """
        Adjust Fixed costs based on looping over parameter values
        So that more choices show up jointly
        """
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.15
        esti_param['R_INFORM_SAVE'] = 1.08
        esti_param['R_INFORM_BORR'] = 1.08
        esti_param['logit_sd_scale'] = 1
        esti_param['BNF_SAVE_P'] = 0
        esti_param['BNF_BORR_P'] = 0
        esti_param['BNI_LEND_P'] = 0
        esti_param['BNI_BORR_P'] = 0

        esti_param['kappa'] = 0.25

    if (sub_type == '20180701'):
        """
        Adjust Fixed costs based on looping over parameter values
        So that more choices show up jointly
        """
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.60
        esti_param['K_DEPRECIATION'] = 0.15
        esti_param['R_INFORM_SAVE'] = 1.08
        esti_param['R_INFORM_BORR'] = 1.08
        esti_param['logit_sd_scale'] = 1

        esti_param['BNF_SAVE_P'] = 0.3
        esti_param['BNF_BORR_P'] = 0.5
        esti_param['BNI_LEND_P'] = 2.0
        esti_param['BNI_BORR_P'] = 0.1

        esti_param['kappa'] = 0.25

    if (sub_type == '20180814'):
        """
        Adjust Fixed costs based on looping over parameter values
        So that more choices show up jointly
        """
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.15

        esti_param['R_INFORM_SAVE'] = 1.094
        esti_param['R_INFORM_BORR'] = 1.094
        esti_param['R_FORMAL_SAVE'] = 1.010
        esti_param['R_FORMAL_BORR'] = 1.054
        esti_param['logit_sd_scale'] = 1

        esti_param['BNF_SAVE_P'] = 0.3
        esti_param['BNF_BORR_P'] = 0.5
        esti_param['BNI_LEND_P'] = 2.0
        esti_param['BNI_BORR_P'] = 0.1
        esti_param['kappa'] = 0.25

    if (sub_type == '20180815'):
        """
        Joint Estimation with two regions:
            THREE SETS of PARAMETERS NOW
        """
        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.15

        esti_param['logit_sd_scale'] = 1

        '''
        Fixed Cost and Collateral, estimated
        '''
        esti_param['BNF_SAVE_P'] = 0.3
        esti_param['BNF_BORR_P'] = 0.5
        esti_param['BNI_LEND_P'] = 2.0
        esti_param['BNI_BORR_P'] = 0.1
        esti_param['kappa'] = 0.25

        esti_param['BNF_SAVE_P' + paramloopstr.peristr(period=1)] = 0.3
        esti_param['BNF_BORR_P' + paramloopstr.peristr(period=1)] = 0.5
        esti_param['BNI_LEND_P' + paramloopstr.peristr(period=1)] = 2.0
        esti_param['BNI_BORR_P' + paramloopstr.peristr(period=1)] = 0.1
        esti_param['kappa' + paramloopstr.peristr(period=1)] = 0.25

        esti_param['BNF_SAVE_P' + paramloopstr.peristr(period=2)] = 0.3
        esti_param['BNF_BORR_P' + paramloopstr.peristr(period=2)] = 0.5
        esti_param['BNI_LEND_P' + paramloopstr.peristr(period=2)] = 2.0
        esti_param['BNI_BORR_P' + paramloopstr.peristr(period=2)] = 0.1
        esti_param['kappa' + paramloopstr.peristr(period=2)] = 0.25

        esti_param['BNF_SAVE_P' + paramloopstr.peristr(period=3)] = 0.3
        esti_param['BNF_BORR_P' + paramloopstr.peristr(period=3)] = 0.5
        esti_param['BNI_LEND_P' + paramloopstr.peristr(period=3)] = 2.0
        esti_param['BNI_BORR_P' + paramloopstr.peristr(period=3)] = 0.1
        esti_param['kappa' + paramloopstr.peristr(period=3)] = 0.25

        esti_param['BNF_SAVE_P' + paramloopstr.peristr(period=4)] = 0.3
        esti_param['BNF_BORR_P' + paramloopstr.peristr(period=4)] = 0.5
        esti_param['BNI_LEND_P' + paramloopstr.peristr(period=4)] = 2.0
        esti_param['BNI_BORR_P' + paramloopstr.peristr(period=4)] = 0.1
        esti_param['kappa' + paramloopstr.peristr(period=4)] = 0.25

        '''
        Interest Rates, data
        '''
        esti_param['R_INFORM_BORR' + paramloopstr.peristr(period=1)] = 1.139
        esti_param['R_INFORM_SAVE' + paramloopstr.peristr(period=1)] = 1.139
        esti_param['R_FORMAL_BORR' + paramloopstr.peristr(period=1)] = 1.061
        esti_param['R_FORMAL_SAVE' + paramloopstr.peristr(period=1)] = 1.011

        esti_param['R_INFORM_BORR' + paramloopstr.peristr(period=2)] = 1.094
        esti_param['R_INFORM_SAVE' + paramloopstr.peristr(period=2)] = 1.094
        esti_param['R_FORMAL_BORR' + paramloopstr.peristr(period=2)] = 1.054
        esti_param['R_FORMAL_SAVE' + paramloopstr.peristr(period=2)] = 1.010

        esti_param['R_INFORM_BORR'] = (1.139 + 1.094) / 2
        esti_param['R_INFORM_SAVE'] = (1.139 + 1.094) / 2
        esti_param['R_FORMAL_SAVE'] = (1.061 + 1.054) / 2
        esti_param['R_FORMAL_BORR'] = (1.011 + 1.010) / 2

        esti_param['R_INFORM_BORR' + paramloopstr.peristr(period=3)] = 1.279
        esti_param['R_INFORM_SAVE' + paramloopstr.peristr(period=3)] = 1.279
        esti_param['R_FORMAL_BORR' + paramloopstr.peristr(period=3)] = 1.148
        esti_param['R_FORMAL_SAVE' + paramloopstr.peristr(period=3)] = 1.033

        esti_param['R_INFORM_BORR' + paramloopstr.peristr(period=4)] = 1.139
        esti_param['R_INFORM_SAVE' + paramloopstr.peristr(period=4)] = 1.139
        esti_param['R_FORMAL_BORR' + paramloopstr.peristr(period=4)] = 1.061
        esti_param['R_FORMAL_SAVE' + paramloopstr.peristr(period=4)] = 1.011

    if ('20181013simu' in sub_type):

        esti_param['rho'] = 1
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.08
        esti_param['R_INFORM_SAVE'] = 1.05
        esti_param['R_INFORM_BORR'] = 1.05
        esti_param['logit_sd_scale'] = 1

        # BNF_BORR_P = 1
        BNF_BORR_P = 0.75
        BNF_SAVE_P = 0.25

        # BNI_LEND_P = 3
        BNI_LEND_P = 1.5
        BNI_BORR_P = 0.25

        R_FORMAL_SAVE = 1.02
        R_FORMAL_BORR = 1.06

        if (sub_type == '20181013simuinfFC'):
            '''_1ja7'''
            esti_param['R_INFORM_SAVE'] = 0.01
            esti_param['BNI_LEND_P'] = 45

        if (sub_type == '20181013simu'):
            '''_2j12'''
            esti_param['BNI_LEND_P'] = BNI_LEND_P
            esti_param['BNI_BORR_P'] = BNI_BORR_P

        if (sub_type == '20181013simuFC5j12347'):
            '''_4j1237'''
            esti_param['BNF_BORR_P'] = BNF_BORR_P
            esti_param['BNF_SAVE_P'] = BNF_SAVE_P
            esti_param['BNI_LEND_P'] = BNI_LEND_P
            esti_param['BNI_BORR_P'] = BNI_BORR_P
            esti_param['R_FORMAL_SAVE'] = R_FORMAL_SAVE
            esti_param['R_FORMAL_BORR'] = R_FORMAL_BORR

    if ('20181021bench' in sub_type):
        esti_param['rho'] = 1.5
        esti_param['beta'] = 0.96
        esti_param['alpha_k'] = 0.36
        esti_param['K_DEPRECIATION'] = 0.08
        esti_param['R_INFORM_SAVE'] = 1.05
        esti_param['R_INFORM_BORR'] = 1.05

    main_type_str_list = ['20201025']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):
        esti_param_update = {
            'rho': 1.3,
            'beta': 0.96,
            'alpha_k': 0.36,
            'K_DEPRECIATION': 0.15,
            'logit_sd_scale': 1,
            'BNF_SAVE_P': 0,
            'BNF_BORR_P': 0,
            'BNI_LEND_P': 0,
            'BNI_BORR_P': 0,
            'kappa': 0.25,
            'R_INFORM_SAVE': 1.15,
            'R_INFORM_BORR': 1.15,
            'R_FORMAL_SAVE': 1.02,
            'R_FORMAL_BORR': 1.05,
            'R_AVG_INT': 1.10
        }
        esti_param.update(esti_param_update)

    main_type_str_list = ['19E1']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        esti_param_update = {}

        """
        A. Common
        """
        esti_param_NE_fixed = {
            'rho': 2.0,
            'beta': 0.88,
            'alpha_k': 0.15,
            'K_DEPRECIATION': 0.056,
            'logit_sd_scale': 1.5,
        }
        esti_param_update.update(esti_param_NE_fixed)

        """
        Some scaling options
        """
        st_scale_opt = 'polA1A2B1B2_V4_20210113'
        if st_scale_opt == 'polA1A2B1B2_V4_20210113':
            # trying these cost, kind of randomly?
            fl_cost_multiple = 10
            fl_bni_lend_p_divider = 2.5
        elif st_scale_opt == 'polA1A2B1B2_V5_20210113':
            fl_cost_multiple = 1
            fl_bni_lend_p_divider = 1
        else:
            raise ValueError(f'{st_scale_opt=} is not feasible')

        """
        B. Earlier Period Specific, exercise A1 Parameters
        """
        esti_param_NE_99 = {
            'BNF_BORR_P': 0.090 * fl_cost_multiple,
            'BNF_SAVE_P': 0.083 * fl_cost_multiple,
            'BNI_BORR_P': 0.053 * fl_cost_multiple,
            'BNI_LEND_P': 0.134 * fl_cost_multiple / fl_bni_lend_p_divider,
            'kappa': 0.28,
        }
        # per = partial equilibrium rates
        esti_per_NE_99 = {
            'R_FORMAL_SAVE': 1.033,
            'R_FORMAL_BORR': 1.148,
        }
        # ger = ge rates
        esti_ger_NE_99 = {
            'R_INFORM_SAVE': 1.279,
            'R_INFORM_BORR': 1.279,
            'R_AVG_INT': 1.279
        }

        """
        C. Later Period Specific, exericse A2a, A2b, and B1 parameters
        """
        esti_param_NE_02 = {
            'BNF_BORR_P': 0.046 * fl_cost_multiple,
            'BNF_SAVE_P': 0.071 * fl_cost_multiple,
            'BNI_BORR_P': 0.053 * fl_cost_multiple,
            'BNI_LEND_P': 0.186 * fl_cost_multiple / fl_bni_lend_p_divider,
            'kappa': 0.56,
        }
        # per = partial equilibrium rates
        esti_per_NE_02 = {
            'R_FORMAL_SAVE': 1.011,
            'R_FORMAL_BORR': 1.061,
        }
        # ger = ge rates
        esti_ger_NE_02 = {
            'R_INFORM_SAVE': 1.139,
            'R_INFORM_BORR': 1.139,
            'R_AVG_INT': 1.139
        }

        """
        Exercise A1, solve at GE (1st)
        """
        if '19E1NEp99r99' in sub_type:
            esti_param_update.update(esti_param_NE_99)
            esti_param_update.update(esti_per_NE_99)
            esti_param_update.update(esti_ger_NE_99)

        """
        Exercise A2a
        """
        if '19E1NEp02r99' in sub_type:
            esti_param_update.update(esti_param_NE_02)
            esti_param_update.update(esti_per_NE_99)
            esti_param_update.update(esti_ger_NE_99)

        """
        Exercise A2b
        """
        if '19E1NEp02per02ger99' in sub_type:
            esti_param_update.update(esti_param_NE_02)
            esti_param_update.update(esti_per_NE_02)
            esti_param_update.update(esti_ger_NE_99)

        """
        Exercise B1, solve at GE (2nd)
        """
        if '19E1NEp02r02' in sub_type:
            esti_param_update.update(esti_param_NE_02)
            esti_param_update.update(esti_per_NE_02)
            esti_param_update.update(esti_ger_NE_02)
            """
            # Exercise B2a, solve at GE (3rd)
            """
            if '19E1NEp02r02f11A' in sub_type:
                # this kind of goes back to previous time interest rate for savings levels
                esti_param_update['R_FORMAL_SAVE'] = esti_param_update['R_FORMAL_SAVE'] + 0.02
            if '19E1NEp02r02f11B' in sub_type:
                esti_param_update['R_FORMAL_SAVE'] = esti_param_update['R_FORMAL_SAVE'] + 0.08
            if '19E1NEp02r02f11C' in sub_type:
                esti_param_update['R_FORMAL_SAVE'] = esti_param_update['R_FORMAL_SAVE'] + 0.16
            """
            Exercise B2b, solve at GE (4th)
            """
            if '19E1NEp02r02f12A' in sub_type:
                esti_param_update['BNF_SAVE_P'] = esti_param_update['BNF_SAVE_P'] * 0.9
            if '19E1NEp02r02f12B' in sub_type:
                esti_param_update['BNF_SAVE_P'] = esti_param_update['BNF_SAVE_P'] * 0.5
            if '19E1NEp02r02f12C' in sub_type:
                esti_param_update['BNF_SAVE_P'] = esti_param_update['BNF_SAVE_P'] * 0.1

            """
            Exercise B2c, collateral relaxation
            """
            if '19E1NEp02r02cltA' in sub_type:
                esti_param_update['kappa'] = 0.42
            if '19E1NEp02r02cltB' in sub_type:
                esti_param_update['kappa'] = 0.28
            if '19E1NEp02r02cltC' in sub_type:
                esti_param_update['kappa'] = 0.14
            if '19E1NEp02r02cltD' in sub_type:
                esti_param_update['kappa'] = 0.04
            if '19E1NEp02r02cltE' in sub_type:
                esti_param_update['kappa'] = 0.70
            if '19E1NEp02r02cltF' in sub_type:
                esti_param_update['kappa'] = 0.84

        """
        Exercise C1, solve at GE (2nd)
        """

        if '19E1kap' in sub_type:
            # all parameter base are equal to 2002 values.
            esti_param_update.update(esti_param_NE_02)
            esti_param_update.update(esti_per_NE_02)
            esti_param_update.update(esti_ger_NE_02)

            # 19E1kapTkTr: tight kappa, tight kappa equilibrium r
            if '19E1kapTkTr28' in sub_type:
                esti_param_update['kappa'] = 0.28
                esti_param_update['R_INFORM_SAVE'] = 1.1279
                esti_param_update['R_INFORM_BORR'] = 1.1279
                esti_param_update['R_AVG_INT'] = 1.1279

            # 19E1kapRkTr: relax kappa, tight kappa equilibrium r
            if '19E1kapRkTr' in sub_type:
                esti_param_update['R_INFORM_SAVE'] = 1.1279
                esti_param_update['R_INFORM_BORR'] = 1.1279
                esti_param_update['R_AVG_INT'] = 1.1279
                if '19E1kapRkTr42' in sub_type:
                    esti_param_update['kappa'] = 0.42
                if '19E1kapRkTr56' in sub_type:
                    esti_param_update['kappa'] = 0.56
                if '19E1kapRkTr70' in sub_type:
                    esti_param_update['kappa'] = 0.70
                if '19E1kapRkTr84' in sub_type:
                    esti_param_update['kappa'] = 0.84

            # 19E1kapRkRr: relax kappa, Relax kappa equilibrium r
            if '19E1kapRkRr' in sub_type:
                if '19E1kapRkRr42' in sub_type:
                    esti_param_update['kappa'] = 0.42
                    R_INFORM = 1.1220
                elif '19E1kapRkRr56' in sub_type:
                    esti_param_update['kappa'] = 0.56
                    R_INFORM = 1.1201
                elif '19E1kapRkRr70' in sub_type:
                    esti_param_update['kappa'] = 0.70
                    R_INFORM = 1.1076
                elif '19E1kapRkRr84' in sub_type:
                    esti_param_update['kappa'] = 0.84
                    R_INFORM = 1.1005
                else:
                    raise ValueError(f'{sub_type=} with 19E1kapRkRr substring unexpected full string')
                esti_param_update['R_INFORM_SAVE'] = R_INFORM
                esti_param_update['R_INFORM_BORR'] = R_INFORM
                esti_param_update['R_AVG_INT'] = R_INFORM

        # Update esti_param
        esti_param.update(esti_param_update)

    return esti_param, subtitle
