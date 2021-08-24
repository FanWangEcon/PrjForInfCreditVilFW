'''
Created on Jul 7, 2018

@author: fan

import dataandgrid.genchoices_fbibfsil as fbibfsis
'''

import numpy as np


def genfibs_mjall(j, j_ktp=0, j_btp=None, param_inst=None, fb_f_max_btp=None,
                  invoke_type='genchoices'):
    """
    all choices except for j=105 are actual chioce ranges, j=105 formal borrow
    at max not included in j_btp, hence adjustments below
    
    import dataandgrid.genchoices_fb_ib_fs_is as fbibfsis
    
    Parameters
    ----------
    j_ktp: numpy array
        generated from genchoices.py (from minmaxgen.py)
    j_btp: numpy array
        generated from genchoices.py (from minmaxgen.py)
    invoke_type: string
        only matters for 105
        
    """

    b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = 0, 0, 0, 0

    if (j == 0):
        k_tp = j_ktp
        b_tp_borr_inf = j_btp

    if (j == 1):
        k_tp = j_ktp
        b_tp_lend_inf = j_btp

    if (j == 2 or j == 102):
        k_tp = j_ktp
        b_tp_borr_for = j_btp

    if (j == 3):
        k_tp = j_ktp
        b_tp_save_for = j_btp

    if (j == 4 or j == 104):
        if (j == 4):
            k_tp = j_ktp
            b_tp_borr_for = fb_f_max_btp
            b_tp_borr_inf = j_btp
        if (j == 104):
            k_tp, b_tp_borr_for, b_tp_borr_inf = genchoices_104(j_ktp, j_btp, param_inst)

    if (j == 5 or j == 105):
        if (j == 5):
            k_tp = j_ktp
            b_tp_borr_for = fb_f_max_btp
            b_tp_lend_inf = j_btp

        if (j == 105):
            k_tp, b_tp_borr_for, b_tp_lend_inf = genchoices_105(j_ktp, j_btp, param_inst,
                                                                invoke_type=invoke_type)

    if (j == 6):
        k_tp = j_ktp

    # old
    '''
    if (j == 7):
        'Informal borrowing at min, formal borrow cts, formal borr cheaper'
        k_tp = self.ibfb_f_imin_ktp
        b_tp_borr_for = self.ibfb_f_imin_btp
        b_tp_borr_inf = self.BNI_BORR_P_startVal
    
    if (j == 8):
        k_tp = self.fbis_f_imin_ktp
        b_tp_borr_for = self.fbis_f_imin_btp
        b_tp_lend_inf = self.BNI_LEND_P_startVal
    '''

    return k_tp, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf


def genfibs_btpstack(choice_set_list, btp_opti_allJ, ktp_opti_allJ, param_inst=None,
                     invoke_type='btp_opti'):
    """
    btp_opti is from btp_stack 
    btp_stack from mjall.get_all_outputs
    btp_stack = sum(b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf)
    
    goal is to get back to b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf
    
    import dataandgrid.genchoices_fbibfsil as fbibfsis
    
    Parameters
    ----------
    btp_opti: numpy array 2d
        this should be 2d array with 7 columns (each of the js) and rows are states 
    """

    b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = 0, 0, 0, 0

    btp_fb_opti_allJ = np.zeros(np.shape(btp_opti_allJ))
    btp_ib_opti_allJ = np.zeros(np.shape(btp_opti_allJ))
    btp_fs_opti_allJ = np.zeros(np.shape(btp_opti_allJ))
    btp_il_opti_allJ = np.zeros(np.shape(btp_opti_allJ))

    for ctr, j in enumerate(choice_set_list):

        j_btp_opti = btp_opti_allJ[:, ctr]
        j_ktp_opti = ktp_opti_allJ[:, ctr]

        if (j == 0 or j == 1 or j == 2 or j == 102 or j == 3):
            __, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                genfibs_mjall(j, j_btp=j_btp_opti)

        elif (j == 4 or j == 104):
            __, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                genfibs_mjall(j, j_ktp=j_ktp_opti, j_btp=j_btp_opti, param_inst=param_inst)

        elif (j == 5 or j == 105):
            __, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                genfibs_mjall(j, j_ktp=j_ktp_opti, j_btp=j_btp_opti, param_inst=param_inst,
                              invoke_type=invoke_type)

        elif (j == 6):
            __, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                genfibs_mjall(j, j_ktp=j_ktp_opti)

        btp_fb_opti_allJ[:, ctr] = b_tp_borr_for
        btp_ib_opti_allJ[:, ctr] = b_tp_borr_inf
        btp_fs_opti_allJ[:, ctr] = b_tp_save_for
        btp_il_opti_allJ[:, ctr] = b_tp_lend_inf

    return btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ


