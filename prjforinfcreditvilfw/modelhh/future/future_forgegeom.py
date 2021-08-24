'''
Created on May 27, 2018

@author: fan

Interpolation Based on Econforge method with geomspace. Contains functions
used by griddata and also geomforge future, could be invoked from two places.
'''

# from interpolation.splines import LinearSpline, CubicSpline
import interpolation.splines as econforge
import logging
import numpy as np
import pyfan.amto.array.geomspace as geomspace
import pyfan.stats.interpolate.interpolate2d as interp2d

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

    if (interpolant is None):
        interpolant = {'interp_type': 'forgegeom',
                       'interp_type_option': {
                           'method': 'linear'
                       },
                       'maxinter': 15,
                       'econforge_interpolant': None,
                       'interp_EV_k_b': {'B_Vepszr_square_max': None,
                                         'B_Vepszr_square_min': None,
                                         'K_Vepszr_square_max': None,
                                         'K_Vepszr_square_min': None,
                                         'start': 0,
                                         'stop': 1,
                                         'geom_ratio': 1.03}
                       }

    len_states = param_inst.grid_param['len_states']
    len_eps_E = param_inst.grid_param['len_eps_E']
    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']

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
    3B. Interpolate
    '''
    interpolant['econforge_interpolant'] = forgegeom_interplant(param_inst, EV)

    B_Vepszr_square = B_Vepszr + K_Vepszr * (1 - K_DEPRECIATION)
    interpolant['interp_EV_k_b']['B_Vepszr_square_max'] = np.max(B_Vepszr_square)
    interpolant['interp_EV_k_b']['B_Vepszr_square_min'] = np.min(B_Vepszr_square)

    interpolant['interp_EV_k_b']['K_Vepszr_square_max'] = np.max(K_Vepszr)
    interpolant['interp_EV_k_b']['K_Vepszr_square_min'] = np.min(K_Vepszr)

    logger.debug('EV:\n%s', EV)

    return interpolant


def func_forgegeom_EV_predict(param_inst, interpolant, b_tp, k_tp):
    """Econ-forge quick interpolation method + my geom transform
    """

    if (interpolant['econforge_interpolant'] is None):
        EV_pred = 0

    else:
        K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']
        b_tp_square = b_tp + k_tp * (1 - K_DEPRECIATION)
        EV_pred = forgegeom_interpolating(param_inst, interpolant,
                                          b_tp_square=b_tp_square, k_tp=k_tp)

    return EV_pred


def forgegeom_interp(param_inst, interpolant,
                     EV, B_Vepszr_square, K_Vepszr,
                     b_tp_square, k_tp,
                     start=0, stop=1, geom_ratio=1.03):
    '''        
    Parameters see two functions below
    '''

    '''
    A. Interpolant
    This is not best way to invoke things because interpolant         
    '''
    interpolant['econforge_interpolant'] = forgegeom_interplant(param_inst, EV)

    interpolant['interp_EV_k_b']['B_Vepszr_square_max'] = np.max(B_Vepszr_square)
    interpolant['interp_EV_k_b']['B_Vepszr_square_min'] = np.min(B_Vepszr_square)

    interpolant['interp_EV_k_b']['K_Vepszr_square_max'] = np.max(K_Vepszr)
    interpolant['interp_EV_k_b']['K_Vepszr_square_min'] = np.min(K_Vepszr)

    '''
    B. Interpolate
    '''
    EV_pred = forgegeom_interpolating(param_inst, interpolant,
                                      b_tp_square=b_tp_square, k_tp=k_tp,
                                      start=start, stop=stop, geom_ratio=geom_ratio)

    return EV_pred


def forgegeom_interplant(param_inst, EV):
    '''
    Get Interpolant, based on assumption that there is a regular equi-size grid
    transform for interpolating surface. 
        
    Parameters
    ----------
    B_Vepszr_square: 1c2d array
        vector saved basis for interpolant
        B_Vepszr_square = B_Vepszr + K_Vepszr*(1-K_DEPRECIATION)
    K_Vepszr: 1c2d array
        vector saved basis for interpolant
        K vector
    b_tp_square: 1c2d array
        vector to get value for using interpolant
        b_tp_square = b_tp + k_tp*(1-K_DEPRECIATION)        
    k_tp: 1c2d array
        vector to get value for using interpolant
        K vector        
    '''
    #         start = 0
    #         stop = 1
    #         geom_ratio = 1.03

    len_k = param_inst.grid_param['len_k_start']
    len_states = param_inst.grid_param['len_states']
    len_b = int(len_states / len_k)

    a = np.array([0, 0])
    b = np.array([len_k - 1, len_b - 1])
    orders = np.array([len_k, len_b])
    values = np.reshape(EV, (len_k, len_b))

    '''
    B. Interpolate
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
    econforge_interpolant = econforge.LinearSpline(a, b, orders, values)

    return econforge_interpolant


