'''
Created on Apr 14, 2018

@author: fan

Linear Interpolation Splines

Approximate Polynomial Approximation

This will be invoked three times in soluvalue:

1. Given V(DATA=[K,B,A]), find V_Pie
    a. get data_mat
        + data_mat =future_polyquad(DATA, eps=0, return_type='DATAMAT')
    b. first interpolant
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

'''

import logging
import numpy as np
import pyfan.stats.interpolate.interpolate2d as interp2d

import modelhh.component as modelcomponent
# from interpolation.splines import LinearSpline, CubicSpline
# import interpolation.splines as econforge
import modelhh.future.future_forgegeom as forgegeom
import projectsupport.systemsupport as proj_sys_sup

# import dsge.grid.geomspace as dsgegeom

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
        interpolant = {'interp_type': 'griddata',
                       'interp_type_option': {
                           'method': 'linear'
                       },
                       'interp_V_k_cash': {
                           'V': None,
                           'k': None,
                           'cash': None,
                       },
                       'interp_EV_k_b': {
                           'EV': None,
                           'k': None,
                           'b': None,
                       }
                       }

    len_states = param_inst.grid_param['len_states']
    len_eps = param_inst.grid_param['len_eps']
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
    interpolant['interp_V_k_cash']['V'] = EjV
    interpolant['interp_V_k_cash']['k'] = K_V
    interpolant['interp_V_k_cash']['cash'] = cash_partial
    V_eps = interp2d.interp_griddata(cur_u=EjV,
                                     cur_x1=cash_partial, cur_x2=K_V,
                                     new_x1=cash_partial_eps, new_x2=K_Veps)

    proj_sys_sup.debug_panda('EjV,cash_partial,K_V, B_V, eps_V',
                             np.column_stack((EjV, cash_partial, K_V, B_V, eps_V)),
                             subfolder='test_future_griddata', filename='V', export_panda=False)
    proj_sys_sup.debug_panda('V_eps,cash_partial_eps,K_Veps,B_Veps, eps_Veps',
                             np.column_stack((V_eps, cash_partial_eps, K_Veps, B_Veps, eps_Veps)),
                             subfolder='test_future_griddata', filename='V_eps', export_panda=False)
    '''
    3. Average to get EV(K,B,A), integrated over shocks
    '''
    EV = np.mean(np.reshape(V_eps, (len_states, len_eps_E)), axis=1)
    proj_sys_sup.debug_panda('EV,K_Vepszr,B_Vepszr', np.column_stack((EV, K_Vepszr, B_Vepszr)),
                             subfolder='test_future_griddata', filename='EV', export_panda=False)

    logger.debug('EV:\n%s', EV)
    interpolant['interp_EV_k_b']['EV'] = EV
    interpolant['interp_EV_k_b']['k'] = K_Vepszr
    interpolant['interp_EV_k_b']['b'] = B_Vepszr

    return interpolant


def func_griddata_EV_predict(param_inst, interpolant, b_tp, k_tp):
    interp_EV_k_b = interpolant['interp_EV_k_b']
    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']

    if (interp_EV_k_b['EV'] is None):
        EV_pred = 0

    else:

        EV = interp_EV_k_b['EV']
        K_Vepszr = interp_EV_k_b['k']
        B_Vepszr = interp_EV_k_b['b']

        """
        two lines below due to:
        1. K and B are tilted by (1-dep) when grid was generated
        2. to interpolate, uneven grid requires triangulation, even bilinear
        3. bilinear might be more stablshowe, so rotate grids to make them even first
        4. in practice, results seem better, not too muchthough with this transform.
        """
        B_Vepszr_square = B_Vepszr + K_Vepszr * (1 - K_DEPRECIATION)
        b_tp_square = b_tp + k_tp * (1 - K_DEPRECIATION)

        transform_geom_interp = True

        if (transform_geom_interp):
            EV_pred = forgegeom.forgegeom_interp(param_inst, interpolant,
                                                 EV,
                                                 B_Vepszr_square, K_Vepszr,
                                                 b_tp_square, k_tp,
                                                 start=0, stop=1, geom_ratio=1.03)
        else:
            EV_pred = interp2d.interp_griddata(cur_u=EV,
                                               cur_x1=B_Vepszr_square, cur_x2=K_Vepszr,
                                               new_x1=b_tp_square, new_x2=k_tp)

    return EV_pred
