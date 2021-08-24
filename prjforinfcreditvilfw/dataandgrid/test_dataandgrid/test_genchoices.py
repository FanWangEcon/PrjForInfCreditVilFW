'''
Created on Feb 3, 2018

@author: fan
'''
import unittest
import logging

import projectsupport.systemsupport as proj_sys_sup

import pyfan.graph.generic.allpurpose as grh_sup
import pylab as pylab

import dataandgrid.genchoices as genchoices
import modelhh.functions.constraints as constraints
import numpy as np

import projectsupport.graph.choices_i_eachj_polygon as choices_ieachj_poly

logger = logging.getLogger(__name__)


class TestChoices(unittest.TestCase):

    def setUp(self):
        logger.debug('setUp module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test', sub_folder_name='test_genchoices')

    def tearDown(self):
        logger.debug('teardown module')

    def test_gen_choices(self,
                         cash=np.array([14]),
                         k_tt=np.array([10]),
                         len_choices=200,
                         R_INFORM=1.10,
                         R_FORMAL_BORR=1.05,
                         R_FORMAL_SAVE=1.01,
                         DELTA_DEPRE=0.1, borr_constraint_KAPPA=0.4,
                         BNF_SAVE_P=1, BNF_SAVE_P_startVal=0.5,
                         BNF_BORR_P=4, BNF_BORR_P_startVal=-2,
                         BNI_LEND_P=5, BNI_LEND_P_startVal=3,
                         BNI_BORR_P=2, BNI_BORR_P_startVal=-1,
                         choice_set_list=[0, 1, 102, 3, 104, 105, 6],
                         K_interp_range={'K_max': 100},
                         B_interp_range={'B_max': 100},
                         graph=True, save_suffix=''):
        """        
        """

        '''
        Save Name
        '''
        if (hasattr(cash, '__len__')):
            c_cash_str = 'c' + str(len(cash)) + 'k' + str(len(k_tt))
        else:
            c_cash_str = 'c' + str((cash)) + 'k' + str((k_tt))

        save_suffix = save_suffix + c_cash_str + \
                      'Km' + str(int(K_interp_range['K_max'])) + \
                      'Bm' + str(int(B_interp_range['B_max'])) + \
                      'Ri' + str(int(R_INFORM * 100)) + \
                      'Rb' + str(int(R_FORMAL_BORR * 100)) + \
                      'Rs' + str(int(R_FORMAL_SAVE * 100)) + \
                      'Fb' + str(int(BNF_BORR_P)) + \
                      'b' + str(int(BNF_BORR_P_startVal)) + \
                      'Ib' + str(int(BNI_BORR_P)) + \
                      'b' + str(int(BNI_BORR_P_startVal)) + \
                      'Fs' + str(int(BNF_SAVE_P)) + \
                      's' + str(int(BNF_SAVE_P_startVal)) + \
                      'Is' + str(int(BNI_LEND_P)) + \
                      's' + str(int(BNI_LEND_P_startVal)) + \
                      'DD' + str(int(DELTA_DEPRE * 10)) + \
                      'KK' + str(int(borr_constraint_KAPPA * 10))

        '''
        Choice Set
        '''
        fb_f_max_btp = constraints.get_borrow_constraint(borr_constraint_KAPPA, k_tt, R_FORMAL_BORR)

        'A. Generate Choice Vectors'
        all_minmax, \
        ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
        ibfb_i_ktp, fbis_i_ktp, \
        none_ktp, \
        ibfb_f_imin_ktp, fbis_f_imin_ktp, \
        ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
        ibfb_i_btp, fbis_i_btp, \
        none_btp, \
        ibfb_f_imin_btp, fbis_f_imin_btp = \
            genchoices.choices_kb_each(
                len_choices=len_choices,
                cont_choice_count=2,
                cash=cash,
                k_tt=k_tt,
                fb_f_max_btp=fb_f_max_btp,
                R_INFORM=R_INFORM, R_FORMAL_BORR=R_FORMAL_BORR, R_FORMAL_SAVE=R_FORMAL_SAVE,
                DELTA_DEPRE=DELTA_DEPRE, borr_constraint_KAPPA=borr_constraint_KAPPA,
                BNF_SAVE_P=BNF_SAVE_P, BNF_SAVE_P_startVal=BNF_SAVE_P_startVal,
                BNF_BORR_P=BNF_BORR_P, BNF_BORR_P_startVal=BNF_BORR_P_startVal,
                BNI_LEND_P=BNI_LEND_P, BNI_LEND_P_startVal=BNI_LEND_P_startVal,
                BNI_BORR_P=BNI_BORR_P, BNI_BORR_P_startVal=BNI_BORR_P_startVal,
                choice_set_list=choice_set_list,
                K_interp_range=K_interp_range,
                B_interp_range=B_interp_range
            )

        '''
        Grapher
        '''
        saveDirectory = self.saveDirectory
        saveFileName = 'choice_' + save_suffix
        title = 'cash and k = ' + c_cash_str

        choices_ieachj_poly.graph_i_polygon_j(
            choice_set_list,
            saveDirectory, saveFileName, title,
            ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
            ibfb_i_ktp, fbis_i_ktp, \
            none_ktp, \
            ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
            ibfb_i_btp, fbis_i_btp, \
            none_btp)

    def test_minmax_multistates(self):
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='MultiStates')

        """Change Formal Borrowing Interest
        """
        save_suffix = '_cash_'
        k_tt = np.linspace(20, 50, 5)
        cash = k_tt + np.linspace(10, 30, 5)
        #         k_tt = np.array([10])
        #         cash = np.array([20])
        self.test_gen_choices(
            cash=cash,
            k_tt=k_tt,
            save_suffix=save_suffix)

    def test_choice_sets(self):

        #         choice_set_list_list = [[0,1,102,3,6],
        #                                 [0,1,102,3,104,105,6]]
        choice_set_list_list = [[0, 1, 102, 3, 104, 105, 6]]

        for choice_set_list in choice_set_list_list:
            self.minmax_loop_Kmax(choice_set_list)
            self.minmax_loop_R(choice_set_list)
            self.minmax_loop_Pecuniary_Cost(choice_set_list)
            self.minmax_loop_min_borr_save(choice_set_list)
            self.minmax_loop_depreciate_collatearl(choice_set_list)

    def minmax_loop_Kmax(self, choice_set_list):

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='Kmax_J' + str(len(choice_set_list)))

        """Change Formal Borrowing Interest
        """
        save_suffix = '_Kmax_'
        K_interp_max_list = [100, 50, 15]
        B_interp_max_list = [30, 10]
        for K_interp_max in K_interp_max_list:
            for B_interp_max in B_interp_max_list:
                self.test_gen_choices(
                    R_INFORM=1.20,
                    R_FORMAL_BORR=1.10,
                    R_FORMAL_SAVE=1.03,
                    BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                    BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                    BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                    BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                    choice_set_list=choice_set_list,
                    save_suffix=save_suffix,
                    K_interp_range={'K_max': K_interp_max},
                    B_interp_range={'B_max': B_interp_max})

    def minmax_loop_R(self, choice_set_list):
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='Interest_J' + str(len(choice_set_list)))

        """Change Formal Borrowing Interest
        """
        save_suffix = '_R_FS_'
        R_FORMAL_SAVE_list = [1.15, 1.7, 1.02, 1.00]
        for R_FORMAL_SAVE in R_FORMAL_SAVE_list:
            self.test_gen_choices(
                R_INFORM=1.08,
                R_FORMAL_BORR=1.05,
                R_FORMAL_SAVE=R_FORMAL_SAVE,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        """Change Formal Borrowing Interest
        """
        save_suffix = '_R_FB_'
        R_FORMAL_BORR_list = [1.20, 1.10, 1.05, 1.00]
        for R_FORMAL_BORR in R_FORMAL_BORR_list:
            self.test_gen_choices(
                R_INFORM=1.08,
                R_FORMAL_BORR=R_FORMAL_BORR,
                R_FORMAL_SAVE=1.02,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        """Change Informal Interest Rate
        Higher Informal Rate expands savings triangle, reduces borrowing
        """
        save_suffix = '_R_I_'
        R_INFORM_list = [2.00, 1.55, 1.10]
        for R_INFORM in R_INFORM_list:
            self.test_gen_choices(
                R_INFORM=R_INFORM,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

    def minmax_loop_Pecuniary_Cost(self, choice_set_list):
        """Change Borrowing Fixed Cost
        
        For both formal and informal borrowing:
            pushes down top left and top right of triangle
        
        higher fixed cost reduces coh available, reduces the borrowing multiplier.        
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='FixedCost_J' + str(len(choice_set_list)))

        save_suffix = '_P_FB_'
        BORR_P_list = [0.5, 2, 3.5, 10]
        for BORR_P in BORR_P_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=1,
                BNF_BORR_P=BORR_P, BNF_BORR_P_startVal=-1,
                BNI_LEND_P=0, BNI_LEND_P_startVal=1,
                BNI_BORR_P=0, BNI_BORR_P_startVal=-1,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_P_IB_'
        BORR_P_list = [10, 3.5, 2, 0.5]
        for BORR_P in BORR_P_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=1,
                BNF_BORR_P=0, BNF_BORR_P_startVal=-1,
                BNI_LEND_P=0, BNI_LEND_P_startVal=1,
                BNI_BORR_P=BORR_P, BNI_BORR_P_startVal=-1,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_P_FS_'
        SAVE_P_list = [0.5, 2, 3.5, 10]
        for SAVE_P in SAVE_P_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=SAVE_P, BNF_SAVE_P_startVal=1,
                BNF_BORR_P=0, BNF_BORR_P_startVal=-1,
                BNI_LEND_P=0, BNI_LEND_P_startVal=1,
                BNI_BORR_P=0, BNI_BORR_P_startVal=-1,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_P_IS_'
        SAVE_P_list = [0.5, 2, 3.5, 10]
        for SAVE_P in SAVE_P_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=1,
                BNF_BORR_P=0, BNF_BORR_P_startVal=-1,
                BNI_LEND_P=SAVE_P, BNI_LEND_P_startVal=1,
                BNI_BORR_P=0, BNI_BORR_P_startVal=-1,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_P_FBIS_'
        BORR_P_list = [1, 3.5, 6]
        SAVE_P_list = [1, 3.5, 6]
        for BORR_P in BORR_P_list:
            for SAVE_P in SAVE_P_list:
                self.test_gen_choices(
                    R_INFORM=1.20,
                    R_FORMAL_BORR=1.20,
                    R_FORMAL_SAVE=1.01,
                    BNF_SAVE_P=0, BNF_SAVE_P_startVal=1,
                    BNF_BORR_P=BORR_P, BNF_BORR_P_startVal=-1,
                    BNI_LEND_P=SAVE_P, BNI_LEND_P_startVal=1,
                    BNI_BORR_P=0, BNI_BORR_P_startVal=-1,
                    choice_set_list=choice_set_list,
                    save_suffix=save_suffix)

    def minmax_loop_min_borr_save(self, choice_set_list):
        """Change Borrowing Fixed Cost
        
        For both formal and informal borrowing:
            pushes down top left and top right of triangle
        
        higher fixed cost reduces coh available, reduces the borrowing multiplier.        
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='MinB_J' + str(len(choice_set_list)))

        save_suffix = '_SV_FB_'
        BORR_SV_list = [-0.5, -2, -5, -10]
        for BORR_SV in BORR_SV_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.10,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=BORR_SV,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_SV_IB_'
        BORR_SV_list = [-0.5, -2, -5, -10]
        for BORR_SV in BORR_SV_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.10,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=BORR_SV,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_SV_FS_'
        SAVE_SV_list = [0.5, 2, 5, 10]
        for SAVE_SV in SAVE_SV_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.10,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=SAVE_SV,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_SV_IS_'
        SAVE_SV_list = [0.5, 2, 5, 10]
        for SAVE_SV in SAVE_SV_list:
            self.test_gen_choices(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.10,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=SAVE_SV,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_SV_FBIS_'
        BORR_P_list = [-1, -3.5, -6]
        SAVE_P_list = [1, 3.5, 6]
        for BORR_SV in BORR_P_list:
            for SAVE_SV in SAVE_P_list:
                self.test_gen_choices(
                    R_INFORM=1.20,
                    R_FORMAL_BORR=1.20,
                    R_FORMAL_SAVE=1.01,
                    BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                    BNF_BORR_P=2, BNF_BORR_P_startVal=BORR_SV,
                    BNI_LEND_P=4, BNI_LEND_P_startVal=SAVE_SV,
                    BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                    choice_set_list=choice_set_list,
                    save_suffix=save_suffix)

    def minmax_loop_depreciate_collatearl(self, choice_set_list):
        """Change Depreciation and Collateral
        
        Collateral determines formal borrowing amount (old collateral based on 
        current state, new collateral based on current choice, both in terms of K)        
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_genchoices',
            subsub_folder_name='DepColl_J' + str(len(choice_set_list)))

        save_suffix = '_DELTA_'
        DELTA_list = np.linspace(0, 1, 10)
        for DELTA_DEPRE in DELTA_list:
            self.test_gen_choices(
                DELTA_DEPRE=DELTA_DEPRE,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)

        save_suffix = '_KAPPA_'
        KAPPA_list = np.linspace(0, 1, 10)
        for borr_constraint_KAPPA in KAPPA_list:
            self.test_gen_choices(
                borr_constraint_KAPPA=borr_constraint_KAPPA,
                choice_set_list=choice_set_list,
                save_suffix=save_suffix)


if __name__ == '__main__':
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
