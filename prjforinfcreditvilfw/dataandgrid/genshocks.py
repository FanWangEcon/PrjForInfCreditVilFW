'''
Created on Dec 16, 2017

@author: fan

Several parameters relate to shocks. 

import dataandgrid.genshocks as genshocks
'''

import logging

import numpy as np
from scipy.stats import norm

logger = logging.getLogger(__name__)


def stateSpaceShocks(e_mean, e_sd, e_count,
                     seed=1230, draw_type=0,
                     lower_sd=-3, higher_sd=+3):
    if (seed):
        # these were generated in genBasePoints
        np.random.seed(seed)

    logger.debug('e_mean:%s', e_mean)
    logger.debug('e_sd:%s', e_sd)
    logger.debug('e_count:%s', e_count)
    logger.debug('seed:%s', seed)
    logger.debug('draw_type:%s', draw_type)

    lower_q = norm.cdf(lower_sd)
    higher_q = norm.cdf(higher_sd)

    'randomly drawing and then sorting'
    if (draw_type == 0):
        #         pnorm(-3)=0.0013
        #         pnorm(3) =0.9987
        e_draws = np.random.normal(0, 1, e_count)
        e_draws = np.sort(e_draws)
        e_draws[e_draws < lower_sd] = lower_sd
        e_draws[e_draws > higher_sd] = higher_sd
        e_draws = e_mean + e_sd * e_draws

    'randomly drawing'
    if (draw_type == 1):
        #         + or - 3 SD
        #         e_quantiles = np.linspace(0.0013, 0.9987, e_count)
        #         e_quantiles = np.linspace(lower_q, higher_q, e_count)
        #         e_draws = norm.ppf(e_quantiles, loc=e_mean, scale=e_sd)

        e_quantiles = np.linspace(lower_q, higher_q, e_count)
        e_draws = norm.ppf(e_quantiles, loc=e_mean, scale=e_sd)

        logger.debug('e_quantiles:%s', e_quantiles)

    #         # Addition: 2018-10-25 12:31
    #         # https://www.evernote.com/shard/s10/nl/1203171/18d67b6e-da9f-4808-9dce-211e1aee900e
    #         A_pbreaks = np.linspace(0, 1, e_count+1)
    #         A_pbreaks_mid = (A_pbreaks[1:] + A_pbreaks[:-1])/2
    #         e_draws = norm.ppf(A_pbreaks_mid, loc=e_mean, scale=e_sd)

    #         logger.debug('A_pbreaks_mid:%s', A_pbreaks_mid)

    'randomly drawing and not sorting and cut outliers'
    if (draw_type == 2):
        #         pnorm(-3)=0.0013
        #         pnorm(3) =0.9987
        e_draws = np.random.normal(0, 1, e_count)
        e_draws[e_draws < lower_sd] = lower_sd
        e_draws[e_draws > higher_sd] = higher_sd
        e_draws = e_mean + e_sd * e_draws

    logger.debug('e_draws:%s', e_draws)

    '''
    Return Sequenceis crucial, can not change,
    '''
    return e_draws
