'''
Created on May 16, 2018

@author: fan
'''

import logging
import numpy as np

import dataandgrid.genshocks as genshocks
import modelhh.component as component

logger = logging.getLogger(__name__)


def aiyagari_fig2_data(param_inst, btp_opti, ktp_opti,
                       shock_simu_count=5000, simu_seed=123,
                       lower_sd=-3, higher_sd=+3,
                       dist_percentiles=None):
    """Conditional Cash Distribution given optimal choices
    
    Policy function provides optimal choices, so given states today, what is the
    btp and ktp. Given these, simulate, using random shocks the distribution of
    cash on hand next period. 
    
    Moved over from Graphing File initially
    
    Parameters
    ----------
    btp_opti: 2d 1col 
        financial choice
    ktp_opti: 2d 1col
        physical capital choice
        
    Returns
    ----------
    cash_partial: 2d
        row=len(btp_opti), col=shock_simu_count 
    """

    if (dist_percentiles is None):
        dist_percentiles = [0.1, 20, 50, 80, 99.9]

    A = param_inst.data_param['A']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']

    eps = genshocks.stateSpaceShocks(mean_eps, std_eps, shock_simu_count,
                                     seed=simu_seed, draw_type=0, lower_sd=lower_sd, higher_sd=higher_sd)
    eps = np.reshape(eps, (1, -1))

    # cash_tt already there
    __, cash_partial = component.gen_Y_gen_cash_param(
        param_inst,
        b_t=btp_opti, k_t=ktp_opti,
        A=A, eps=eps, shockNegInf=False)

    logger.debug('cash_partial.shape:%s', cash_partial.shape)
    cash_partial_percentiles = np.percentile(cash_partial, dist_percentiles, axis=1)
    cash_partial_percentiles = np.transpose(cash_partial_percentiles)
    logger.debug('cash_partial_percentiles.shape:%s', cash_partial_percentiles.shape)

    cashpartial_min = np.min(cash_partial, axis=1)
    logger.debug('cashpartial_min.shape:%s', cashpartial_min.shape)
    cashpartial_max = np.max(cash_partial, axis=1)
    logger.debug('cashpartial_max.shape:%s', cashpartial_max.shape)

    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']
    compo_certain = btp_opti + ktp_opti * (1 - K_DEPRECIATION)

    return cash_partial_percentiles, cashpartial_min, cashpartial_max, compo_certain, cash_partial
