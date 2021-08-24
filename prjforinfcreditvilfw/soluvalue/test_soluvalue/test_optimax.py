'''
Created on Feb 26, 2018

@author: fan
'''
import logging
import numpy as np
import time
import unittest

import soluvalue.optimax as optimax

logger = logging.getLogger(__name__)


class TestOptiMax(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        logger.warning('%s: %s', self.id(), t)
        logger.debug('teardown module')

    def Atest_max_value_overJ_drop8(self):
        'Case 1: choice 7 (8 if 0=1) not a part of this'
        choice_set_list = [0, 1, 2, 3]
        util_opti_eachj = np.random.uniform(-2, 2, (5, 4))
        util_opti_eachj = optimax.max_value_overJ_drop8(util_opti_eachj, choice_set_list)
        logger.info("util_opti_eachj:%s", util_opti_eachj)

        'Case 1: choice 7 in weird spot'
        choice_set_list = [0, 1, 7, 5]
        util_opti_eachj = np.random.uniform(-2, 2, (5, 4))
        logger.info("util_opti_eachj:%s", util_opti_eachj)
        util_opti_eachj = optimax.max_value_overJ_drop8(util_opti_eachj, choice_set_list)
        logger.info("util_opti_eachj:%s", util_opti_eachj)

        'Case 1: choice 7 in final spot'
        choice_set_list = [0, 1, 2, 3, 4, 5, 6, 7]
        util_opti_eachj = np.random.uniform(-2, 2, (5, 8))
        logger.info("util_opti_eachj:%s", util_opti_eachj)
        util_opti_eachj = optimax.max_value_overJ_drop8(util_opti_eachj, choice_set_list)
        logger.info("util_opti_eachj:%s", util_opti_eachj)

    def test_max_value_overJ(self):
        'Case 1: choice 7 in final spot'
        choice_set_list = [0, 1, 2, 3, 4, 5, 6, 7]
        util_opti_eachj = np.random.uniform(-2, 2, (5, 8))
        logger.info("util_opti_eachj:%s", util_opti_eachj)
        util_opti_eachj = optimax.max_value_overJ(util_opti_eachj, choice_set_list)
        logger.info("util_opti_eachj:%s", util_opti_eachj)


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
