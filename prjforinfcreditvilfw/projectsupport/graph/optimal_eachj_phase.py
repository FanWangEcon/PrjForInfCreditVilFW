'''
Created on Apr 21, 2018

@author: fan

Can see dynamics from policy function, depending on were lines are with respect
to 45 degree line.
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import parameters.model.a_model as param_model_a
import parameters.paraminstpreset as get_param_inst_preset
import projectsupport.graph.optimal_maxj_policyphase as opti_dynamics
import projectsupport.systemsupport as proj_sys_sup
import solusteady.distribution.condidist_simu as condisimu

matplotlib.use('Agg')


def graph_phase_diagram_fromcsv(param_combo, data_folder, csv_file_name,
                                x_var_label, y_var_label,
                                title_display,
                                image_save_suffix, image_folder):
    #     csv_file = 'solu_'+combo_type[1]+'.csv'
    csv_file_folder = data_folder + csv_file_name + '.csv'
    solu_data_pd = proj_sys_sup.read_csv(csv_file_folder)

    param_inst = get_param_inst_preset.get_param_inst_preset_combo(param_combo)

    return graph_solu_dist(solu_data_pd, param_inst,
                           title_display,
                           image_save_suffix, image_folder)


def graph_solu_dist(solu_data_pd, param_inst,
                    title_display,
                    image_save_name, image_folder):
    """
    See Aiyagari 1994, Figure 2. These are suppose to to versions of those
    figures. For each of the J choices
    ---------------------------------------------
    -- Cash on Cash  -- Same j=1 -- Same j=2 
    -- Dist Tomorrow -- Same j=1 -- Same j=2 
    ---------------------------------------------
    -- Cash on Cash  -- Same j=3 -- Same j=4 
    -- Dist Tomorrow -- Same j=3 -- Same j=4 
    ---------------------------------------------
    """

    solu_data_pd = solu_data_pd.sort_values(by=['cash_tt'])

    """
    A. Get Relevant Parameters    
    """
    prob_cols = [col for col in solu_data_pd.columns if 'prob ' in col]
    kn_cols = [col for col in solu_data_pd.columns if 'kn ' in col]
    bn_cols = [col for col in solu_data_pd.columns if 'bn ' in col]
    cc_cols = [col for col in solu_data_pd.columns if 'cc ' in col]

    prb_matrix = solu_data_pd[prob_cols].to_numpy()
    ktp_matrix = solu_data_pd[kn_cols].to_numpy()
    btp_matrix = solu_data_pd[bn_cols].to_numpy()
    ccc_matrix = solu_data_pd[cc_cols].to_numpy()
    cash_tt = solu_data_pd[['cash_tt']].to_numpy()

    """
    B. Generate Variables
    """
    choice_set_list = param_inst.model_option['choice_set_list']
    cash_min = param_inst.grid_param['min_steady_coh']
    cash_max = param_inst.grid_param['max_steady_coh']
    choice_names_use = param_inst.model_option['choice_names_full_use']

    """
    """
    subplot_rows = 2
    subplot_cols = 4
    figsize = (16, 6)
    plt.close('all')
    plt.figure(figsize=figsize)

    for ctr, choicej in enumerate(choice_set_list):

        '''Get Policies'''
        btp = np.reshape(btp_matrix[:, ctr], (-1, 1))
        ktp = np.reshape(ktp_matrix[:, ctr], (-1, 1))

        '''Compute Distribution'''
        cash_partial_percentiles, \
        cashpartial_min, cashpartial_max, __, __ = \
            condisimu.aiyagari_fig2_data(param_inst, btp, ktp)

        '''Gen Graphs'''
        translate1t9 = param_model_a.choice_index_names()['translate1t9']

        ax = plt.subplot(subplot_rows, subplot_cols, translate1t9[choicej] + 1)
        ax.set_title(choice_names_use[ctr], fontsize=4)

        plt.grid()
        opti_dynamics.aiyagari_fig2_graph(ax, cash_tt,
                                          cashpartial_min, cashpartial_max,
                                          cash_partial_percentiles)

        '''Graphing Stuff'''
        x_label = 'coh today'
        y_label = 'distribution'
        plt.xlim(cash_min, cash_max)
        if (choicej == 1):
            plt.ylabel(y_label, fontsize=6)
        if (choicej == 2):
            pass
        if (choicej == 3):
            pass
        if (choicej == 4):
            pass
        if (choicej == 5):
            plt.xlabel(x_label, fontsize=6)
            plt.ylabel(y_label, fontsize=6)
        if (choicej == 6):
            plt.xlabel(x_label, fontsize=6)
        if (choicej == 7):
            plt.xlabel(x_label, fontsize=6)
        if (choicej == 8):
            plt.xlabel(x_label, fontsize=6)

    '''
    Save Graph
    '''
    plt.suptitle(title_display, fontsize=8)
    save_file_name = image_save_name
    plt.savefig(image_folder + save_file_name, dpi=300, orientation='portrait',
                papertype='a3')
    plt.clf()
    plt.clf()

#     different_figsize = False
#     if (different_figsize):
#         if (choice_set_list == 1):
#             subplot_rows = 1
#             subplot_cols = 1
#             figsize = (8,6)
#         if (choice_set_list == 2):
#             subplot_rows = 1
#             subplot_cols = 2
#             figsize = (8,6)
#         if (choice_set_list == 3 | choice_set_list == 4):
#             subplot_rows = 2
#             subplot_cols = 2
#             figsize = (8,6)
#         if (choice_set_list == 5):
#             subplot_rows = 2
#             subplot_cols = 3
#             figsize = (12,6)
#         if (choice_set_list == 6):
#             subplot_rows = 2
#             subplot_cols = 3
#             figsize = (12,6)
#         if (choice_set_list == 7):
#             subplot_rows = 2
#             subplot_cols = 4
#             figsize = (16,6)
#     else:
