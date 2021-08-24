'''
Created on Dec 7, 2017

@author: fan

Approximate Polynomial Approximation

This will be invoked three times in soluvalue:

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

'''

import logging
import numpy as np
import statsmodels.api as sm

logger = logging.getLogger(__name__)


def gen_Y_gen_cash(bdgt_inst, prod_inst, b_t, k_t, A, eps=0, shockNegInf=False):
    logger.debug(['shape(b_t)', np.shape(b_t)])
    logger.debug(['shape(k_t)', np.shape(k_t)])
    logger.debug(['shape(A)', np.shape(A)])
    logger.debug(['shape(eps)', np.shape(eps)])

    '''
    A1. Next Period Partial Income (shock = 0)
    '''
    Y_partial = prod_inst.cobb_douglas_nolabor(eps, A, k_t, alphaed=False)
    logger.debug(['shape(Y_partial)', np.shape(Y_partial)])

    '''
    A2. cash_partial next period
    '''
    cash_partial = bdgt_inst.cash(Y_partial, k_t, b_t)
    logger.debug(['shape(cash_partial)', np.shape(cash_partial)])

    try:
        logger.debug('b_t, k_t, eps, Y_partial, cash_partial:\n%s',
                     np.column_stack((b_t, k_t, eps, Y_partial, cash_partial)))
    except:
        logger.debug('eps:\n%s', np.transpose(eps))
        logger.debug('b_t:\n%s', np.transpose(b_t))
        logger.debug('k_t, Y_partial, cash_partial:\n%s',
                     np.column_stack((k_t, Y_partial, cash_partial)))

    return Y_partial, cash_partial


def func_polyquad_V(bdgt_inst, prod_inst, interpolant,
                    b_t, k_t, A, eps,
                    shockNegInf=False,
                    return_type='', approx_type=''):
    """
    We need to integrate over V, Hence, the state here is Y and K, Y the revenue 
    from household production function so that we can add shocks to this directly
    and predict values at various shock values
        
    Parameters
    ----------
    return_type: string
        'DATAMAT' or 'PREDICT'
    approx_type: string
        some string about type of approximation
    """

    if (approx_type == 'V_ONE'):
        Y_partial, cash_partial = \
            gen_Y_gen_cash(bdgt_inst, prod_inst, b_t, k_t, A, eps, shockNegInf=False)
        const = np.zeros((cash_partial.shape)) + 1
        data_mat = np.column_stack((const, cash_partial, cash_partial ** 2, k_t))

    if (return_type == 'DATAMAT'):
        return data_mat

    if (return_type == 'PREDICT'):
        interp_coef = interpolant['V_coef']
        if (interp_coef is None):
            predict = 0
        else:
            predict = np.transpose(data_mat.dot(interp_coef))
            logger.debug('shape(predict):%s', np.shape(predict))
        return predict


def func_polyquad_EV_datamat(interpolant, b_t, k_t, A, approx_type=''):
    """
    Evaluateat EV, for efuture evaluation when making choices, as well as OLS
    
    Parameters
    ----------
    return_type: string
        'DATAMAT' or 'PREDICT'
    approx_type: string
        some string about type of approximation
    """

    if (approx_type == 'EV_ONE'):
        const = np.zeros((b_t.shape)) + 1
        data_mat = np.column_stack((const,
                                    b_t, b_t ** 2,
                                    k_t))

    if (approx_type == 'EV_TWO'):
        # Third Degree Polynomial Basis
        const = np.zeros((b_t.shape)) + 1
        data_mat = np.column_stack((const,
                                    b_t, b_t ** 2,
                                    k_t, k_t ** 2,
                                    b_t * k_t))
    if (approx_type == 'EV_TWO'):
        # Third Degree Polynomial Basis
        const = np.zeros((b_t.shape)) + 1
        data_mat = np.column_stack((const,
                                    b_t, b_t ** 2,
                                    k_t, k_t ** 2,
                                    b_t * k_t))
    if (approx_type == 'EV_THREE'):
        # Third Degree Polynomial Basis
        const = np.zeros((b_t.shape)) + 1
        data_mat = np.column_stack((
            const, b_t, b_t ** 2, b_t ** 3, b_t ** 4,
            k_t, k_t * b_t, k_t * (b_t ** 2), k_t * (b_t ** 3),
            k_t ** 2, (k_t ** 2) * b_t, (k_t ** 2) * (b_t ** 2),
            k_t ** 3, (k_t ** 3) * b_t,
            k_t ** 4))

    return data_mat


