'''
Created on Dec 5, 2017

@author: fan

Relationship: A, eps, and K
'''

import numpy as np
import pyfan.amto.array.mesh as simumesh
import pyfan.devel.obj.classobjsupport as Clsobj_Sup
import pyfan.graph.generic.allpurpose as grh_sup
import unittest
from scipy.stats import norm

import modelhh.functions.production as prod
import projectsupport.systemsupport as proj_sys_sup


class TestProduction(unittest.TestCase):

    def setUp(self):
        print("setup module")
        self.prod_inst = self.get_prod_inst()
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_production')

    def tearDown(self):
        print("teardown module")

    def get_prod_inst(self, alpha_k=0.3):

        esti_param = {'alpha_k': alpha_k}
        attribute_array = ['esti_param']
        attribute_values_array = [esti_param]
        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
        prod_inst = prod.ProductionFunction(param_inst)

        return prod_inst

    def test_output(self, epsilon=0, A=1, k=3):
        output = self.prod_inst.cobb_douglas_nolabor(epsilon, A, k, alphaed=False)
        return output

    def test_alpha_k(self, alpha_k=0.3):
        print('subtest_epsilon_A_k')
        self.prod_inst.alpha_k = alpha_k

        epsilon_percentile = np.linspace(0.25, 0.85, 3)
        sd = 0.5
        epsilon = sd * norm.ppf(epsilon_percentile)
        epsilon = np.reshape(epsilon, (-1, 1))

        A = np.linspace(1, 3, 2)
        A = np.reshape(A, (-1, 1))

        [A_m, epsilon_m] = simumesh.two_mat_mesh(A, epsilon, return_joint=False)

        k_len = 100
        k = np.linspace(0.0001, 5, k_len)

        output_mat = np.zeros((k_len, len(A_m)))
        for idx, (a, eps) in enumerate(zip(A_m, epsilon_m)):
            output_mat[:, idx] = self.test_output(eps, a, k)

        '''
        Graph Results
        '''
        #         saveDirectory = 'C:\\Users\\fan\\Documents\\Dropbox\\Programming\\PYTHON\\MathFunctions\\'
        labelArray = ['A=' + str(a) + ' e=' + str(eps)
                      for a, eps in zip(A_m, epsilon_m)]
        saveFileName = 'test_epsilon_A_alphak' + str('{0:g}'.format(round(alpha_k * 100)))

        title = 'Changing A and eps,' + \
                'Impact on Cobb-Douglas Prod Func, alpha_k=' + str(alpha_k)

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=output_mat, xData=k,
            saveOrNot=True, showOrNot=False, graphType='plot',
            labelArray=labelArray, noLabel=False,
            saveDirectory=self.saveDirectory,
            saveFileName=saveFileName,
            basicTitle=title,
            basicXLabel='Physical Capital K levels',
            basicYLabel='Output', saveDPI=150, toScale=False, sequential_color=True)
        pylabUse.clf()

    def test_epsilon_A_k(self):
        alpha_k_list = np.linspace(0.1, 0.5, 3)
        for alpha_k in alpha_k_list:
            self.test_alpha_k(alpha_k)


if __name__ == '__main__':
    unittest.main()
