'''
Created on Feb 26, 2018

@author: fan
'''

import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import pylab as pylab

import parameters.model.a_model as param_model_a


def graph_optimalChoice7Cates(choice_set_list,
                              x_var, y_var, z_discrete_var,
                              x_var_label, y_var_label, z_var_label,
                              title,
                              save_suffix, save_directory):
    x_min = np.min(x_var)
    x_max = np.max(x_var)
    x_max = x_max + (x_max - x_min) * 0.2

    y_min = np.min(y_var)
    y_max = np.max(y_var)

    grapher = grh_sup.graphFunc()
    pylab.clf()
    fig, ((ax1)) = pylab.subplots(1, 1, sharex=True, sharey=True)
    pylab.sca(ax1)

    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):
        cur_choice_j_idx = (z_discrete_var == choiceJ_counter)

        x_var_cur = x_var[cur_choice_j_idx]
        y_var_cur = y_var[cur_choice_j_idx]

        # ===============================================================
        # xData_coll.append(xData_thisMax)
        # yData_coll.append(yData_thisMax)
        # 
        # label_desc = label_coll.append(titleStringList[optiChoiceIdx])
        # ===============================================================

        choice_names = param_model_a.choice_index_names()['choice_names']
        label_string = choice_names[choiceJ_index]
        graphTitleDisp = title + '\n' + z_var_label
        grapher.xyPlotMultiYOneX(xData=x_var_cur, yDataMat=y_var_cur,
                                 saveOrNot=False, showOrNot=False,
                                 graphType='scatter', scattersize=10,
                                 labelArray=label_string, noLabel=False, labelLoc1t0=5,
                                 basicTitle=graphTitleDisp, basicXLabel=x_var_label, basicYLabel=y_var_label,
                                 xlim=[x_min, x_max], ylim=[y_min, y_max])

    saveFileName = 'opti7_' + save_suffix
    grapher.savingFig(saveDirectory=save_directory,
                      saveFileName=saveFileName,
                      saveDPI=200, pylabUse=fig)
    pylab.clf()
    fig.clf()
