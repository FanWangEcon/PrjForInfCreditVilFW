'''
Created on Jun 27, 2018

@author: fan


'''

import logging
import matplotlib
import matplotlib.pyplot as plt

import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')
logger = logging.getLogger(__name__)


def graph_agg_at_equi(pd_file_equi_out, x_var_name,
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
    
    Example
    -------
    import projectsupport.graph.stationary_agg_informal as graphsteadyaggj2
    
    """

    choice_names = param_model_a.choice_index_names()['choice_names']
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    aggregate_K_col_name = steady_var_suffixes_dict['ktp_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]

    inf_borr_col_name_prefix = choice_names[0] + '_' + steady_var_suffixes_dict['btp_opti_grid']
    aggregate_inf_borrow_col_name = inf_borr_col_name_prefix + steady_agg_suffixes['_j_agg'][0]
    avg_inf_borrow_ifborr_col_name = inf_borr_col_name_prefix + steady_agg_suffixes['_j_agg_ifj'][0]

    inf_save_col_name_prefix = choice_names[1] + '_' + steady_var_suffixes_dict['btp_opti_grid']
    aggregate_inf_save_col_name = inf_save_col_name_prefix + steady_agg_suffixes['_j_agg'][0]
    avg_inf_save_ifinfsave_col_name = inf_save_col_name_prefix + steady_agg_suffixes['_j_agg_ifj'][0]

    p_inf_borrow_col_name = choice_names[0] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                            steady_agg_suffixes['_j_agg'][0]
    p_inf_save_col_name = choice_names[1] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                          steady_agg_suffixes['_j_agg'][0]

    '''A. X Variable'''
    x_var = pd_file_equi_out[x_var_name]

    '''B. Capital Choice'''
    aggregate_K = pd_file_equi_out[aggregate_K_col_name]

    '''C. Total Savings'''
    '''At Equilibrium aggregate_inf_save = aggregate_inf_borrow very close'''
    aggregate_inf_save = pd_file_equi_out[aggregate_inf_save_col_name]
    aggregate_inf_borrow = (-1) * (pd_file_equi_out[aggregate_inf_borrow_col_name])

    equi_R_INFORM_BORR = pd_file_equi_out['esti_param.R_INFORM_BORR']

    avg_inf_borrow_ifborr = (-1) * pd_file_equi_out[avg_inf_borrow_ifborr_col_name]
    avg_inf_save_ifinfsave = pd_file_equi_out[avg_inf_save_ifinfsave_col_name]
    p_inf_borrow = pd_file_equi_out[p_inf_borrow_col_name]
    p_inf_save = pd_file_equi_out[p_inf_save_col_name]

    figsize = (8, 8)
    #     plt.close('all')
    plt.figure(figsize=figsize)

    """
    Fig 1
    """
    plt.subplot(221)
    plt.grid()

    plt.scatter(x_var, aggregate_K, s=1, c='black', label='Capital', alpha=1)
    plt.plot(x_var, aggregate_K, label='_nolegend_', c='black', alpha=0.2)

    plt.scatter(x_var, aggregate_inf_save, s=1, c='red', label='Savings Inf', alpha=1)
    plt.plot(x_var, aggregate_inf_save, label='_nolegend_', c='red', alpha=0.2)

    plt.scatter(x_var, aggregate_inf_borrow, s=1, c='blue', label='Borrowing Inf', alpha=1)
    plt.plot(x_var, aggregate_inf_borrow, label='_nolegend_', c='blue', alpha=0.2)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Assets', fontsize=8)
    plt.suptitle('Aggregate Assets at Equilibrium', fontsize=10)

    plt.legend(fontsize=6)

    """
    Fig 2
    """
    plt.subplot(222)
    plt.grid()

    plt.scatter(x_var, avg_inf_borrow_ifborr, s=1, c='blue', label='avg inf borrow ifborr', alpha=1)
    plt.plot(x_var, avg_inf_borrow_ifborr, c='blue', label='_nolegend_', alpha=0.2)

    plt.scatter(x_var, avg_inf_save_ifinfsave, s=1, c='red', label='avg inf save ifinfsave', alpha=1)
    plt.plot(x_var, avg_inf_save_ifinfsave, c='red', label='_nolegend_', alpha=0.2)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Assets', fontsize=8)
    plt.suptitle('Avg Choice if Choose', fontsize=10)

    plt.legend(fontsize=6)

    """
    Fig 3
    """
    plt.subplot(223)
    plt.grid()

    plt.scatter(x_var, equi_R_INFORM_BORR, s=1, c='blue', label='Equi Inf R', alpha=1)
    plt.plot(x_var, equi_R_INFORM_BORR, c='blue', label='_nolegend_', alpha=0.2)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('R', fontsize=8)
    plt.suptitle('Equilibrium Informal Interest', fontsize=10)

    plt.legend(fontsize=6)

    """
    Fig 4
    """
    plt.subplot(224)
    plt.grid()

    plt.scatter(x_var, p_inf_borrow, s=1, c='blue', label='p inf borrow', alpha=1)
    plt.plot(x_var, p_inf_borrow, c='blue', label='_nolegend_', alpha=0.2)

    plt.scatter(x_var, p_inf_save, s=1, c='red', label='p inf save', alpha=1)
    plt.plot(x_var, p_inf_save, c='red', label='_nolegend_', alpha=0.2)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Prob', fontsize=8)
    plt.suptitle('Aggregate Choice Probability', fontsize=10)

    plt.legend(fontsize=6)

    """
    Save Fig
    """
    image_save_name_full = image_save_name + '_J2'
    plt.suptitle(title_display, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + image_save_name_full,
                          dpi=300)
    plt.clf()
    plt.close('all')
