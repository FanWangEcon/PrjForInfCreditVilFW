'''
Created on Jan 28, 2018

@author: fan
'''
import logging

import dataandgrid.choices.fixed.tics as policytics
import dataandgrid.choices.dynamic.minmaxgen as minmaxgen
import dataandgrid.choices.dynamic.minmaxfill as minmaxfill
import dataandgrid.choices.dynamic.minmaxfill_fbis as minmaxfill_fbis

import numpy as np

logger = logging.getLogger(__name__)


def choices_kb_each(len_choices=200,
                    cont_choice_count=2,
                    cash=np.array((20, 30)),
                    k_tt=np.array((3, 4)),
                    fb_f_max_btp=np.array((1.5, 2)),
                    R_INFORM=1.10, R_FORMAL_BORR=1.05, R_FORMAL_SAVE=1.02,
                    DELTA_DEPRE=0.10, borr_constraint_KAPPA=0.40,
                    BNF_SAVE_P=1, BNF_SAVE_P_startVal=1,
                    BNF_BORR_P=3, BNF_BORR_P_startVal=-1,
                    BNI_LEND_P=4, BNI_LEND_P_startVal=1,
                    BNI_BORR_P=2, BNI_BORR_P_startVal=-1,
                    choice_set_list=np.arange(0, 8, 1),
                    K_interp_range={'K_max': 1000},
                    B_interp_range={'B_max': 1000}
                    ):
    """
    With M states and N choices, this produces: M by N grid
    
    States should be 2d1c array
    Tics should be 1d array
    
    These generate correct principle + interest rate min max bn ranges for all 
    choices except for fbis. 
    
    Returns
    -------
    2d M by N matrix
        because states are 2d1c and B_tics and K_tics are M by N
    """

    '''
    States Array
    make sure thare are 2d array with 1 column
    '''
    cash = np.reshape(cash, (-1, 1))
    k_tt = np.reshape(k_tt, (-1, 1))
    fb_f_max_btp = np.reshape(fb_f_max_btp, (-1, 1))

    '''
    Choice Tics
    make sure thare are 1d array
    '''
    choicegrid_tics_mat, __, __ = policytics.gentics(
        len_states=1,
        len_shocks=1,
        len_choices=len_choices,
        cont_choice_count=cont_choice_count)

    # 30 by 30 choice grid
    K_tics = choicegrid_tics_mat[:, 0]
    B_tics = choicegrid_tics_mat[:, 1]
    K_tics = np.ravel(K_tics)
    B_tics = np.ravel(B_tics)

    logger.debug('K_tics:%s', K_tics)
    logger.debug('B_tics:%s', B_tics)

    '''
    Initialize outcomes, could just be zero if not actually in choice set
    '''
    ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
    ibfb_i_ktp, fbis_i_ktp, \
    none_ktp, \
    ibfb_f_imin_ktp, fbis_f_imin_ktp = 0, 0, 0, 0, 0, 0, 0, 0, 0

    ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
    ibfb_i_btp, fbis_i_btp, \
    none_btp, \
    ibfb_f_imin_btp, fbis_f_imin_btp = 0, 0, 0, 0, 0, 0, 0, 0, 0

    '''
    Borrow Save Set Sets
    '''
    save_subset = [1, 3,
                   5,
                   6,  # mattress
                   8]
    borr_subset = [0, 2, 102,
                   4, 104,
                   7]
    borr_subset_bd = [2, 7]

    '''
    Min Max Choices
    '''
    all_minmax = minmaxgen.minmax_eachchoice(cash, k_tt,
                                             R_INFORM, R_FORMAL_BORR, R_FORMAL_SAVE,
                                             DELTA_DEPRE, borr_constraint_KAPPA,
                                             BNF_SAVE_P, BNF_SAVE_P_startVal,
                                             BNF_BORR_P, BNF_BORR_P_startVal,
                                             BNI_LEND_P, BNI_LEND_P_startVal,
                                             BNI_BORR_P, BNI_BORR_P_startVal,
                                             choice_set_list)

    '''
    Generate Choices
    '''
    for ctr, j in enumerate(choice_set_list):
        logger.debug('Cur ctr:%s, j:%s', ctr, j)

        cur_minmax = all_minmax[ctr]
        if (j != 105):
            cur_minmax = all_minmax[ctr]

            # K_min, K_max: 50 by 50, K by B, and then x 3 (shocks)  
            [[[K_min, K_max], [B_min, B_max]], Y_minCst, RB] = cur_minmax
            upper_slope = -(1 / RB)

        'Save Grid'
        if (j in save_subset):
            K_vec, B_vec = minmaxfill.minmax_fill_save_triangle(
                K_min=K_min, K_max=K_max, K_tics=K_tics,
                B_min=B_min, B_max=B_max, B_tics=B_tics,
                K_interp_range=K_interp_range,
                B_interp_range=B_interp_range)

        'Borrow Grid'
        if (j in borr_subset):
            if (j in borr_subset_bd):
                B_bound = fb_f_max_btp
            else:
                B_bound = False
            K_vec, B_vec, __ = minmaxfill.minmax_fill_borrow_triangle(
                K_min=K_min, K_max=K_max, K_tics=K_tics,
                B_min=B_min, B_max=B_max, B_tics=B_tics,
                upper_slope=upper_slope, B_bound=B_bound,
                K_interp_range=K_interp_range)

        'Formal Borrow, Informal Lend'
        if (j == 105):
            K_vec, B_vec = minmaxfill_fbis.minmax_fill_formalborr_infsave_curved_v2(
                cur_minmax_bfis_borr=cur_minmax['fbis_borr'],
                cur_minmax_bfis_save=cur_minmax['fbis_save'],
                K_tics=K_tics, B_tics=B_tics,
                K_interp_range=K_interp_range,
                B_interp_range=B_interp_range)

        logger.debug('K_vec, choices (rows), states(cols):\n%s', np.transpose(K_vec))
        logger.debug('B_vec, choices (rows), states(cols):\n%s', np.transpose(B_vec))

        # Informal Borrow
        if (j == 0):
            ib_i_ktp, ib_i_btp = K_vec, B_vec

        # Informal Save/Lend
        if (j == 1):
            is_i_ktp, is_i_btp = K_vec, B_vec

        # Formal Borrow
        if (j == 2 or j == 102):
            fb_f_ktp, fb_f_btp = K_vec, B_vec

        # Formal Save
        if (j == 3):
            fs_f_ktp, fs_f_btp = K_vec, B_vec

        # Informal and Formal Borrow            
        if (j == 4 or j == 104):
            ibfb_i_ktp, ibfb_i_btp = K_vec, B_vec

        # Formal Borrow and Informal Save/Lend
        if (j == 5 or j == 105):
            fbis_i_ktp, fbis_i_btp = K_vec, B_vec

        # Mattress          
        if (j == 6):
            none_ktp, none_btp = K_vec, B_vec

        # Informal Borrow Formal Borrow, but formal borrow at minimal not max          
        if (j == 7):
            ibfb_f_imin_ktp, ibfb_f_imin_btp = K_vec, B_vec

        # Informal Borrow Formal save, but formal borrow at minimal not max
        if (j == 8):
            fbis_f_imin_ktp, fbis_f_imin_btp = K_vec, B_vec

    return all_minmax, \
           ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
           ibfb_i_ktp, fbis_i_ktp, \
           none_ktp, \
           ibfb_f_imin_ktp, fbis_f_imin_ktp, \
           ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
           ibfb_i_btp, fbis_i_btp, \
           none_btp, \
           ibfb_f_imin_btp, fbis_f_imin_btp
