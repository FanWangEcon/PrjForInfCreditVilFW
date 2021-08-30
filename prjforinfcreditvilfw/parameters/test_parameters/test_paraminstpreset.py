'''
@author: fan
'''
import logging
import unittest

import parameters.paraminstpreset as get_param_inst_preset

logger = logging.getLogger(__name__)


class Test(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_get_param_inst_cates(self):
        get_param_inst_preset.get_param_inst_preset()

    def test_get_param_inst_cates_update(self):
        state_count = 2
        choice_count = 3
        grid_dict = {'len_choices': state_count * choice_count,
                     'shape_choice': [state_count, choice_count]}
        grid = ['a', 1, grid_dict]  # [3,2] means choice_shape = [3,2]
        esti = ['a', 1]
        param_update_dict = {'grid_type': grid,
                             'esti_type': esti}
        title = 'Basic Friendly'
        get_param_inst_preset.get_param_inst_preset(
            param_update_dict=param_update_dict,
            title=title)

    def test_updatespecificparams(self):
        esti = ['a', 1, {'alpha_k': 1.2, 'logit_sd_scale': 2.3}]
        param_update_dict = {'esti_type': esti}
        title = 'Basic Friendly'
        get_param_inst_preset.get_param_inst_preset(
            param_update_dict=param_update_dict,
            title=title)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    unittest.main()
