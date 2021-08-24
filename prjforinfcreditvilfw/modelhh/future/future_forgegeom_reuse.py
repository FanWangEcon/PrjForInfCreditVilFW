'''
Created on May 27, 2018

@author: fan

Interpolation Based on Econforge method with geomspace
'''

# from interpolation.splines import LinearSpline, CubicSpline
import interpolation.splines as econforge
import logging
import numpy as np
import pyfan.amto.array.geomspace as geomspace
import pyfan.stats.interpolate.interpolate2d as interp2d

import dataandgrid.genstates as genstates
import modelhh.component as modelcomponent

logger = logging.getLogger(__name__)


def get_interpolant(interpolant,
                    bdgt_inst, prod_inst, param_inst,
                    EjV,
                    B_V, K_V, A_V, eps_V,
                    B_Veps, K_Veps, A_Veps, eps_Veps,
                    B_Vepszr=None, K_Vepszr=None, A_Vepszr=None, eps_Vepszr=None,
                    export_panda=False):
    """
    Solve for interoplant, update every round of VFI
    
    1. Given V(DATA=[K,B,A]), find V_Pie
        a. get data_mat
            + data_mat =future_polyquad(DATA, eps=0, return_type='DATAMAT')
        b. V_Pie from regress(V, data_mat)
        c. update V_Pie
            + update_parm_futureval(V_Pie, return_type='V')
            
    2. Given V_pie, solve EV(K,B,A), integrated over shocks
        a. get V_eps
            + V_eps = future_polyquad(DATA_TILE, eps=drawiid, return_type='V')
        b. EV = mean(reshape(V_eps(states*choices, shocks)))
        c. EV_Pie from regress(EV, data)
        d. update EV_Pie
            + update_parm_futureval(EV_Pie, return_type='EV')
            
    3. Given (Kp,Bp, A), find EV(Kp,Bp, A)
        a. get EV at choices
             + EV =future_polyquad(Kp, Bp, A, eps=0, return_type='EV')
    """

    len_states = param_inst.grid_param['len_states']
    len_eps_E = param_inst.grid_param['len_eps_E']

    logger.debug(['len_states:', len_states])
    logger.debug(['len_eps_E:', len_eps_E])

    '''
    1. get cash dimension 
    '''
    __, cash_partial = \
        modelcomponent.gen_Y_gen_cash(bdgt_inst, prod_inst, B_V, K_V, A_V, eps_V, shockNegInf=False)
    __, cash_partial_eps = \
        modelcomponent.gen_Y_gen_cash(bdgt_inst, prod_inst, B_Veps, K_Veps, A_Veps, eps_Veps, shockNegInf=False)

    '''
    2. Evaluate V(K,B,A), integrated over shocks
    '''
    V_eps = interp2d.interp_griddata(cur_u=EjV,
                                     cur_x1=cash_partial, cur_x2=K_V,
                                     new_x1=cash_partial_eps, new_x2=K_Veps)

    #     proj_sys_sup.debug_panda('EjV,cash_partial,K_V, B_V, eps_V',
    #                              np.column_stack((EjV,cash_partial,K_V, B_V, eps_V)),
    #                              subfolder='test_future_griddata', filename='V', export_panda=False)
    #     proj_sys_sup.debug_panda('V_eps,cash_partial_eps,K_Veps,B_Veps, eps_Veps',
    #                              np.column_stack((V_eps,cash_partial_eps,K_Veps,B_Veps, eps_Veps)),
    #                              subfolder='test_future_griddata', filename='V_eps', export_panda=False)

    '''
    3. Average to get EV(K,B,A), integrated over shocks
    and get interpolant, do it here so only invoke this once
    '''
    EV = np.mean(np.reshape(V_eps, (len_states, len_eps_E)), axis=1)
    #     proj_sys_sup.debug_panda('EV,K_Vepszr,B_Vepszr', np.column_stack((EV,K_Vepszr,B_Vepszr)),
    #                              subfolder='test_future_griddata', filename='EV', export_panda=False)

    '''
    4. Interpolate
        interpolate on multilinear over regular equi-span grid
        state-space point on geometric regular grid.
        but the power are equi-span regular grid
        
        state_1 = a*z^0=a
        state_2 = a*z^1
        state_3 = a*z^2
        ...
        ...
        state_50 = a*z^49=b
        
        state_1 to state_50 are geometric with geom_ratio = z= 1.03
        but the powier, 0, 1, to 49 are regular equi-span. 
        interpolate over 0, 1 to 49                 
    '''
    len_k = param_inst.grid_param['len_k_start']
    len_states = param_inst.grid_param['len_states']
    len_b = int(len_states / len_k)

    a = np.array([0, 0])
    b = np.array([len_k - 1, len_b - 1])
    orders = np.array([len_k, len_b])
    values = np.reshape(EV, (len_k, len_b))

    interpolant['econforge_interpolant'] = econforge.LinearSpline(a, b, orders, values)
    logger.debug('EV:\n%s', EV)

    return interpolant


