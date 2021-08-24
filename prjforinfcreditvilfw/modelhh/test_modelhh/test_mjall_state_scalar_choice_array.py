'''
Created on Jan 2, 2018

@author: fan

One State, Muliple Choices, generated from policy tics
'''

import unittest

import logging
import dataandgrid.choices.fixed.tics as policytics
import modelhh.test_modelhh.test_mjall as test_mjall

logger = logging.getLogger(__name__)


class TestMjall_StateScalar_StateScalar_Choices1d(unittest.TestCase):
    """ state scalar values, Choice 1d array
    """

    @classmethod
    def setUpClass(cls):
        """
        class method so only invoked once for all tests
        """
        logger.debug('setup class')

        grid_a_type = 30
        cls.TestMjall_inst = test_mjall.TestMjall(
            grid_type=['a', grid_a_type],  # 3 is 450
            esti_type=['a', 1])

        cls.len_states = cls.TestMjall_inst.param_inst.grid_param['len_states']
        cls.len_choices = cls.TestMjall_inst.param_inst.grid_param['len_choices']

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_ulifetime_state_1_choice_N(
            self,
            eps_tt=0,
            k_tt=12,
            b_tt=3,
            fb_f_max_btp=-2,
            k_choice_min=0, k_choice_max=40,
            b_borr_choice_min=-40, b_borr_choice_max=0,
            b_save_choice_min=0, b_save_choice_max=40):
        """ One state element, N choices
        """

        logger.debug('enter test_ulifetime_state_1_choice_N')

        '''
        len_states = 1 for gentics function
        '''
        choicegrid_tics_mat = policytics.gentics(
            len_states=1,
            len_shocks=1,
            len_choices=self.len_choices,
            cont_choice_count=2,
            k_choice_min=k_choice_min,
            k_choice_max=k_choice_max,
            b_choice_min=b_borr_choice_min,
            b_choice_max=b_borr_choice_max)

        K_borr_tp = choicegrid_tics_mat[:, 0]
        B_borr_tp = choicegrid_tics_mat[:, 1]

        choicegrid_tics_mat = policytics.gentics(
            len_states=1,
            len_shocks=1,
            len_choices=self.len_choices,
            cont_choice_count=2,
            k_choice_min=k_choice_min,
            k_choice_max=k_choice_max,
            b_choice_min=b_save_choice_min,
            b_choice_max=b_save_choice_max)

        K_save_tp = choicegrid_tics_mat[:, 0]
        B_save_tp = choicegrid_tics_mat[:, 1]

        save_suffix = \
            'ki' + str(k_choice_min) + \
            'ka' + str(k_choice_max) + \
            'Bi' + str(b_borr_choice_min * -1) + \
            'Ba' + str(b_borr_choice_max * -1) + \
            'Si' + str(b_save_choice_min) + \
            'Sa' + str(b_save_choice_max) + \
            'st' + str(self.len_states) + \
            'ch' + str(self.len_choices)
        save_suffix = save_suffix.replace(".", "")

        self.TestMjall_inst.invoke_mjall_inst(
            eps_tt=eps_tt,
            k_tt=k_tt,
            b_tt=b_tt,
            fb_f_max_btp=fb_f_max_btp,
            ib_i_ktp=K_borr_tp, is_i_ktp=K_save_tp, fb_f_ktp=K_borr_tp, fs_f_ktp=K_save_tp,
            ibfb_i_ktp=K_borr_tp, fbis_i_ktp=K_save_tp,
            none_ktp=K_save_tp,
            ibfb_f_imin_ktp=K_borr_tp, fbis_f_imin_ktp=K_borr_tp,
            ib_i_btp=B_borr_tp, is_i_btp=B_save_tp, fb_f_btp=B_borr_tp, fs_f_btp=B_save_tp,
            ibfb_i_btp=B_borr_tp, fbis_i_btp=B_save_tp,
            none_btp=B_save_tp,
            ibfb_f_imin_btp=B_borr_tp, fbis_f_imin_btp=B_borr_tp,
            solve=True,
            graph=True, save_suffix=save_suffix, title_suffix='')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    unittest.main()
