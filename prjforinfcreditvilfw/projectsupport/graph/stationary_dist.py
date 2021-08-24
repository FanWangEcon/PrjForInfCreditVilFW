'''
Created on May 7, 2018

@author: fan
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')


def graph_transprob(discrete_cash, trans_prob,
                    title, image_folder, save_file_name, dpi=300, papertype='a4'):
    [discrete_cash_h_m, discrete_cash_v_m] = np.meshgrid(discrete_cash, discrete_cash)

    plt.close('all')
    plt.figure()
    plt.grid()

    sc = plt.scatter(discrete_cash_h_m, discrete_cash_v_m, c=trans_prob,
                     s=5, cmap=plt.cm.get_cmap('Reds'), alpha=1)

    plt.colorbar(sc)
    plt.plot(discrete_cash, discrete_cash, label='45', c='blue')
    plt.xlabel('Cash-On-Hand tomorrow', fontsize=8)
    plt.ylabel('Cash-On-Hand today', fontsize=8)
    plt.suptitle('Conditional Cash-on-Hand Transition Probability', fontsize=10)
    plt.title(title, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + save_file_name,
                          dpi=dpi, papertype=papertype)
    plt.clf()


def graph_marginal_dist(discrete_cash, marginal_dist, trans_prob,
                        title, image_folder, save_file_name, dpi=200, papertype='a4'):
    plt.close('all')
    plt.figure()
    plt.grid()

    plt.plot(discrete_cash, marginal_dist, 'r-', lw=5, alpha=0.6, label='marginal distribution')

    plt.xlabel('Cash-On-Hand Grid')
    plt.ylabel('Density')
    plt.suptitle('(Marginal) Cash-on-Hand Distribution', fontsize=10)
    plt.title(title, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + save_file_name,
                          dpi=dpi, papertype=papertype)
    plt.clf()
