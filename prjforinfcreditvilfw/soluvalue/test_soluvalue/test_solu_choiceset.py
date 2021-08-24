'''
Created on May 16, 2018

@author: fan
'''

import logging
import numpy as np
import time
import unittest

import analyze.analyzesolu as analyzesolu
import parameters.combo as paramcombo
import projectsupport.graph.graph_sets as sup_graphset
import projectsupport.systemsupport as proj_sys_sup
import soluvalue.solu as solu

save_directory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_solu_choice')
timesufx = '_' + proj_sys_sup.save_suffix_time()
timesufx = ''

logger = logging.getLogger(__name__)


class TestSolu(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.save_directory = save_directory
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    def test_combos_one(self):
        combo_type = ['e', '20201025x']

        get_combo_list = paramcombo.get_combo(combo_type)
        for param_combo in get_combo_list:
            self.solve_graph_main(param_combo=param_combo,
                                  title=param_combo['title'],
                                  file_save_suffix=param_combo['file_save_suffix'],
                                  combo_desc=param_combo['combo_desc'])

    def solve_graph_main(self, param_combo=None,
                         title='basic',
                         file_save_suffix='_basic',
                         combo_desc='basic'):
        directory_str_dict = {'title': title,
                              'file_save_suffix': file_save_suffix + timesufx,
                              'combo_desc': combo_desc,
                              'log': save_directory,
                              'csv': save_directory,
                              'csv_detail': save_directory,
                              'img_detail': save_directory,
                              'img_detail_indi': save_directory}

        graph_list = sup_graphset.graph_panda_sets_names('all_graphs_tables')
        interpolant, solu_dict, mjall_inst, param_inst = \
            solu.solve_model(param_combo=param_combo,
                             directory_str_dict=directory_str_dict,
                             graph_list=graph_list)
        analyzesolu.solve_graph_main(solu_dict, mjall_inst, param_inst, directory_str_dict,
                                     graph_list=graph_list)


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    np.set_printoptions(precision=2, linewidth=100, suppress=True, threshold=1000)
    logging.basicConfig(filename=save_directory + '/log_soluchoice' + timesufx + '.py',
                        filemode='w',
                        level=logging.DEBUG, format=FORMAT)
    unittest.main()
