'''
Created on Apr 21, 2018

@author: fan

Can see dynamics from policy function, depending on were lines are with respect
to 45 degree line.
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import parameters.paraminstpreset as get_param_inst_preset
import projectsupport.systemsupport as proj_sys_sup
import solusteady.distribution.condidist_simu as condisimu
import solusteady.distribution.condidist_simu_probj as condisimuprobj

matplotlib.use('Agg')


def graph_phase_diagram_fromcsv(param_combo, data_folder, csv_file_name,
                                x_var_label, y_var_label,
                                title_display,
                                image_save_suffix, image_folder):
    #     csv_file = 'solu_'+combo_type[1]+'.csv'
    csv_file_folder = data_folder + csv_file_name + '.csv'
    solu_data_pd = proj_sys_sup.read_csv(csv_file_folder)

    param_inst = get_param_inst_preset.get_param_inst_preset_combo(param_combo)

    return graph_maxj_nologit(solu_data_pd, param_inst,
                              title_display,
                              image_save_suffix, image_folder)


def graph_maxj_nologit(solu_data_pd, param_inst,
                       title_display,
                       image_save_name, image_folder):
    """
    See Aiyagari 1994, Figure 1 and 2. These are suppose to to versions of those
    figures.    
    ---------------------------------------
    -- Cash on Cash  -- Cash and Optimal --
    -- Dist Tomorrow -- kn, bn policies  --
    ---------------------------------------
    
    Returns
    -------
    Graph: Image File
        sample, https://www.evernote.com/shard/s10/nl/1203171/4abc1b98-f5fd-4db6-9b32-9aad0d014b35
    
    """
    solu_data_pd.columns
    solu_data_pd = solu_data_pd.sort_values(by=['cash_tt'])

    """
    A. Get All Data Vectors and Matrixes
    """
    cash_tt = solu_data_pd[['cash_tt']].to_numpy()
    ktp_opti = solu_data_pd[['ktp_opti']].to_numpy()
    btp_opti = solu_data_pd[['btp_opti']].to_numpy()
    consumption_opti = solu_data_pd[['consumption_opti']].to_numpy()

    prob_cols = [col for col in solu_data_pd.columns if 'prob ' in col]
    kn_cols = [col for col in solu_data_pd.columns if 'kn ' in col]
    bn_cols = [col for col in solu_data_pd.columns if 'bn ' in col]
    cc_cols = [col for col in solu_data_pd.columns if 'cc ' in col]

    prb_matrix = solu_data_pd[prob_cols].to_numpy()
    ktp_matrix = solu_data_pd[kn_cols].to_numpy()
    btp_matrix = solu_data_pd[bn_cols].to_numpy()
    ccc_matrix = solu_data_pd[cc_cols].to_numpy()
    cash_tt = solu_data_pd[['cash_tt']].to_numpy()

    '''Weighted Choices by Probabilities'''
    ktp_opti_wgted = np.sum(ktp_matrix * prb_matrix, axis=1)
    btp_opti_wgted = np.sum(btp_matrix * prb_matrix, axis=1)
    consumption_opti_wgted = np.sum(ccc_matrix * prb_matrix, axis=1)

    """
    B. Get Parameters
    """
    choice_set_list = param_inst.model_option['choice_set_list']
    choice_names_use = param_inst.model_option['choice_names_use']
    choice_names_full_use = param_inst.model_option['choice_names_full_use']

    """
    C. Plot
    """
    plt.close('all')
    figsize = (16, 6)
    plt.figure(figsize=figsize)

    """
    C1. Subpfigure 1
    """
    ax1 = plt.subplot(141)
    plt.grid()
    cash_partial_percentiles, cashpartial_min, cashpartial_max, __, __ = \
        condisimu.aiyagari_fig2_data(param_inst, btp_opti, ktp_opti,
                                     shock_simu_count=5000, simu_seed=123)
    aiyagari_fig2_graph(ax1, cash_tt, cashpartial_min, cashpartial_max, cash_partial_percentiles)
    ax1.set_title('Max of J, t+1, Cash Distribution', fontsize=8)

    """
    C2. Subpfigure 2
    Generate percentiles for each choice category separately, then jointly by weight
    """
    ax2 = plt.subplot(142, sharey=ax1, sharex=ax1)
    plt.grid()
    cash_partial_percentiles, cashpartial_min, cashpartial_max, __ = \
        condisimuprobj.aiyagari_fig2_data_probwgted(
            param_inst,
            prb_matrix, btp_matrix, ktp_matrix,
            shock_simu_count=5000, simu_seed=123,
            lower_sd=-3, higher_sd=+3)
    aiyagari_fig2_graph(ax2, cash_tt, cashpartial_min, cashpartial_max, cash_partial_percentiles)
    ax2.set_title('Weighted t+1 Cash Distribution', fontsize=8)

    """
    C3. Subpfigure 3, policy functions max over discrete choices
    """
    plt.subplot(143, sharey=ax1, sharex=ax1)
    title_use = 'Max of J choices (Interest + Principle)'
    aiyagri_fig1_graph(cash_tt, ktp_opti, btp_opti, consumption_opti,
                       title=title_use)

    """
    C4. Subpfigure 4, weighted policy functions
    """
    plt.subplot(144, sharey=ax1, sharex=ax1)
    title_use = 'Weighted Policy (Interest + Principle)'
    aiyagri_fig1_graph(cash_tt, ktp_opti_wgted, btp_opti_wgted, consumption_opti_wgted,
                       title=title_use)

    '''
    Save Graph
    '''
    plt.suptitle(title_display + ' ' + str(choice_names_use) + '\n' + str(choice_names_full_use),
                 fontsize=8)
    save_file_name = image_save_name
    proj_sys_sup.save_img(plt, image_folder + save_file_name,
                          dpi=300, orientation='portrait',
                          papertype='a3')
    plt.clf()
    plt.clf()


def aiyagri_fig1_graph(cash_tt, ktp_opti, btp_opti, consumption_opti,
                       title=''):
    plt.grid()
    '''
    45 degree line
    '''
    cash_grid = np.linspace(min(cash_tt), max(cash_tt), 100)
    plt.plot(cash_grid, cash_grid, label='45')

    '''
    Plot cash today and cash range tomorrow
    '''
    plt.plot(cash_tt, ktp_opti, c='red', alpha=0.3)
    plt.scatter(cash_tt, ktp_opti, label='ktp', s=1, c='red', alpha=1)
    plt.plot(cash_tt, btp_opti, c='blue', alpha=0.3)
    plt.scatter(cash_tt, btp_opti, label='btp(with r)', s=1, c='blue', alpha=1)
    plt.plot(cash_tt, consumption_opti, c='black', alpha=0.3)
    plt.scatter(cash_tt, consumption_opti, s=1, label='c', c='black', alpha=1)

    plt.xlabel('Cash-On-Hand today', fontsize=8)
    plt.title(title, fontsize=8)
    plt.legend(fontsize=6)


def aiyagari_fig2_graph(ax, cash_tt, cashpartial_min, cashpartial_max, cash_partial_percentiles):
    """
    
    Returns
    -------
    Image: 
        https://www.evernote.com/shard/s10/nl/1203171/8ea6cc5d-3d92-4ecb-bb7f-94770aea2f86
        
    """

    '''
    45 degree line
    '''
    cash_grid = np.linspace(min(cash_tt), max(cash_tt), 100)
    ax.plot(cash_grid, cash_grid, label='45')

    '''
    Plot cash today and cash range tomorrow
    '''

    #     plt.plot(cash_tt, compo_certain, label='certain', c='black', alpha=0.2)

    #     plt.plot(cash_tt, cashpartial_min, label='min', c='blue', alpha=0.3)
    ax.scatter(cash_tt, cashpartial_min, label='min(-3sd)', s=1, c='blue', alpha=1)
    ax.plot(cash_tt, cashpartial_max, label='max', c='blue', alpha=0.3)
    ax.scatter(cash_tt, cashpartial_max, label='max(+3sd)', s=1, c='blue', alpha=1)

    #     plt.plot(cash_tt, cash_partial_percentiles[:,1], label='p20', c='red', alpha=0.3)
    ax.scatter(cash_tt, cash_partial_percentiles[:, 1], s=1, label='p20', c='red', alpha=1)
    #     plt.plot(cash_tt, cash_partial_percentiles[:,3], label='p80', c='red', alpha=0.3)
    ax.scatter(cash_tt, cash_partial_percentiles[:, 3], s=1, label='p80', c='red', alpha=1)

    #     plt.plot(cash_tt, cash_partial_percentiles[:,2], label='p50', c='black', alpha=0.3)
    ax.scatter(cash_tt, cash_partial_percentiles[:, 2], s=1, label='p50', c='black', alpha=1)

    ax.set_xlabel('Cash-On-Hand today', fontsize=8)

    ax.legend(fontsize=6)
