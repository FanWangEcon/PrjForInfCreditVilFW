'''
Created on Dec 12, 2017

@author: fan
'''
import logging

import numpy as np

logger = logging.getLogger(__name__)


def opti_value_eachj(ulife, states_dim, choices_dim):
    """Optimal Choices and Value
    Evaluate utility at all choices/states for for all 7 categories, ulife
    collects these in NxM by 7 Matrix, where N is state count, M is choice count 
    
    Parameters
    ----------
    ulife: 2D array        
        each column one of potentially seven, might might be less, formal informal
        credit market choices
    states_dim: scalar
        N*M
    choices_dim: scalar
        7
        
    Returns
    -------
    util_opti: 2D array
        N by 7 matrix, util just at one choice, the max utility one.
    argmax_index: 2D array
        N by 7 matrix, index of optimal choices in terms of NxM elements
            
    """

    credit_cates = ulife.shape[1]
    logger.debug('credit_cates:%s', credit_cates)
    logger.debug('states_dim:%s', states_dim)

    util_opti = np.zeros((states_dim, credit_cates))
    argmax_index = np.zeros((states_dim, credit_cates), dtype=int)

    for credit_j in range(credit_cates):
        ulife_j = ulife[:, credit_j]
        util_opti_j, argmax_index_j = opti_value(ulife_j, states_dim, choices_dim)

        util_opti[:, credit_j] = util_opti_j
        argmax_index[:, credit_j] = argmax_index_j

    logger.debug('util_opti:\n%s', util_opti)
    logger.debug('argmax_index:\n%s', argmax_index)

    return util_opti, argmax_index


def opti_value(utility_lifetime, states_dim, choices_dim):
    """Optimal Choices and Value
    """
    argmax_index = np.nanargmax(np.reshape(utility_lifetime, \
                                           (states_dim, choices_dim)), axis=1)
    #     argmax_index = np.argmax(np.reshape(utility_lifetime, \
    #                       (states_dim, choices_dim)), axis=1)
    util_opti = utility_lifetime[np.arange(states_dim), argmax_index]
    return util_opti, argmax_index


def opti_choices_givenargmax(argmax_index, choice_set_mat, states_dim):
    """Optimal Choices and Value
    Evaluate utility at all choices/states for for all 7 categories, ulife
    collects these in NxM by 7 Matrix, where N is state count, M is choice count 
    
    Parameters
    ----------
    ulife: 2D array        
        each column one of potentially seven, might might be less, formal informal
        credit market choices
    states_dim: scalar
        N*M
    choices_dim: scalar
        7
        
    Returns
    -------
    util_opti: 2D array
        N by 7 matrix, util just at one choice, the max utility one.
    argmax_index: 2D array
        N by 7 matrix, index of optimal choices in terms of NxM elements
            
    """

    credit_cates = choice_set_mat.shape[1]
    logger.debug('credit_cates:%s', credit_cates)
    logger.debug('states_dim:%s', states_dim)

    choice_opti = np.zeros((states_dim, credit_cates))

    for credit_j in range(credit_cates):
        argmax_index_j = argmax_index[:, credit_j]
        choice_set_j = choice_set_mat[:, credit_j]

        choice_set_opti_j = choice_set_j[np.arange(states_dim), argmax_index_j]
        choice_opti[:, credit_j] = choice_set_opti_j

    return choice_opti


def max_value_overJ_drop8(util_opti_eachj, choice_set_list):
    """
    ignore choice category 8 (formal informal borrow, but informal borrow only at minimal level, cts formal borr)
    8 is only needed for probabilistic world, not for deterministic
    """
    if (7 in choice_set_list):
        return np.delete(util_opti_eachj, choice_set_list.index(7), axis=1)
    else:
        return util_opti_eachj


def max_value_overJ(util_opti_eachj, choice_set_list):
    """
    Ignore probability, just max of possible choices.
    """

    util_opti_eachj = max_value_overJ_drop8(util_opti_eachj, choice_set_list)
    J_opti_each_state = np.argmax(util_opti_eachj, axis=1)

    return J_opti_each_state


def max_choice_overJ_givenargmax(J_opti_each_state, choice_opti_eachj, choice_set_list, states_dim):
    """
    Ignore probability, just max of possible choices.
    """

    choice_opti_eachj = max_value_overJ_drop8(choice_opti_eachj, choice_set_list)
    J_opti_each_state = choice_opti_eachj[np.arange(states_dim), J_opti_each_state]

    return J_opti_each_state