def genchoices_105(fbis_i_ktp, fbis_i_btp, param_inst, invoke_type='genchoices'):
    """
    
    Parameters
    ----------
    btp_type: string
        'genchoices' or 'btp_opti'
        'genchoices': btp for informal lending feasible set, given fb at max, 
                        because fbis arbitrage will max out all fb, so choice is 
                        only in terms of is. but btp that is produced, based on
                        the sum of (b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf)
                        that has both the is as well as fb
        'btp_opti': this is the sum of (b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf)
                        unlike genchoices, it is no longer just feasible is set
                        but fb and is summed up.
        note this difference only exists for choice category 105s         
    """
    kappa = param_inst.esti_param['kappa']
    k_tp = fbis_i_ktp
    b_tp_borr_for = (-1) * k_tp * kappa

    if (invoke_type == 'genchoices'):
        b_tp_lend_inf = fbis_i_btp
    if (invoke_type == 'btp_opti'):
        """
        suppose that: fbis_i_btp = 30 and k = 10
            that means b_tp_borr_for + b_tp_lend_inf = 30
            30 - b_tp_borr_for = b_tp_lend_inf
            lending could be 35, and borrowing -5, net is 30
        """
        b_tp_lend_inf = fbis_i_btp - b_tp_borr_for

    return k_tp, b_tp_borr_for, b_tp_lend_inf


def genchoices_104(ibfb_i_ktp, ibfb_i_btp, param_inst):
    """
    
    K choice collateral.
        - b_tp_borr_for not fixed
        - b_tp_borr_for <= k_tp*collateral, hence
            + b_tp_borr_for = ibfb_i_btp, if {-1*ibfb_i_btp < k_tp*collateral}
              b_tp_borr_for = k_tp*collateral, otherwise
            + b_tp_borr_inf = 0, if {-1*ibfb_i_btp < k_tp*collateral}
              b_tp_borr_inf = ibfb_i_btp + k_tp*collateral, otherwise
    the idea here is that:
        - formal choices and informal co-exist with minimal borrow for both
        - formal choices do not have to max out
        - formal + informal joint borrow means two fixed costs two minimal borrowing
    
    Example
    -------
    k_tp, b_tp_borr_for, b_tp_borr_inf = genchoices_104(ibfb_i_ktp, ibfb_i_btp, 
                                                        kappa, BNI_BORR_P_startVal) 
    """

    kappa = param_inst.esti_param['kappa']
    BNI_BORR_P_startVal = param_inst.grid_param['BNI_BORR_P_startVal']

    k_tp = ibfb_i_ktp

    b_tp_borr_for = np.zeros(k_tp.shape)
    b_tp_borr_inf = np.zeros(k_tp.shape)

    # In Formal Bound = in_formal_bd
    in_formal_bd_idx = (-1 * ibfb_i_btp <= k_tp * kappa)

    b_tp_borr_for[in_formal_bd_idx == True] = ibfb_i_btp[in_formal_bd_idx == True] - BNI_BORR_P_startVal
    b_tp_borr_for[in_formal_bd_idx == False] = (-1) * k_tp[in_formal_bd_idx == False] * kappa - BNI_BORR_P_startVal

    b_tp_borr_inf = ibfb_i_btp + k_tp * kappa + BNI_BORR_P_startVal
    b_tp_borr_inf[in_formal_bd_idx == True] = 0 + BNI_BORR_P_startVal

    return k_tp, b_tp_borr_for, b_tp_borr_inf

