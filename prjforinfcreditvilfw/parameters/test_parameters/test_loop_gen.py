'''
@author: fan
'''
import logging
import numpy as np
import pyfan.amto.json.json as support_json
import unittest

import parameters.loop_param_combo_list.loops_gen as paramloop
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

save_directory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_params')

FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'

np.set_printoptions(precision=2, linewidth=100, suppress=True, threshold=3000)
logging.basicConfig(filename=save_directory + '/esti_start_points.py',
                    filemode='w',
                    level=logging.INFO, format=FORMAT)


class LoopGenTest(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_rand_start_points(self):
        param_group_key_list = ['esti_param.BNF_BORR_P', 'esti_param.BNF_BORR_P_ce0209',
                                'esti_param.BNF_BORR_P_ce9901']
        minmax_f = 'a'
        minmax_t = '20180917'
        param_vec_count = 36
        param_grid_or_rand = 'rand'
        param_list_coll, param_type_coll, param_name_coll, param_shortname_col = \
            paramloop.gen_initial_params(param_group_key_list, minmax_f, minmax_t, param_vec_count,
                                         param_grid_or_rand)

        support_json.jdump(param_list_coll, 'param_list_coll', logger=logger.info)
        support_json.jdump(param_type_coll, 'param_type_coll', logger=logger.info)
        support_json.jdump(param_name_coll, 'param_name_coll', logger=logger.info)
        support_json.jdump(param_shortname_col, 'param_shortname_col', logger=logger.info)


if __name__ == "__main__":
    unittest.main()
