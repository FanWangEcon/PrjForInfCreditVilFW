'''
Created on Dec 16, 2017

@author: fan

copied over from Support/ArraySupport.py previous JMP codes
'''
import logging
import numpy as np

logger = logging.getLogger(__name__)


def gentics_KB_count(len_choices, addExtra=0):
    """
    I use gentics algorithm below to generate K and B choice tics, want to grab
    tic count unique for K and B out.
    Just trying to understant what is happening in code below.

    Same code exists under Support.dsge.grid.twoctsdimfactor.py
    """

    # different tics for each continuous choices: 1, number of continuous choices

    choicespace_ele_len_l2 = len_choices - addExtra
    choicespace_ele_len_sqrt = np.sqrt(choicespace_ele_len_l2)
    choicespace_ele_len_sqrt_int = int(choicespace_ele_len_sqrt)
    B_choice_discretePoints_start = choicespace_ele_len_sqrt_int
    logger.debug('choicespace_ele_len_sqrt:%s', choicespace_ele_len_sqrt)
    logger.debug('choicespace_ele_len_sqrt_int:%s', choicespace_ele_len_sqrt_int)
    logger.debug('B_choice_discretePoints_start:%s', B_choice_discretePoints_start)
    remainder_cur = 1

    while (remainder_cur != 0):
        B_choice_discretePoints = B_choice_discretePoints_start
        K_choice_discretePoints = choicespace_ele_len_l2 / B_choice_discretePoints

        remainder_cur = choicespace_ele_len_l2 % B_choice_discretePoints
        if (remainder_cur == 0):
            break
        else:
            B_choice_discretePoints_start = B_choice_discretePoints_start - 1

        logger.debug('len_choices:%s', len_choices)
        logger.debug('B_choice_discretePoints_start:%s', B_choice_discretePoints_start)
        logger.debug('K_choice_discretePoints:%s', K_choice_discretePoints)
        logger.debug('remainder_cur:%s', remainder_cur)

    B_choice_discretePoints = int(B_choice_discretePoints)
    K_choice_discretePoints = int(K_choice_discretePoints)

    logger.debug('B_choice_discretePoints:%s', B_choice_discretePoints)
    logger.debug('K_choice_discretePoints:%s', K_choice_discretePoints)

    return K_choice_discretePoints, B_choice_discretePoints


def gentics(len_states, len_shocks, len_choices, cont_choice_count=2,
            k_choice_min=0, k_choice_max=1,
            b_choice_min=0, b_choice_max=1):
    """
    Parameters could be larger or smaller for VFI or not VFI.

    Parameters
    ----------
    len_states: int
        number of times to duplicate choice grid (downwards)
    cont_choice_count: int
        old parameter from when coding for cases with no continuous variables

    """
    addExtra = 0
    # different tics for each continuous choices: 1, number of continuous choices
    K_choice_discretePoints, B_choice_discretePoints = gentics_KB_count(len_choices, addExtra)

    choicegrid_tics_mat = np.zeros((len_states * len_shocks * len_choices,
                                    cont_choice_count))

    B_choice_discretePoints = int(B_choice_discretePoints)
    K_choice_discretePoints = int(K_choice_discretePoints)

    logger.debug('B_choice_discretePoints:%s', B_choice_discretePoints)
    logger.debug('K_choice_discretePoints:%s', K_choice_discretePoints)
    logger.debug('choicegrid_tics_mat shape :%s', np.shape(choicegrid_tics_mat))

    # =======================================================================
    # for cur_cts_choice in np.arange(0,cont_choice_count):
    #     cur_tic = (np.arange(0,len_choices,1,dtype='d')/(len_choices-1))
    #     np.random.seed(seed=(100*cur_cts_choice+10))
    #     np.random.shuffle(cur_tic)
    #     cur_tic[0] = 0
    #     cur_tic[len(cur_tic)-1] = 1
    #     choicegrid_tics_out = np.tile(cur_tic,statespace_ele_len*shockspace_ele_len)
    #     choicegrid_tics_mat[:,cur_cts_choice] = choicegrid_tics_out
    # =======================================================================

    """
    Evenly Spanned Choice Grid
    assume there are two choice variables
    1, first choice variable tile
    2, second repeat
    something like that
    """

    # addExtra = 2

    'uniform grid for kprime, few points'
    # unif1 = np.linspace(0,1,K_choice_discretePoints)
    K_choice_discretePoints += addExtra
    logger.debug('K_choice_discretePoints:%s', K_choice_discretePoints)
    unif1 = (np.arange(0,
                       K_choice_discretePoints,
                       1,
                       dtype='d') / (K_choice_discretePoints - 1))
    # unif1 = unif1[1:(len(unif1)-1)]
    unif1 = k_choice_min + (k_choice_max - k_choice_min) * unif1
    unif1 = np.repeat(unif1, B_choice_discretePoints, axis=0)
    # =======================================================================
    # unif1 = np.append(unif1, 0)
    # unif1 = np.append(unif1, 1)
    # =======================================================================

    'bprime grid'
    # unif2 = np.linspace(0,1,B_choice_discretePoints)
    B_choice_discretePoints += addExtra
    logger.debug('B_choice_discretePoints:%s', B_choice_discretePoints)
    unif2 = (np.arange(0,
                       B_choice_discretePoints,
                       1,
                       dtype='d') / (B_choice_discretePoints - 1))
    # unif2 = unif2[1:(len(unif2)-1)]
    unif2 = b_choice_min + (b_choice_max - b_choice_min) * unif2
    unif2 = np.tile(unif2, (K_choice_discretePoints, 1))
    unif2 = np.ravel(unif2)
    # =======================================================================
    # unif2 = np.append(unif2, 0)
    # unif2 = np.append(unif2, 1)
    # =======================================================================

    'Extend'
    unif1 = np.tile(unif1, len_states * len_shocks)
    unif2 = np.tile(unif2, len_states * len_shocks)

    choicegrid_tics_mat[:, 0] = unif1
    choicegrid_tics_mat[:, 1] = unif2

    return choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints
