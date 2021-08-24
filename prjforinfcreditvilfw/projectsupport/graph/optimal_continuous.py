'''
Created on Feb 26, 2018

@author: fan
'''

import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import pylab as pylab


def graph_optimal_continuous(x_var, y_var, c_var,
                             x_var_label, y_var_label, c_var_label,
                             title_display,
                             save_suffix, save_directory,
                             x_min=None, x_max=None, line45Deg=False):
    if (x_min is None):
        x_min = np.min(x_var)
    if (x_max is None):
        x_max = np.max(x_var)
        x_max = x_max + (x_max - x_min) * 0.2

    y_min = np.min(y_var)
    y_max = np.max(y_var)

    grapher = grh_sup.graphFunc()
    pylab.clf()
    fig, ((ax1)) = pylab.subplots(1, 1, sharex=True, sharey=True)
    pylab.sca(ax1)

    # ===============================================================
    # xData_coll.append(xData_thisMax)
    # yData_coll.append(yData_thisMax)
    # 
    # label_desc = label_coll.append(titleStringList[optiChoiceIdx])
    # ===============================================================
    grapher.xyPlotMultiYOneX(
        xData=x_var, yDataMat=y_var, colorVar=c_var,
        saveOrNot=False, showOrNot=False,
        graphType='scatter', scattersize=50,
        labelArray=str(c_var_label), noLabel=False, labelLoc1t0=5,
        basicTitle=title_display,
        basicXLabel=x_var_label,
        basicYLabel=y_var_label,
        line45Deg=line45Deg,
        xlim=[x_min, x_max], ylim=[y_min, y_max])

    saveFileName = 'opticts_x' + x_var_label.replace(" ", "") + \
                   '_y' + y_var_label.replace(" ", "") + \
                   '_c' + c_var_label.replace(" ", "") + \
                   save_suffix

    #     pylab.ylim(y_min, y_max)
    pylab.ylim(x_min, x_max)
    grapher.savingFig(saveDirectory=save_directory,
                      saveFileName=saveFileName,
                      saveDPI=200, pylabUse=fig)
    pylab.clf()
    fig.clf()


def graph_xyz_3D(xData, yData, zData,
                 x_var_label, y_var_label, zLabStr,
                 graphTitleDisp='', save_suffix='',
                 subpath_img_save='',
                 angleType=None):
    """Simplified Graph Function
    """

    if (angleType is None):
        angleType = [1, [1, 2, 3, 4, 5, 6]]

    saveFileName = 'opti3d_x' + x_var_label.replace(" ", "") + \
                   '_y' + y_var_label.replace(" ", "") + \
                   '_z' + zLabStr.replace(" ", "") + \
                   save_suffix

    graphTitleSave = subpath_img_save + saveFileName
    grh_sup.contourAnd3D(xData, yData, zData,
                         x_var_label, y_var_label, zLabStr,
                         graphTitleDisp, graphTitleSave,
                         savedpi=125, angleType=angleType,
                         drawContour=False, draw3D=True,
                         draw3DSurf=False,
                         contourXres=100, contourYres=100,
                         s=5, alpha=0.6)
