'''
Created on Feb 18, 2018

@author: fan
'''

import logging
import numpy as np
import time
import unittest

import projectsupport.systemsupport as proj_sys_sup
import soluvalue.genmodel as genmodel

logger = logging.getLogger(__name__)

saveDirectory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_genmodel')
timesufx = '_' + proj_sys_sup.save_suffix_time()

FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
np.set_printoptions(precision=2, linewidth=100, suppress=True, threshold=1000)
logging.basicConfig(filename=saveDirectory + '/test_genmodel' + timesufx + '.py',
                    filemode='w',
                    level=logging.DEBUG, format=FORMAT)


class TestGenModel(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    #     def test_genmodelinst_default(self):
    #         grid_type = ['a',3]
    #         param_update_dict= {'grid_type':grid_type}
    #         param_combo = {'param_update_dict':param_update_dict}
    #         genmodel.gen_model_instances(param_combo)
    #
    #     def test_genmodelinst_five(self):
    #         """
    #         5 choices
    #         """
    #         param_update_dict= {'grid_type':['a', 3],
    #                             'esti_type':['a', 20180613],
    #                             'data_type':['b', 20180607],
    #                             'model_type':['a', 20180613]}
    #         param_combo = {'param_update_dict':param_update_dict}
    #         genmodel.gen_model_instances(param_combo)

    def test_genmodelinst_seven(self):
        """
        5 choices
        """
        param_update_dict = {'grid_type': ['a', 3],
                             'esti_type': ['a', 20180628],
                             'data_type': ['b', 20180607],
                             'model_type': ['a', 20180701]}
        param_combo = {'param_update_dict': param_update_dict}
        genmodel.gen_model_instances(param_combo)


if __name__ == "__main__":
    unittest.main()
