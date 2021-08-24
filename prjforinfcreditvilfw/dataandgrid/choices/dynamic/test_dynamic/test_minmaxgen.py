'''
Created on Dec 28, 2017

@author: fan
'''
import logging
import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import pylab as pylab
import unittest

import dataandgrid.choices.dynamic.minmaxgen as minmaxgen
import modelhh.functions.constraints as constraints
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


class TestMinMaxGen(unittest.TestCase):
    """
    The top right point for borrowing is not properly calculated in this testing
    tool. Actual genchoices.py code uses structure in minmaxfill.py with upper
    and lower slope to generate proper choice set.
    
    check out genchoices.py tester. 
    
    This is, for borrowing, only really testing lower right and upper left of triangle. 
    """

    def setUp(self):
        logger.debug('setUp module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxgen')

    def tearDown(self):
        logger.debug('teardown module')

    #                                cash=8, k_tt=3,
    #                                R_INFORM=1.30,
    #                                R_FORMAL_BORR=1.05,

    def test_minmax_eachchoice(self,
                               cash=8, k_tt=3,
                               R_INFORM=1.80,
                               R_FORMAL_BORR=1.40,
                               R_FORMAL_SAVE=1.01,
                               DELTA_DEPRE=0.1, borr_constraint_KAPPA=0.3,
                               BNF_SAVE_P=1, BNF_SAVE_P_startVal=0.5,
                               BNF_BORR_P=3, BNF_BORR_P_startVal=-2,
                               BNI_LEND_P=5, BNI_LEND_P_startVal=1.5,
                               BNI_BORR_P=2, BNI_BORR_P_startVal=-1,
                               graph=True, save_suffix=''):

        all_minmax = minmaxgen.minmax_eachchoice(
            cash, k_tt,
            R_INFORM, R_FORMAL_BORR, R_FORMAL_SAVE,
            DELTA_DEPRE, borr_constraint_KAPPA,
            BNF_SAVE_P, BNF_SAVE_P_startVal,
            BNF_BORR_P, BNF_BORR_P_startVal,
            BNI_LEND_P, BNI_LEND_P_startVal,
            BNI_BORR_P, BNI_BORR_P_startVal,
            choice_set_list=[0, 1, 102, 3, 4, 5, 6, 7])

        logger.debug('all_minmax:%s', all_minmax)

        if (graph):
            save_suffix = save_suffix + 'c' + str(cash) + \
                          'k' + str(k_tt) + \
                          'Ri' + str(int(R_INFORM * 100)) + \
                          'Rb' + str(int(R_FORMAL_BORR * 100)) + \
                          'Rs' + str(int(R_FORMAL_SAVE * 100)) + \
                          'Fb' + str(int(BNF_BORR_P)) + \
                          'Fb' + str(int(BNF_BORR_P_startVal)) + \
                          'Ib' + str(int(BNI_BORR_P)) + \
                          'Ib' + str(int(BNI_BORR_P_startVal)) + \
                          'Fs' + str(int(BNF_SAVE_P)) + \
                          'Fs' + str(int(BNF_SAVE_P_startVal)) + \
                          'Is' + str(int(BNI_LEND_P)) + \
                          'Is' + str(int(BNI_LEND_P_startVal))

            #                            'Fb'+str(int(BNF_BORR_P*10))+\
            #                            'Ib'+str(int(BNI_BORR_P*10))+\
            #                            'Fs'+str(int(BNF_SAVE_P*10))+\
            #                            'Is'+str(int(BNI_LEND_P*10))

            #                            'd'+str(int(DELTA_DEPRE*100))+\
            #                            'Kappa'+str(int(borr_constraint_KAPPA*100))

            save_suffix = save_suffix.replace(".", "")

            self.graph_minmaxgen(all_minmax,
                                 save_suffix=save_suffix, title_suffix='A')

    def test_minmax_loop_cash_vector(self, ):
        self.test_minmax_eachchoice(cash=5, k_tt=2)

    def test_minmax_loop_R(self):
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxgen',
            subsub_folder_name='Interest')

        """Change Formal Borrowing Interest
        """
        save_suffix = '_R_FS_'
        R_FORMAL_SAVE_list = [1.15, 1.7, 1.03, 1.00]
        for R_FORMAL_SAVE in R_FORMAL_SAVE_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.10,
                R_FORMAL_SAVE=R_FORMAL_SAVE,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        """Change Formal Borrowing Interest
        """
        save_suffix = '_R_FB_'
        R_FORMAL_BORR_list = [1.20, 1.10, 1.05, 1.00]
        for R_FORMAL_BORR in R_FORMAL_BORR_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=R_FORMAL_BORR,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        """Change Informal Interest Rate
        Higher Informal Rate expands savings triangle, reduces borrowing
        """
        save_suffix = '_R_I_'
        R_INFORM_list = [2.00, 1.55, 1.10]
        for R_INFORM in R_INFORM_list:
            self.test_minmax_eachchoice(
                R_INFORM=R_INFORM,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

    def test_minmax_loop_Pecuniary_Cost(self):
        """Change Borrowing Fixed Cost
        
        For both formal and informal borrowing:
            pushes down top left and top right of triangle
        
        higher fixed cost reduces coh available, reduces the borrowing multiplier.        
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxgen',
            subsub_folder_name='FixedCost')

        save_suffix = '_P_FB_'
        BORR_P_list = [0.5, 2, 3.5, 10]
        for BORR_P in BORR_P_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=BORR_P, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        save_suffix = '_P_IB_'
        BORR_P_list = [10, 3.5, 2, 0.5]
        for BORR_P in BORR_P_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=BORR_P, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        save_suffix = '_P_FS_'
        SAVE_P_list = [0.5, 2, 3.5, 10]
        for SAVE_P in SAVE_P_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=SAVE_P, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=0, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        save_suffix = '_P_IS_'
        SAVE_P_list = [0.5, 2, 3.5, 10]
        for SAVE_P in SAVE_P_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=0, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=0, BNF_BORR_P_startVal=0,
                BNI_LEND_P=SAVE_P, BNI_LEND_P_startVal=0,
                BNI_BORR_P=0, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

    def test_minmax_loop_min_borr_save(self):
        """Change Borrowing Fixed Cost
        
        For both formal and informal borrowing:
            pushes down top left and top right of triangle
        
        higher fixed cost reduces coh available, reduces the borrowing multiplier.        
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxgen',
            subsub_folder_name='MinB')

        save_suffix = '_SV_FB_'
        BORR_SV_list = [-0.5, -2, -5, -10]
        for BORR_SV in BORR_SV_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=BORR_SV,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        save_suffix = '_SV_IB_'
        BORR_SV_list = [-0.5, -2, -5, -10]
        for BORR_SV in BORR_SV_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=BORR_SV,
                save_suffix=save_suffix)

        save_suffix = '_SV_FS_'
        SAVE_SV_list = [0.5, 2, 5, 10]
        for SAVE_SV in SAVE_SV_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=SAVE_SV,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=0,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

        save_suffix = '_SV_IS_'
        SAVE_SV_list = [0.5, 2, 5, 10]
        for SAVE_SV in SAVE_SV_list:
            self.test_minmax_eachchoice(
                R_INFORM=1.20,
                R_FORMAL_BORR=1.20,
                R_FORMAL_SAVE=1.01,
                BNF_SAVE_P=1, BNF_SAVE_P_startVal=0,
                BNF_BORR_P=3, BNF_BORR_P_startVal=0,
                BNI_LEND_P=4, BNI_LEND_P_startVal=SAVE_SV,
                BNI_BORR_P=2, BNI_BORR_P_startVal=0,
                save_suffix=save_suffix)

    def graph_minmaxgen(self, all_minmax, save_suffix='', title_suffix=''):
        """
        Graphing, if satisfy requirement above
        """
        grapher = grh_sup.graphFunc()
        pylab.clf()
        # ===============================================================
        # fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')
        # loopColl = [[0,1],[2,3],[0,4],[1,5],[4,5],[0,1,2,3,4,5]]
        # axisList = [ax1,ax2,ax3,ax4,ax5,ax6]
        # ===============================================================

        fig, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10)) = \
            pylab.subplots(2, 5, sharex=True, sharey=True, figsize=(16, 10))
        # fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')
        loopColl = [[0, 1], [2, 3], [0, 2], [1, 3],
                    [0, 4], [1, 5], [4, 5], [7],
                    [6], [0, 1, 2, 3, 4, 5, 6]]
        axisList = [ax1, ax6, ax2, ax7, ax3, ax8, ax4, ax9, ax5, ax10]
        loopCollStr = ['inf', 'for', 'borr', 'save',
                       'ib fbib', 'is fbis', 'forinf', 'fb(cts)ib(min)', 'bed', 'all']

        '''
        Get Min Max Bounds
        '''
        all_k = []
        all_b = []
        for ctr_cur in [0, 1, 2, 3, 4, 5, 6, 7]:
            minmaxlist = all_minmax[ctr_cur]
            minKprime, maxKprime, minBprime, maxBprime, Y_minCst, _ = \
                minmax_list2tuple(minmaxlist)
            all_k.append(minKprime)
            all_k.append(maxKprime)
            all_b.append(minBprime)
            all_b.append(maxBprime)

        ylim = [np.minimum(np.min(all_k), -10), np.maximum(np.max(all_k), 40)]
        xlim = [np.minimum(np.min(all_b), -30), np.maximum(np.max(all_b), 15)]

        ylim = [np.min(all_k), np.max(all_k)]
        xlim = [np.min(all_b), np.max(all_b)]

        '''
        Draw Polygons
        '''
        for loopidx, loopCur in enumerate(loopColl):
            pylab.sca(axisList[loopidx])

            for ctr_cur in loopCur:
                minmaxlist = all_minmax[ctr_cur]
                minKprime, maxKprime, minBprime, maxBprime, Y_minCst, _ = \
                    minmax_list2tuple(minmaxlist)

                if (ctr_cur == 0 or ctr_cur == 2 or ctr_cur == 4 or ctr_cur == 7 or ctr_cur == 8):
                    polygon_path = borr_corners(
                        minKprime, maxKprime, minBprime, maxBprime, Y_minCst)

                else:
                    polygon_path = save_corners(
                        minKprime, maxKprime, minBprime, maxBprime)

                logger.debug('polygon_path:%s', polygon_path)

                xLabel = 'Bprime, min Bprimce:' + str(minBprime) + ', max Bprimce:' + str(maxBprime)
                yLabel = 'Kprime, max Kprimce:' + str(maxKprime) + ', min Kprimce:' + str(minKprime)

                #     pylab.ylim([np.min(yDataMat),np.max(yDataMat)])
                #     pylab.xlim([np.min(xData),np.max(xData)])
                grapher.xyPlotMultiYOneX(yDataMat=polygon_path,
                                         saveOrNot=False,
                                         graphType='polygon',
                                         basicTitle=loopCollStr[loopidx],
                                         ylim=ylim, xlim=xlim,
                                         basicXLabel='',
                                         basicYLabel='')

        """
        Aggregate Up Graphs
        """
        fig.subplots_adjust(wspace=0, hspace=0)
        fig.text(0.5, 0, 'B choice', ha='center')
        fig.text(0, 0.5, 'K choice', va='center', rotation='vertical')
        saveFileName = 'minmaxgen_poly' + save_suffix
        grapher.savingFig(saveDirectory=self.saveDirectory,
                          saveFileName=saveFileName,
                          saveDPI=200, pylabUse=fig)
        pylab.clf()
        fig.clf()


