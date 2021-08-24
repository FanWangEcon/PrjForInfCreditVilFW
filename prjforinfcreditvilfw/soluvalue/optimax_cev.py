'''
Similar to :func:`optimax`, however, here no maximization done, assume we already know max index.
This is done when solving for CEV, fixing policy function, iterate until converge.
'''

import logging
import numpy as np

logger = logging.getLogger(__name__)


def opti_value_eachj_cev(ulife, argmax_index, states_dim):
    """Optimal Choices and Value
    Find optimal given optimal index from value matrix. The value matrix is updating
    because we are interating with proportional increase in consumption.
    However, the policy function needs to stay the same. Note this is only necessary
    because exp(a*b) can not be split to exp(a) and exp(b).

    Parameters
    ----------
    ulife: 2D array
        each column one of potentially seven, might might be less, formal informal
        credit market choices
    arg_max_indx: 2D array
        each column one of potentially seven, might might be less, formal informal
        credit market choices, value stores optimal index among continuous choices.
        Solved previously
    states_dim: scalar
        N*M

    Returns
    -------
    util_opti: 2D array
        N by 7 matrix, util just at one choice, the max utility one.
    """

    credit_cates = ulife.shape[1]
    logger.debug('credit_cates:%s', credit_cates)
    logger.debug('states_dim:%s', states_dim)

    util_opti = np.zeros((states_dim, credit_cates))

    for credit_j in range(credit_cates):
        ulife_j = ulife[:, credit_j]
        argmax_index_j = argmax_index[:, credit_j]

        util_opti_j = opti_value_cev(ulife_j, argmax_index_j, states_dim)

        util_opti[:, credit_j] = util_opti_j

    logger.debug('util_opti:\n%s', util_opti)

    return util_opti


def opti_value_cev(utility_lifetime, argmax_index_optimal, states_dim):
    """Optimal Choices and Value
    """
    util_opti = utility_lifetime[np.arange(states_dim), argmax_index_optimal]
    return util_opti
