'''
Created on Apr 21, 2018

@author: fan

Plotting probability of choosing into each choice category, and optimal choices
within each choice category
'''
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import parameters.paraminstpreset as get_param_inst_preset
import projectsupport.graph.colorsize as color
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')


def graph_eachj_prob_fromcsv(param_combo, data_folder, csv_file_name,
                             x_var_label, y_var_label,
                             title_display,
                             image_save_suffix, image_folder):
    #     csv_file = 'solu_'+combo_type[1]+'.csv'
    csv_file_folder = data_folder + csv_file_name + '.csv'
    solu_data_pd = proj_sys_sup.read_csv(csv_file_folder)

    param_inst = get_param_inst_preset.get_param_inst_preset_combo(param_combo)

    return graph_eachj_prob(solu_data_pd, param_inst,
                            title_display,
                            image_save_suffix, image_folder)


def graph_eachj_prob(solu_data_pd, param_inst,
                     title_display,
                     image_save_name, image_folder):
    """
    Graph out in the following fashion: 
    
    state-space values on the x-axis
    choices/prob etc on the y-axis
    
    2 by 2
    
    ---------------
    -- Prob -- C --
    ---------------
    -- Kp --  Bp --
    ---------------
    
    Returns
    -------
    Graph: image file
        sample, https://www.evernote.com/shard/s10/nl/1203171/240f21bc-d496-4ad6-a519-308b373f6d47
                
    """

    solu_data_pd.columns
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
    A = param_inst.data_param['A']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']
    cash_min = param_inst.grid_param['min_steady_coh']
    cash_max = param_inst.grid_param['max_steady_coh']

    """
    C. Plot
    """
    plt.close('all')
    plt.figure()
    seven_colors = color.seven_cate_colors()

    """
    C1. Subpfigure 1
    """
    for curplot in [1, 2, 3, 4]:

        if (curplot == 1):
            plot_idx = 221
            data_plot = prb_matrix
            data_label = prob_cols
            y_label = 'probability'
        if (curplot == 2):
            plot_idx = 222
            data_plot = ccc_matrix
            data_label = cc_cols
            y_label = 'consumption'
        if (curplot == 3):
            plot_idx = 223
            data_plot = ktp_matrix
            data_label = kn_cols
            y_label = 'kn'
        if (curplot == 4):
            plot_idx = 224
            data_plot = btp_matrix
            data_label = bn_cols
            y_label = 'bn'

        plt.subplot(plot_idx)
        plt.grid()

        cur_y_min = 99
        cur_y_max = -99
        for ctr, choicej in enumerate(choice_set_list):
            plt.scatter(cash_tt, data_plot[:, ctr],
                        label=data_label[ctr],
                        s=1, c=seven_colors[choicej], alpha=1)
            plt.plot(cash_tt, data_plot[:, ctr],
                     c=seven_colors[choicej], alpha=0.3)

            '''Find data Min and Max within X Range'''
            y_min_new = np.min(data_plot[(np.ravel(cash_tt) <= cash_max) &
                                         (np.ravel(cash_tt) >= cash_min),
                                         ctr])
            cur_y_min = min(cur_y_min, y_min_new)

            y_max_new = np.max(data_plot[(np.ravel(cash_tt) <= cash_max) &
                                         (np.ravel(cash_tt) >= cash_min)
            , ctr])
            cur_y_max = max(cur_y_max, y_max_new)

        plt.xlim(cash_min, cash_max)

        if (curplot == 1):
            plt.ylabel(y_label, fontsize=6)
        if (curplot == 2):
            pass
        if (curplot == 3):
            plt.xlabel('Cash-On-Hand today', fontsize=6)
            plt.ylabel(y_label, fontsize=6)
        if (curplot == 4):
            plt.xlabel('Cash-On-Hand today', fontsize=6)

        if (curplot != 1):
            cash_grid = np.linspace(cash_min, cash_max, 100)
            plt.plot(cash_grid, cash_grid, label='45')
            plt.ylim(cur_y_min, cur_y_max)

        plt.legend(fontsize=6)

    '''
    Save Graph
    '''
    plt.suptitle(title_display, fontsize=8)
    save_file_name = image_save_name
    proj_sys_sup.save_img(plt, image_folder + save_file_name,
                          dpi=300, orientation='portrait',
                          papertype='a3')
    plt.clf()
    plt.clf()