###################################
# Prvious codes from within mjall
###################################    
#     def vector_selection(self, j):
#             
#         b_tp_borr_for, b_tp_borr_inf, \
#             b_tp_save_for, b_tp_lend_inf=0,0,0,0
#                                 
#         if (j == 0):
#             k_tp = self.ib_i_ktp
#             b_tp_borr_inf = self.ib_i_btp
#             
#         if (j == 1):
#             k_tp = self.is_i_ktp
#             b_tp_lend_inf = self.is_i_btp
#             
#         if (j == 2 or j == 102):
#             k_tp = self.fb_f_ktp
#             b_tp_borr_for = self.fb_f_btp
#         if (j == 3):
#             k_tp = self.fs_f_ktp
#             b_tp_save_for = self.fs_f_btp
#             
#         if (j == 4 or j == 104):
#             if (j == 4):
#                 k_tp = self.ibfb_i_ktp                
#                 b_tp_borr_for = self.fb_f_max_btp
#                 b_tp_borr_inf = self.ibfb_i_btp
#             if (j == 104):
#                 """
#                 K choice collateral.
#                     - b_tp_borr_for not fixed
#                     - b_tp_borr_for <= k_tp*collateral, hence
#                         + b_tp_borr_for = ibfb_i_btp, if {-1*ibfb_i_btp < k_tp*collateral}
#                           b_tp_borr_for = k_tp*collateral, otherwise
#                         + b_tp_borr_inf = 0, if {-1*ibfb_i_btp < k_tp*collateral}
#                           b_tp_borr_inf = ibfb_i_btp + k_tp*collateral, otherwise
#                 the idea here is that:
#                     - formal choices and informal co-exist with minimal borrow for both
#                     - formal choices do not have to max out
#                     - formal + informal joint borrow means two fixed costs two minimal borrowing
#                     - 
#                 """
#                 k_tp = self.ibfb_i_ktp
#                 
#                 b_tp_borr_for = np.zeros(k_tp.shape)  
#                 b_tp_borr_inf = np.zeros(k_tp.shape) 
#                 
#                 # In Formal Bound = in_formal_bd
#                 in_formal_bd_idx = ( -1*self.ibfb_i_btp <= k_tp*self.kappa )
# 
#                 b_tp_borr_for[in_formal_bd_idx==True]  =  self.ibfb_i_btp[in_formal_bd_idx==True] - self.BNI_BORR_P_startVal
#                 b_tp_borr_for[in_formal_bd_idx==False] =  (-1)*k_tp[in_formal_bd_idx==False]*self.kappa - self.BNI_BORR_P_startVal
#                 
#                 b_tp_borr_inf = self.ibfb_i_btp + k_tp*self.kappa + self.BNI_BORR_P_startVal
#                 b_tp_borr_inf[in_formal_bd_idx==True]  = 0 + self.BNI_BORR_P_startVal
# 
#         if (j == 5 or j == 105):
#             if (j == 5):
#                 k_tp = self.fbis_i_ktp
#                 b_tp_borr_for = self.fb_f_max_btp
#                 b_tp_lend_inf = self.fbis_i_btp
#                 
#             if (j == 105):
#                 k_tp = self.fbis_i_ktp
#                 
#                 b_tp_borr_for = (-1)*k_tp*self.kappa  
#                 b_tp_lend_inf = self.fbis_i_btp 
#                             
#         if (j == 6):
#             k_tp = self.none_ktp
#                 
#         if (j == 7):
#             'Informal borrowing at min, formal borrow cts, formal borr cheaper'
#             k_tp = self.ibfb_f_imin_ktp
#             b_tp_borr_for = self.ibfb_f_imin_btp
#             b_tp_borr_inf = self.BNI_BORR_P_startVal
#         if (j == 8):
#             k_tp = self.fbis_f_imin_ktp
#             b_tp_borr_for = self.fbis_f_imin_btp
#             b_tp_lend_inf = self.BNI_LEND_P_startVal
#     
#         return k_tp, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf
