'''
Created on Jan 13, 2018

@author: fan
'''

import unittest

import logging
import dataandgrid.choices.fixed.ticsborrsave as ticsborrsave
import modelhh.test_modelhh.test_mjall as test_mjall
import parameters.combo as paramcombo
import soluvalue.solu as solu
import numpy as np

import time

logger = logging.getLogger(__name__)


class TestMjall_StateScalar_State1Col_Choices1d(unittest.TestCase):
    """
    The code was older. 
    The idea is that there are two ways of invoking this:
    1. invoking without soluvalue
        no interpolant
        - 
        
    2. invoking after soluvalue
        has interpolant. 
    """

    def setUp(self):
        logger.debug('setup module')
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    def MjallInst(self, combo_type=None):

        if (combo_type is None):
            combo_type = ['a', '20180512_bquick_nofc']
        get_combo_list = paramcombo.get_combo(combo_type=combo_type)
        param_combo = get_combo_list[0]

        mjalltest_inst = test_mjall.TestMjall(param_combo)

        return mjalltest_inst

    def gen_state_M_choice_N(self, combo_type, mjalltest_inst, states_dict=None,
                             k_choice_min=0, k_choice_max=40,
                             b_borr_choice_min=-40, b_borr_choice_max=0,
                             b_save_choice_min=0, b_save_choice_max=40):
        """ One state element, N choices
        """
        logger.debug('test_ulifetime_state_M_choice_N')

        '''
        A. Gen States
        '''
        logger.debug('gen M states')
        len_states = mjalltest_inst.param_inst.grid_param['len_states']
        len_choices = mjalltest_inst.param_inst.grid_param['len_choices']

        np.random.seed(942)
        if (states_dict is None):
            eps_tt = 0
            k_tt = 12
            b_tt = 3
            fb_f_max_btp = -2

            eps_tt_v = np.random.rand(len_states) + eps_tt
            k_tt_v = np.floor(np.random.rand(len_states) * k_tt)
            b_tt_v = np.floor(np.random.rand(len_states) * b_tt)
            fb_f_max_btp_v = np.floor(np.random.rand(len_states) * fb_f_max_btp)
        else:
            eps_tt_v = states_dict['eps_tt']
            k_tt_v = states_dict['k_tt_v']
            b_tt_v = states_dict['b_tt_v']
            fb_f_max_btp_v = states_dict['fb_f_max_btp_v']

            logger.debug('eps_tt:%s', eps_tt_v)
            logger.debug('k_tt:%s', k_tt_v)
            logger.debug('b_tt:%s', b_tt_v)
            logger.debug('fb_f_max_btp:%s', fb_f_max_btp_v)

        '''
        B. Gen Choices
        len_states = 1 for gentics function
        '''
        cont_choice_count = 2
        K_borr_tp, B_borr_tp, K_save_tp, B_save_tp = \
            ticsborrsave.gen_polfixed_borr_save_pair(len_choices=len_choices,
                                                     cont_choice_count=cont_choice_count,
                                                     k_choice_min=k_choice_min, k_choice_max=k_choice_max,
                                                     b_borr_choice_min=b_borr_choice_min,
                                                     b_borr_choice_max=b_borr_choice_max,
                                                     b_save_choice_min=b_save_choice_min,
                                                     b_save_choice_max=b_save_choice_max)

        save_suffix = \
            'st' + str(len_states) + \
            'ch' + str(len_choices) + \
            '_' + str(combo_type[1]) + \
            '_ki' + str(k_choice_min) + \
            'ka' + str(k_choice_max) + \
            'Bi' + str(b_borr_choice_min * -1) + \
            'Ba' + str(b_borr_choice_max * -1) + \
            'Si' + str(b_save_choice_min) + \
            'Sa' + str(b_save_choice_max)

        save_suffix = save_suffix.replace(".", "")

        '''
        C. Invoke
        len_states = 1 for gentics function
        '''

        return eps_tt_v, k_tt_v, b_tt_v, fb_f_max_btp_v, K_borr_tp, B_borr_tp, K_save_tp, B_save_tp, save_suffix

    def ulifetime_state1col_choice1dor2d(
            self,
            combo_type, states_dict, interpolant=None,
            save_suffix='', title_suffix='',
            choice_dim=1,
            k_choice_min=0, k_choice_max=15,
            b_borr_choice_min=-40, b_borr_choice_max=0,
            b_save_choice_min=0, b_save_choice_max=40,
            graph=False, calc_loop=1):
        """ One state element, N choices
        """
        logger.debug('test_ulifetime_state_M_choice_N')

        """
        A. get mjalltest instance 
        """
        mjalltest_inst = self.MjallInst(combo_type=combo_type)

        '''
        A. Get Data        
        '''
        eps_tt_v, k_tt_v, b_tt_v, fb_f_max_btp_v, \
        K_borr_tp, B_borr_tp, K_save_tp, B_save_tp, \
        save_suffix_old = \
            self.gen_state_M_choice_N(combo_type, mjalltest_inst, states_dict,
                                      k_choice_min=k_choice_min, k_choice_max=k_choice_max,
                                      b_borr_choice_min=b_borr_choice_min,
                                      b_borr_choice_max=b_borr_choice_max,
                                      b_save_choice_min=b_save_choice_min,
                                      b_save_choice_max=b_save_choice_max)

        '''
        B. Reshape        
        '''
        if (choice_dim == 0):
            state_count = len(eps_tt_v)
            choice_count = len(K_borr_tp)

            eps_tt_v = np.reshape(np.repeat(eps_tt_v[:, None], choice_count, 1), (1, -1))
            k_tt_v = np.reshape(np.repeat(k_tt_v[:, None], choice_count, 1), (1, -1))
            b_tt_v = np.reshape(np.repeat(b_tt_v[:, None], choice_count, 1), (1, -1))
            fb_f_max_btp_v = np.reshape(np.repeat(fb_f_max_btp_v[:, None], choice_count, 1), (1, -1))

            K_borr_tp = np.reshape(np.repeat(K_borr_tp[None, :], state_count, 0), (1, -1))
            B_borr_tp = np.reshape(np.repeat(B_borr_tp[None, :], state_count, 0), (1, -1))
            K_save_tp = np.reshape(np.repeat(K_save_tp[None, :], state_count, 0), (1, -1))
            B_save_tp = np.reshape(np.repeat(B_save_tp[None, :], state_count, 0), (1, -1))

            save_suffix = '1c1c_' + save_suffix
            title_suffix = '1c1c ' + title_suffix

        else:
            eps_tt_v = np.reshape(eps_tt_v, (-1, 1))
            k_tt_v = np.reshape(k_tt_v, (-1, 1))
            b_tt_v = np.reshape(b_tt_v, (-1, 1))
            fb_f_max_btp_v = np.reshape(fb_f_max_btp_v, (-1, 1))

            state_count = len(eps_tt_v)

            if (choice_dim == 1):
                save_suffix = '1c1d_' + save_suffix
                title_suffix = '1c1d ' + title_suffix
            if (choice_dim == 2):
                K_borr_tp = np.repeat(K_borr_tp[None, :], state_count, 0)
                B_borr_tp = np.repeat(B_borr_tp[None, :], state_count, 0)
                K_save_tp = np.repeat(K_save_tp[None, :], state_count, 0)
                B_save_tp = np.repeat(B_save_tp[None, :], state_count, 0)
                save_suffix = '1c2d_' + save_suffix
                title_suffix = '1c2d ' + title_suffix

        '''
        C. Invoke
        len_states = 1 for gentics function
        '''
        looper = 0
        while (looper < calc_loop):
            looper = looper + 1
            utility_today_stack, \
            b_tp_principle_stack, consumption_stack, cash, y, \
            utility_future_stack, \
            b_tp_stack, \
            ulifetime = mjalltest_inst.invoke_mjall_inst(
                interpolant=interpolant,
                eps_tt=eps_tt_v,
                k_tt=k_tt_v,
                b_tt=b_tt_v,
                fb_f_max_btp=fb_f_max_btp_v,
                ib_i_ktp=K_borr_tp, is_i_ktp=K_save_tp, fb_f_ktp=K_borr_tp, fs_f_ktp=K_save_tp,
                ibfb_i_ktp=K_borr_tp, fbis_i_ktp=K_save_tp,
                none_ktp=K_save_tp,
                ibfb_f_imin_ktp=K_borr_tp, fbis_f_imin_ktp=K_borr_tp,
                ib_i_btp=B_borr_tp, is_i_btp=B_save_tp, fb_f_btp=B_borr_tp, fs_f_btp=B_save_tp,
                ibfb_i_btp=B_borr_tp, fbis_i_btp=B_save_tp,
                none_btp=B_save_tp,
                ibfb_f_imin_btp=B_borr_tp, fbis_f_imin_btp=B_borr_tp,
                solve=True,
                graph=graph, save_suffix=save_suffix, title_suffix=title_suffix)

        return ulifetime

    #     def test_ulifetime_equal(self):
    #         self.MjallInst(grid_a_type = 31)
    #         ulifetime_a = self.ulifetime_state1col_choice1dor2d(choice_dim=1, graph=True, calc_loop=1)
    #         self.MjallInst(grid_a_type = 32)
    #         ulifetime_b = self.ulifetime_state1col_choice1dor2d(choice_dim=1, graph=True, calc_loop=1)
    #         self.assertEqual(ulifetime_a.tolist(),
    #                          ulifetime_b.tolist(), '[M 1] x [N] = [M 1] x [M N]')

    #     def test_ulifetime_state1col_choice1d(self):
    #         self.MjallInst(grid_a_type = 31)
    #         self.ulifetime_state1col_choice1dor2d(choice_dim=1, graph=True, calc_loop=1)

    def test_ulifetime_state1col_choice2d(self):
        """
        Given state space point, and future = 0, what is the 
        utility surface? today, future utility? Does the choice set look right?
        """

        interpolant = None
        """2. Given Interpolant, Solve at specific States"""
        save_suffix = '201805161859'
        combo_type = ['a', '20180512_mjalltest']
        # combo_type = ['a', '2018051617'] has 3 states

        eps_tt = np.array([0, 0, 0])
        k_tt_v = np.array([10, 5, 3])
        b_tt_v = np.array([1, 10, 3])
        bmax_v = np.array([-1, -1.5, -2])
        states_dict = {'eps_tt': eps_tt, 'k_tt_v': k_tt_v, 'b_tt_v': b_tt_v,
                       'fb_f_max_btp_v': bmax_v}
        title_suffix = combo_type[1] + ' module ' + combo_type[0] + ' name=' + save_suffix
        self.ulifetime_state1col_choice1dor2d(combo_type=combo_type,
                                              states_dict=states_dict,
                                              interpolant=interpolant,
                                              save_suffix=save_suffix,
                                              title_suffix=title_suffix,
                                              graph=True, calc_loop=1)

    def test_interp_then_solveatstates(self):
        """
        Given state space point, and current interpolant, what is the 
        utility surface? today, future utility? Does the choice set look right?
        """

        """1. Solve for interpolant"""
        combo_type = ['a', '20180512_bench_nofc_J2']
        get_combo_list = paramcombo.get_combo(combo_type=combo_type)
        param_combo = get_combo_list[0]
        interpolant, __, __, __ = solu.solve_model(param_combo)

        """2. Given Interpolant, Solve at specific States"""
        save_suffix = '201805161814'
        combo_type = ['a', '20180512_mjalltest']
        # combo_type = ['a', '2018051617'] has 3 states

        eps_tt = np.array([0, 0, 0])
        k_tt_v = np.array([10, 5, 3])
        b_tt_v = np.array([1, 10, 3])
        bmax_v = np.array([-1, -1.5, -2])
        states_dict = {'eps_tt': eps_tt, 'k_tt_v': k_tt_v, 'b_tt_v': b_tt_v,
                       'fb_f_max_btp_v': bmax_v}
        title_suffix = combo_type[1] + ' module ' + combo_type[0] + ' name=' + save_suffix
        self.ulifetime_state1col_choice1dor2d(combo_type=combo_type,
                                              states_dict=states_dict,
                                              interpolant=interpolant,
                                              save_suffix=save_suffix,
                                              title_suffix=title_suffix,
                                              graph=True, calc_loop=1)

    #     def test_ulifetime_state1d_choice1d(self):


#         """
#         no graphs made, even if graph == True,
#         does not support graphing
#         """                
#         self.MjallInst(grid_a_type = 33)
#         self.ulifetime_state1col_choice1dor2d(choice_dim=0, graph=True, calc_loop=1)
#         
#     def test_speed_ulifetime_state1col_choice1d(self):     
#         self.MjallInst(grid_a_type = 41)
#         self.ulifetime_state1col_choice1dor2d(choice_dim=1, graph=False, calc_loop=30)
#           
#     def test_speed_ulifetime_state1col_choice2d(self):
#         self.MjallInst(grid_a_type = 42)
#         self.ulifetime_state1col_choice1dor2d(choice_dim=2, graph=False, calc_loop=30)    
#           
#     def test_speed_ulifetime_state1d_choice1d(self):        
#         self.MjallInst(grid_a_type = 43)
#         self.ulifetime_state1col_choice1dor2d(choice_dim=0, graph=False, calc_loop=30)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.WARNING, format=FORMAT)
    unittest.main()
