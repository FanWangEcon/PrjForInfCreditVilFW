'''
Created on May 16, 2018

@author: fan
'''

import logging
import numpy as np

import dataandgrid.genshocks as genshocks
import solusteady.distribution.condidist_simu as condisimu

logger = logging.getLogger(__name__)


def aiyagari_fig2_data_probwgted(param_inst,
                                 prb_matrix, btp_matrix, ktp_matrix,
                                 shock_simu_count=5000, simu_seed=123,
                                 lower_sd=-3, higher_sd=+3,
                                 dist_percentiles=None):
    """Conditional Cash Distribution given optimal choices for each j of J
    
    Need to consider probability. 
    
    The strategy here is the following: 
        for each j of J simulate for each current coh M shock_simu_count
        then replace state-specific probability subset of rows. for each j of J
        
        1. cash_partial Matrix zeros: len(btp_opti) by shock_simu_count
        2a. simulate cash_partial for j = 0 
        2b. cash_partial = cash_partial_j0
        3a. simulate cash_partial for j = 1
        3b. prob_idx_j1 [row_ctr/5000 < prob_j1] 
        3b. cash_partial[prob_idx_j1==True] = cash_partial_j1[prob_idx_j1==True]
        4. repeat step 3 until finishes. 
        
        see ProjectSupport.Testing.Numpy.replace_by_index.py
        for testing out the basic idea here. 
    
    Parameters
    ----------
    prb_matrix: 2d array 
        states by len(J), j sequence prb btp ktp same
    btp_matrix: 2d 1col
        states by len(J), j sequence prb btp ktp same
    ktp_matrix: 2d 1col
        states by len(J), j sequence prb btp ktp same
        
    Returns
    ----------
    cash_partial: 2d
        row=len(btp_opti), col=shock_simu_count
    """

    if (dist_percentiles is None):
        dist_percentiles = [0.1, 20, 50, 80, 99.9]

    """
    A. Parameters
    """
    A = param_inst.data_param['A']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']
    choice_set_list = param_inst.model_option['choice_set_list']
    choice_names_use = param_inst.model_option['choice_names_use']
    choice_names_full_use = param_inst.model_option['choice_names_full_use']

    eps = genshocks.stateSpaceShocks(mean_eps, std_eps, shock_simu_count,
                                     seed=simu_seed, draw_type=0, lower_sd=lower_sd, higher_sd=higher_sd)
    eps = np.reshape(eps, (1, -1))

    """
    B. Properly Probability Weighted Distribution
    """
    # see \ProjectSupport\Testing\Numpy\replace_by_index.py
    a_col_ratio = np.linspace(0, 1, shock_simu_count)
    cash_partial = np.zeros(btp_matrix.shape)
    for ctr, choicej in enumerate(choice_set_list):

        '''Get Policies'''
        btp = np.reshape(btp_matrix[:, ctr], (-1, 1))
        ktp = np.reshape(ktp_matrix[:, ctr], (-1, 1))

        if (ctr >= 1):
            prob_weight = np.reshape(np.sum(prb_matrix[:, 0:ctr], axis=1), (-1, 1))
            prob_weight_idx = (prob_weight > a_col_ratio)

        '''Compute Distribution'''
        __, __, __, __, cash_partial_j = \
            condisimu.aiyagari_fig2_data(param_inst, btp, ktp,
                                         shock_simu_count=shock_simu_count,
                                         simu_seed=simu_seed)

        '''Save Results'''
        if (ctr == 0):
            # see \ProjectSupport\Testing\Numpy\replace_by_index.py
            cash_partial = cash_partial_j
        else:
            cash_partial[prob_weight_idx == False] = cash_partial_j[prob_weight_idx == False]

    """
    C. Compute Statistics
    """
    logger.debug('cash_partial.shape:%s', cash_partial.shape)
    cash_partial_percentiles = np.percentile(cash_partial, dist_percentiles, axis=1)
    cash_partial_percentiles = np.transpose(cash_partial_percentiles)
    logger.debug('cash_partial_percentiles.shape:%s', cash_partial_percentiles.shape)

    cashpartial_min = np.min(cash_partial, axis=1)
    logger.debug('cashpartial_min.shape:%s', cashpartial_min.shape)
    cashpartial_max = np.max(cash_partial, axis=1)
    logger.debug('cashpartial_max.shape:%s', cashpartial_max.shape)

    return cash_partial_percentiles, cashpartial_min, cashpartial_max, cash_partial
