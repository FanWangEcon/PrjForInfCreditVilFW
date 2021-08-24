'''
Created on Dec 16, 2017

@author: fan

copied over from Function.py previous JMP codes

import dataandgrid.choices.dynamic.minmaxfunc as minmaxfunc
'''

import logging
import numpy as np

import modelhh.functions.constraints as constraints

logger = logging.getLogger(__name__)


def minmax_KB_Informal_Borrow(d=0.1, Y_minCst=5, Bstart=-1, RB=1.1):
    """
    Does not consider collateral constraint for formal borrowing only

     -- (B_min, K_max)
        --    --
            --        -- upper_slope (b_max_upper)
                --            --
       lower_slope  --              -- (B_max, K_mid)
       (b_min_lower)    --          --  
                            --      --
                                --  --
                                   --- (B_max, K_min)
        
    B_min = borrow_B_min
    B_min = borrow_B_min
    
    Parameters
    ----------
    Bstart: minimal borrowing required
        in multinomial choice logit, every choice is feasible,
        so if a choice is chosen, even if it is optimal to borrow 0 from
        that category, need to pay the category fixed cost and minimal
        borrowing or savings.
    """

    logger.debug('Z0. Prep Variables')
    rB = RB - 1

    logger.debug('Z1. Cash on Hand without Fixed Costs')
    Y_minCst = constraints.get_consumption_constraint(Y_minCst, False)

    logger.debug('A. Normal Case, triangle of choices, B_max > B_min, cash >=0')

    logger.debug('A1. Lower Right Generic')
    B_max = Bstart
    K_min = (-Bstart) / (1 - d)

    logger.debug('A2. Upper Left individual specific based on Y_minCst')
    ratB = (1 + rB) / (d + rB)
    B_min_i = - (Y_minCst) * ratB * (1 - d)
    K_max_i = (Y_minCst) * ratB

    logger.debug('B. Special Case, if B_max < B_min (that implices K_Max > K_min\
                     single point top left in choice set\
                         or\
                     signle point at origin')
    B_max_i = np.maximum(B_max, B_min_i)
    K_min_i = np.minimum(K_max_i, K_min)

    return [[[K_min_i, K_max_i],
             [B_min_i, B_max_i]],
            Y_minCst, RB]


def minmax_KB_Borrow(DELTA_DEPRE=0.1, Y_minCst=0, Bstart=0, RB=0, Z=None, RZ=None):
    """
    Does not consider collateral constraint for formal borrowing only

     -- (B_min, K_max)
        --    --
            --        -- upper_slope (b_max_upper)
                --            --
       lower_slope  --              -- (B_max, K_mid)
       (b_min_lower)    --          --  
                            --      --
                                --  --
                                   --- (B_max, K_min)
        
    B_min = borrow_B_min
    B_min = borrow_B_min
    
    Parameters
    ----------
    Bstart: minimal borrowing required
        in multinomial choice logit, every choice is feasible,
        so if a choice is chosen, even if it is optimal to borrow 0 from
        that category, need to pay the category fixed cost and minimal
        borrowing or savings.
    """

    logger.debug('\nDELTA_DEPRE=%s\nBstart=%s\nRB=%s\nZ=%s\nRZ=%s',
                 DELTA_DEPRE, Bstart, RB, Z, RZ)
    logger.debug('Y_minCst:\n%s', Y_minCst)

    logger.debug('0. Prep Variables')
    d = DELTA_DEPRE
    rB = RB - 1
    if (Z is not None):
        rZ = RZ - 1

    logger.debug('A. Cash on Hand without Fixed Costs')
    Y_minCst = constraints.get_consumption_constraint(Y_minCst, False)

    logger.debug('B1. Maximum Borrowing (B_min) Feasible Given Cash on Hand and Rates,')
    ratB = (1 + rB) / (d + rB)
    borrow_B_min = - (Y_minCst) * ratB * (1 - d)

    logger.debug('B2. Minimal Borrowing (B_max) required')
    borrow_B_max = Bstart
    # borrow_B_max = -float(abs(Bstart))
    if (Z is not None):
        borrow_B_min += borrow_B_min + (-Z * ratB * ((d + rZ) / (1 + rZ)))

    logger.debug('B3. if B_max < B_min, set B_max = B_min, single dot choice point')
    # if Bstart = -1, but Y_minCst = 0, then max borrow < min borrow
    borrow_B_max = np.maximum(borrow_B_max, borrow_B_min)

    logger.debug('C1. Minimum K (K_min) Feasible Given Cash on Hand and Rates')
    # k_min
    #    = (-Bstart) / (1 - d)
    #        for having enough capital to repay minimal borrowing required
    kapitalnext_min = (-Bstart) / (1 - d)

    logger.debug('C2. Maximum K (K_max) Feasible Given Cash on Hand and Rates')
    kapitalnext_max = (Y_minCst) * ratB
    if (Z is not None):
        try:
            kapitalnext_min += np.maximum((-Z) / (1 - d), 0)
        except:
            'If formula, k*gamma'
            kapitalnext_min += (-Z) / (1 - d)

        kapitalnext_max += -(Z * (rB - rZ)) / ((1 + rZ) * (d + rB))

    logger.debug('B3. Minimal Borrowing (B_max) required')
    # if Bstart = -1, then kapitalnext_min = 1/(1-d), but with Y_minCst = 0, kap_max = 0, so then max < min
    # in this case, even though there is minimal borrowing requirement, not valid because can't pay for it'
    kapitalnext_min = np.minimum(kapitalnext_max, kapitalnext_min)

    'Z<0 means there is minimum borrowing, '
    'If z > 0, has minimum savings, min will be 0'

    if (Z is not None):
        Y_minCst = Y_minCst + (-Z / (1 + rZ))

    #     logger.debug('RB:%s',RB)
    #     logger.debug('cur_minmax:\n%s',
    #                  np.concatenate((kapitalnext_min, kapitalnext_max,
    #                                  borrow_B_min, borrow_B_max,
    #                                  Y_minCst)))

    if (np.isscalar(kapitalnext_min)):
        kapitalnext_min = np.zeros(kapitalnext_max.shape) + kapitalnext_min

    #     The algorithm above for joint formal + informal borrow is incorrect
    #     when Y_minCst = 0. If Y_minCst for this category, no resource, can not borrow_B_max
    #     can not have K. and when borrowing, can not have positive number.

    if (np.isscalar(Y_minCst)):
        if (borrow_B_min > 0):
            kapitalnext_min = 0
            kapitalnext_max = 0
            borrow_B_min = -0
            borrow_B_max = -0
    else:
        borrow_B_min_pos = (borrow_B_min > 0)
        kapitalnext_min[borrow_B_min_pos] = 0
        kapitalnext_max[borrow_B_min_pos] = 0
        borrow_B_min[borrow_B_min_pos] = -0
        borrow_B_max[borrow_B_min_pos] = -0

    return [[[kapitalnext_min, kapitalnext_max],
             [borrow_B_min, borrow_B_max]],
            Y_minCst, RB]


