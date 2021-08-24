'''
Created on May 3, 2018

@author: fan

This is for the inner loop in optimization. 
'''

import numpy as np


def minmax_fill_quad(top_left_K, top_right_K, bottom_left_K, bottom_right_K,
                     top_left_B, top_right_B, bottom_left_B, bottom_right_B,
                     K_tics, B_tics):
    """
    Any four point quadrilateral
    assume top line and bottom lines are parallel (that is what happens in my code) 
        - top left and top right Y-axis points are the same.
        - bottom left and bottom right Y-axis points are the same. 
        - Y-axis happens to be K
        
    This method is more general than method in minmaxfill in some sense, although
    here no longer have bounds. 
    
    this is assume to be used for inner grid, zooming in to subsets of grid choices. 
        
        top left       top right
            -- -- -- -- --
                --          --
                     --         -- slope_higher 
            slope_lower   --        --
                               --       --
                                   -----------
                            bottom left    bottom right
    
    Linear:
        Y = a + b*X        
        top_left_K = a + b * top_left_B
        bottom_left_K = a + b * bottom_left_B

        slope_lower:
        tlK = a + b * tlB
        blK = a + b * blB
        
        slope_higher:
        trK = c + d * trB
        brK = c + d * brB
            d = (trK - brK)/(trB - brB)
            c = trk - d * trB
            
    Algorithm:        
        1. K_vec = K_tics * (top_K - bottom_K)
        2. Upper and lower slope (find subset where tlB=blB, or trB = brB)
            a, b, c, d
            inf = 1 if tlB=blB, or trB = brB
                b = (tlK - blK)/(tlB - blB)
                a = tlk - b * tlB  
                d = (trK - brK)/(trB - brB)
                c = trk - d * trB            
        3. Generate K specific left and right B bounds
            note each set of B_tics are matched with one specific K value
            right_B_cur = ((K_vec) - c)/d
            left_B_cur =  ((K_vec) - a)/b
            right_B_cur[inf==0] = trB or brB (same)
            left_B_cur[inf==0] = tlB or blB (same)
            these two new values are specific to each set of B_tics, common for all tics 
        4. B_vec = B_tics * (right_B_cur - left_B_cur) 
        
    Parameters
    ----------
    top_left_K : array (or scalar)
        assume = top_right_K
    
    """

    '''
    1. K_vec = K_tics * (top_K - bottom_K)
    '''
    K_vec = K_tics * (top_left_K - bottom_left_K) + bottom_left_K

    '''
    2. a, b, c, d
    '''
    b = (top_left_K - bottom_left_K) / (top_left_B - bottom_left_B)
    a = top_left_K - b * top_left_B
    left_zero_run_idx = (top_left_B == bottom_left_B)

    d = (top_right_K - bottom_right_K) / (top_right_B - bottom_right_B)
    c = top_right_K - d * top_right_B
    right_zero_run_idx = (top_right_B == bottom_right_B)

    '''
    3. Generate K specific left and right B bounds
    '''
    left_B_cur = ((K_vec) - a) / b
    left_B_cur[np.ravel(left_zero_run_idx), :] = top_left_B[np.ravel(left_zero_run_idx), :]

    right_B_cur = ((K_vec) - c) / d
    right_B_cur[np.ravel(right_zero_run_idx), :] = top_right_B[np.ravel(right_zero_run_idx), :]

    '''
    4. B_vec = B_tics * (right_B_cur - left_B_cur)
    '''
    B_vec = B_tics * (right_B_cur - left_B_cur) + left_B_cur

    return K_vec, B_vec
