'''
Created on Dec 19, 2017

@author: fan
'''

import logging

import unittest

import numpy as np

import pyfan.amto.array.mesh as mesh
import pyfan.amto.array.gridminmax as gridminmax

import modelhh.future.future_polyquad as f_polyquad
import modelhh.future.future_loginf as f_loginf

import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.obj.classobjsupport as Clsobj_Sup

import modelhh.functions.test_functions.test_production as test_prod
import modelhh.functions.test_functions.test_preference as test_pref
import modelhh.functions.test_functions.test_budget as test_bdgt

logger = logging.getLogger(__name__)


class TestFuturPolyQuad(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_future_polyquad')

    def tearDown(self):
        logger.debug('teardown module')

    def get_future_polyquad_dep_inst(
            self,
            len_states, len_eps, len_eps_E,
            R_AVG_INT=1.10, beta=0.9, c_min_bound=0.01,
            alpha_k=0.3, rho=3,
            BNF_SAVE_P=1, BNF_BORR_P=4,
            BNI_LEND_P=5, BNI_BORR_P=2):
        """
        use this to mimic what value function evlauated at K and B would look like
        """
        esti_param = {'R_AVG_INT': R_AVG_INT, 'beta': beta, 'c_min_bound': c_min_bound}
        grid_param = {'len_states': len_states,
                      'len_eps': len_eps,
                      'len_eps_E': len_eps_E}
        attribute_array = ['esti_param', 'grid_param']
        attribute_values_array = [esti_param, grid_param]
        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)

        test_prod_inst = test_prod.TestProduction()
        prod_inst = test_prod_inst.get_prod_inst(alpha_k)

        test_crra_inst = test_pref.TestPreference()
        crra_inst = test_crra_inst.get_crra_inst(rho)

        test_bdgt_inst = test_bdgt.TestBudget()
        bdgt_inst = test_bdgt_inst.get_bdgt_inst(
            BNF_SAVE_P=BNF_SAVE_P, BNF_BORR_P=BNF_BORR_P,
            BNI_LEND_P=BNI_LEND_P, BNI_BORR_P=BNI_BORR_P)

        return prod_inst, crra_inst, param_inst, bdgt_inst

    def test_gen_B_K_E(self,
                       varB_min=-5, varB_max=5, varB_grid=3,
                       varK_min=0.1, varK_max=2, varK_grid=4,
                       varE_min=-0.2, varE_max=0.2, varE_grid=3,
                       eps_mean=0, eps_sd=0.5, eps_grid_count=100,
                       eps_gridtype='rand', eps_seed=433):
        a, b = gridminmax.three_vec_grids(
            vara_min=varB_min, vara_max=varB_max, vara_grid=varB_grid, vara_grid_add=None,
            varb_min=varK_min, varb_max=varK_max, varb_grid=varK_grid, varb_grid_add=None,
            gridtype='grid', tomesh=True,
            return_joint=False, return_single_col=True)
        B_Vepszr = a
        K_Vepszr = b
        BK_Vepszr = np.column_stack((B_Vepszr, K_Vepszr))
        logger.debug(['shape(B_Vepszr)', np.shape(B_Vepszr)])
        logger.debug(['shape(K_Vepszr)', np.shape(K_Vepszr)])
        logger.debug(['shape(B_Vepszr, K_Vepszr)', np.shape(np.column_stack((B_Vepszr, K_Vepszr)))])
        logger.debug(['B_Vepszr, K_Vepszr', np.column_stack((B_Vepszr, K_Vepszr))])

        a, b, c = gridminmax.three_vec_grids(
            vara_min=varB_min, vara_max=varB_max, vara_grid=varB_grid, vara_grid_add=None,
            varb_min=varK_min, varb_max=varK_max, varb_grid=varK_grid, varb_grid_add=None,
            varc_min=varE_min, varc_max=varE_max, varc_grid=varE_grid, varc_grid_add=None,
            gridtype='grid', tomesh=True,
            return_joint=False, return_single_col=True)
        B_V = a
        K_V = b
        eps_V = c
        logger.debug(['shape(B_V)', np.shape(B_V)])
        logger.debug(['shape(K_V)', np.shape(K_V)])
        logger.debug(['shape(eps_V)', np.shape(eps_V)])
        logger.debug(['shape(B_V, K_V, eps_V)', np.shape(np.column_stack((B_V, K_V, eps_V)))])
        logger.debug(['B_V, K_V, eps_V', np.column_stack((B_V, K_V, eps_V))])

        eps_grid = gridminmax.random_vector_mean_sd(
            eps_mean, eps_sd, eps_grid_count, eps_gridtype, eps_seed)
        BK_Veps, eps_Veps = mesh.two_mat_mesh(BK_Vepszr, eps_grid,
                                              return_joint=False)
        B_Veps = np.reshape(BK_Veps[:, 0], (-1, 1))
        K_Veps = np.reshape(BK_Veps[:, 1], (-1, 1))
        logger.debug(['shape(B_Veps)', np.shape(B_Veps)])
        logger.debug(['shape(K_Veps)', np.shape(K_Veps)])
        logger.debug(['shape(B_Veps, K_Veps, eps_Veps)', np.shape(np.column_stack((B_Veps, K_Veps, eps_Veps)))])
        logger.debug(['B_Veps, K_Veps, eps_Veps', np.column_stack((B_Veps, K_Veps, eps_Veps))])

        return B_V, K_V, eps_V, \
               B_Veps, K_Veps, eps_Veps, \
               B_Vepszr, K_Vepszr

    def test_interpolant_V_B_K_E(self,
                                 varB_min=-5, varB_max=5, varB_grid=3,
                                 varK_min=0.1, varK_max=2, varK_grid=4,
                                 varE_min=0, varE_max=0, varE_grid=1,
                                 A=1.0,
                                 R_AVG_INT=1.10, beta=0.9, c_min_bound=0.01,
                                 alpha_k=0.3, rho=3,
                                 BNF_SAVE_P=1, BNF_BORR_P=4,
                                 BNI_LEND_P=5, BNI_BORR_P=2):
        varB_grid = 3
        varK_grid = 4
        eps_grid_count = 100

        B_V, K_V, eps_V, \
        B_Veps, K_Veps, eps_Veps, \
        B_Vepszr, K_Vepszr = \
            self.test_gen_B_K_E(varB_grid=varB_grid,
                                varK_grid=varK_grid,
                                eps_grid_count=eps_grid_count)

        len_states = varB_grid * varK_grid
        len_eps = 1
        len_eps_E = eps_grid_count

        prod_inst, crra_inst, param_inst, bdgt_inst = \
            self.get_future_polyquad_dep_inst(
                len_states=len_states,
                len_eps=len_eps,
                len_eps_E=len_eps_E,
                R_AVG_INT=R_AVG_INT, beta=beta, c_min_bound=c_min_bound,
                alpha_k=alpha_k, rho=rho,
                BNF_SAVE_P=BNF_SAVE_P, BNF_BORR_P=BNF_BORR_P,
                BNI_LEND_P=BNI_LEND_P, BNI_BORR_P=BNI_BORR_P)

        utility_forever = f_loginf.future_loginf(
            prod_inst, crra_inst, param_inst,
            b_tp=B_V, k_tp=K_V, A=A, eps_tt=eps_V)

        EjV = utility_forever

        logger.debug(['shape(EjV, B_V, K_V, eps_V)', np.shape(np.column_stack((EjV, B_V, K_V, eps_V)))])
        logger.debug(['EjV, B_V, K_V, eps_V', np.column_stack((EjV, B_V, K_V, eps_V))])

        A_V = A
        A_Veps = A
        A_Vepszr = A
        eps_Vepszr = 0
        interpolant = None
        interpolant = f_polyquad.get_interpolant(interpolant,
                                                 bdgt_inst, prod_inst, param_inst,
                                                 EjV,
                                                 B_V, K_V, A_V, eps_V,
                                                 B_Veps, K_Veps, A_Veps, eps_Veps,
                                                 B_Vepszr, K_Vepszr, A_Vepszr, eps_Vepszr)

        return EjV, B_V, K_V


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s \n%(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