def func_forgegeom_EV_predict(param_inst, interpolant,
                              b_tp=None, k_tp=None,
                              choice_set_list_j=None):
    """Econ-forge quick interpolation method + my geom transform
    
    Expected Value prediction, every round of VFI
    
    Parameters
    ----------
    b_tp_square_geom_k_tp_geom: 2d array 2 column
        np.column_stack((k_tp_geom, b_tp_square_geom))    
    """

    if (interpolant['econforge_interpolant'] is None):
        EV_pred = 0
        interpolant = get_interpolant_grid_maxmin(param_inst, interpolant)

    else:
        # this is invoked at the start of VFI, also when zooming in, see solumain.py
        if (interpolant['bktp_geom'][choice_set_list_j] is None):
            b_tp_square_geom_k_tp_geom = set_ktpsqrgeom_btpgeom(param_inst, interpolant, b_tp, k_tp)
            interpolant['bktp_geom'][choice_set_list_j] = b_tp_square_geom_k_tp_geom

        econforge_interpolant = interpolant['econforge_interpolant']
        b_tp_square_geom_k_tp_geom = interpolant['bktp_geom'][choice_set_list_j]
        EV_pred = econforge_interpolant(b_tp_square_geom_k_tp_geom)

        logger.info('b_tp:\n%s', np.shape(k_tp))
        logger.info('EV_pred:\n%s', np.shape(EV_pred))

        # reshape needs to use k_tp rather than b_tp, b_tp does not exist for choice 6 
        EV_pred = np.reshape(EV_pred, (np.shape(k_tp)))

    return EV_pred


def set_ktpsqrgeom_btpgeom(param_inst, interpolant, b_tp, k_tp):
    """
    About 30 percent of compute time spent on 
        grid_to_geom_short 
            and on
        S = np.column_stack((k_tp_geom, b_tp_square_geom))
    But within VFI, within the same mjall, S is constant. 
    Here, given the number of choice list, pre-generate and store a list of S for
    all financial choices.
    """

    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']
    b_tp_square = b_tp + k_tp * (1 - K_DEPRECIATION)

    len_k = param_inst.grid_param['len_k_start']
    len_states = param_inst.grid_param['len_states']
    len_b = int(len_states / len_k)

    start = interpolant['interp_EV_k_b']['start']  # = 0
    stop = interpolant['interp_EV_k_b']['stop']  # = 1
    geom_ratio = interpolant['interp_EV_k_b']['geom_ratio']  # =1.03

    B_Vepszr_square_max = interpolant['interp_EV_k_b']['B_Vepszr_square_max']
    B_Vepszr_square_min = interpolant['interp_EV_k_b']['B_Vepszr_square_min']
    K_Vepszr_square_max = interpolant['interp_EV_k_b']['K_Vepszr_square_max']
    K_Vepszr_square_min = interpolant['interp_EV_k_b']['K_Vepszr_square_min']

    num = len_b
    b_tp_square_geom = geomspace.grid_to_geom_short(np.ravel(b_tp_square),
                                                    B_Vepszr_square_max, B_Vepszr_square_min,
                                                    start, stop, num, geom_ratio, 1)

    num = len_k
    k_tp_geom = geomspace.grid_to_geom_short(np.ravel(k_tp),
                                             K_Vepszr_square_max, K_Vepszr_square_min,
                                             start, stop, num, geom_ratio, 1)

    b_tp_square_geom_k_tp_geom = np.column_stack((k_tp_geom, b_tp_square_geom))

    return b_tp_square_geom_k_tp_geom


def get_interpolant_grid_maxmin(param_inst, interpolant):
    """
    See Figures in 
        C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_genstates
        https://www.evernote.com/shard/s10/nl/1203171/cfc85e04-d5cf-465c-ad55-5d561da62a9c
        
    These were initially:
        K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']
        B_Vepszr_square = B_Vepszr + K_Vepszr*(1-K_DEPRECIATION)
        interpolant['interp_EV_k_b']['B_Vepszr_square_max'] = np.max(B_Vepszr_square)
        interpolant['interp_EV_k_b']['B_Vepszr_square_min'] = np.min(B_Vepszr_square)
    
        interpolant['interp_EV_k_b']['K_Vepszr_square_max'] = np.max(K_Vepszr)
        interpolant['interp_EV_k_b']['K_Vepszr_square_min'] = np.min(K_Vepszr)
    
    But I realized, by studying gen_state file (see evernote link and test_genstates charts)
        by construction:
            minimum transformed B: B_Vepszr_square_min, is how much maximum borrowing (minimum borrowing)
                given current K could be obtained. When transformed, they all shift to 0
            the maximum B, based on the way I do this, is surprisingly to me at first:
                max(K)*(1-depreciation) + max(B), why?
                    https://www.evernote.com/shard/s10/nl/1203171/cfc85e04-d5cf-465c-ad55-5d561da62a9c
                B at K max shows actual specified max B, but B at K min adds the triangle displaced
                from left to the right.
    """

    B_Vepszr_square_max, B_Vepszr_square_min, \
    K_Vepszr_square_max, K_Vepszr_square_min = \
        genstates.max_min_K_B_sqr(param_inst)

    interpolant['interp_EV_k_b']['B_Vepszr_square_max'] = B_Vepszr_square_max
    interpolant['interp_EV_k_b']['B_Vepszr_square_min'] = B_Vepszr_square_min

    interpolant['interp_EV_k_b']['K_Vepszr_square_max'] = K_Vepszr_square_max
    interpolant['interp_EV_k_b']['K_Vepszr_square_min'] = K_Vepszr_square_min

    return interpolant
