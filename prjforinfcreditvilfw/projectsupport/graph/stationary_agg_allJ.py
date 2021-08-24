'''
Created on Jun 27, 2018

@author: fan

import projectsupport.graph.stationary_agg_allJ as graphsteadyaggjall
'''

import logging
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import parameters.model.a_model as param_model_a
import projectsupport.graph.colorsize as support_colors
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')

logger = logging.getLogger(__name__)


def graph_agg_at_equi_allJ(pd_file_equi_out, x_var_name,
                           title_display, image_save_name, image_folder):
    """
    Aggregate Probabiliity, B and K graphs
    
    Six Graphs
    - Informal R over Parameters
    - B, K, C: netB, K, C aggregates
    - Prob: Loop over J
    - Bn: loop over J, borrow to negative
    - Kn: loop over J, borrow to negative
    - C: loop over J, borrow to negative
    
    Example
    -------
    import projectsupport.graph.stationary_agg_allJ as graphsteadyaggjall
    graphsteadyaggjall.graph_agg_at_equi_allJ(
                            choice_set_list, pd_file_equi_out, x_var_name,
                            title_display, image_save_name, image_folder)    
    """

    '''0. Coloring'''
    cts_colors = support_colors.choice_cts_colors()
    discrete_colors = support_colors.seven_cate_colors()

    '''1. Scatter Line'''
    line_specs = support_colors.scatter_size(pd_file_equi_out.shape[0])
    scatter_size = line_specs['scatter_size']
    scatter_alpha = line_specs['scatter_alpha']
    scatter_marker = line_specs['scatter_marker']
    line_width = line_specs['line_width']
    line_alpha = line_specs['line_alpha']

    '''2. String Names'''
    choice_names = param_model_a.choice_index_names()['choice_names']
    choice_names_borrow = param_model_a.choice_index_names()['choice_names_borrow']
    choice_names_graph_labels = param_model_a.choice_index_names()['choice_names_graph_labels']

    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_var_cts_desc = hardstring.get_steady_var_cts_desc()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    '''3. Column Names'''
    aggregate_Bn_col_name = steady_var_suffixes_dict['btp_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_Kn_col_name = steady_var_suffixes_dict['ktp_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_Cc_col_name = steady_var_suffixes_dict['consumption_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_Yy_col_name = steady_var_suffixes_dict['y_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_Pr_col_name = steady_var_suffixes_dict['probJ_opti_grid'] + steady_agg_suffixes['_allJ_agg'][
        0]  # == 1

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
    #     if (x_var_name == None or x_var_name == 'None'):
    #         # if none, no looping parameter, just use this to allow for single point plotting
    #         x_var = pd_file_equi_out['grid_param.len_k_start']
    #     else:
    x_var = pd_file_equi_out[x_var_name]

    '''B. Aggregate Bn, Kn and C'''
    aggregate_Bn = pd_file_equi_out[aggregate_Bn_col_name]
    aggregate_Kn = pd_file_equi_out[aggregate_Kn_col_name]
    aggregate_Cc = pd_file_equi_out[aggregate_Cc_col_name]
    try:  # old results don't have y
        aggregate_Yy = pd_file_equi_out[aggregate_Yy_col_name]
    except:
        pass
    if (aggregate_Pr_col_name in pd_file_equi_out.columns):
        '''
        normal simulation has this
        '''
        aggregate_Pr = pd_file_equi_out[aggregate_Pr_col_name]
    else:
        '''
        mpoly predict simulation do not, sum up from the other probabilities
        '''
        aggregate_Pr = None

    '''Find Current choice_set_list'''
    choice_set_list = []
    for choiceJ_index in choice_names.keys():

        try:
            """
            Try all possible choice_set_list element, but curret invoke will not have all of them
            """
            prob_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                            steady_agg_suffixes['_j_agg'][0]
            pd_file_equi_out[prob_col_name]
            choice_set_list.append(choiceJ_index)
        except:
            pass

    '''C. B f'''
    agg_prob_eachJ_dict = {}  # each value is a array of probability for that category
    agg_bn_eachJ_dict_j_agg = {}
    agg_kn_eachJ_dict_j_agg = {}
    agg_cc_eachJ_dict_j_agg = {}
    agg_bn_eachJ_dict_j_agg_ifj = {}
    agg_kn_eachJ_dict_j_agg_ifj = {}
    agg_cc_eachJ_dict_j_agg_ifj = {}
    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):

        '''Probability'''
        prob_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                        steady_agg_suffixes['_j_agg'][0]

        agg_prob_eachJ_dict[choiceJ_index] = pd_file_equi_out[prob_col_name]

        '''Aggregate each J b asset'''
        # 0. loop over: 'btp_opti_grid':2, 'ktp_opti_grid':3, 'consumption_opti_grid':4
        for steady_var_suffixes_cur in [steady_var_suffixes_dict['btp_opti_grid'],
                                        steady_var_suffixes_dict['ktp_opti_grid'],
                                        steady_var_suffixes_dict['consumption_opti_grid']]:

            '''Kn, Bn, and cc'''
            cur_j_opti_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_cur
            col_name_j_agg = cur_j_opti_col_name + steady_agg_suffixes['_j_agg'][0]
            col_name_j_agg_ifj = cur_j_opti_col_name + steady_agg_suffixes['_j_agg_ifj'][0]

            '''Data and Assign'''
            data_array_j_agg = pd_file_equi_out[col_name_j_agg]
            data_array_j_agg_ifj = pd_file_equi_out[col_name_j_agg_ifj]
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['btp_opti_grid']):

                if (choiceJ_index in choice_names_borrow.keys()):
                    # multiply by -1, so that can see demand and supply crossing
                    data_array_j_agg = (-1) * data_array_j_agg
                    data_array_j_agg_ifj = (-1) * data_array_j_agg_ifj

                agg_bn_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_bn_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj

            if (steady_var_suffixes_cur == steady_var_suffixes_dict['ktp_opti_grid']):
                agg_kn_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_kn_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['consumption_opti_grid']):
                agg_cc_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_cc_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj

    figsize = (12, 12)
    #     plt.close('all')
    plt.figure(figsize=figsize)

    """
    Fig 1
    """
    plt.subplot(331)
    plt.grid()

    equi_R_INFORM_BORR = pd_file_equi_out['esti_param.R_INFORM_BORR']

    plt.scatter(x_var, equi_R_INFORM_BORR, c='blue', label='Equi Inf R',
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, equi_R_INFORM_BORR, c='blue', label='_nolegend_',
             linewidth=line_width, alpha=line_alpha)

    if 'EjV_unweighted_stats.mean' in pd_file_equi_out:
        EjV_unweighted_stats_mean = pd_file_equi_out['EjV_unweighted_stats.mean']
        # demean, for graphical reasons, use the mean of interest rate to re-mean
        fl_EjV_unweighted_stats_mean_mean = np.mean(EjV_unweighted_stats_mean)
        EjV_unweighted_stats_mean = ((EjV_unweighted_stats_mean - fl_EjV_unweighted_stats_mean_mean) / 100) + \
                                    np.mean(equi_R_INFORM_BORR)

        plt.scatter(x_var, EjV_unweighted_stats_mean, c='red', label='EjV Mean (remeaned unweighted)',
                    s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
        plt.plot(x_var, EjV_unweighted_stats_mean, c='red', label='_nolegend_',
                 linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('R', fontsize=8)
    plt.suptitle('Equilibrium Informal Interest + EjV', fontsize=10)

    plt.legend(fontsize=6)

    """
    Fig 2
    """
    plt.subplot(332)
    plt.grid()

    plt.scatter(x_var, aggregate_Bn, c=cts_colors['colorBn'], label=steady_var_cts_desc['btp_opti_grid'][0],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_Bn, label='_nolegend_', c=cts_colors['colorBn'], linewidth=line_width,
             alpha=line_alpha)

    plt.scatter(x_var, aggregate_Kn, c=cts_colors['colorKn'], label=steady_var_cts_desc['ktp_opti_grid'][0],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_Kn, label='_nolegend_', c=cts_colors['colorKn'],
             linewidth=line_width, alpha=line_alpha)

    plt.scatter(x_var, aggregate_Cc, c=cts_colors['colorCc'],
                label=steady_var_cts_desc['consumption_opti_grid'][0],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_Cc, label='_nolegend_', c=cts_colors['colorCc'],
             linewidth=line_width, alpha=line_alpha)
    try:  # old results don't have y
        plt.scatter(x_var, aggregate_Yy, c=cts_colors['colorYy'], label=steady_var_cts_desc['y_opti_grid'][0],
                    s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
        plt.plot(x_var, aggregate_Yy, label='_nolegend_', c=cts_colors['colorYy'],
                 linewidth=line_width, alpha=line_alpha)
    except:
        pass

    if (aggregate_Pr is not None):
        plt.scatter(x_var, aggregate_Pr, c=cts_colors['colorPr'], label=steady_var_cts_desc['probJ_opti_grid'][0],
                    s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
        plt.plot(x_var, aggregate_Pr, label='_nolegend_', c=cts_colors['colorPr'],
                 linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Assets', fontsize=8)
    plt.suptitle('Aggregate Assets at Equilibrium', fontsize=10)

    plt.legend(fontsize=6)

    """
    Fig 3
    """
    plt.subplot(333)
    plt.grid()

    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):
        data = agg_prob_eachJ_dict[choiceJ_index]
        label = choice_names_graph_labels[choiceJ_index]
        color = discrete_colors[choiceJ_index]
        plt.scatter(x_var, data, c=color, label=label,
                    s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
        plt.plot(x_var, data, c=color, label='_nolegend_',
                 linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel(steady_var_cts_desc['probJ_opti_grid'][0], fontsize=8)
    #     plt.suptitle('', fontsize=10)
    plt.legend(fontsize=6)

    """
    Fig 4, 5 and 6, and 7, 8 and 9
    """
    for cur_var in ['bn', 'kn', 'cc', 'bn_ifj', 'kn_ifj', 'cc_ifj']:

        if (cur_var == 'bn'):
            plt.subplot(334)
            agg_dict_j_cur = agg_bn_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['btp_opti_grid'][0]
            subtitle = 'weight by j prob'
        if (cur_var == 'kn'):
            plt.subplot(335)
            agg_dict_j_cur = agg_kn_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['ktp_opti_grid'][0]
            subtitle = 'weight by j prob'
        if (cur_var == 'cc'):
            plt.subplot(336)
            agg_dict_j_cur = agg_cc_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['consumption_opti_grid'][0]
            subtitle = 'weight by j prob'

        if (cur_var == 'bn_ifj'):
            plt.subplot(337)
            agg_dict_j_cur = agg_bn_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['btp_opti_grid'][0]
            subtitle = 'if choose j'
        if (cur_var == 'kn_ifj'):
            plt.subplot(338)
            agg_dict_j_cur = agg_kn_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['ktp_opti_grid'][0]
            subtitle = 'if choose j'
        if (cur_var == 'cc_ifj'):
            plt.subplot(339)
            agg_dict_j_cur = agg_cc_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['consumption_opti_grid'][0]
            subtitle = 'if choose j'
        plt.grid()

        for choiceJ_index in (choice_set_list):
            data = agg_dict_j_cur[choiceJ_index]
            label_str = choice_names_graph_labels[choiceJ_index]
            color = discrete_colors[choiceJ_index]
            plt.scatter(x_var, data, c=color, label=ytitle + ':' + label_str,
                        s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
            plt.plot(x_var, data, c=color, label='_nolegend_',
                     linewidth=line_width, alpha=line_alpha)

        plt.xlabel(x_var_name, fontsize=8)
        plt.ylabel(ytitle + ' (' + subtitle + ')', fontsize=8)
        #         plt.suptitle(subtitle, fontsize=10)
        plt.legend(fontsize=6)

    """
    Save Fig
    """
    image_save_name_full = image_save_name + '_J' + str(len(choice_set_list))
    plt.suptitle(title_display, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + image_save_name_full,
                          dpi=300)
    plt.clf()
    plt.close('all')
