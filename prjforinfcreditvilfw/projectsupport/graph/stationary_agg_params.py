'''
Created on Jun 27, 2018

@author: fan

Graph out how parameters are changing across estimation iteration, or simulation loop
'''

import logging
import matplotlib
import matplotlib.pyplot as plt
import pyfan.graph.tools.subplot as sup_graph_subplot

import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.minmax.a_minmax as param_minmax_a
import projectsupport.graph.colorsize as support_colors
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')

logger = logging.getLogger(__name__)


def graph_parameters(pd_file_equi_out, param_group_key_list,
                     combo_list, x_var_name,
                     title_display, image_save_name, image_folder):
    """
    Graph Parameters
    
    
    Graphs: 
    ---------------------------------------------------------
    - Param 1  - Param 2 ...
    ---------------------------------------------------------
    - Param ..., Param ... 
    ---------------------------------------------------------
    
    Parameters
    ----------
    x_var_name: string
        should just be index key string
    param_group_key_list: list of strings
        list of type.name from parameters.loop_combo_type_list.param_str.py val[1]
        
    Examples
    --------
    import projectsupport.graph.stationary_agg_params as graphsteadyparam
    graphsteadyparam.graph_parameters(
                            pd_file_equi_out, param_group_key_list, x_var_name,
                            title_display, image_save_name, image_folder)
                                                
    """

    '''
    A. Strings
    '''
    figsize, rows, cols = sup_graph_subplot.subplot_design(plot_count=len(param_group_key_list),
                                                           base_multiple=4,
                                                           base_multiple_high_frac=0.60)

    line_specs = support_colors.scatter_size(pd_file_equi_out.shape[0])
    scatter_size = line_specs['scatter_size']
    scatter_alpha = line_specs['scatter_alpha']
    scatter_marker = line_specs['scatter_marker']
    line_width = line_specs['line_width']
    line_alpha = line_specs['line_alpha']

    '''
    A1. Get Min Max Bounds 
    '''
    minmax_type = combo_list[0]['param_update_dict']['minmax_type']
    minmax_file = minmax_type[0]
    if (minmax_file == 'a'):
        minmax_param, minmax_subtitle = param_minmax_a.param(minmax_type)

    '''
    B. x variable, could be a list of parameters, or a single parameter
        - simulation, parameters looping over
        - estimation, parameters estimating over
    '''
    x_var = pd_file_equi_out[x_var_name]

    '''
    D. Initialize Figure
    '''
    #     plt.close('all')
    plt.figure(figsize=figsize)

    '''
    C. looping over parameters
    '''
    for fig_ctr, param_group_key in enumerate(param_group_key_list):
        param_shortname, param_type, param_name = \
            paramloopstr.param_type_param_name(param_group_key=param_group_key)

        """
        D1. Figure Plot Parameter 
        """
        plt.subplot(rows, cols, fig_ctr + 1)
        plt.grid()

        current_parameter = pd_file_equi_out[param_group_key]

        plt.scatter(x_var, current_parameter, c='b', label=param_shortname + '(' + param_group_key + ')',
                    s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
        #         plt.plot(x_var, current_parameter, c='b', label='_nolegend_',
        #                  linewidth=line_width, alpha=line_alpha)

        '''
        D2. Plot Bounds
        '''
        param_bound = minmax_param[param_type][param_name]
        param_bound_gap = param_bound[1] - param_bound[0]
        if ((param_bound[1] - max(current_parameter)) / param_bound_gap) <= 0.05:
            plt.axhline(y=param_bound[1], c='k', linestyle='--', alpha=line_alpha)
        if ((min(current_parameter) - param_bound[0]) / param_bound_gap) <= 0.05:
            plt.axhline(y=param_bound[0], c='k', linestyle='--', alpha=line_alpha)

        plt.xlabel(x_var_name, fontsize=8)
        plt.ylabel('R', fontsize=8)
        plt.legend(fontsize=6)

    """
    Save Fig
    """
    image_save_name_full = image_save_name + '_param'
    plt.suptitle(title_display, fontsize=8)
    proj_sys_sup.save_img(plt, image_folder + image_save_name_full,
                          dpi=300)
    plt.clf()
    plt.close('all')