def func_polyquad_EV_predict(interpolant, b_t, k_t, A, approx_type=''):
    """
    Explicitly write out equation because b_t k_t come in matrix, don't want to
    deal with reshaping
    """

    interp_coef = interpolant['EV_coef']
    if (interp_coef is None):
        EV = 0
    else:
        if (approx_type == 'EV_ONE'):
            EV = interp_coef[0] + \
                 b_t * interp_coef[1] + \
                 (b_t ** 2) * interp_coef[2] + \
                 k_t * interp_coef[3]

        if (approx_type == 'EV_TWO'):
            # Third Degree Polynomial Basis
            EV = (interp_coef[0] + \
                  b_t * interp_coef[1] + \
                  (b_t ** 2) * interp_coef[2] + \
                  k_t * interp_coef[3] + \
                  (k_t ** 2) * interp_coef[4] + \
                  b_t * k_t * interp_coef[5])

        if (approx_type == 'EV_THREE'):
            # Third Degree Polynomial Basis
            EV = (interp_coef[0] + \
                  b_t * interp_coef[1] + \
                  (b_t ** 2) * interp_coef[2] + \
                  k_t * interp_coef[3] + \
                  (k_t ** 2) * interp_coef[4] + \
                  b_t * k_t * interp_coef[5])

    return EV


def get_interpolant(interpolant,
                    bdgt_inst, prod_inst, param_inst,
                    EjV,
                    B_V, K_V, A_V, eps_V,
                    B_Veps, K_Veps, A_Veps, eps_Veps,
                    B_Vepszr=None, K_Vepszr=None, A_Vepszr=None, eps_Vepszr=None):
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
        interpolant = {'interp_type': ['polyquad', 'V_ONE', 'EV_ONE'],
                       'V_coef': None, 'EV_coef': None}

    len_states = param_inst.grid_param['len_states']
    len_eps = param_inst.grid_param['len_eps']
    len_eps_E = param_inst.grid_param['len_eps_E']

    logger.debug(['len_states:', len_states])
    logger.debug(['len_eps_E:', len_eps_E])

    '''
    0. Approximation Type
    '''
    V_type = interpolant['interp_type'][1]
    EV_type = interpolant['interp_type'][2]

    '''
    1. Given V(DATA=[K,B,A]), find V_Pie
    '''
    data_mat = func_polyquad_V(bdgt_inst, prod_inst, interpolant,
                               b_t=B_V, k_t=K_V, A=A_V, eps=eps_V,
                               shockNegInf=False,
                               return_type='DATAMAT', approx_type=V_type)
    logger.info('EjV + V(DATA=[K,B,A]) data_mat shape %s', np.shape(np.column_stack((EjV, data_mat))))
    logger.debug('data_mat:\n%s', np.column_stack((EjV, data_mat)))

    model = sm.OLS(EjV, data_mat)
    results = model.fit()
    logger.info('OLS results V(K,B):\n%s', results.summary())
    interpolant['V_coef'] = (results.params).tolist()
    V_pie_t = results.tvalues

    '''
    2. Given V_pie, solve EV(K,B,A), integrated over shocks
    '''
    V_eps = func_polyquad_V(bdgt_inst, prod_inst, interpolant,
                            b_t=B_Veps, k_t=K_Veps, A=A_Veps, eps=eps_Veps,
                            shockNegInf=False,
                            return_type='PREDICT', approx_type=V_type)
    logger.info('np.shape(V_eps): %s', np.shape(V_eps))
    logger.debug('V_eps reshape:\n%s', np.reshape(V_eps, (len_states, len_eps_E)))

    EV = np.mean(np.reshape(V_eps, (len_states, len_eps_E)), axis=1)
    logger.debug('EV:\n%s', EV)

    if (B_Vepszr is None):
        data_mat_epszr = data_mat
    else:
        data_mat_epszr = func_polyquad_EV_datamat(interpolant,
                                                  b_t=B_Vepszr, k_t=K_Vepszr,
                                                  A=A_Vepszr,
                                                  approx_type=EV_type)
    logger.info('data_mat_epszr shape %s', np.shape(data_mat_epszr))
    logger.debug('data_mat_epszr:\n%s', data_mat_epszr)

    #     exp_EV = np.exp(EV)
    model = sm.OLS(EV, data_mat_epszr)
    results = model.fit()
    logger.info('OLS results exp_EV(K,B):\n%s', results.summary())
    interpolant['EV_coef'] = (results.params).tolist()
    EV_pie_t = results.tvalues

    return interpolant
