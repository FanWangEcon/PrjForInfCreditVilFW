'''
Created on Dec 11, 2017

@author: fan
'''

import unittest
import modelhh.functions.test_functions.test_production as test_prod
import modelhh.functions.test_functions.test_preference as test_pref
import pyfan.devel.obj.classobjsupport as Clsobj_Sup
import modelhh.future.future_loginf as f_loginf
import projectsupport.systemsupport as proj_sys_sup
import pyfan.graph.generic.allpurpose as grh_sup
import numpy as np

import logging

logger = logging.getLogger(__name__)


class TestFutureLogInf(unittest.TestCase):

    def setUp(self):
        print("setup module")
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_future_loginf')

    def tearDown(self):
        print("teardown module")

    def get_future_loginf_dep_inst(
            self,
            R_AVG_INT=1.10, beta=0.9,
            alpha_k=0.3, rho=3):
        """
        use this to mimic what value function evlauated at K and B would look like
        """
        esti_param = {'R_AVG_INT': R_AVG_INT, 'beta': beta}
        attribute_array = ['esti_param']
        attribute_values_array = [esti_param]
        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)

        test_prod_inst = test_prod.TestProduction()
        prod_inst = test_prod_inst.get_prod_inst(alpha_k)

        test_crra_inst = test_pref.TestPreference()
        crra_inst = test_crra_inst.get_crra_inst(rho)

        return prod_inst, crra_inst, param_inst

    def test_future_loginf(
            self, A=1, b_tp=1, k_tp=2, eps_tt=0,
            R_AVG_INT=1.10, beta=0.9, alpha_k=0.3, rho=3):

        prod_inst, crra_inst, param_inst = \
            self.get_future_loginf_dep_inst(
                R_AVG_INT=R_AVG_INT, beta=beta,
                alpha_k=alpha_k, rho=rho)

        utility_forever = f_loginf.future_loginf(
            prod_inst, crra_inst, param_inst,
            b_tp=b_tp, k_tp=k_tp, A=A, eps_tt=eps_tt)

        logger.debug(['utility_forever', utility_forever])

        return utility_forever

    def test_future_loginf_btp(
            self, A=1, b_tp=np.linspace(-0.1, 1, 10), k_tp=2, eps_tt=0, rho=3):

        utility_forever = self.test_future_loginf(
            A=A, b_tp=b_tp, k_tp=k_tp, eps_tt=eps_tt, rho=rho)

        return utility_forever

    def test_future_loginf_rho(self):

        rho_list = np.linspace(-1, 3, 10)
        rho_list = np.sort(np.append(rho_list, 1))

        for rho_idx, rho in enumerate(rho_list):
            self.test_future_loginf_rho_btp_A(rho_idx + 1, rho=rho)

    def test_future_loginf_rho_btp_A(self, rho_idx=0, rho=3):

        b_tp_len = 100
        b_tp_list = np.linspace(-3, 3, b_tp_len)
        A_len = 5
        A_list = np.linspace(0.5, 1.5, A_len)

        utilforever_mat = np.zeros((b_tp_len, len(A_list)))
        for idx, A in enumerate(A_list):
            utilforever_mat[:, idx] = self.test_future_loginf_btp(
                A=A, b_tp=b_tp_list, rho=rho)

        '''
        Graph Results
        '''
        saveFileName = 'test_loginf_rhoidx' + str(rho_idx)

        labelArray = ['A=' + str(A) for A in A_list]
        title = 'loginf futureever utility, rho=' + str(rho)

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=utilforever_mat, xData=b_tp_list,
            saveOrNot=True, showOrNot=False, graphType='plot',
            labelArray=labelArray, noLabel=False,
            saveDirectory=self.saveDirectory,
            saveFileName=saveFileName,
            basicTitle=title,
            basicXLabel='b_tp level',
            basicYLabel='Future forever', saveDPI=250, toScale=False, sequential_color=True)
        pylabUse.clf()

    def test_future_loginf_eps(self):

        eps_list = np.linspace(-2, 2, 10)
        eps_list = np.sort(np.append(eps_list, 1))

        for eps_idx, eps in enumerate(eps_list):
            self.test_future_loginf_eps_btp_ktp(eps_idx + 1, eps=eps, A=2, rho=3)

    def test_future_loginf_eps_btp_ktp(self, eps_idx=0, eps=0, A=2, rho=3):

        k_tp_len = 100
        k_tp_list = np.linspace(0.25, 2, k_tp_len)

        b_tp_len = 5
        b_tp_list = np.linspace(-3, 3, b_tp_len)

        utilforever_mat = np.zeros((k_tp_len, len(b_tp_list)))

        for idx, b_tp in enumerate(b_tp_list):
            utilforever_mat[:, idx] = self.test_future_loginf_btp(
                A=A, b_tp=b_tp, k_tp=k_tp_list, eps_tt=eps, rho=rho)

        '''
        Graph Results
        '''
        saveFileName = 'test_loginf_epsidx' + str(eps_idx)

        labelArray = ['b_tp=' + str(b_tp) for b_tp in b_tp_list]
        title = 'loginf futureever utility, eps=' + str(eps)

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=utilforever_mat, xData=k_tp_list,
            saveOrNot=True, showOrNot=False, graphType='plot',
            labelArray=labelArray, noLabel=False,
            saveDirectory=self.saveDirectory,
            saveFileName=saveFileName,
            basicTitle=title,
            basicXLabel='k_tp level',
            basicYLabel='Future forever', saveDPI=250, toScale=False, sequential_color=True)
        pylabUse.clf()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
