'''
Created on Apr 14, 2018

@author: fan
'''

import logging
import numpy as np

import modelhh.functions.budget as bdgt
import modelhh.functions.production as prod

logger = logging.getLogger(__name__)


def gen_Y_gen_cash_param(param_inst, b_t, k_t, A, eps=0, shockNegInf=False):
    bdgt_inst = bdgt.BudgetConsumption(param_inst)
    prod_inst = prod.ProductionFunction(param_inst)

    Y_partial, cash_partial = gen_Y_gen_cash(bdgt_inst, prod_inst, b_t, k_t, A, eps, shockNegInf)
    return Y_partial, cash_partial


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
