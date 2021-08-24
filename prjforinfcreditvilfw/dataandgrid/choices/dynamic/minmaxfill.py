'''
Created on Dec 31, 2017

@author: fan

import dataandgrid.choices.dynamic.minmaxfill as minmaxfill
'''
import logging

import numpy as np

logger = logging.getLogger(__name__)


def minmax_fill_borrow_triangle(
        K_min, K_max, K_tics,
        B_min, B_max, B_tics,
        upper_slope, B_bound=False,
        K_interp_range=False, return_all=False):
    """
    
    see evernote minmaxfill.py for more detailed graph:
        https://www.evernote.com/shard/s10/nl/1203171/0470fc0c-7c6b-4eab-96ad-abea7789bce2        
    
    two points, one slope
    
    lower_slope as well as K_mid are endogenous. 
        
     -- (B_min, K_max)
        --    --
            --        -- upper_slope (b_max_upper)
                --            --
       lower_slope  --              -- (B_max, K_mid)
       (b_min_lower)    --          --  
                            --      --
                                --  --
                                   --- (B_max, K_min)
    
    Parameters
    ----------
    B_bound:
        B_bound >= B_max
    lower_slope:
        not a parameter, calculcated based on K B min and max
        lower_slope must be steeper than upper_slope
        but code here does not enforce this
        so input parameter must enforce this
    return_all: boolean
        created for use by formal borrow informal lend category only
        
    """

    '''
    A: K_vec
    '''
    if (B_bound is False):
        K_max_use = K_max
    else:
        #         if ( B_bound > B_min ):
        #             # k_bound_high
        #             K_max_use = K_max + (B_bound-B_min)*upper_slope
        # #             logger.debug('B_min: %s', B_min)
        # #             logger.debug('B_bound: %s', B_bound)
        # #             logger.debug('(B_bound-B_min)*upper_slope: %s', (B_bound-B_min)*upper_slope)
        # #             logger.debug('K_max_use: %s', K_max_use)
        #         else:
        #             K_max_use = K_max
        #
        #         logger.debug('K_max_use: %s', K_max_use)

        # This happens when invoked by gengrids.py
        B_bound_greater_idx = np.argwhere(B_bound > B_min)

        #         logger.debug('B_bound: %s', B_bound)
        #         logger.debug('B_min: %s', B_min)
        #         logger.debug('B_bound_greater_idx: %s', B_bound_greater_idx)
        #         logger.debug('K_max: %s', K_max)

        K_max_use = np.copy(K_max)
        # upper_slope = 1/Rb, just a number, common across cash levels 

        logger.debug('After adjustments to formal borrow bound, np.transpose(K_max_use):\n%s',
                     np.transpose(K_max_use))

        if (isinstance(K_max, (list, tuple, np.ndarray))):
            K_max_use[B_bound_greater_idx] = K_max[B_bound_greater_idx] + (
                    B_bound[B_bound_greater_idx] - B_min[B_bound_greater_idx]) * upper_slope
        else:
            if (B_bound > B_min):
                K_max_use = K_max + (B_bound - B_min) * upper_slope
            else:
                pass

        logger.debug('After adjustments to formal borrow bound, np.transpose(K_max_use):\n%s',
                     np.transpose(K_max_use))

    #         if ( B_bound > B_min ):
    #             # k_bound_high
    #             K_max_use = K_max + (B_bound-B_min)*upper_slope
    # #             logger.debug('B_min: %s', B_min)
    # #             logger.debug('B_bound: %s', B_bound)
    # #             logger.debug('(B_bound-B_min)*upper_slope: %s', (B_bound-B_min)*upper_slope)
    # #             logger.debug('K_max_use: %s', K_max_use)
    #         else:
    #             K_max_use = K_max

    #         if (np.isscalar(B_bound)):
    #             # this only happens when testing code
    #             if ( B_bound > B_min ):
    #                 # k_bound_high
    #                 K_max_use = K_max + (B_bound-B_min)*upper_slope
    #     #             logger.debug('B_min: %s', B_min)
    #     #             logger.debug('B_bound: %s', B_bound)
    #     #             logger.debug('(B_bound-B_min)*upper_slope: %s', (B_bound-B_min)*upper_slope)
    #     #             logger.debug('K_max_use: %s', K_max_use)
    #             else:
    #                 K_max_use = K_max
    #         else:
    #             # This happens when invoked by gengrids.py
    #             B_bound_greater_idx = np.argwhere(B_bound > B_min)
    #
    #             logger.debug('B_bound: %s', B_bound)
    #             logger.debug('B_min: %s', B_min)
    #             logger.debug('B_bound_greater_idx: %s', B_bound_greater_idx)
    #             logger.debug('K_max: %s', K_max)
    #
    #             K_max_use = K_max
    #             # upper_slope = 1/Rb, just a number, common across cash levels
    #
    #             K_max_use[B_bound_greater_idx] = K_max[B_bound_greater_idx] + (B_bound[B_bound_greater_idx]-B_min[B_bound_greater_idx])*upper_slope

    """
    If we solved for K between 0 and 50, choosing beyond 50 requires extrapolation
    if that is not allowed, then we have to restrict choice set
    """
    if (K_interp_range is not False):
        K_max_use = np.minimum(K_interp_range['K_max'], K_max_use)

    """
    K choice grid
        - K_min, K_max_use: both single column, each row a state, 50x50x3 rows
        - K_tics, 1d array, 30x30 elements
        - K_vec, result of broadcasting, K_vec is 50x50x3 rows and 30x30 columns
    """
    K_vec = K_min + (K_max_use - K_min) * K_tics

    '''
    B0: if B_min - B_max = 0, that means there is zero cash on hand
    '''

    '''
    B: B_min_lower
    lower_slope = (K_max-K_min)/(B_min-B_max)
    B_min_lower = (K_vec-K_min)*(1/lower_slope) + B_max
    in some cases, if Cash too low (to pay for fixed costs)
    then K_max=0, K_min=0, B_min = 0, B_max = 0
    but can not divide B_min-B_Max = 0
    But because K_vec - K_min=0 (K_max = 0 and K_min = 0) in cases where B_min-B_Max = 0
    so does not matter what we divide by
    # any number is fine, K_vec-K_min for here = 0 anyway 
    '''

    B_min_max_gap = B_min - B_max
    if (isinstance(B_min_max_gap, (list, tuple, np.ndarray))):
        B_min_max_gap[(B_min_max_gap == 0)] = -1
    else:
        if (B_min_max_gap == 0):
            B_min_max_gap = -1

    lower_slope = (K_max - K_min) / B_min_max_gap

    if (isinstance(lower_slope, (list, tuple, np.ndarray))):
        lower_slope[lower_slope == 0] = -1
    else:
        if (lower_slope == 0):
            lower_slope = -1

    B_min_lower = (K_vec - K_min) * (1 / lower_slope) + B_max
    #     lower_slope = np.zeros(B_min.shape)
    #     B_min_lower = np.zeros(B_min.shape)
    #     lower_slope(nzr_idx) = (K_max(nzr_idx)-K_min(nzr_idx))/(B_min(nzr_idx)-B_max(nzr_idx))
    #     B_min_lower = (K_vec-K_min)*(1/lower_slope) + B_max

    '''
    C: B_max_upper
    '''
    K_mid = K_max + (B_max - B_min) * upper_slope
    B_max_upper = np.maximum(0, (K_vec - K_mid)) * (1 / upper_slope) + B_max
    #     logger.debug('K_mid: %s', K_mid)

    '''
    D: If B_bound
    '''
    if (B_bound is False):
        pass
    else:
        B_min_lower = np.maximum(B_min_lower, B_bound)
        B_max_upper = np.maximum(B_max_upper, B_bound)

    '''
    E: B_vec
    '''
    B_vec = B_min_lower + (B_max_upper - B_min_lower) * B_tics

    if (return_all):
        return K_vec, B_vec, lower_slope, B_max_upper, B_min_lower, K_max_use, K_mid
    else:
        return K_vec, B_vec, lower_slope


