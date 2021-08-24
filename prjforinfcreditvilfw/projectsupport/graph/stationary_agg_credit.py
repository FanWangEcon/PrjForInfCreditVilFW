'''
Created on Jun 27, 2018

@author: fan

Credit market aggregation graphs
'''

import logging
import matplotlib
import matplotlib.pyplot as plt

import parameters.model.a_model as param_model_a
import projectsupport.graph.colorsize as support_colors
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')

logger = logging.getLogger(__name__)


def graph_agg_at_equi_bn(pd_file_equi_out, x_var_name,
                         title_display, image_save_name, image_folder):
    """
    Graph Demand and Supply curves for credit

    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/simu/a_20180517_quick'
    file_name = '_20180517_quick_A-150'
    csv_file_folder = directory + '/' + file_name + '.csv'
    
    
    Graphs: 
    ---------------------------------------------------------
    - R        - total posB negB - inf posNegB - for posNegB
    ---------------------------------------------------------
    - FB all J - IB all J        - FS all J    - IL all J 
    ---------------------------------------------------------
    - same as second row, conditional on choosing j
    ---------------------------------------------------------
    
    """

    '''A. Strings'''
    discrete_colors = support_colors.seven_cate_colors()

    line_specs = support_colors.scatter_size(pd_file_equi_out.shape[0])
    scatter_size = line_specs['scatter_size']
    scatter_alpha = line_specs['scatter_alpha']
    scatter_marker = line_specs['scatter_marker']
    line_width = line_specs['line_width']
    line_alpha = line_specs['line_alpha']

    choice_names = param_model_a.choice_index_names()['choice_names']
    choice_names_graph_labels = param_model_a.choice_index_names()['choice_names_graph_labels']

    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()
    steady_var_cts_desc = hardstring.get_steady_var_cts_desc()

    '''B. x variable'''
    #     if (x_var_name == None or x_var_name == 'None'):
    #         # if none, no looping parameter, just use this to allow for single point plotting
    #         x_var = pd_file_equi_out['grid_param.len_k_start']
    #     else:
    x_var = pd_file_equi_out[x_var_name]

    '''C. aggregate borrow and saves'''
    aggregate_fb_col_name = steady_var_suffixes_dict['btp_fb_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_ib_col_name = steady_var_suffixes_dict['btp_ib_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_fs_col_name = steady_var_suffixes_dict['btp_fs_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_il_col_name = steady_var_suffixes_dict['btp_il_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]

    aggregate_for_borrow = (-1) * (pd_file_equi_out[aggregate_fb_col_name])
    aggregate_inf_borrow = (-1) * (pd_file_equi_out[aggregate_ib_col_name])
    aggregate_borrow = aggregate_inf_borrow + aggregate_for_borrow

    aggregate_for_save = pd_file_equi_out[aggregate_fs_col_name]
    aggregate_inf_lend = pd_file_equi_out[aggregate_il_col_name]
    aggregate_save = aggregate_for_save + aggregate_inf_lend

    equi_R_INFORM_BORR = pd_file_equi_out['esti_param.R_INFORM_BORR']

    '''D. Initial Figure'''
    figsize = (16, 12)
    #     plt.close('all')
    plt.figure(figsize=figsize)

    """
    E. Generate Choice list 
    """
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

    """
    F. Generate Data
    """
    agg_bn_fb_eachJ_dict_j_agg = {}
    agg_bn_ib_eachJ_dict_j_agg = {}
    agg_bn_fs_eachJ_dict_j_agg = {}
    agg_bn_il_eachJ_dict_j_agg = {}
    agg_bn_fb_eachJ_dict_j_agg_ifj = {}
    agg_bn_ib_eachJ_dict_j_agg_ifj = {}
    agg_bn_fs_eachJ_dict_j_agg_ifj = {}
    agg_bn_il_eachJ_dict_j_agg_ifj = {}
    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):
        for steady_var_suffixes_cur in [steady_var_suffixes_dict['btp_fb_opti_grid'],
                                        steady_var_suffixes_dict['btp_ib_opti_grid'],
                                        steady_var_suffixes_dict['btp_fs_opti_grid'],
                                        steady_var_suffixes_dict['btp_il_opti_grid']]:

            '''Kn, Bn, and cc'''
            cur_j_opti_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_cur
            col_name_j_agg = cur_j_opti_col_name + steady_agg_suffixes['_j_agg'][0]
            col_name_j_agg_ifj = cur_j_opti_col_name + steady_agg_suffixes['_j_agg_ifj'][0]

            '''Data and Assign'''
            data_array_j_agg = pd_file_equi_out[col_name_j_agg]
            data_array_j_agg_ifj = pd_file_equi_out[col_name_j_agg_ifj]

            '''Assign'''
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['btp_fb_opti_grid']):
                agg_bn_fb_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_bn_fb_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['btp_ib_opti_grid']):
                agg_bn_ib_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_bn_ib_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['btp_fs_opti_grid']):
                agg_bn_fs_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_bn_fs_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['btp_il_opti_grid']):
                agg_bn_il_eachJ_dict_j_agg[choiceJ_index] = data_array_j_agg
                agg_bn_il_eachJ_dict_j_agg_ifj[choiceJ_index] = data_array_j_agg_ifj

    """
    G1. Fig 1
    """
    plt.subplot(3, 4, 1)
    plt.grid()

    plt.scatter(x_var, equi_R_INFORM_BORR, c='blue', label='Equi Inf R',
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, equi_R_INFORM_BORR, c='blue', label='_nolegend_',
             linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('R', fontsize=8)
    plt.suptitle('Equilibrium Informal Interest', fontsize=10)

    plt.legend(fontsize=6)

    """
    G2. Fig 2
    """
    plt.subplot(3, 4, 2)
    plt.grid()

    plt.scatter(x_var, aggregate_inf_borrow,
                c=discrete_colors[0], label=choice_names_graph_labels['04'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_inf_borrow, label='_nolegend_', c=discrete_colors[0],
             linewidth=line_width, alpha=line_alpha)

    plt.scatter(x_var, aggregate_inf_lend,
                c=discrete_colors[1], label=choice_names_graph_labels['15'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_inf_lend, label='_nolegend_', c=discrete_colors[1],
             linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Informal Aggregates', fontsize=8)
    plt.legend(fontsize=6)

    """
    G3. Fig 3
    """
    plt.subplot(3, 4, 3)
    plt.grid()

    plt.scatter(x_var, aggregate_for_borrow,
                c=discrete_colors[2], label=choice_names_graph_labels['245'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_for_borrow, label='_nolegend_', c=discrete_colors[2],
             linewidth=line_width, alpha=line_alpha)

    plt.scatter(x_var, aggregate_for_save,
                c=discrete_colors[3], label=choice_names_graph_labels['3'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_for_save, label='_nolegend_', c=discrete_colors[3],
             linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('Formal Aggregates', fontsize=8)
    plt.legend(fontsize=6)

    """
    C3. Fig 4
    """
    plt.subplot(3, 4, 4)
    plt.grid()

    plt.scatter(x_var, aggregate_borrow,
                c=discrete_colors[0], label=choice_names_graph_labels['0245'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_borrow, label='_nolegend_', c=discrete_colors[0],
             linewidth=line_width, alpha=line_alpha)

    plt.scatter(x_var, aggregate_save,
                c=discrete_colors[1], label=choice_names_graph_labels['135'],
                s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
    plt.plot(x_var, aggregate_save, label='_nolegend_', c=discrete_colors[1],
             linewidth=line_width, alpha=line_alpha)

    plt.xlabel(x_var_name, fontsize=8)
    plt.ylabel('All Aggregates', fontsize=8)
    plt.legend(fontsize=6)

    """
    D. Fig 5 through 8, 9 to 12
    """
    for cur_var in ['fb', 'ib', 'fs', 'il',
                    'fb_ifj', 'ib_ifj', 'fs_ifj', 'il_ifj']:

        '''
        csv column names look like this:
            btp_fb_opti_grid_allJ_agg
            btp_ib_opti_grid_allJ_agg
        '''

        if (cur_var == 'fb'):
            plt.subplot(3, 4, 5)
            agg_dict_j_cur = agg_bn_fb_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['btp_fb_opti_grid'][0]
            subtitle = 'weight by j prob'
        if (cur_var == 'ib'):
            plt.subplot(3, 4, 6)
            agg_dict_j_cur = agg_bn_ib_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['btp_ib_opti_grid'][0]
            subtitle = 'weight by j prob'
        if (cur_var == 'fs'):
            plt.subplot(3, 4, 7)
            agg_dict_j_cur = agg_bn_fs_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['btp_fs_opti_grid'][0]
            subtitle = 'weight by j prob'
        if (cur_var == 'il'):
            plt.subplot(3, 4, 8)
            agg_dict_j_cur = agg_bn_il_eachJ_dict_j_agg
            ytitle = steady_var_cts_desc['btp_il_opti_grid'][0]
            subtitle = 'weight by j prob'

        if (cur_var == 'fb_ifj'):
            plt.subplot(3, 4, 9)
            agg_dict_j_cur = agg_bn_fb_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['btp_fb_opti_grid'][0]
            subtitle = 'if choose j'
        if (cur_var == 'ib_ifj'):
            plt.subplot(3, 4, 10)
            agg_dict_j_cur = agg_bn_ib_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['btp_ib_opti_grid'][0]
            subtitle = 'if choose j'
        if (cur_var == 'fs_ifj'):
            plt.subplot(3, 4, 11)
            agg_dict_j_cur = agg_bn_fs_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['btp_fs_opti_grid'][0]
            subtitle = 'if choose j'
        if (cur_var == 'il_ifj'):
            plt.subplot(3, 4, 12)
            agg_dict_j_cur = agg_bn_il_eachJ_dict_j_agg_ifj
            ytitle = steady_var_cts_desc['btp_il_opti_grid'][0]
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
    image_save_name_full = image_save_name + '_bJ2'
    plt.suptitle(title_display, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + image_save_name_full,
                          dpi=300)
    plt.clf()
    plt.close('all')
