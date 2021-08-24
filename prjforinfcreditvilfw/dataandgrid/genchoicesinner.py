'''
Created on Jan 28, 2018

@author: fan
'''
import logging

import dataandgrid.choices.fixed.tics as policytics
import dataandgrid.choices.dynamic.minmaxgen as minmaxgen
import dataandgrid.choices.dynamic.minmaxfill as minmaxfill

import numpy as np

import dataandgrid.choices.dynamic.tics_nearest as ticsnear

logger = logging.getLogger(__name__)


def choices_kb_each_inner(argmax_index, mjall_inst, param_inst):
    """Inner Matrix for optimization
    """

    choice_set_list = mjall_inst.choice_set_list
    cdim_row = param_inst.grid_param['len_choices_k']
    cdim_col = param_inst.grid_param['len_choices_b']
    len_choices = param_inst.grid_param['len_choices']
    cont_choice_count = 2

    '''
    Choice Tics
    make sure thare are 1d array
    '''

    choicegrid_tics_mat, __, __ = policytics.gentics(
        len_states=1,
        len_shocks=1,
        len_choices=len_choices,
        cont_choice_count=cont_choice_count)

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
    Generate Choices
    '''
    for ctr, j in enumerate(choice_set_list):
        logger.debug('Cur ctr:%s, j:%s', ctr, j)

        # Informal Borrow
        if (j == 0):
            ib_i_ktp, ib_i_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.ib_i_ktp, mjall_inst.ib_i_btp,
                                          K_tics, B_tics)

        # Informal Save/Lend
        if (j == 1):
            is_i_ktp, is_i_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.is_i_ktp, mjall_inst.is_i_btp,
                                          K_tics, B_tics)

            # Formal Borrow
        if (j == 2 or j == 102):
            fb_f_ktp, fb_f_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.fb_f_ktp, mjall_inst.fb_f_btp,
                                          K_tics, B_tics)

        # Formal Save
        if (j == 3):
            fs_f_ktp, fs_f_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.fs_f_ktp, mjall_inst.fs_f_btp,
                                          K_tics, B_tics)

            # Informal and Formal Borrow
        if (j == 4 or j == 104):
            ibfb_i_ktp, ibfb_i_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.ibfb_i_ktp, mjall_inst.ibfb_i_btp,
                                          K_tics, B_tics)

        # Formal Borrow and Informal Save/Lend
        if (j == 5 or j == 105):
            fbis_i_ktp, fbis_i_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.fbis_i_ktp, mjall_inst.fbis_i_btp,
                                          K_tics, B_tics)

        # Mattress          
        if (j == 6):
            none_ktp, none_btp, __ = \
                ticsnear.get_max_tics_box(argmax_index[:, ctr], cdim_row, cdim_col,
                                          mjall_inst.none_ktp, mjall_inst.none_btp,
                                          K_tics, B_tics)

    return ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
           ibfb_i_ktp, fbis_i_ktp, \
           none_ktp, \
           ibfb_f_imin_ktp, fbis_f_imin_ktp, \
           ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
           ibfb_i_btp, fbis_i_btp, \
           none_btp, \
           ibfb_f_imin_btp, fbis_f_imin_btp