def minmax_KB_Save(DELTA_DEPRE=0.1, Y_minCst=0, Bstart=0, RB=0, Z=None, RZ=None):
    """
    Parameters
    ----------
    Bstart: minimal Savings required
        in multinomial choice logit, every choice is feasible,
        so if a choice is chosen, even if it is optimal to borrow 0 from
        that category, need to pay the category fixed cost and minimal
        borrowing or savings.    
    """

    assume_informal_lending_full_repay_always = True

    d = DELTA_DEPRE
    Y_minCst = constraints.get_consumption_constraint(Y_minCst, False)

    rB = RB - 1
    if (Z is not None):
        rZ = RZ - 1

    # Savings min and max determined first, save_B_min < save_B_max
    save_B_min = Bstart
    save_B_max = (Y_minCst) * (1 + rB)
    if (Z is not None):

        # Y_minCst: coh minus fixed costs
        # Y_minCst - Z / (1 + rZ):
        #     coh minus fixed costs + how much was borrowed from formal sources to add to coh
        # Y_minCst - Z / (1 + rZ) + Z/(1 - d):  
        #     coh minus fixed costs + how much was borrowed from formal sources to add to coh
        #     + minimal commitment towards k to enable repayment in b next period.
        if (assume_informal_lending_full_repay_always is True):
            # Assuming that informal lending will be fully repaid and can cover formal loans
            save_B_max = (Y_minCst - Z / (1 + rZ)) * (1 + rB)
        else:
            # considering that need to have physical capital for formal loan repayment
            save_B_max = (Y_minCst - Z / (1 + rZ) + Z / (1 - d)) * (1 + rB)

    save_B_min = np.minimum(save_B_max, save_B_min)

    # Kapital
    kapitalnext_min = 0
    kapitalnext_max = Y_minCst - save_B_min / (1 + rB)
    if (Z is not None):

        if (assume_informal_lending_full_repay_always is True):
            pass
        else:
            # have to have physical capital for loan repayment
            kapitalnext_min = (-Z) / (1 - d)

        kapitalnext_max = (Y_minCst - Z / (1 + rZ)) - save_B_min / (1 + rB)

    """
    The slope  of the savings triangle should be the savings rate or rather 1/（1+rB)
    
    see the below equation, the problem is with Z/(1-d), when we add to min capital
    level Z/(1-d) that is pushing the whole triangle up, B_max save need to go up as well. 
            
    [Y_minCst -  Bstart / (1 + rB)]
    /
    [(Y_minCst) * (1 + rB)] - Bstart 
        
        
    [Y_minCst - Z/(1 + rZ) - save_B_min/(1 + rB) + (Z)/(1 - d)] 
    /
    [(Y_minCst - Z/(1 + rZ)) * (1 + rB) - Bstart] 
    """

    if (Z is not None):
        Y_minCst = Y_minCst + (-Z / (1 + rZ))

    if (np.isscalar(kapitalnext_min)):
        kapitalnext_min = np.zeros(kapitalnext_max.shape) + kapitalnext_min

    return [[[kapitalnext_min, kapitalnext_max],
             [save_B_min, save_B_max]],
            Y_minCst, RB]


def minmax_KB_save_fbis_a(K_min_br, Y_minCst, RB):
    """
    Solve for alpha + beta*x = y and y = lambda, find x
    
    Parameters
    ----------
    K_min_br: array
        lambda = K_min_br,     
    Y_minCst: array
        alpha = Y_minCst
    RB: scalar
        beta = -1/RB, RB is informal borrowing rate    
    """

    save_B_max_wthKminbr = (K_min_br - Y_minCst) / (-1 / RB)

    return save_B_max_wthKminbr


def minmax_KB_save_fbis_b(K_vec, Y_minCst, RB):
    """
    Solve for b: k = alpha + beta*b
    
    Given K vector, what is the upper slope current K's corresponding B?
    
    Parameters
    ----------
    K_vec: array
        K_vec = k     
    Y_minCst: array
        alpha = Y_minCst
    RB: scalar
        beta = -1/RB, RB is informal borrowing rate        
    """

    borr_B_max_upper = (K_vec - Y_minCst) / (-1 / RB)

    return borr_B_max_upper
