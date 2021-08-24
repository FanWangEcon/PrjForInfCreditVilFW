'''
Created on Dec 31, 2017

@author: fan
'''
import logging
import pyfan.graph.generic.allpurpose as grh_sup
import unittest

import dataandgrid.choices.dynamic.minmaxfill as minmaxfill
import dataandgrid.choices.fixed.tics as policytics
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


class TestMinMaxFill(unittest.TestCase):

    def setUp(self):
        logger.debug('setup module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxfill')

        len_states = 10
        len_shocks = 1
        len_choices = 200
        cont_choice_count = 2

        choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints = \
            policytics.gentics(len_states=len_states,
                               len_shocks=len_shocks,
                               len_choices=len_choices,
                               cont_choice_count=cont_choice_count)

        self.K_tics = choicegrid_tics_mat[:, 0]
        self.B_tics = choicegrid_tics_mat[:, 1]

    def tearDown(self):
        logger.debug('teardown module')

    def test_minmax_fill(self,
                         K_min=1, K_max=20,
                         B_min=-20, B_max=-2,
                         upper_slope=-0.9,
                         Borrow=True,
                         B_bound=False,
                         K_interp_range={'K_max': 21},
                         B_interp_range={'B_max': 21},
                         graph=True,
                         save_suffix=''):

        if (Borrow):
            K_vec, B_vec, lower_slope = minmaxfill.minmax_fill_borrow_triangle(
                K_min=K_min, K_max=K_max, K_tics=self.K_tics,
                B_min=B_min, B_max=B_max, B_tics=self.B_tics,
                upper_slope=upper_slope, B_bound=B_bound,
                K_interp_range=K_interp_range)

            graph = minmaxfill.catch_minmax_fill_borrow_lowerupper(lower_slope, upper_slope)

        else:
            K_vec, B_vec = minmaxfill.minmax_fill_save_triangle(
                K_min=K_min, K_max=K_max, K_tics=self.K_tics,
                B_min=B_min, B_max=B_max, B_tics=self.B_tics,
                K_interp_range=K_interp_range, B_interp_range=B_interp_range)

        if (graph):
            save_suffix = save_suffix + \
                          'Bd' + str(B_bound * -10) + \
                          'kbmx' + str(K_interp_range['K_max']) + 'a' + str(B_interp_range['B_max']) + \
                          'ki' + str(K_min) + \
                          'ka' + str(K_max) + \
                          'Ri' + str(B_min * -1) + \
                          'Rb' + str(B_max * -1) + \
                          'Fb' + str(int(upper_slope * -100))

            save_suffix = save_suffix.replace(".", "")

            self.graph_minmaxfill(K_vec, B_vec,
                                  save_suffix=save_suffix,
                                  title_suffix=save_suffix)

    def test_minmax_fill_borrow_quadrilateral(self):
        """Test if there is constraint
        """

        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test', sub_folder_name='test_minmaxfill',
            subsub_folder_name='borr')
        self.minmax_fill_borrow_triangle_loop(B_bound=False)

        for B_bound in [-1.5, -5, -10]:
            #         for B_bound in [-5, -10]:
            self.saveDirectory = proj_sys_sup.get_paths(
                'model_test', sub_folder_name='test_minmaxfill',
                subsub_folder_name='borr_bd')

            self.minmax_fill_borrow_triangle_loop(B_bound=B_bound, save_suffix='bnd_')

    def minmax_fill_borrow_triangle_loop(self, B_bound=False, save_suffix=''):

        for K_max in [5, 13, 25]:
            #         for K_max in [5, 13]:
            for B_min in [-5, -13, -25]:
                save_suffix_use = save_suffix + 'KmaxBmin_'
                self.test_minmax_fill(K_max=K_max,
                                      B_min=B_min,
                                      B_bound=B_bound,
                                      save_suffix=save_suffix_use)

        '''Adjust B_max adjusts lower_slope, two points determine lower slope'''
        for B_max in [-5, -3, 0]:
            for upper_slope in [-0.3, -0.6 - 0.9]:
                save_suffix_use = save_suffix + 'SLOPE_'
                self.test_minmax_fill(upper_slope=upper_slope,
                                      B_max=B_max,
                                      B_bound=B_bound,
                                      save_suffix=save_suffix_use)

        '''Adjust K_interp_range'''
        K_interp_range = {'K_max': 21}
        for K_max in [5, 10, 15, 20, 25]:
            save_suffix_use = save_suffix + 'Kmax_'
            K_interp_range['K_max'] = K_max
            self.test_minmax_fill(B_bound=B_bound,
                                  K_interp_range=K_interp_range,
                                  save_suffix=save_suffix_use)

    def test_minmax_fill_save_triangle_loop(self, save_suffix=''):

        logger.debug('setup module')
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_minmaxfill',
            subsub_folder_name='save')
        #
        #         for K_max in [5, 13, 25]:
        #                 save_suffix_use = save_suffix + 'save_KmaxBmin_'
        #                 self.test_minmax_fill(Borrow=False,
        #                                       K_max=K_max, B_min=1, B_max=20,
        #                                       save_suffix=save_suffix_use)
        #
        #         for B_max in [20, 15, 10]:
        #             for B_min in [1, 2, 3]:
        #                 save_suffix_use = save_suffix + 'save_BmaxBmin_'
        #                 self.test_minmax_fill(Borrow=False,
        #                                       B_min=B_min, B_max=B_max,
        #                                       save_suffix=save_suffix_use)

        K_interp_range = {'K_max': 21}
        B_interp_range = {'B_max': 21}
        for K_interp_max in [10, 15, 25]:
            for B_interp_max in [7, 10]:
                K_interp_range = {'K_max': K_interp_max}
                B_interp_range = {'B_max': B_interp_max}
                save_suffix_use = save_suffix + 'save_IntpMax_'
                self.test_minmax_fill(Borrow=False,
                                      B_min=1, B_max=10,
                                      K_interp_range=K_interp_range,
                                      B_interp_range=B_interp_range,
                                      save_suffix=save_suffix_use)

    def graph_minmaxfill(self, K_vec, B_vec, save_suffix='', title_suffix=''):

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=K_vec, xData=B_vec, saveOrNot=True,
            showOrNot=False, graphType='scatter', scattersize=3,
            saveDirectory=self.saveDirectory,
            saveFileName='KB_prime_vals_' + save_suffix,
            basicTitle='K prime and B prime choices values' + title_suffix,
            basicXLabel='B prime', basicYLabel='K prime')

        pylabUse.clf()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    unittest.main()
