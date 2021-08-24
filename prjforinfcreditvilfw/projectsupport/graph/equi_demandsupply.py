'''
Created on May 21, 2018

@author: fan
'''

import logging
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')

logger = logging.getLogger(__name__)


def graph_demand_supply_interest(R_INFORM_BORR, aggregate_inf_borrow, aggregate_inf_save,
                                 title_display, image_save_name, image_folder):
    """
    Graph Demand and Supply curves for credit

    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/simu/a_20180517_quick'
    file_name = '_20180517_quick_A-150'
    csv_file_folder = directory + '/' + file_name + '.csv'
    
    image_folder = directory + '/' 
    image_save_name = file_name + '.png'
    dpi = 300
    title = file_name
            
    agg_steadysolu_pd = proj_sys_sup.read_csv(csv_file_folder)
    
    R_INFORM_BORR, aggregate_inf_borrow, aggregate_inf_save = \
        soluequiint.get_demand_supply_vec(agg_steadysolu_pd)
    """

    aggregate_inf_borrow_adj = np.log(-aggregate_inf_borrow + 1)
    aggregate_inf_save_adj = np.log(aggregate_inf_save + 1)
    plt.close('all')
    plt.figure()
    plt.grid()

    plt.scatter(R_INFORM_BORR, aggregate_inf_borrow_adj, s=1, c='blue', label='Credit Demand', alpha=1)
    plt.plot(R_INFORM_BORR, aggregate_inf_borrow_adj, c='blue', alpha=0.2)
    plt.scatter(R_INFORM_BORR, aggregate_inf_save_adj, s=1, c='red', label='Credit Supply', alpha=1)
    plt.plot(R_INFORM_BORR, aggregate_inf_save_adj, c='red', alpha=0.2)

    plt.xlabel('Informal Interest Rate', fontsize=8)
    plt.ylabel('log(Aggregate Credit Demand Supply+1)', fontsize=8)
    plt.suptitle('Equilibrium Interest Rate', fontsize=10)
    plt.title(title_display, fontsize=8)

    plt.legend(fontsize=6)
    proj_sys_sup.save_img(plt, image_folder + image_save_name,
                          dpi=300)
    plt.clf()
