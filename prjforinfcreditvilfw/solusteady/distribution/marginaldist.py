'''
Created on Apr 30, 2018

@author: fan

Markov Transition Cash only
'''

import logging
from scipy.stats import lognorm
# from scipy.linalg import eig
import numpy as np
import pyfan.stats.markov.transprobcheck as pyfan_stats_transprobcheck

logger = logging.getLogger(__name__)


def marginal_dist_from_conditional(trans_prob, state_count):
    """
    Standard formula for deriving steady state assets distribution.

    on 2020-12-06 20:01, switch from fl_atol_avg_row=1e-08 to fl_atol_avg_row=1e-07
    during fl_atol_avg_row=1e-07 of x run. raised valueerror at 1e-08

    Parameters
    ----------
    trans_prob: 2d numpy array
        each row a current state, each column a future state
        each cell is P(COH_{t+1} | COH{t})
        lower index rows correspond to smaller COH values, higher higher.        
    """

    '''
    Check if the final cell for transitional probability is 1
    this would be an obsorbing high state, very possible given max bound      
    '''

    # if any final 5 values degenerate, final five rows in the last column
    any_large_degenerate = any([np.allclose(cur_trans_prob, 1, rtol=1e-05, atol=1e-08)
                                for cur_trans_prob in trans_prob[:-5:-1, -1]])

    # if any initial 5 values degenerate, first five rows in initial column
    any_small_degenerate = any([np.allclose(cur_trans_prob, 1, rtol=1e-05, atol=1e-08)
                                for cur_trans_prob in trans_prob[0:5, 0]])

    if (any_large_degenerate):
        marginal_dist = np.zeros(trans_prob.shape[1])
        marginal_dist[-1] = 1

    elif (any_small_degenerate):
        marginal_dist = np.zeros(trans_prob.shape[1])
        marginal_dist[0] = 1

    else:

        #         trans_prob_zero_threshold = 5.0e-03
        #         marginal_p_zero_threshold = 1.0e-05
        #         marginal_p_neg_threshold = 5.0e-04
        #
        #         '''
        #         Transform Conditional Distribution so that each row sums up to one
        #         Get rid of small trans_prob values
        #         '''
        #         trans_prob[abs(trans_prob) <= trans_prob_zero_threshold] = 0
        #         trans_prob = trans_prob/np.reshape(np.sum(trans_prob, axis=1),(-1,1))


        bl_ar1_sum_pass, *_ = pyfan_stats_transprobcheck.markov_trans_prob_check(
            trans_prob, fl_atol_per_row=5e-05, fl_atol_avg_row=5e-07)

        if bl_ar1_sum_pass:
            '''Conditional Distribution sum very close to 1'''
            trans_prob = pyfan_stats_transprobcheck.markov_condi_prob2one(trans_prob)

        else:
            message = 'trans_prob row does not sum up to 1'
            bl_ar1_sum_pass, *_ = pyfan_stats_transprobcheck.markov_trans_prob_check(
                trans_prob, fl_atol_per_row=5e-05, fl_atol_avg_row=5e-07)
            logger.warning(message)
            logger.warning('marginal_dist:\n%s', np.sum(trans_prob, axis=1))
            raise ValueError(message)

        '''
        Transition - I
        P = P*T
        0 = P*T - P
        0 = P*(T-1)
        '''

        Q = trans_prob - np.identity(state_count)

        '''
        add all 1 as final column, (because P*1 = 1) 
        '''
        one_col = np.ones((state_count, 1))
        Q = np.column_stack((Q, one_col))

        '''
        b is the LHS 
        b = [0,0,0,...,1]
        '''
        b = np.zeros((1, (state_count + 1)))
        b[0, state_count] = 1

        '''
        solve
        b = P*Q
        b*Q^{T} = P*Q*Q^{T}
        P*Q*Q^{T} = b*Q^{T}
        P = (b*Q^{T})[(Q*Q^{T})^{-1}]
        '''
        Q_t = np.transpose(Q)
        b_QT = np.dot(b, Q_t)
        Q_QT = np.dot(Q, Q_t)
        try:
            inv_Q_QT = np.linalg.inv(Q_QT)
        except:
            print(Q_QT)

        P = np.dot(b_QT, inv_Q_QT)

        #     print(np.transpose(P))
        logger.debug('np.transpose(P):\n%s', np.transpose(P))

        #     fig, ax = plt.subplots(1, 1)
        #     ax.plot(cash_grid_centered, P.ravel(),
        #            'r-', lw=5, alpha=0.6, label='lognorm cdf')

        #     save_file_name ='phase_' + csv_file_name + image_save_suffix
        #     plt.savefig(image_folder + save_file_name, dpi=200, papertype='a4')
        #     plt.clf()
        #     fig.clf()

        marginal_dist = P.ravel()

        #         # Total difference between aggregate probability and 1 should be less than 0.01
        #         if (np.allclose(np.sum(marginal_dist), 1, rtol=0, atol=1e-02)):
        #             pass
        #         else:
        #             message = 'Marginal probability sum 0.01 away from 1'
        #             logger.warning(message)
        #             logger.warning('marginal_dist:\n%s', marginal_dist)
        #             logger.warning('min(marginal_dist):\n%s', min(marginal_dist))
        #             logger.warning('max(marginal_dist):\n%s', max(marginal_dist))
        #             logger.warning('np.sum(marginal_dist):\n%s', np.sum(marginal_dist, axis=1))
        #             raise ValueError(message)
        #
        '''
        2018-07-20 14:28
            We could have proper Conditional Distribution, Approximation Error Small Negative Density
            see evernote:
                https://www.evernote.com/shard/s10/nl/1203171/090f26fd-afa6-4ba8-9158-8b0e577dafa4
            Eliminate here the possibility that there are small negative density due
            to floating point approximation issues
            
            for 1.0e-06, do not need to do further adjustments to reweight
            others, because at most this is tiny total difference, but could reweight
        '''
        #         marginal_dist[abs(marginal_dist) <= marginal_p_zero_threshold] = 0

        '''
        2018-07-20 14:45
            Continue to have problem, some with proper conditional distribution (summing each row to one)
            but larger negative marginal, just correct the negative distribution here
            
            -5.0e-04 = -.0005, 0.05% negative density allowed potentially, will even out
            but why is that even here, very weird? Do not allow for larger, because bug
            need to show through if even bigger, there might be something bigger wrong. 
        '''
        #         marginal_dist[(marginal_dist < 0) & (marginal_dist >= marginal_p_neg_threshold)] = 0

        #         marginal_dist = marginal_dist/np.sum(marginal_dist)

        if (len(marginal_dist[marginal_dist < 0])):

            marginal_dist_2_mat = np.linalg.matrix_power(trans_prob, 1000)
            marginal_dist_2 = marginal_dist_2_mat[0, :]

            if (len(marginal_dist_2[marginal_dist_2 < 0])):
                message = 'some marginal_dist are negative'
                logger.warning(message)
                logger.warning('marginal_dist:\n%s', marginal_dist)
                logger.warning('min(marginal_dist):\n%s', min(marginal_dist))
                raise ValueError(message)

            marginal_dist = marginal_dist_2

    return marginal_dist
