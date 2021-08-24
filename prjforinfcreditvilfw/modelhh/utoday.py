'''
Created on Dec 5, 2017

@author: fan
 
'''

import logging
import numpy as np

logger = logging.getLogger(__name__)


class TodayUtility:

    def __init__(self,
                 bdgt_inst, prod_inst,
                 crra_inst, param_inst):
        """Gets all model parametesr and disects data vectors
    
        invoke this separately from future because sometimes future utility might
        be dealt with differently depending on 
        """

        self.bdgt_inst = bdgt_inst
        self.prod_inst = prod_inst
        self.crra_inst = crra_inst

        # Production Function
        self.c_min_bound = param_inst.esti_param['c_min_bound']

    def get_cash(self, A, eps_tt, k_tt, b_tt):

        y = self.prod_inst.cobb_douglas_nolabor(eps_tt, A, k_tt, alphaed=False)
        cash = self.bdgt_inst.cash(y, k_tt, b_tt)

        return cash, y

    def utility_today(
            self, A, eps_tt, k_tt, b_tt,
            k_tp,
            b_tp_borr_for, b_tp_borr_inf,
            b_tp_save_for, b_tp_lend_inf,
            check_scalar=False):
        cash, y = self.get_cash(A, eps_tt, k_tt, b_tt)
        utility_today, consumption, b_tp_principle_fc = self.utility_today_cash(
            cash, k_tp,
            b_tp_borr_for, b_tp_borr_inf,
            b_tp_save_for, b_tp_lend_inf,
            check_scalar=check_scalar)

        return utility_today, y, consumption, cash, b_tp_principle_fc

    def utility_today_cash(
            self, cash,
            k_tp,
            b_tp_borr_for, b_tp_borr_inf,
            b_tp_save_for, b_tp_lend_inf,
            check_scalar=False):
        """With Cash As Input
        Cash might be pre-calculated, common across all choices
        """
        consumption, b_tp_principle_fc = self.bdgt_inst.budget_consumption_cash(
            cash,
            k_tp,
            b_tp_borr_for, b_tp_borr_inf,
            b_tp_save_for, b_tp_lend_inf,
            check_scalar=check_scalar)

        'adjust c, kp and bp for too low, chaning kp and bp as self'
        #         consumption, cash, b_tp_principle_fc = self.inada_min_c_kp_bp(self.c_min_bound, consumption)

        'utility'
        utility_today = self.crra_inst.utility_consumption_crra(consumption=consumption)

        logger.debug('np.transpose(consumption):\n%s', np.transpose(consumption))
        logger.debug('np.transpose(utility_today):\n%s', np.transpose(utility_today))

        return utility_today, consumption, b_tp_principle_fc

    def inada_min_c_kp_bp(self, c_min_bound, consumption):
        """Minimum consumption for some negative consumption today choices
        """
        pass
        return consumption

    def bp_below_cmin(self, c_min_bound, consumption):
        'Borrowing required to cover consumption'
        borrowing_cover_c = -abs(c_min_bound - consumption)

        '''
        save choice too much:
            sometimes very low c for grid where B savings large given y
            sometimes very low c for because very low y, can not repay
        not enough to repay:
            sometimes not enough money to repay debt.
        '''

        '''
        the choice cannot be out of bounds
        '''
        borr_too_much = (borrowing_cover_c <= self.bp_min)
        borrowing_cover_c[borr_too_much] = self.bp_min

        return borrowing_cover_c
