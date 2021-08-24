'''
Created on May 16, 2018

@author: fan
'''

import logging
import numpy as np
import pandas as pd
import scipy.interpolate as interpolate
from scipy.stats import lognorm

import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup
import solusteady.distribution.marginaldist as marginaldist

logger = logging.getLogger(__name__)


def semi_analytical_marginal(param_inst,
                             cash_tt, ktp_opti, btp_opti, consumption_opti,
                             each_j_prob=None,
                             export_panda=False,
                             trans_prob_only=False,
                             cur_col_prefix=''):
    """
    Given Model Solution (optimal choices on states), solve for steady state
    asset distribution analytically.
    
    Max of J
    
    Parameters
    ----------
    
    Returns
    -------
    trans_prob: 2d array
        each row current state, each column future state
        conditional distribution
    """

    '''
    Step 1: find bound
    '''
    cash_min = param_inst.grid_param['min_steady_coh']
    cash_max = param_inst.grid_param['max_steady_coh']
    markov_points = param_inst.grid_param['markov_points']

    '''
    Step 2: Generate Grid given bound
    '''
    grid_span = (cash_max - cash_min) / markov_points
    grid_span_half = grid_span / 2
    cash_grid_centered = np.linspace(cash_min + grid_span_half,
                                     cash_max + grid_span_half, markov_points, endpoint=False)
    cash_grid_rightcdf = np.linspace(cash_min, cash_max, markov_points + 1, endpoint=True)

    '''
    Step 3: K' and B' at cash_grid centered
    '''
    ks = interpolate.interp1d(np.ravel(cash_tt), np.ravel(ktp_opti))
    bs = interpolate.interp1d(np.ravel(cash_tt), np.ravel(btp_opti))
    cs = interpolate.interp1d(np.ravel(cash_tt), np.ravel(consumption_opti))
    ktp_opti_grid = ks(cash_grid_centered)
    btp_opti_grid = bs(cash_grid_centered)
    consumption_opti_grid = cs(cash_grid_centered)

    if (each_j_prob is not None):
        probs = interpolate.interp1d(np.ravel(cash_tt), np.ravel(each_j_prob))
        probJ_opti_grid = probs(cash_grid_centered)

    '''
    Step 4: Next Period
    '''

    ''' 4a: Invoke Model '''
    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']
    alpha_k = param_inst.esti_param['alpha_k']
    A = param_inst.data_param['A']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']

    ''' 4b: Construct Probability'''
    compo_certain = btp_opti_grid + ktp_opti_grid * (1 - K_DEPRECIATION)
    '''This is now mean-preserving'''
    compo_Y_scale = np.exp(A + mean_eps) * ((ktp_opti_grid + 0.0001) ** alpha_k)
    compo_Y_s = std_eps

    ''' 4c: Construct CDF'''
    cash_diff_grid = np.transpose(cash_grid_rightcdf - np.reshape(compo_certain, (-1, 1)))
    cash_future_cdf = lognorm.cdf(cash_diff_grid, s=compo_Y_s, scale=compo_Y_scale)
    cash_future_cdf[-1, :] = 1

    ''' 4d: CDF gaps'''
    cash_future_cdf_gap = np.transpose(np.diff(cash_future_cdf, n=1, axis=0))
    # cash_future_cdf_gap[500,:]
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=1000)
    logger.debug('cash_future_cdf_gap:\n%s', cash_future_cdf_gap)

    '''
    5. Steady State Probability
    '''
    trans_prob = cash_future_cdf_gap
    logger.debug('np.sum(trans_prob, axis=1):\n%s', np.sum(trans_prob, axis=1))

    '''
    6. Get Rid of tiny values which lead to each row possibly not summing up 
    exactly to 1
    '''
    #
    state_count = trans_prob.shape[0]
    #     trans_prob_2 = trans_prob/np.sum(trans_prob, axis=1)
    marginal_dist = marginaldist.marginal_dist_from_conditional(trans_prob, state_count)
    discrete_cash = cash_grid_centered

    '''
    Save Results: column names and store matrix
    '''
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()

    steady_var_suffixes = [steady_var_suffixes_dict['cash_grid_centered'],
                           steady_var_suffixes_dict['marginal_dist'],
                           steady_var_suffixes_dict['btp_opti_grid'],
                           steady_var_suffixes_dict['ktp_opti_grid'],
                           steady_var_suffixes_dict['consumption_opti_grid']]

    varnames_list = [cur_col_prefix + strn for strn in steady_var_suffixes]
    varnames = ",".join(map(str, varnames_list))

    varmat = np.column_stack((np.ravel(cash_grid_centered), np.ravel(marginal_dist),
                              np.ravel(btp_opti_grid), np.ravel(ktp_opti_grid),
                              np.ravel(consumption_opti_grid)))
    simu_output_pd = proj_sys_sup.debug_panda(varnames, varmat,
                                              export_panda=export_panda, log=True)

    if (each_j_prob is not None):
        simu_output_pd[cur_col_prefix +
                       steady_var_suffixes_dict['probJ_opti_grid']] = \
            pd.Series(probJ_opti_grid, index=simu_output_pd.index)

    return simu_output_pd, trans_prob
