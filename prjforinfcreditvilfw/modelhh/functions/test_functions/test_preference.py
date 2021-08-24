'''
Created on Dec 11, 2017

@author: fan
'''
import numpy as np
import pyfan.devel.obj.classobjsupport as Clsobj_Sup
import pyfan.graph.generic.allpurpose as grh_sup
import unittest

import modelhh.functions.preference as crra
import projectsupport.systemsupport as proj_sys_sup


class TestPreference(unittest.TestCase):

    def setUp(self):
        print("setup module")
        self.crra_inst = self.get_crra_inst()
        self.saveDirectory = proj_sys_sup.get_paths(
            'model_test',
            sub_folder_name='test_preference')

    def tearDown(self):
        print("teardown module")

    def get_crra_inst(self, rho=3.0, c_min_bound=0.01):
        esti_param = {'rho': rho, 'c_min_bound': c_min_bound}
        attribute_array = ['esti_param']
        attribute_values_array = [esti_param]

        param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
        crra_inst = crra.PeriodUtility(param_inst)

        return crra_inst

    def test_utility_consumption_crra(self, c=1.0):
        c = np.array(c)
        u_c = self.crra_inst.utility_consumption_crra(consumption=c)
        return u_c

    def test_rho(self):
        print("test_rho")

        c_len = 100
        consumption = np.linspace(0.2, 1.5, c_len)
        rho_list = np.linspace(-1, 3, 10)
        rho_list = np.sort(np.append(rho_list, 1))

        u_c_mat = np.zeros((c_len, len(rho_list)))
        for idx, rho in enumerate(rho_list):
            self.crra_inst.rho = rho
            u_c_mat[:, idx] = self.test_utility_consumption_crra(consumption)

        '''
        Graph Results
        '''
        saveFileName = 'test_rho'

        labelArray = ['rho=' + str(rho) for rho in rho_list]
        title = 'Changing consumption with different rho,' + \
                'Impact on CRRA utility'

        grapher = grh_sup.graphFunc()
        pylabUse = grapher.xyPlotMultiYOneX(
            yDataMat=u_c_mat, xData=consumption,
            saveOrNot=True, showOrNot=False, graphType='plot',
            labelArray=labelArray, noLabel=False,
            saveDirectory=self.saveDirectory,
            saveFileName=saveFileName,
            basicTitle=title,
            basicXLabel='Consumption Levels',
            basicYLabel='Output', saveDPI=150, toScale=False, sequential_color=True)
        pylabUse.clf()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
