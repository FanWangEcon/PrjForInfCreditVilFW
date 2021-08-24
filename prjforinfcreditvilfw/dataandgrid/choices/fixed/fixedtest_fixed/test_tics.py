'''
Created on Dec 28, 2017

@author: fan
'''
import logging
import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import unittest

import dataandgrid.choices.fixed.tics as tics
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)
saveDirectory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_tics')


class TestPolicyTics(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_tic_kb_count(self):
        for len_choices in np.arange(10, 100):
            logger.debug('')
            logger.debug('len_choices:%s', len_choices)
            tics.gentics_KB_count(len_choices=len_choices)

    def test_policytics(self,
                        len_states=2,
                        len_shocks=1,
                        len_choices=250,
                        cont_choice_count=2,
                        k_choice_min=0, k_choice_max=1,
                        b_choice_min=0, b_choice_max=1,
                        graph=True,
                        save_suffix=''):

        choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints \
            = tics.gentics(len_states=len_states,
                           len_shocks=len_shocks,
                           len_choices=len_choices,
                           cont_choice_count=cont_choice_count,
                           k_choice_min=k_choice_min,
                           k_choice_max=k_choice_max,
                           b_choice_min=b_choice_min,
                           b_choice_max=b_choice_max)

        K_tp = choicegrid_tics_mat[:, 0]
        B_tp = choicegrid_tics_mat[:, 1]

        if (graph):
            save_suffix = save_suffix + \
                          'ki' + str(k_choice_min) + \
                          'ka' + str(k_choice_max) + \
                          'Bi' + str(b_choice_min) + \
                          'Ba' + str(b_choice_max) + \
                          'st' + str(len_states) + \
                          'sk' + str(len_shocks) + \
                          'ch' + str(len_choices) + \
                          'cs' + str(cont_choice_count)

            save_suffix = save_suffix.replace(".", "")

            self.graph_policytics(K_tp, B_tp,
                                  save_suffix=save_suffix,
                                  title_suffix=save_suffix)

    def test_states_basic_loopsize(self):
        save_suffix = '_size_'
        size_list_1 = np.arange(50, 200, 50)
        size_list_2 = np.arange(500, 4000, 500)
        size_list = np.sort(np.append(size_list_1, size_list_2))
        size_list = np.sort(np.append(size_list, [9, 10, 16, 20, 25, 30, 36, 40, 49, 64, 60, 70, 81, 90]))
        for len_choices in size_list:
            self.test_policytics(len_choices=len_choices, save_suffix=save_suffix)

        self.test_policytics(len_choices=16, save_suffix=save_suffix)

    def test_states_kb_minmax(self):

        save_suffix = '_kbmimx_'

        self.test_policytics(k_choice_min=3, k_choice_max=20,
                             b_choice_min=2, b_choice_max=10,
                             save_suffix=save_suffix)

        self.test_policytics(k_choice_min=3, k_choice_max=10,
                             b_choice_min=-10, b_choice_max=-1,
                             save_suffix=save_suffix)

    def graph_policytics(self, K_tp, B_tp, save_suffix='', title_suffix=''):

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=K_tp, xData=B_tp, saveOrNot=True,
            showOrNot=False, graphType='scatter', scattersize=3,
            saveDirectory=saveDirectory,
            saveFileName='KB_prime_tics' + save_suffix,
            basicTitle='K prime and B prime choices tics' + title_suffix,
            basicXLabel='B prime', basicYLabel='K prime')

        pylabUse.clf()


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=np.nan)
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=3000)
    logging.basicConfig(filename=saveDirectory + '/logtic.py',
                        filemode='w',
                        level=logging.DEBUG, format=FORMAT)
    unittest.main()