def forgegeom_interpolating(param_inst, interpolant,
                            b_tp_square=None, k_tp=None,
                            start=None, stop=None, geom_ratio=None):
    '''
    Interpolating based on interpolant
        
    if b_tp_square is None b_tp_square_geom must not be none, vice versa
    if k_tp_geom is None k_tp must not be none, vice versa
    b_tp_square_geom and k_tp_geom are not None if we pre-save them for re-use
    
    Parameters
    ----------
    B_Vepszr_square: 1c2d array
        vector saved basis for interpolant
        B_Vepszr_square = B_Vepszr + K_Vepszr*(1-K_DEPRECIATION)
    K_Vepszr: 1c2d array
        vector saved basis for interpolant
        K vector
    b_tp_square: 1c2d array
        vector to get value for using interpolant
        b_tp_square = b_tp + k_tp*(1-K_DEPRECIATION)
    k_tp: 1c2d array
        vector to get value for using interpolant
        K vector
    start: float, int
        start geom initial value from genstates
        specify as none if interpolant contains this as a key
    stop: float, int
        end geom initial value from genstates
        specify as none if interpolant contains this as a key
    geom_ratio: float
        geom initial value from genstates from geom_ratio
        specify as none if interpolant contains this as a key        
    '''
    #         start = 0
    #         stop = 1
    #         geom_ratio = 1.03

    if (start is None):
        start = interpolant['interp_EV_k_b']['start']  # = 0
    if (stop is None):
        stop = interpolant['interp_EV_k_b']['stop']  # = 1
    if (geom_ratio is None):
        geom_ratio = interpolant['interp_EV_k_b']['geom_ratio']  # =1.03

    len_k = param_inst.grid_param['len_k_start']
    len_states = param_inst.grid_param['len_states']
    len_b = int(len_states / len_k)

    '''
    C. Translate choices to z's power scale (see above)
        we start with some choice kn:
            kn = a*z^(kn_geom)
        the code below, grid_to_geom finds given kn what is kn_geom
    '''
    # converge b and k choices from value to geom-value power which are equi-spac
    num = len_b
    B_Vepszr_square_max = interpolant['interp_EV_k_b']['B_Vepszr_square_max']
    B_Vepszr_square_min = interpolant['interp_EV_k_b']['B_Vepszr_square_min']
    b_tp_square_geom = geomspace.grid_to_geom_short(np.ravel(b_tp_square),
                                                    B_Vepszr_square_max, B_Vepszr_square_min,
                                                    start, stop, num, geom_ratio, 1)

    num = len_k
    K_Vepszr_square_max = interpolant['interp_EV_k_b']['K_Vepszr_square_max']
    K_Vepszr_square_min = interpolant['interp_EV_k_b']['K_Vepszr_square_min']
    k_tp_geom = geomspace.grid_to_geom_short(np.ravel(k_tp),
                                             K_Vepszr_square_max, K_Vepszr_square_min,
                                             start, stop, num, geom_ratio, 1)

    '''
    D. Interpolate
    '''
    econforge_interpolant = interpolant['econforge_interpolant']

    S = np.column_stack((k_tp_geom, b_tp_square_geom))
    EV_pred = econforge_interpolant(S)
    EV_pred = np.reshape(EV_pred, (np.shape(b_tp_square)))

    return EV_pred