def borr_corners(kapitalnext_min, kapitalnext_max, borrow_B_min, borrow_B_max, Y_minCst,
                 k_tt=False,
                 DELTA_DEPRE=False, borr_constraint_KAPPA=False):
    '''
    b' on x-axis, borrowing negative, saving positive
    k' on-y axis, 
    '''

    'borrow_B_max add to cash minum fixed cost = k_prime max'
    upper_right = [borrow_B_max, Y_minCst - borrow_B_max]
    lower_right = [borrow_B_max, kapitalnext_min]

    if (k_tt):
        formal_borr_bound = constraints.get_borrow_constraint(borr_constraint_KAPPA, k_tt)
        borrow_B_min = np.max(formal_borr_bound, borrow_B_min)
        '''enough k_prime to enable borrow_B_min'''
        kapitalnext_max_lower = - borrow_B_min / (1 - DELTA_DEPRE)
    else:
        kapitalnext_max_lower = kapitalnext_max

    upper_left = [borrow_B_min, kapitalnext_max]
    lower_left = [borrow_B_min, kapitalnext_max_lower]

    return [lower_right, upper_right, upper_left, lower_left]


def save_corners(kapitalnext_min, kapitalnext_max, save_B_min, save_B_max):
    '''
    b' on x-axis, borrowing negative, saving positive
    k' on-y axis, 
    '''

    'borrow_B_max add to cash minum fixed cost = k_prime max'
    right = [save_B_max, kapitalnext_min]

    upper_left = [save_B_min, kapitalnext_max]
    lower_left = [save_B_min, kapitalnext_min]

    return [right, upper_left, lower_left]


def minmax_list2tuple(minmaxlist):
    [[[kapitalnext_min, kapitalnext_max], [B_min, B_max]], Y_minCst, RB] = minmaxlist

    return kapitalnext_min, kapitalnext_max, B_min, B_max, Y_minCst, RB


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
