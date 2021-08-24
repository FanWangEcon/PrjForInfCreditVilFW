'''
Created on Dec 15, 2017

@author: fan
'''
import logging
import numpy as np
import pyfan.devel.obj.classobjsupport as Clsobj_Sup
import unittest

import modelhh.functions.preflogit as lgit

logger = logging.getLogger(__name__)


class TestBudget(unittest.TestCase):

    def setUp(self):
        logger.debug('setUp module')
        self.lgit_inst = self.get_lgit_inst()

    def tearDown(self):
        logger.debug('teardown module')

    def get_lgit_inst(self, logit_sd_scale=2):
        esti_param = {'logit_sd_scale': logit_sd_scale}
        attribute_array = ['esti_param']
        attribute_values_array = [esti_param]

        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
        lgit_inst = lgit.MultinomialLogitU(param_inst)

        return lgit_inst

    def test_mlogit_onerow(self):
        all_J_indirect_utility = np.array([[1, 1, 1]])
        each_j_prob, optiV_Exp7 = self.lgit_inst.integrate_prob(all_J_indirect_utility)
        logger.debug(['optiV_Exp7', optiV_Exp7])
        self.assertEqual(np.sum(each_j_prob), 1, 'probability sums to 1')
        self.assertEqual(each_j_prob[0, 0] - each_j_prob[0, 1], 0, 'equal indirect u, equal prob, 0 1')
        self.assertEqual(each_j_prob[0, 1] - each_j_prob[0, 2], 0, 'equal indirect u, equal prob, 1 2')

    def test_mlogit_mat(self):
        all_J_indirect_utility = np.random.normal(0, 1, (3, 4))
        each_j_prob, optiV_Exp7 = self.lgit_inst.integrate_prob(
            all_J_indirect_utility)

        logger.debug(['optiV_Exp7', optiV_Exp7])

        prob_sum = np.sum(each_j_prob, 1)
        logger.debug(['prob_sum', prob_sum])

        self.assertAlmostEqual(sum(prob_sum - 1), 0, places=10, msg='probability sums to 1')

        for row in np.arange(1, np.shape(each_j_prob)[0]):
            '''
            Probability max index sequence should be the same as the utility max index
            sequence
            '''
            each_j_prob_row = each_j_prob[row, :]
            all_J_indirect_utility_row = all_J_indirect_utility[row, :]
            logger.debug(['row', row])
            logger.debug(['each_j_prob_row', each_j_prob_row])
            logger.debug(['all_J_indirect_utility_row', all_J_indirect_utility_row])
            max_prob_sort_idx = np.argsort(each_j_prob_row)
            max_u_sort_idx = np.argsort(all_J_indirect_utility_row)
            logger.debug(['row:', row, max_prob_sort_idx, max_u_sort_idx])
            self.assertListEqual(max_prob_sort_idx.tolist(),
                                 max_u_sort_idx.tolist(),
                                 'umax and pmax index index equal')


if __name__ == '__main__':
    import logging

    FORMAT = '%(filename)s - %(funcName)s -\n %(asctime)s - %(levelname)s  - %(message)s'
    FORMAT = '%(funcName)s - %(asctime)s - %(levelname)s  - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
