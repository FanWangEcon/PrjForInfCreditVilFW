'''
Created on Jan 1, 2018

@author: fan

Most basic test, one state at a time, same choice grid all choices
'''

import unittest
import logging
import modelhh.test_modelhh.test_mjall as test_mjall
import numpy as np

logger = logging.getLogger(__name__)


class TestMjall_Scalar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.debug('setup class')
        cls.TestMjall_inst = test_mjall.TestMjall(grid_type=['a', 1],
                                                  esti_type=['a', 1])

    def setUp(self):
        logger.debug('setup module')

    def tearDown(self):
        logger.debug('teardown module')

    def test_ulifetime_zero(self):
        logger.debug('enter test_ulifetime_zero')
        self.TestMjall_inst.invoke_mjall_inst(
            solve=True)

    def test_ulifetime_one(self):
        logger.debug('enter test_ulifetime_one')
        self.TestMjall_inst.invoke_mjall_inst(
            ib_i_ktp=1, is_i_ktp=1, fb_f_ktp=1, fs_f_ktp=1,
            ibfb_i_ktp=1, fbis_i_ktp=1,
            none_ktp=1,
            ibfb_f_imin_ktp=1, fbis_f_imin_ktp=1,
            ib_i_btp=-1, is_i_btp=1, fb_f_btp=-1, fs_f_btp=1,
            ibfb_i_btp=-1, fbis_i_btp=1,
            none_btp=1,
            ibfb_f_imin_btp=-1, fbis_f_imin_btp=-1,
            solve=True)

    def test_ulifetime_rand(self):
        logger.debug('test_ulifetime_rand')
        np.random.seed(100)
        rd = 1 + (2 - 1) * np.random.rand(18)
        self.TestMjall_inst.invoke_mjall_inst(
            ib_i_ktp=rd[0], is_i_ktp=rd[1], fb_f_ktp=rd[2], fs_f_ktp=rd[3],
            ibfb_i_ktp=rd[4], fbis_i_ktp=rd[5],
            none_ktp=rd[6],
            ibfb_f_imin_ktp=rd[7], fbis_f_imin_ktp=rd[8],
            ib_i_btp=-rd[9], is_i_btp=rd[10], fb_f_btp=-rd[11], fs_f_btp=rd[12],
            ibfb_i_btp=-rd[13], fbis_i_btp=rd[14],
            none_btp=rd[15],
            ibfb_f_imin_btp=-rd[16], fbis_f_imin_btp=-rd[17],
            solve=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
