'''
Created on Dec 21, 2017

@author: fan
'''

import logging
import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import unittest

import dataandgrid.choices.dynamic.minmaxfunc as minmaxfunc
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

saveDirectory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_minmaxfunc')


class TestMinMaxFunc(unittest.TestCase):

    def setUp(self):
        logger.debug('setUp module')
        self.saveDirectory = saveDirectory

    def tearDown(self):
        logger.debug('teardown module')

    def Atest_states_minmax_save(self, DELTA_DEPRE=0.1,
                                 Y_minCst=10,
                                 Bstart=1, RB=1.1, Z=None, RZ=None,
                                 graph=True):
        """
        Parameters
        ----------
        Bstart: float
            must be postiive, minimal savings            
        """

        self.test_states_minmax_borr(Save=True,
                                     DELTA_DEPRE=DELTA_DEPRE, Y_minCst=Y_minCst,
                                     Bstart=Bstart, RB=RB, Z=Z, RZ=RZ,
                                     graph=graph)

    def Atest_states_minmax_borr_wthZ(self, Z=-3, RZ=1.10):
        """Joint Formal Informal
        
        Save=False is joint formal and informal borrowing
        
        Save=True is joint formal borrowing and informal saving
        
        Parameters
        ----------
        Z: negative float
            this is the amount of max informal borrowing for joint for+inf borr
        RZ: float
            informal borrowing interest rate
        """

        Save = False
        Bstart = (-1) * 1  # min Borrowing if choose this category
        self.test_states_minmax_borr(Save=Save,
                                     DELTA_DEPRE=0.1, Y_minCst=10,
                                     Bstart=Bstart, RB=1.1,
                                     Z=-3, RZ=1.10,
                                     graph=True)

        Save = True
        Bstart = (+1) * 1  # min Savings if choose this category
        self.test_states_minmax_borr(Save=Save,
                                     DELTA_DEPRE=0.1, Y_minCst=10,
                                     Bstart=Bstart, RB=1.1,
                                     Z=Z, RZ=1.10,
                                     graph=True)

    def Atest_states_minmax_borr_minKcash(self):
        DELTA_DEPRE = 0.1
        Bstart = -0.2
        RB = 1.15
        Y_minCst = -4.73
        Z = -0.25
        RZ = 1.05
        self.test_states_minmax_borr(Save=False,
                                     DELTA_DEPRE=DELTA_DEPRE,
                                     Y_minCst=Y_minCst,
                                     Bstart=Bstart,
                                     RB=RB,
                                     Z=Z,
                                     RZ=RZ,
                                     graph=True)

    def test_states_inf_borrow(self, Z=None, RZ=None):
        """
        There are three possibles cases for borrowing:
        1. zero k' and b'
            + if FC is too high, higher than cash available
        2. one point of positive k' and negative b'
            + If minimal borrowing is too low, then borrow up to max feasible, but
            would still be below minimal borrowing for category 
        3. a grid of possible k' and b' 
            + a triangle of feasible values
            + lower Bstart (more negative), 
            
        We need to see correct graphs
        """

        for cur_loop in [1, 2, 3, 4, 5]:
            DELTA_DEPRE = 0.1
            RB = 1.15
            if (cur_loop == 1):
                'kp=0, bp=0'
                Bstart = 0
                Y_minCst = -1
                Suffix = '_IBcase1'
                title_suffix = 'Bstart=0, Y_minCst=-1'
            if (cur_loop == 2):
                'triangle starting at origin'
                Bstart = 0
                Y_minCst = 5
                Suffix = '_IBcase2a'
                title_suffix = 'Bstart=0, Y_minCst=5'
            if (cur_loop == 3):
                'triangle starting at Bstart -4 on the right'
                Bstart = -4
                Y_minCst = 5
                Suffix = '_IBcase2b'
                title_suffix = 'Bstart=-4, Y_minCst=5'
            if (cur_loop == 4):
                'single dot bp!=0, kp!=0'
                Bstart = -25
                Y_minCst = 5
                Suffix = '_IBcase3a'
                title_suffix = 'Bstart=-25, Y_minCst=5'
            if (cur_loop == 5):
                Bstart = -25
                Y_minCst = 0
                Suffix = '_IBcase3b'
                title_suffix = 'Bstart=-25, Y_minCst=0'

            self.Atest_states_minmax_borr(Save=False, Type='IB',
                                          Suffix=Suffix, title_suffix=title_suffix,
                                          DELTA_DEPRE=DELTA_DEPRE,
                                          Y_minCst=Y_minCst,
                                          Bstart=Bstart,
                                          RB=RB,
                                          Z=Z,
                                          RZ=RZ,
                                          graph=True)

    def Atest_states_minmax_borr(self, Save=False, Type='IB', Suffix='', title_suffix='',
                                 DELTA_DEPRE=0.1, Y_minCst=10, Bstart=-1, RB=1.1, Z=None, RZ=None,
                                 graph=True):
        """
        use this to mimic what value function evlauated at K and B would look like
        """

        [[[kapitalnext_min, kapitalnext_max], \
          [borrow_B_min, borrow_B_max]], Y_minCst, RB] = \
            minmax_KB_SaveBorrow(Type=Type,
                                 d=DELTA_DEPRE,
                                 Y_minCst=Y_minCst,
                                 Bstart=Bstart, RB=RB, Z=Z, RZ=RZ)

        logger.debug('\nkapitalnext_min:%s, kapitalnext_max:%s',
                     kapitalnext_min, kapitalnext_max)
        logger.debug('\nborrow_B_min:%s, borrow_B_max:%s',
                     borrow_B_min, borrow_B_max)
        logger.debug('Y_minCst:%s, RB:%s',
                     Y_minCst, RB)

        # Graphing: x-axis = b', y-axis = k', 4 points
        if (graph):
            B_vec = np.zeros((3, 1))
            K_vec = np.zeros((3, 1))
            if (Save):
                B_vec[0, 0], K_vec[0, 0] = borrow_B_min, kapitalnext_min
                B_vec[1, 0], K_vec[1, 0] = borrow_B_min, Y_minCst
                B_vec[2, 0], K_vec[2, 0] = borrow_B_max, kapitalnext_min
            else:
                B_vec[0, 0], K_vec[0, 0] = borrow_B_max, kapitalnext_min
                B_vec[1, 0], K_vec[1, 0] = 0, Y_minCst
                B_vec[2, 0], K_vec[2, 0] = borrow_B_min, kapitalnext_max
            #
            if (RZ is None):
                RZ = 0.0
            if (Z is None):
                Z = 0.0

            save_suffix = 'SB' + str(Save) + \
                          'C' + str(int(Y_minCst * 100)) + \
                          'd' + str(int(DELTA_DEPRE * 100)) + \
                          'bs' + str(-1 * Bstart) + \
                          'RB' + str(int(RB * 100)) + \
                          'Z' + str(Z) + \
                          'RZ' + str(int(RZ * 100)) + Suffix
            save_suffix = save_suffix.replace(".", "")

            self.graph_minmax(K_vec, B_vec,
                              save_suffix=save_suffix,
                              title_suffix=title_suffix)

        return kapitalnext_min, kapitalnext_max, \
               borrow_B_min, borrow_B_max, \
               Y_minCst, RB

    def graph_minmax(self, K, B, save_suffix='', title_suffix=''):

        y_min = min(K)
        y_max = max(K)
        if (y_min == y_max):
            y_min = y_min - 0.5
            y_max = y_max + 0.5
        y_lim = [y_min, y_max]

        x_min = min(B)
        x_max = max(B)
        if (x_min == x_max):
            x_min = x_min - 0.5
            x_max = x_max + 0.5
        x_lim = [x_min, x_max]

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=K, xData=B, saveOrNot=True,
            showOrNot=False, graphType='scatter', scattersize=3,
            saveDirectory=self.saveDirectory,
            saveFileName='kb_choice_minmax ' + save_suffix,
            basicTitle='show (0, Y_minCst) ' + title_suffix,
            basicXLabel='B choice min and max ',
            basicYLabel='K choice min and max',
            ylim=y_lim, xlim=x_lim)
        pylabUse.clf()


def minmax_KB_SaveBorrow(Type='IB', d=0.1, Y_minCst=0, Bstart=0, RB=0, Z=0, RZ=0):
    if (Type == 'IB'):
        return minmaxfunc.minmax_KB_Informal_Borrow(d, Y_minCst, Bstart, RB)
    else:
        return minmaxfunc.minmax_KB_Save(DELTA_DEPRE=d, Y_minCst=Y_minCst,
                                         Bstart=Bstart, RB=RB, Z=Z, RZ=RZ)
        return minmaxfunc.minmax_KB_Borrow(DELTA_DEPRE=d, Y_minCst=Y_minCst,
                                           Bstart=Bstart, RB=RB, Z=Z, RZ=RZ)


if __name__ == '__main__':
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    np.set_printoptions(precision=3, linewidth=100, suppress=True, threshold=3000)
    logging.basicConfig(filename=saveDirectory + '/logminmaxfunc.py',
                        filemode='w',
                        level=logging.DEBUG, format=FORMAT)
    unittest.main()
