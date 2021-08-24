'''
Created on Dec 10, 2017

@author: fan

getting overall utility from all seven choices. 

'''

import logging
import numpy as np

# from numba import jit
import projectsupport.graph.choices_i_eachj_polygon as choices_ieachj_poly

logger = logging.getLogger(__name__)


class LifeTimeUtility():

    def __init__(
            self,
            utoday_inst, ufuture_inst, param_inst,
            eps_tt, k_tt, b_tt,
            fb_f_max_btp,
            ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp,
            ibfb_i_ktp, fbis_i_ktp,
            none_ktp,
            ibfb_f_imin_ktp, fbis_f_imin_ktp,
            ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp,
            ibfb_i_btp, fbis_i_btp,
            none_btp,
            ibfb_f_imin_btp, fbis_f_imin_btp):

        """
        Parameters
        ----------
        choice_set_list: array 
            basic form: np.arange(1,7,1)
            but suppose only want to consider categories 1 and 2, 
            then could be np.array([1,3,4]) etc
            suppose I want to only allow for one choice.
            0 = informal borrow
            1 = informal save/lend
            2 = formal borrow
            3 = formal save
            4 = joint formal and informal borrow
            5 = formal borrow, informal lend
            6 = cash under mattress?
            7 = formbal borrow + pay informal borrow cost and min inf borrow
                compare 7 and 4 to fine optimal first, then compare to rest
            8 = formbal borrow + pay informal save cost and min inf save
                compare 8 and 5 to fine optimal first, then compare to rest
        """

        choice_set_list = param_inst.model_option['choice_set_list']
        self.choice_set_list = choice_set_list
        self.choice_set_count = len(choice_set_list)

        # instances joint functions         
        self.utoday_inst = utoday_inst
        self.ufuture_inst = ufuture_inst

        'Today'
        self.eps_tt = eps_tt
        self.k_tt = k_tt
        self.b_tt = b_tt

        # ktp        
        self.ib_i_ktp = ib_i_ktp
        self.is_i_ktp = is_i_ktp
        self.fb_f_ktp = fb_f_ktp
        self.fs_f_ktp = fs_f_ktp

        self.ibfb_i_ktp = ibfb_i_ktp
        self.fbis_i_ktp = fbis_i_ktp
        self.none_ktp = none_ktp

        self.ibfb_f_imin_ktp = ibfb_f_imin_ktp
        self.fbis_f_imin_ktp = fbis_f_imin_ktp

        # btp        
        self.ib_i_btp = ib_i_btp
        self.is_i_btp = is_i_btp
        self.fb_f_btp = fb_f_btp
        self.fs_f_btp = fs_f_btp

        self.fb_f_max_btp = fb_f_max_btp

        self.ibfb_i_btp = ibfb_i_btp
        self.fbis_i_btp = fbis_i_btp
        self.none_btp = none_btp

        self.ibfb_f_imin_btp = ibfb_f_imin_btp
        self.fbis_f_imin_btp = fbis_f_imin_btp

        # len_stack
        '''
        A is simulated data grid points, but solve for each A optimal choices
        Value separately, treat as parameter to save matrix space. 
        '''
        self.param_inst = param_inst
        self.A = param_inst.data_param['A']
        self.beta = param_inst.esti_param['beta']
        self.kappa = param_inst.esti_param['kappa']

        self.shape_choice_type = param_inst.grid_param['shape_choice']['type']
        logger.info('shape_choice_type:%s', self.shape_choice_type)
        self.len_choices = param_inst.grid_param['len_choices']
        self.len_statesshocks = len(k_tt)

        if (self.shape_choice_type in ('broadcast', 'broadcast_kron')):
            self.stack_shape = [self.len_statesshocks, self.choice_set_count, self.len_choices]
            if (self.shape_choice_type == 'broadcast'):
                self.stack_shape_choice = self.stack_shape
            if (self.shape_choice_type == 'broadcast_kron'):
                self.stack_shape_choice = [self.len_choices, self.choice_set_count]
        else:
            self.stack_shape = [self.len_statesshocks * self.len_choices, self.choice_set_count]
            self.stack_shape_choice = self.stack_shape

        logger.info('stack_shape:%s', self.stack_shape)
        logger.info('stack_shape_choice:%s', self.stack_shape_choice)

        self.interpolant = param_inst.interpolant
        self.BNF_SAVE_P_startVal = param_inst.grid_param['BNF_SAVE_P_startVal']
        self.BNF_BORR_P_startVal = param_inst.grid_param['BNF_BORR_P_startVal']
        self.BNI_LEND_P_startVal = param_inst.grid_param['BNI_LEND_P_startVal']
        self.BNI_BORR_P_startVal = param_inst.grid_param['BNI_BORR_P_startVal']

    def vector_selection(self, j):

        b_tp_borr_for, b_tp_borr_inf, \
        b_tp_save_for, b_tp_lend_inf = 0, 0, 0, 0

        if (j == 0):
            k_tp = self.ib_i_ktp
            b_tp_borr_inf = self.ib_i_btp

        if (j == 1):
            k_tp = self.is_i_ktp
            b_tp_lend_inf = self.is_i_btp

        if (j == 2 or j == 102):
            k_tp = self.fb_f_ktp
            b_tp_borr_for = self.fb_f_btp
        if (j == 3):
            k_tp = self.fs_f_ktp
            b_tp_save_for = self.fs_f_btp

        if (j == 4 or j == 104):
            if (j == 4):
                k_tp = self.ibfb_i_ktp
                b_tp_borr_for = self.fb_f_max_btp
                b_tp_borr_inf = self.ibfb_i_btp
            if (j == 104):
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
                    - 
                """
                k_tp = self.ibfb_i_ktp

                b_tp_borr_for = np.zeros(k_tp.shape)
                b_tp_borr_inf = np.zeros(k_tp.shape)

                # In Formal Bound = in_formal_bd
                in_formal_bd_idx = (-1 * self.ibfb_i_btp <= k_tp * self.kappa)

                b_tp_borr_for[in_formal_bd_idx == True] = self.ibfb_i_btp[
                                                              in_formal_bd_idx == True] - self.BNI_BORR_P_startVal
                b_tp_borr_for[in_formal_bd_idx == False] = (-1) * k_tp[
                    in_formal_bd_idx == False] * self.kappa - self.BNI_BORR_P_startVal

                b_tp_borr_inf = self.ibfb_i_btp + k_tp * self.kappa + self.BNI_BORR_P_startVal
                b_tp_borr_inf[in_formal_bd_idx == True] = 0 + self.BNI_BORR_P_startVal

        if (j == 5 or j == 105):
            if (j == 5):
                k_tp = self.fbis_i_ktp
                b_tp_borr_for = self.fb_f_max_btp
                b_tp_lend_inf = self.fbis_i_btp

            if (j == 105):
                k_tp = self.fbis_i_ktp

                b_tp_borr_for = (-1) * k_tp * self.kappa
                b_tp_lend_inf = self.fbis_i_btp

        if (j == 6):
            k_tp = self.none_ktp

        if (j == 7):
            'Informal borrowing at min, formal borrow cts, formal borr cheaper'
            k_tp = self.ibfb_f_imin_ktp
            b_tp_borr_for = self.ibfb_f_imin_btp
            b_tp_borr_inf = self.BNI_BORR_P_startVal
        if (j == 8):
            k_tp = self.fbis_f_imin_ktp
            b_tp_borr_for = self.fbis_f_imin_btp
            b_tp_lend_inf = self.BNI_LEND_P_startVal

        return k_tp, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf

    def get_utoday(self, info=False, check_scalar=False):
        """Utility Today
        These only need to be calculated once given parameters for each 
        iteration        
        """

        '''A. Matrix To Save Results'''
        utility_today_stack = np.zeros(self.stack_shape)
        if info:
            consumption_stack = np.zeros(self.stack_shape)
            b_tp_principle_stack = np.zeros(self.stack_shape)

            b_tp_borr_for_stack, b_tp_borr_inf_stack, \
            b_tp_save_for_stack, b_tp_lend_inf_stack = None, None, None, None

        'B. Cash, same for all 7 choices'
        cash, y = self.utoday_inst.get_cash(A=self.A, eps_tt=self.eps_tt,
                                            k_tt=self.k_tt, b_tt=self.b_tt)
        self.cash_tt = cash
        '''
        C. Loop over 7 choices
            ctr = count from 0 to len(choice_set_list) the current choice index
            j   = index for which of the 7 choices
        '''
        for ctr, j in enumerate(self.choice_set_list):
            logger.info('TODAY %s OF %s IN choice_set_list', j, len(self.choice_set_list))

            'C1. Get K and B choices for each of the 7'
            k_tp, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                self.vector_selection(j)

            'C2. Obtain Utility today etc'
            utility_today, consumption, b_tp_principle = \
                self.utoday_inst.utility_today_cash(
                    cash=cash, k_tp=k_tp,
                    b_tp_borr_for=b_tp_borr_for, b_tp_borr_inf=b_tp_borr_inf,
                    b_tp_save_for=b_tp_save_for, b_tp_lend_inf=b_tp_lend_inf,
                    check_scalar=check_scalar)

            'C3a. Store Utility Today'
            logger.debug('utility_today.shape:%s', utility_today.shape)
            logger.debug('utility_today_stack.shape:%s', utility_today_stack.shape)
            utility_today_stack[:, ctr] = utility_today
            if info:
                consumption_stack[:, ctr] = consumption
                b_tp_principle_stack[:, ctr] = b_tp_principle

                if (b_tp_borr_for_stack is not None):
                    b_tp_borr_for_stack[:, ctr] = b_tp_borr_for
                if (b_tp_borr_inf_stack is not None):
                    b_tp_borr_inf_stack[:, ctr] = b_tp_borr_inf
                if (b_tp_save_for_stack is not None):
                    b_tp_save_for_stack[:, ctr] = b_tp_save_for
                if (b_tp_lend_inf_stack is not None):
                    b_tp_lend_inf_stack[:, ctr] = b_tp_lend_inf

        'D. Return'
        if info:
            return utility_today_stack, b_tp_principle_stack, consumption_stack, cash, y, \
                   b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack
        else:
            return utility_today_stack

    def get_ufuture(self, interpolant, info=False):
        """Utility Future
        
        Parameters
        ----------
        b_tp_stack: 2d array
            produced by get_uycb_today, reused here
            
        """

        'A. Matrix To Save Results'
        utility_future_stack = np.zeros(self.stack_shape)
        if info:
            b_tp_stack = np.zeros(self.stack_shape)

        'B. Loop over 7 choices'
        for ctr, j in enumerate(self.choice_set_list):
            logger.info('FUTURE %s OF %s IN choice_set_list', j, len(self.choice_set_list))

            'B1. Get K and B choices for each of the 7'
            k_tp, b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf = \
                self.vector_selection(j)

            'B2. b_tp this is principle + interests'
            b_tp = b_tp_borr_for + b_tp_borr_inf + b_tp_save_for + b_tp_lend_inf

            'B3. Obtain Utility today etc'
            utility_future = \
                self.ufuture_inst.get_integrated_util_future(
                    interpolant,
                    b_tp=b_tp, k_tp=k_tp, A=self.A,
                    eps_tt=0, eps_tp=0, choice_set_list_j=j)

            'B3. Store Utility Today'
            utility_future_stack[:, ctr] = utility_future
            if info:
                b_tp_stack[:, ctr] = b_tp

        'C. Return'
        if info:
            return utility_future_stack, b_tp_stack
        else:
            return utility_future_stack

    def get_ktp_stack(self):

        ktp_stack = np.zeros(self.stack_shape_choice)
        for ctr, j in enumerate(self.choice_set_list):
            if (j == 0):
                ktp_array = self.ib_i_ktp
            if (j == 1):
                ktp_array = self.is_i_ktp
            if (j == 2 or j == 102):
                ktp_array = self.fb_f_ktp
            if (j == 3):
                ktp_array = self.fs_f_ktp
            if (j == 4 or j == 104):
                ktp_array = self.ibfb_i_ktp
            if (j == 5 or j == 105):
                ktp_array = self.fbis_i_ktp
            if (j == 6):
                ktp_array = self.none_ktp
            if (j == 7):
                ktp_array = self.ibfb_f_imin_ktp
            if (j == 8):
                ktp_array = self.fbis_f_imin_ktp

            ktp_stack[:, ctr] = ktp_array

        return ktp_stack

    def get_btp_stack(self):

        btp_stack = np.zeros(self.stack_shape_choice)

        for ctr, j in enumerate(self.choice_set_list):
            if (j == 0):
                btp_array = self.ib_i_btp
            if (j == 1):
                btp_array = self.is_i_btp
            if (j == 2 or j == 102):
                btp_array = self.fb_f_btp
            if (j == 3):
                btp_array = self.fs_f_btp
            if (j == 4 or j == 104):
                btp_array = self.ibfb_i_btp
            if (j == 5 or j == 105):
                btp_array = self.fbis_i_btp
            if (j == 6):
                btp_array = self.none_btp
            if (j == 7):
                btp_array = self.ibfb_f_imin_btp
            if (j == 8):
                btp_array = self.fbis_f_imin_btp

            btp_stack[:, ctr] = btp_array

        return btp_stack

    def get_ulifetime(self, utoday, ufuture):

        ulife = utoday + self.beta * ufuture

        # the line below was taking up 10 percent of time, even when warning is called, not info
        #         logger.info('today, future, all:\n%s', np.asarray([[utoday[i,:,:], ufuture[i,:,:], ulife[i,:,:]]for i in np.arange(self.len_statesshocks)]) )
        logger.info('today:\n%s', np.asarray([[utoday[i, :, :]] for i in np.arange(self.len_statesshocks)]))
        logger.info('future:\n%s', np.asarray([[ufuture[i, :, :]] for i in np.arange(self.len_statesshocks)]))
        logger.info('all:\n%s', np.asarray([[ulife[i, :, :]] for i in np.arange(self.len_statesshocks)]))

        return ulife

    def get_all_outputs(self, interpolant=None, check_scalar=False,
                        directory_str_dict=None,
                        graph_list=None):
        """
        get_utoday: btp_principle_stack
            vs 
        get_ufuture: btp_stack
        
            btp_principle_stack from: b_tp_principle_fc_array function
                net b along with fixed cost, the impact of the borrow save choices
                on consumption today.
            
            btp_stack from: get_ufuture function
                btp_stack = b_tp_borr_for + b_tp_borr_inf + b_tp_save_for + b_tp_lend_inf                
        """
        utoday_stack, b_tp_principle_stack, consumption_stack, \
        cash, y, \
        b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack \
            = self.get_utoday(info=True, check_scalar=check_scalar)

        if (interpolant is None):
            interpolant = self.interpolant

        ufuture_stack, btp_stack = \
            self.get_ufuture(interpolant=interpolant, info=True)

        ulifetime_stack = self.get_ulifetime(utoday_stack, ufuture_stack)

        ktp_stack = self.get_ktp_stack()
        #         btp_stack = self.get_btp_stack()

        if graph_list is not None:
            if (('graph_choices_i_eachj_polygon' in graph_list) and (directory_str_dict is not None)):
                save_directory = directory_str_dict['img_detail_indi']
                save_filename_prefix = directory_str_dict['file_save_suffix']
                save_filename_suffix = directory_str_dict['graph_mi_polygon_j_suffix']

                choices_ieachj_poly.graph_mi_polygon_j(
                    self.choice_set_list,
                    save_directory, save_filename_prefix, save_filename_suffix,
                    self.A, self.cash_tt, self.k_tt,
                    self.ib_i_ktp, self.is_i_ktp, self.fb_f_ktp, self.fs_f_ktp, \
                    self.ibfb_i_ktp, self.fbis_i_ktp, \
                    self.none_ktp, \
                    self.ibfb_f_imin_ktp, self.fbis_f_imin_ktp, \
                    self.ib_i_btp, self.is_i_btp, self.fb_f_btp, self.fs_f_btp, \
                    self.ibfb_i_btp, self.fbis_i_btp, \
                    self.none_btp, \
                    self.ibfb_f_imin_btp, self.fbis_f_imin_btp)

        return utoday_stack, b_tp_principle_stack, consumption_stack, cash, y, \
               ufuture_stack, btp_stack, ktp_stack, \
               ulifetime_stack, \
               b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack
