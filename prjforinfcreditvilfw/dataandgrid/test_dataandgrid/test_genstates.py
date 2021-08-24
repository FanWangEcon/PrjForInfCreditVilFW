'''
Created on Dec 21, 2017

@author: fan
'''

import unittest
import logging

import pyfan.devel.obj.classobjsupport as Clsobj_Sup

import modelhh.functions.test_functions.test_budget as test_bdgt
import dataandgrid.genstates as states

import pyfan.graph.generic.allpurpose as grh_sup

import projectsupport.systemsupport as proj_sys_sup

import numpy as np

logger = logging.getLogger(__name__)


class TestStates(unittest.TestCase):

    def setUp(self):
        logger.debug('setUp module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test', sub_folder_name='test_genstates')

    def tearDown(self):
        logger.debug('teardown module')

    def get_states_dep_inst(self,
                            len_states=27,
                            len_k_start=4,
                            max_kapital=10,
                            min_kapital=0.1,
                            max_netborrsave=3,
                            K_DEPRECIATION=0.1):
        """
        use this to mimic what value function evlauated at K and B would look like
        """

        test_bdgt_inst = test_bdgt.TestBudget()
        bdgt_inst = test_bdgt_inst.get_bdgt_inst(K_DEPRECIATION=K_DEPRECIATION)

        grid_param = {'len_states': len_states,
                      'len_k_start': len_k_start,
                      'max_kapital': max_kapital,
                      'min_kapital': min_kapital,
                      'max_netborrsave': max_netborrsave}

        attribute_array = ['grid_param']
        attribute_values_array = [grid_param]

        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)

        return bdgt_inst, param_inst

    def test_states_basic(self, len_states=27, len_k_start=4,
                          max_kapital=10,
                          min_kapital=0.1,
                          max_netborrsave=3,
                          K_DEPRECIATION=0.1):

        suf = 's' + str(len_states) + 'k' + str(len_k_start)
        bdgt_inst, param_inst = self.get_states_dep_inst(
            len_states=len_states, len_k_start=len_k_start,
            max_kapital=max_kapital,
            min_kapital=min_kapital,
            max_netborrsave=max_netborrsave,
            K_DEPRECIATION=K_DEPRECIATION)

        logger.debug('fixed_unif_grid=True')
        kapital_points, netborrsave_points = states.state_grids_fi(
            param_inst, bdgt_inst, fixed_unif_grid=True)
        self.graph_states(bdgt_inst, kapital_points, netborrsave_points,
                          save_suffix='_fixed' + suf,
                          title_suffix=' fixed_unif_grid=True ' + suf)

        logger.debug('fixed_unif_grid=False')
        kapital_points, netborrsave_points = states.state_grids_fi(
            param_inst, bdgt_inst, fixed_unif_grid=False, seed=1230)
        self.graph_states(bdgt_inst, kapital_points, netborrsave_points,
                          save_suffix='_rand' + suf,
                          title_suffix=' fixed_unif_grid=False ' + suf)

    def test_states_basic_loopsize(self):
        self.test_states_basic(len_states=1000, len_k_start=2)
        self.test_states_basic(len_states=4, len_k_start=2)
        for len_states in np.arange(20, 220, 50):
            for len_k_start in np.arange(5, 20, 5):
                if (len_states / 2 > len_k_start):
                    self.test_states_basic(len_states=len_states,
                                           len_k_start=len_k_start)

        for len_k_start in np.arange(20, 100, 10):
            self.test_states_basic(len_states=len_k_start ** 2,
                                   len_k_start=len_k_start,
                                   max_kapital=50,
                                   min_kapital=0,
                                   max_netborrsave=50,
                                   K_DEPRECIATION=0.08)

    def graph_states(self, bdgt_inst, K, B, save_suffix='', title_suffix=''):

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=K, xData=B, saveOrNot=True,
            showOrNot=False, graphType='scatter', scattersize=3,
            saveDirectory=self.saveDirectory,
            saveFileName='KB_states' + save_suffix,
            basicTitle='K and B States' + title_suffix,
            basicXLabel='B', basicYLabel='K')

        pylabUse.clf()

        cash = bdgt_inst.cash(Y=0, k_tt=K, b_tt=B)
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=K, xData=cash, saveOrNot=True,
            showOrNot=False, graphType='scatter', scattersize=3,
            saveDirectory=self.saveDirectory,
            saveFileName='KCOH_states' + save_suffix,
            basicTitle='K and B States' + title_suffix,
            basicXLabel='COH', basicYLabel='K')
        pylabUse.clf()


if __name__ == '__main__':
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
