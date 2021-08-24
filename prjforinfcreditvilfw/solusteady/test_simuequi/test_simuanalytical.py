'''
Created on Mar 27, 2018

@author: fanin
'''
import unittest

import logging

import numpy as np

import time
import projectsupport.systemsupport as proj_sys_sup
import projectsupport.datamanage.data_from_json as datajson
import parameters.combo as paramcombo
import solusteady.simuanalytical as simu_analytical
import analyze.analyzesteady as analyzesteady
import analyze.analyzesolu as analyzesolu
import projectsupport.graph.graph_sets as sup_graphset

logger = logging.getLogger(__name__)

save_directory = proj_sys_sup.get_paths('model_test', sub_folder_name='simu_ana_a')
combo_type = ['e', '20201025x']
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
# np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=np.nan)
np.set_printoptions(precision=2, linewidth=100, suppress=True, threshold=3000)
logging.basicConfig(filename=save_directory + '/logsimuanalytical_' + combo_type[1] + '.py',
                    filemode='w',
                    level=logging.WARNING, format=FORMAT)


class TestSimuInterp(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime

        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    def test_invoke(self):

        get_combo_list = paramcombo.get_combo(combo_type)
        counter = 0
        for param_combo in get_combo_list:
            counter = counter + 1
            print(counter)
            self.main_solu_steady(param_combo=param_combo)

        panda_df = datajson.json_to_panda(directory=save_directory,
                                          file_str='*' + combo_type[1] + '*')
        proj_sys_sup.save_panda(save_directory + combo_type[1] + '.csv', panda_df)

    def main_solu_steady(self, param_combo=None, max_of_J=True, weightJ=True):

        directory_str_dict = {'title': param_combo['title'],
                              'file_save_suffix': param_combo['file_save_suffix'],
                              'combo_desc': param_combo['combo_desc'],
                              'log': save_directory,
                              'csv': save_directory,
                              'json': save_directory,
                              'csv_detail': save_directory,
                              'img_detail': save_directory,
                              'img_detail_indi': save_directory}

        graph_list = sup_graphset.graph_panda_sets_names('all_solu_graphs_tables')
        solu_dict, mjall_inst, param_inst = simu_analytical.solve_policy(
            param_combo, directory_str_dict, graph_list)

        if (max_of_J):
            directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + '_maxJ'
            trans_prob, simu_output_pd, simu_moments_output = \
                simu_analytical.solve_dist(
                    param_combo, solu_dict, mjall_inst, param_inst,
                    max_of_J=True)
            analyzesteady.steady_graph_main(trans_prob, simu_output_pd,
                                            simu_moments_output, param_inst,
                                            directory_str_dict,
                                            graph_list=graph_list, export_json=True)

        if (weightJ):
            directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + '_wgtJ'
            trans_prob, simu_output_pd, simu_moments_output = \
                simu_analytical.solve_dist(
                    param_combo, solu_dict, mjall_inst, param_inst,
                    max_of_J=False)
            analyzesteady.steady_graph_main(trans_prob, simu_output_pd,
                                            simu_moments_output, param_inst,
                                            directory_str_dict,
                                            graph_list=graph_list, export_json=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
