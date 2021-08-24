'''
Created on Mar 25, 2018

@author: fan
'''
import logging
import numpy as np
import unittest

import dataandgrid.choices.dynamic.tics_nearest as ticsnear
import projectsupport.graph.optimal_continuous as opticts
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)
saveDirectory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_policyticsnear')


class TestPolicyTics(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_policytics')

    def tearDown(self):
        logger.debug('teardown module')

    def test_tics_multi(self):
        self.test_tics(get_tics_grid=100, func_type='a', tiltratio=0, intertiltratio=0)
        self.test_tics(get_tics_grid=100, func_type='b', tiltratio=0, intertiltratio=0)
        self.test_tics(get_tics_grid=49, func_type='a', tiltratio=0, intertiltratio=0)
        self.test_tics(get_tics_grid=49, func_type='b', tiltratio=0, intertiltratio=0)

        self.test_tics(get_tics_grid=100, func_type='a', tiltratio=0.5, intertiltratio=0)
        self.test_tics(get_tics_grid=100, func_type='b', tiltratio=0.5, intertiltratio=0)
        self.test_tics(get_tics_grid=49, func_type='a', tiltratio=0.5, intertiltratio=0)
        self.test_tics(get_tics_grid=49, func_type='b', tiltratio=0.5, intertiltratio=0)

        self.test_tics(get_tics_grid=100, func_type='a', tiltratio=0.5, intertiltratio=1)
        self.test_tics(get_tics_grid=100, func_type='b', tiltratio=0.5, intertiltratio=1)
        self.test_tics(get_tics_grid=49, func_type='a', tiltratio=0.5, intertiltratio=1)
        self.test_tics(get_tics_grid=49, func_type='b', tiltratio=0.5, intertiltratio=1)

    def test_tics(self, get_tics_grid=49, func_type='b', tiltratio=0.5, intertiltratio=1):

        value_list, choicegrid_list, max_val, max_idx, bound_box_index \
            = ticsnear.get_tics_grid(get_tics_grid, func_type, tiltratio, intertiltratio)

        logger.debug('max_val:\n%s', max_val)
        logger.debug('max_idx:\n%s', max_idx)
        logger.debug('bound_box_index:\n%s', bound_box_index)

        for ctr, (value, choicegrid) in enumerate(zip(value_list, choicegrid_list)):
            if (ctr == 0):
                x_var = choicegrid[:, 0]
                y_var = choicegrid[:, 1]
                z_data = np.ravel(value)
            else:
                x_var = np.concatenate((x_var, choicegrid[:, 0]))
                y_var = np.concatenate((y_var, choicegrid[:, 1]))
                z_data = np.concatenate((z_data, np.ravel(value)))

        x_var_label = 'k'
        y_var_label = 'b'
        save_suffix = '_f' + func_type + '_tics' + str(get_tics_grid) + \
                      '_t' + str(int(np.floor(tiltratio * 100))) + '_it' + str(int(np.floor(intertiltratio * 100)))
        opticts.graph_xyz_3D(x_var, y_var, z_data,
                             x_var_label, y_var_label, 'value',
                             graphTitleDisp='quadratic value 3d',
                             save_suffix=save_suffix,
                             subpath_img_save=saveDirectory,
                             angleType=[1, [1, 2, 3]])


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=np.nan)
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=3000)
    logging.basicConfig(filename=saveDirectory + '/logticsnear.py',
                        filemode='w',
                        level=logging.DEBUG, format=FORMAT)
    unittest.main()
