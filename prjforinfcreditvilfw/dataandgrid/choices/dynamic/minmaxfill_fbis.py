'''
Created on Jul 2, 2018

@author: fan

This is the most complicated choice to generate it seems.
Separate file for it to work on this more.
'''

import numpy as np

import dataandgrid.choices.dynamic.minmaxfill as minmaxfill
import dataandgrid.choices.dynamic.minmaxfunc as minmaxfunc


def minmax_fill_formalborr_infsave_curved_v1(
        cur_minmax_bfis_borr, cur_minmax_bfis_save,
        K_tics, B_tics,
        B_bound=False,
        K_interp_range=False,
        B_interp_range=False):
    """
    This version does not fully work: 
        - It works when there is no minimal borrowing and savings
        - breaks down when there is mimimmal borrowing and savings.  
    """

    'Formal Borrow Side Grid'
    [[[K_min, K_max], [B_min, B_max]], Y_minCst, RB] = cur_minmax_bfis_borr
    upper_slope = -(1 / RB)
    K_vec, __, __, \
    borr_B_max_upper, borr_B_min_lower, borr_K_max_use, borr_K_min, K_mid = \
        minmaxfill.minmax_fill_borrow_triangle(
            K_min=K_min, K_max=K_max, K_tics=K_tics,
            B_min=B_min, B_max=B_max, B_tics=B_tics,
            upper_slope=upper_slope, B_bound=B_bound,
            K_interp_range=K_interp_range,
            return_all=True)

    # this is how much of borrowing could be saved from 0 to this gap
    fbis_save_max = (-1) * (borr_B_min_lower - borr_B_max_upper)
    normal_save_idx = (K_vec < K_mid)
    normal_save_idx_tics = np.reshape(normal_save_idx, np.shape(K_tics))

    'Informal lend only add to subset of total tics'
    K_tics_informal_save = K_tics[normal_save_idx_tics]
    # Rescale tic to be 0 to 100, otherwise save triangle is bottom portion only
    max_tic_ratio_rescale_multiplier = 1.0 / np.max(K_tics_informal_save)
    # Rescaling
    K_tics_informal_save = max_tic_ratio_rescale_multiplier * K_tics_informal_save

    B_tics_informal_save = B_tics[normal_save_idx_tics]

    'Informal Lend Side Grid'
    [[[K_min, K_max], [B_min_save, B_max]], Y_minCst, RB] = cur_minmax_bfis_save

    __, __, \
    save_B_max_upper_sv, save_K_max_use, save_K_min = \
        minmaxfill.minmax_fill_save_triangle(
            K_min=K_min, K_max=K_max, K_tics=K_tics_informal_save,
            B_min=B_min_save, B_max=B_max, B_tics=B_tics_informal_save,
            K_interp_range=K_interp_range,
            B_interp_range=B_interp_range,
            return_all=True)

    'Combine gaps'
    save_B_max_upper_sv = np.reshape(save_B_max_upper_sv, np.shape(fbis_save_max[normal_save_idx]))
    # save_B_max_upper_sv not B_vec, because subtracting B_min_save below
    fbis_save_max[normal_save_idx] = fbis_save_max[normal_save_idx] + save_B_max_upper_sv

    'Overall'

    'Set too Small to null'
    B_vec = B_min_save + (fbis_save_max - B_min_save) * B_tics
    #     borrow_too_small_idx = (fbis_save_max < B_min_save)
    #     B_vec[borrow_too_small_idx] = B_min_save

    return K_vec, B_vec


