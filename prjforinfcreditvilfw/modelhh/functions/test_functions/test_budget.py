'''
Created on Nov 29, 2017

@author: fan
'''
import logging
import numpy as np
import pyfan.amto.array.scalararray as scalararray
# import Support.ClassObSupport as Clsobj_Sup
import pyfan.devel.obj.classobjsupport as Clsobj_Sup
# import Support.arraytools.scalararray as scalararray
import time
import unittest

import modelhh.functions.budget as bdgt

logger = logging.getLogger(__name__)


class TestBudget(unittest.TestCase):
    """
    when calc_loop = 25:
    .test_budget.py - tearDown - 26 -  2018-01-14 09:13:18,605 - WARNING __main__.TestBudget.test_broadcast_state_2_choice_2by3: 38.665627002716064
    .test_budget.py - tearDown - 26 -  2018-01-14 09:13:24,463 - WARNING __main__.TestBudget.test_broadcast_state_2_choice_3: 5.857644557952881
    .test_budget.py - tearDown - 26 -  2018-01-14 09:14:12,181 - WARNING __main__.TestBudget.test_broadcast_state_6_choice_6: 47.71705412864685
    .      
    """

    def setUp(self):
        logger.debug('setup module')
        self.bdgt_inst = self.get_bdgt_inst()
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    def get_bdgt_inst(self,
                      R_INFORM_SAVE=1.10, R_INFORM_BORR=1.10,
                      R_FORMAL_SAVE=1.02, R_FORMAL_BORR=1.05,
                      BNF_SAVE_P=1, BNF_BORR_P=4,
                      BNI_LEND_P=5, BNI_BORR_P=2,
                      K_DEPRECIATION=0.1,
                      shape_choice={'shape': 1}):

        esti_param = {'R_INFORM_SAVE': R_INFORM_SAVE,
                      'R_INFORM_BORR': R_INFORM_BORR,
                      'R_FORMAL_SAVE': R_FORMAL_SAVE,
                      'R_FORMAL_BORR': R_FORMAL_BORR,
                      'BNF_SAVE_P': BNF_SAVE_P,
                      'BNF_BORR_P': BNF_BORR_P,
                      'BNI_LEND_P': BNI_LEND_P,
                      'BNI_BORR_P': BNI_BORR_P,
                      'K_DEPRECIATION': K_DEPRECIATION}
        grid_param = {'shape_choice': shape_choice}
        attribute_array = ['esti_param', 'grid_param']
        attribute_values_array = [esti_param, grid_param]

        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
        bdgt_inst = bdgt.BudgetConsumption(param_inst)

        return bdgt_inst

    def get_consumption(self,
                        y=100,
                        k_tt=0, k_tp=0,
                        b_tt=0,
                        b_tp_borr_for=0, b_tp_borr_inf=0,
                        b_tp_save_for=0, b_tp_lend_inf=0,
                        check_scalar=False):

        consumption, cash, b_tp = self.bdgt_inst.budget_consumption(
            y,
            k_tt, k_tp,
            b_tt,
            b_tp_borr_for, b_tp_borr_inf, b_tp_save_for, b_tp_lend_inf,
            check_scalar=check_scalar)

        return consumption, cash, b_tp

    def A_test_k_tp(self):
        logger.debug('test_k_tp')

        k_tp = np.linspace(0, 100, 5)
        k_tp = np.reshape(k_tp, (-1, 1))
        self.bdgt_inst.shape_choice = {'shape': 5}
        consumption, cash, b_tp = self.get_consumption(y=100, k_tp=k_tp)
        logger.debug('consumption:%s', consumption)

        self.assertEqual(consumption[4], 0, 'come with 100, save 100 k, c=0')
        self.assertEqual(consumption[0], 100, 'come with 100, save 0 k, c=100')

    def states_common_choices(self, state_count, choice_count, default=False):

        if (default):
            'States Today'
            y = np.array([100, 120])
            k_tt = np.array([0, 1])
            b_tt = np.array([1, 3])

            'Choices'
            k_tp = np.array([1, 1, 1]),
            a_principle = np.array([-2, -1, -3])
            c_principle = np.array([-3.5, -2, -3])

        else:
            'States Today'
            y = np.linspace(100, 120, state_count)
            k_tt = np.linspace(0, 1, state_count)
            b_tt = np.linspace(1, 3, state_count)

            np.random.seed(120)
            np.random.shuffle(y)
            np.random.shuffle(k_tt)
            np.random.shuffle(b_tt)

            'Choices'
            k_tp = np.linspace(1, 1, choice_count)
            a_principle = np.linspace(-3, -1, choice_count)
            c_principle = np.linspace(-3.5, -2, choice_count)

            np.random.seed(120)
            np.random.shuffle(k_tp)
            np.random.shuffle(a_principle)
            np.random.shuffle(c_principle)

        logger.debug('y:%s', y)
        logger.debug('k_tt:%s', k_tt)
        logger.debug('b_tt:%s', b_tt)
        logger.debug('k_tp:%s', k_tp)
        logger.debug('a_principle:%s', a_principle)
        logger.debug('c_principle:%s', c_principle)

        return y, k_tt, b_tt, k_tp, a_principle, c_principle

    def test_broadcast_state_2_choice_3(self, state_count=5000, choice_count=5000, calc_loop=10):
        """2 states, 3 Choices for each state, 2 x 1 array + 3 array
        """
        logger.debug('test_broadcast_state_2_choice_3')

        y, k_tt, b_tt, k_tp, a_principle, c_principle = \
            self.states_common_choices(state_count, choice_count)

        'States Today'
        y = y[:, None]
        k_tt = k_tt[:, None]
        b_tt = b_tt[:, None]

        looper = 0
        while (looper < calc_loop):
            looper = looper + 1
            self.invoke_b_forinf_borr(
                y=y,
                k_tt=k_tt, k_tp=k_tp,
                b_tt=b_tt,
                a_principle=a_principle,
                c_principle=c_principle,
                check_scalar=True)

        return self.invoke_b_forinf_borr(
            y=y,
            k_tt=k_tt, k_tp=k_tp,
            b_tt=b_tt,
            a_principle=a_principle,
            c_principle=c_principle,
            check_scalar=False)

    def test_broadcast_state_2_choice_2by3(self, state_count=5000, choice_count=5000, calc_loop=10):
        """2 states, 3 Choices for each state, 2 x 1 array + 2 x 3 array
        """
        logger.debug('test_broadcast_state_2_choice_2by3')

        y, k_tt, b_tt, k_tp, a_principle, c_principle = \
            self.states_common_choices(state_count, choice_count)

        'States Today'
        y = y[:, None]
        k_tt = k_tt[:, None]
        b_tt = b_tt[:, None]

        'Choices Today'
        k_tp = np.repeat(k_tp[None, :], state_count, 0)
        a_principle = np.repeat(a_principle[None, :], state_count, 0)
        c_principle = np.repeat(c_principle[None, :], state_count, 0)

        looper = 0
        while (looper < calc_loop):
            looper = looper + 1
            self.invoke_b_forinf_borr(
                y=y,
                k_tt=k_tt, k_tp=k_tp,
                b_tt=b_tt,
                a_principle=a_principle,
                c_principle=c_principle,
                check_scalar=True)

        return self.invoke_b_forinf_borr(
            y=y,
            k_tt=k_tt, k_tp=k_tp,
            b_tt=b_tt,
            a_principle=a_principle,
            c_principle=c_principle,
            check_scalar=False)

    def test_broadcast_state_6_choice_6(self, state_count=5000, choice_count=5000, calc_loop=10):
        """2 states, 3 Choices for each state, 6 x 1 array + 6 x 1 array
        SLowest
        """
        logger.debug('test_broadcast_state_6_choice_6')

        y, k_tt, b_tt, k_tp, a_principle, c_principle = \
            self.states_common_choices(state_count, choice_count)

        'States Today'
        y = np.reshape(np.repeat(y[:, None], choice_count, 1), (1, -1))
        k_tt = np.reshape(np.repeat(k_tt[:, None], choice_count, 1), (1, -1))
        b_tt = np.reshape(np.repeat(b_tt[:, None], choice_count, 1), (1, -1))

        'Choices Today'
        k_tp = np.reshape(np.repeat(k_tp[None, :], state_count, 0), (1, -1))
        a_principle = np.reshape(np.repeat(a_principle[None, :], state_count, 0), (1, -1))
        c_principle = np.reshape(np.repeat(c_principle[None, :], state_count, 0), (1, -1))

        looper = 0
        while (looper < calc_loop):
            looper = looper + 1
            self.invoke_b_forinf_borr(
                y=y,
                k_tt=k_tt, k_tp=k_tp,
                b_tt=b_tt,
                a_principle=a_principle,
                c_principle=c_principle,
                check_scalar=True)

        'return'
        return self.invoke_b_forinf_borr(
            y=y,
            k_tt=k_tt, k_tp=k_tp,
            b_tt=b_tt,
            a_principle=a_principle,
            c_principle=c_principle,
            check_scalar=True)

    def test_broadcast_methods(self):
        """2 states, 3 Choices for each state        
        three methods, should yield the same results
        """
        logger.debug('test_broadcast_methods')

        state_count = 2
        choice_count = 3
        calc_loop = 0

        consumption_2_3, cash_2_3, b_tp_2_3 = \
            self.test_broadcast_state_2_choice_3(state_count, choice_count, calc_loop)

        consumption_2_23, cash_2_23, b_tp_2_23 = \
            self.test_broadcast_state_2_choice_2by3(state_count, choice_count, calc_loop)

        consumption_6_6, cash_6_6, b_tp_6_6 = \
            self.test_broadcast_state_6_choice_6(state_count, choice_count, calc_loop)

        logger.info('consumption_2_3:%s', consumption_2_3)
        logger.info('consumption_2_23:%s', consumption_2_23)
        logger.info('consumption_6_6:%s', consumption_6_6)

        self.assertAlmostEqual(np.reshape(consumption_2_3, (-1, 1)).tolist(),
                               np.reshape(consumption_2_23, (-1, 1)).tolist(), 3)
        self.assertAlmostEqual(np.reshape(consumption_2_3, (-1, 1)).tolist(),
                               np.reshape(consumption_6_6, (-1, 1)).tolist(), 3)

    def invoke_b_forinf_borr(
            self,
            y=100,
            k_tt=0, k_tp=0,
            b_tt=0,
            a_principle=np.reshape(np.array([-2, -2, -3, -3]), (-1, 1)),
            c_principle=np.reshape(np.array([-3, -3, -0, -1]), (-1, 1)),
            check_scalar=False):

        """Jointly borrowing from formal and informal sectors
        
        Array of len = 4. 4 borr save arrays of different nonzero sizes
        
        point is to test the ability of the code to handle zeros, even array
        with only 1 zero (for the choice not reelvant for this set considered)                        
        """
        logger.debug('test_b_forinf_borr_1D')

        '''
        A. Initial Arrays
        First principle,
        then Borrow enough to pay for fixed cost and adjust for interest
        '''

        BNF_BORR_P = self.bdgt_inst.BNF_BORR_P
        R_FORMAL_BORR = self.bdgt_inst.R_FORMAL_BORR
        BNI_BORR_P = self.bdgt_inst.BNI_BORR_P
        R_INFORM_BORR = self.bdgt_inst.R_INFORM_BORR

        #         BNF_BORR_P = 4
        #         R_FORMAL_BORR = 1.05
        #         BNI_BORR_P = 2
        #         R_INFORM_BORR = 1.02

        #         a_principle = np.array([-2,-2,-3,-3])  # a is say formal borrow
        #         a_principle = np.reshape(a_principle,(-1,1))

        a = (a_principle - BNF_BORR_P) * (R_FORMAL_BORR)

        b = scalararray.zero_ndims(a)  # b is not chosen for this array, formal save say
        b = 0  # b is not chosen for this array, formal save say

        #         c_principle = np.array([-3,-3,-0,-1])  # c is informal borrow, jointly with a, one 0
        #         c_principle = np.reshape(c_principle,(-1,1))
        c = (c_principle - BNI_BORR_P) * (R_INFORM_BORR)

        d = scalararray.zero_ndims(c)  # c is informal borrow, jointly with a, one 0
        d = 0  # c is informal borrow, jointly with a, one 0

        '''
        B. this is what is happening in the budget_consumption code, for transparency
        suppose to have time saving in that:
            - b and d are kept empty
            - c has 3 non-zero components, not calculating for 4, just for 3.
        '''

        '''
        C. invoke actual code
        '''
        logger.debug('y:%s', y)
        logger.debug('k_tt:%s', k_tt)
        logger.debug('b_tt:%s', b_tt)

        logger.debug('k_tp:%s', k_tp)
        logger.debug('b_tp_borr_for:%s', a)
        logger.debug('b_tp_save_for:%s', b)
        logger.debug('b_tp_borr_inf:%s', c)
        logger.debug('b_tp_lend_inf:%s', d)

        shape_choice = {'shape': a.shape}
        self.bdgt_inst.shape_choice = shape_choice['shape']
        consumption, cash, b_tp = self.get_consumption(
            y=y,
            k_tt=k_tt, k_tp=k_tp,
            b_tt=b_tt,
            b_tp_borr_for=a, b_tp_borr_inf=c,
            b_tp_save_for=b, b_tp_lend_inf=d,
            check_scalar=check_scalar)

        logger.debug('consumption:%s', consumption)
        #         logger.debug('c_expected:%s',c_expected)
        #         self.assertAlmostEqual(np.reshape(consumption, (-1,1)).tolist(),
        #                                np.reshape(c_expected, (-1,1)).tolist(),
        'Given that we have adjusted borrowing to pay for FC and interest, these should match'

        '''
        How the code is suppose to work
        '''

        #         self.assertEqual(c_b_tp_borr_for[4], 0, 'come with 100, save 100 k, c=0')
        #         self.assertEqual(consumption[0], 100, 'come with 100, save 0 k, c=100')

        return consumption, cash, b_tp

    def get_expected(self, a, b, c, d,
                     y, b_tt, k_tt, a_principle, c_principle):
        a_nonzero_idx = np.nonzero(a)
        b_nonzero_idx = np.nonzero(b)
        c_nonzero_idx = np.nonzero(c)
        d_nonzero_idx = np.nonzero(d)

        aa = a[a_nonzero_idx] * 1.3 + 4
        bb = b[b_nonzero_idx] + 10
        cc = c[c_nonzero_idx] / 2 - 3
        dd = d[d_nonzero_idx] * 2

        zz = np.zeros((np.shape(a_principle)))

        zz[a_nonzero_idx] = zz[a_nonzero_idx] + aa
        zz[b_nonzero_idx] = zz[b_nonzero_idx] + bb
        zz[c_nonzero_idx] = zz[c_nonzero_idx] + cc
        zz[d_nonzero_idx] = zz[d_nonzero_idx] + dd

        logger.debug('y + b_tt + k_tt:%s', y + b_tt + k_tt)
        c_expected = y + b_tt + k_tt - a_principle - c_principle
        c_expected = np.reshape(c_expected, (-1, 1))

        a_mat = a.reshape((2, 2))
        b_mat = b
        c_mat = c.reshape((2, 2))
        d_mat = d

        a_mat_nonzero_idx = np.nonzero(a_mat)
        b_mat_nonzero_idx = np.nonzero(b_mat)
        c_mat_nonzero_idx = np.nonzero(c_mat)
        d_mat_nonzero_idx = np.nonzero(d_mat)

        aa_mat = a_mat[a_mat_nonzero_idx] * 1.3 + 4
        bb_mat = b_mat[b_mat_nonzero_idx] + 10
        cc_mat = c_mat[c_mat_nonzero_idx] / 2 - 3
        dd_mat = d_mat[d_mat_nonzero_idx] * 2

        zz_mat = np.zeros((2, 2))
        zz_mat[a_mat_nonzero_idx] = zz_mat[a_mat_nonzero_idx] + aa_mat
        zz_mat[b_mat_nonzero_idx] = zz_mat[b_mat_nonzero_idx] + bb_mat
        zz_mat[c_mat_nonzero_idx] = zz_mat[c_mat_nonzero_idx] + cc_mat
        zz_mat[d_mat_nonzero_idx] = zz_mat[d_mat_nonzero_idx] + dd_mat


if __name__ == '__main__':
    import logging

    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.WARNING, format=FORMAT)
    unittest.main()