def catch_minmax_fill_borrow_lowerupper(lower_slope, upper_slope):
    if (lower_slope < upper_slope):
        logger.debug('VALID: lower_slope=%s <= upper_slope=%s', lower_slope, upper_slope)
        graph = True
    else:
        logger.debug('INVALID: lower_slope=%s >= upper_slope=%s', lower_slope, upper_slope)
        graph = False
    return graph


def minmax_fill_borrow_quadrilateral(
        K_min, K_max, K_tics,
        B_min, B_max, B_tics,
        upper_slope, B_bound):
    """
    
    see evernote minmaxfill.py for more detailed graph:
    
    two points, one slope
    
    lower_slope as well as K_mid are endogenous. 
        
     -- (B_min, K_max)
        --    -- upper_slope (b_max_upper)
            --      ---- (B_bound, K_bound_high)
                --  --        --
       lower_slope  --              -- (B_max, K_mid)
       (b_min_lower)    --          --  
                            --      --
                                --  --
                    -- (B_bound     --- (B_max, K_min)
    
        
    """

    return minmax_fill_borrow_triangle(
        K_min, K_max, K_tics,
        B_min, B_max, B_tics,
        upper_slope, B_bound)


def minmax_fill_save_triangle(
        K_min, K_max, K_tics,
        B_min, B_max, B_tics,
        K_interp_range=False,
        B_interp_range=False,
        return_all=False):
    """
            (B_min, K_max)
            -- 
            -    -
            -        -
            -            -
            -                -   B_max_upper
            -                    -
            -                        -
            -                            -
            -                                -
            --------------------------------------
            (B_min, K_min)                        (B_max, K_min)
            
        left-bound = b_min_lower
        
    """

    """
    If we solved for K between 0 and 50, choosing beyond 50 requires extrapolation
    if that is not allowed, then we have to restrict choice set
    """
    K_max_use = np.copy(K_max)
    if (K_interp_range is not False):
        K_max_use = np.minimum(K_interp_range['K_max'], K_max_use)

    '''
    A: K_vec
    '''
    K_vec = K_min + (K_max_use - K_min) * K_tics

    '''
    B: B_max_upper
    see lower_slope earlier
    originally:
        upper_slope = (K_min-K_max)/(B_max-B_min)
        B_max_upper = (K_vec - K_max)*(1/upper_slope) + B_min     
    '''

    B_max_min_gap = B_max - B_min
    if (np.isscalar(B_max_min_gap)):
        # for mattress
        if (B_max_min_gap == 0):
            B_max_upper = B_min
        else:
            upper_slope = (K_min - K_max) / B_max_min_gap
            B_max_upper = (K_vec - K_max) * (1 / upper_slope) + B_min

        if (B_interp_range is not False):
            B_max_upper = np.minimum(B_interp_range['B_max'], B_max_upper)

        '''
        C: B_vec
        '''
        B_vec = B_min + (B_max_upper - B_min) * B_tics

    else:
        B_max_min_gap[(B_max_min_gap == 0)] = 0.00001

        upper_slope = (K_min - K_max) / B_max_min_gap
        upper_slope[upper_slope == 0] = 1

        B_max_upper = (K_vec - K_max) * (1 / upper_slope) + B_min

        if (B_interp_range is not False):
            B_max_upper = np.minimum(B_interp_range['B_max'], B_max_upper)

        '''
        C: B_vec
        '''
        B_vec = B_min + (B_max_upper - B_min) * B_tics

    #
    if (return_all):
        return K_vec, B_vec, B_max_upper, K_max_use, K_min
    else:
        return K_vec, B_vec