def minmax_fill_formalborr_infsave_curved_v2(
        cur_minmax_bfis_borr, cur_minmax_bfis_save,
        K_tics, B_tics,
        K_interp_range=False,
        B_interp_range=False):
    """
    This version does not fully work: 
        - It works when there is no minimal borrowing and savings
        - breaks down when there is mimimmal borrowing and savings.  
    """

    'Formal Borrow Side Grid'
    [[[K_min_br, K_max_br], [B_min_br, B_max_br]], Y_minCst, RB_fb] = cur_minmax_bfis_borr
    upper_slope = -(1 / RB_fb)
    K_vec, __, __, \
    borr_B_max_upper, borr_B_min_lower, borr_K_max_use, K_mid = \
        minmaxfill.minmax_fill_borrow_triangle(
            K_min=K_min_br, K_max=K_max_br, K_tics=K_tics,
            B_min=B_min_br, B_max=B_max_br, B_tics=B_tics,
            upper_slope=upper_slope, B_bound=False,
            K_interp_range=K_interp_range,
            return_all=True)

    '''
    B. Available cash for lending: fbis_save_max
        - this comes from actual cash, but also from formal borrowing
        - normal borrowing rate is lower than save rate, would never borrow and save
        - here, borrow first then save to arbitrage. 
        - note that there is also k' choice, informal lending upper bound is given k' and formal borrow, c > 0
        
        See evernote:
        https://www.evernote.com/shard/s10/nl/1203171/de22deae-0a2d-47c3-9834-f5082bfbeeaa
    '''

    'Informal Lend Side Grid'
    [[[__, K_max_sv], [B_min_sv, B_max_sv]], Y_minCst_sv, RB_il] = cur_minmax_bfis_save

    #     # B1. this is how much of borrowing could be saved from 0 to this gap
    #     fbis_save_max = (-1)*(borr_B_min_lower - borr_B_max_upper)

    # B2. if c_none_zero_idx == True:
    #     - Below here, touches y-axis, even if there is minimal borrowing, can lend minimal borrowing out
    #     - Hence, can ignore upper slope zero consumption line, which would have prevented
    #        the lending the minimal borrowing quantities    

    #     # B2a, this is version 1
    #     #    - problem: there is a little triangle of missing borrowing
    #     c_none_zero_idx = (K_vec < Y_minCst)
    #     fbis_save_max[c_none_zero_idx] = (-1)*borr_B_min_lower[c_none_zero_idx]

    #     # B2b, this is version 2
    #     #     - this includes some infeasible points, but has all feasible points
    #     #     - this is bad too, too much min formal, weird looking choice set
    #     fbis_save_max[normal_save_idx] = (-1)*borr_B_min_lower[normal_save_idx]

    # B3. this is how much of borrowing could be saved from 0 to this gap
    '''
    for how much is borrowed, need upper to go to b = 0 point, what is upper slope
    this is how much savings is available from borrowing up (Down) to Y_minCst point
    
    below this point, additiona savings from savings
    '''
    borr_B_max_upper = minmaxfunc.minmax_KB_save_fbis_b(K_vec, Y_minCst, RB_fb)

    '''
    Major bug:
        initially: fbis_save_max = (-1)*(borr_B_min_lower - borr_B_max_upper)
        - but this ignores interest rate. 
        - borrow 1 dollar principle + interest, in consumption term that is 
            + b/(1+rB) = added consumption
        - it is b/(1+r_borrow_formal) that we use towards saving
            + (b/(1+r_borrow_formal))*(1+r_inf_lend) in terms of b tomorrow lend    
    '''
    #     fbis_save_max = (-1)*(borr_B_min_lower - borr_B_max_upper)
    fbis_save_max = (-1) * ((borr_B_min_lower - borr_B_max_upper) / RB_fb) * (RB_il)
    c_none_zero_idx = (K_vec < Y_minCst)
    fbis_save_max[c_none_zero_idx] = (-1) * (borr_B_min_lower[c_none_zero_idx] / RB_fb) * (RB_il)

    below_Kmaxsv_idx = (K_vec < K_max_sv)

    '''
    C. Generate Sub-tics
        - Formal borrow determine K_vec min and max
        - Less K_tics left for informal lend
        - individual specific
        - adjust K_tics for informal lend 
    '''

    # C1. Expand tics wich are 1d array into full 2d each row a state, col a choice
    K_tics_informal_save = np.tile(K_tics, (np.shape(K_max_sv)[0], 1))
    K_tics_informal_save[below_Kmaxsv_idx == False] = 0
    B_tics_informal_save = np.tile(B_tics, (np.shape(K_max_sv)[0], 1))
    B_tics_informal_save[below_Kmaxsv_idx == False] = 0

    if (K_tics_informal_save.size != 0):

        'Informal lend only add to subset of total tics'
        # Rescale tic to be 0 to 100, otherwise save triangle is bottom portion only
        max_tic_ratio_rescale_multiplier = 1.0 / np.max(K_tics_informal_save, 1)
        max_tic_ratio_rescale_multiplier = np.reshape(max_tic_ratio_rescale_multiplier, (-1, 1))
        # Rescaling
        K_tics_informal_save = max_tic_ratio_rescale_multiplier * K_tics_informal_save

        save_B_max_wthKminbr = minmaxfunc.minmax_KB_save_fbis_a(K_min_br, Y_minCst, RB_il)

        __, __, \
        save_B_max_upper_sv, save_K_max_use, save_K_min = \
            minmaxfill.minmax_fill_save_triangle(
                K_min=K_min_br, K_max=K_max_sv, K_tics=K_tics_informal_save,
                B_min=B_min_sv, B_max=save_B_max_wthKminbr, B_tics=B_tics_informal_save,
                K_interp_range=K_interp_range,
                B_interp_range=B_interp_range,
                return_all=True)

        'Combine gaps'
        # save_B_max_upper_sv not B_vec, because subtracting B_min_save below
        #         fbis_save_max[below_Kmaxsv_idx] = fbis_save_max[below_Kmaxsv_idx]
        #         fbis_save_max[below_Kmaxsv_idx] = save_B_max_upper_sv
        fbis_save_max[below_Kmaxsv_idx] = fbis_save_max[below_Kmaxsv_idx] + save_B_max_upper_sv[below_Kmaxsv_idx]

    else:
        '''Formal Borrow Min so high all lending from formally borrowed'''
        pass

    '''
    Generate B_vec
        fbis_save_max is not max, it is the difference 
    '''
    fbis_save_max = np.minimum(B_interp_range['B_max'], fbis_save_max)
    B_vec = B_min_sv + (fbis_save_max - B_min_sv) * B_tics
    B_vec[B_vec > fbis_save_max] = fbis_save_max[B_vec > fbis_save_max]

    #     B_vec[B_vec<=B_min_save] = int(B_min_save)
    #     B_vec[B_vec>=np.max(fbis_save_max)] = np.max(fbis_save_max)

    return K_vec, B_vec
