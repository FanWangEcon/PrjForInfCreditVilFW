'''
@author: fan
'''
import logging
import unittest

import parameters.combo as combos
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

save_directory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_combo')
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'

logging.basicConfig(
    filename=save_directory + '/log_test_combo.py',
    filemode='w',
    level=logging.INFO, format=FORMAT)


class TestCombo(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_1(self):
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        logger.info('start test_1')
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        combo_type = ['a', '20180403a']
        self.process_tests(combo_type=combo_type)
        combo_type = ['a', '20180404a']
        self.process_tests(combo_type=combo_type)
        combo_type = ['a', '20180417a']
        self.process_tests(combo_type=combo_type)

        # Previous Estimation Results depended on 20180918 and 20180925
        combo_type = ['c', '20180918']
        self.process_tests(combo_type=combo_type)

        combo_type = ['c', '20180925']
        self.process_tests(combo_type=combo_type)

    def test_2(self):
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        logger.info('start test_2')
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        combo_type = ['a', '20180607_A', ['data_param.A']]
        self.process_tests(combo_type=combo_type)
        combo_type = ['a', '20180607_alpha_k', ['esti_param.alpha_k']]
        self.process_tests(combo_type=combo_type)

    def test_3(self):
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        logger.info('start test_3')
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        combo_type = ['a', '20180607_lenstates', ['grid_param.len_states']]
        self.process_tests(combo_type=combo_type)
        combo_type = ['a', '20180607_lenmaxstd', ['grid_param.max_steady_coh']]
        self.process_tests(combo_type=combo_type)

    def process_tests(self, combo_type, compesti_specs=None):
        if compesti_specs is None:
            compesti_specs = combos.gen_compesti_spec()
        combos.get_combo(combo_type=combo_type, compesti_specs=compesti_specs)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
