'''
Created on Jun 27, 2018

@author: fan

Graph out how parameters are changing across estimation iteration, or simulation loop
'''

import logging
import matplotlib
import matplotlib.pyplot as plt
import pyfan.graph.tools.subplot as sup_graph_subplot

import projectsupport.graph.colorsize as support_colors
import projectsupport.systemsupport as proj_sys_sup

matplotlib.use('Agg')

logger = logging.getLogger(__name__)


def graph_estiobj(pd_file_equi_out,
                  x_var_name,
                  title_display, image_save_name, image_folder):
    """
    Graph Parameters
    
    
    Graphs: 
    ---------------------------------------------------------
    - overall obj  - main_obj_set1 - main_obj_set2 ...
    ---------------------------------------------------------
    - main_obj_set3 - ... - main_obj_sets_together - other_obj_sets_together
    ---------------------------------------------------------
    
    Parameters
    ----------
    x_var_name: string
        should just be index key string
        
    Examples
    --------
    import projectsupport.graph.stationary_agg_moments as graphsteadymoments
    graphsteadymoments.graph_estiobj(
                            pd_file_equi_out, x_var_name,
                            title_display, image_save_name, image_folder)
                                                
    """

    if ('esti_obj.main_obj' in pd_file_equi_out.columns):

        '''
        A. Get Columns in esti_obj
            see momcomp.py, source of 'subsets_other' and 'subsets_main'
        '''
        subsets_main_cols = [col for col in pd_file_equi_out.columns if 'subsets_main' in col]
        subsets_other_cols = [col for col in pd_file_equi_out.columns if 'subsets_other' in col]

        # 1. overall obj; 2. main obj components together; 3. other obj components together
        image_base = 3
        image_total = 3
        if ('esti_obj.main_allperiods_obj' in pd_file_equi_out.columns):
            # multi period estimation with individual period objective and overall objectie
            image_base = 4
            image_total = 4
        if (len(subsets_main_cols) > 1):
            # if subsets_main_cols = 1, no component subsets, so just 3 figures
            image_total = image_base + len(subsets_main_cols)

        '''
        B. Strings and figure initialization
        '''
        figsize, rows, cols = sup_graph_subplot.subplot_design(plot_count=image_total,
                                                               base_multiple=4,
                                                               base_multiple_high_frac=0.60)

        line_specs = support_colors.scatter_size(pd_file_equi_out.shape[0])
        scatter_size = line_specs['scatter_size']
        scatter_alpha = line_specs['scatter_alpha']
        scatter_marker = line_specs['scatter_marker']
        line_width = line_specs['line_width']
        line_alpha = line_specs['line_alpha']

        '''
        C. x variable, could be a list of parameters, or a single parameter
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
        E0. Three Main Plots Always
        '''
        fig_ctr_list = [1, 2, 3]
        if ('esti_obj.main_allperiods_obj' in pd_file_equi_out.columns):
            fig_ctr_list = [0, 1, 2, 3]

        ctr_actual = 0
        for fig_ctr in fig_ctr_list:
            ctr_actual = ctr_actual + 1
            if (fig_ctr == 0):
                # overall objective
                looping_columns = ['esti_obj.main_allperiods_obj']
                y_name = 'esti_obj.main_allperiods_obj'
            if (fig_ctr == 1):
                # overall objective
                looping_columns = ['esti_obj.main_obj']
                y_name = 'esti_obj.main_obj'
            if (fig_ctr == 2):
                # subsets of overall
                looping_columns = subsets_main_cols
                y_name = 'esti_obj.main_obj subsets'
            if (fig_ctr == 3):
                # overall objective
                looping_columns = subsets_other_cols
                y_name = 'other obj subsets'

            '''
            E1. Figure Plot Parameter 
            '''
            plt.subplot(rows, cols, ctr_actual)
            plt.grid()

            '''
            E2. Looping Over Each Values
            '''
            for cur_col in looping_columns:
                current_obj = pd_file_equi_out[cur_col]
                plt.scatter(x_var, current_obj, label=cur_col,
                            s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
                plt.plot(x_var, current_obj, label='_nolegend_',
                         linewidth=line_width, alpha=line_alpha)

            plt.xlabel(x_var_name, fontsize=8)
            plt.ylabel(y_name, fontsize=8)
            plt.legend(fontsize=6)

        '''
        F. looping over parameters
        '''
        if (image_total > image_base):
            for subset_col_ctr, cur_subset_col in enumerate(subsets_main_cols):
                plt.subplot(rows, cols, subset_col_ctr + image_base + 1)
                plt.grid()

                current_obj = pd_file_equi_out[cur_subset_col]
                plt.scatter(x_var, current_obj, label=cur_subset_col,
                            s=scatter_size, marker=scatter_marker, alpha=scatter_alpha)
                plt.plot(x_var, current_obj, label='_nolegend_',
                         linewidth=line_width, alpha=line_alpha)

                plt.xlabel(x_var_name, fontsize=8)
                plt.ylabel(y_name, fontsize=8)
                plt.legend(fontsize=6)

        """
        Save Fig
        """
        image_save_name_full = image_save_name + '_estiobj'
        plt.suptitle(title_display, fontsize=8)
        proj_sys_sup.save_img(plt, image_folder + image_save_name_full,
                              dpi=300)
        plt.clf()
        plt.close('all')
