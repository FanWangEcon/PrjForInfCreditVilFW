"""
The :mod:`prjforinfcreditvilfw.analyze.analyzeequi` provides equilibrium visualizations.

Includes method :func:`equi_graph_main`.
"""

import estimation.postprocess.jsoncsv.gen_counter_3dims_data as gen_counter3dims
import projectsupport.graph.stationary_agg_allJ as graphsteadyaggjall
import projectsupport.graph.stationary_agg_credit as graphsteadyaggbn
import projectsupport.graph.stationary_agg_informal as graphsteadyaggj2
import projectsupport.graph.stationary_agg_moments as graphsteadymoments
import projectsupport.graph.stationary_agg_params as graphsteadyparam
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup
import soluequi.panda_param_loop as pd_paramloop


def equi_graph_main(combo_type, combo_list, compute_specs,
                    jsons_panda_df,
                    exo_or_endo_graph_row_select,
                    select_r_equi=False, R_INFROM_common_cur=None,
                    save_directory='', title_display='',
                    image_save_name='', image_save_name_prefix='',
                    graph_list=None,
                    x_var_override=None,
                    sort_by_var_override=None):
    """
    These do not have to graph equilibrium results, just graphs any sequence of
    aggregate outcomes. These aggregate outcomes could be equilibrium outcomes,
    or could be partial. It is plotted after multiple steady have been solved, the
    x-axis is iterating over different parameter values in a grid vector for simulation
    or iterative parameters from estimation routine.

    Examples
    --------
    import analyze.analyzeequi as analyzeequi
    """

    '''
    Count rows, foe esitmation, stop estimation when rows exceed threshold
    '''

    if (x_var_override):
        x_var_name = x_var_override
    else:
        if len(combo_type) == 2:
            # combo_type can be specified with only len = 2 for single simulation.
            combo_type.insert(2, None)

        x_var_name = combo_type[2]

        if isinstance(x_var_name, list):
            if len(x_var_name) == 1:
                x_var_name = combo_type[2][0]

        if (x_var_name is None) or (x_var_name is 'None'):
            # if we are not looping over a particular parameter for simulation
            # but are looping over random initial parameters for estimation for example
            # then just use the dataframe index as the sorting column
            #             x_var_name = 'support_arg.time_end'
            x_var_name = 'pdindex'
            jsons_panda_df[x_var_name] = jsons_panda_df.index
        #             panda_df[x_var_name] = panda_df.index
        else:
            # string or list
            '''
            if doing estimation, see estimate.specs.py
            esti_param_vec_count only appears if doing estimation.
            will not be there if simulation has moments_type momsets_type keys
            '''
            if ('esti_param_vec_count' in compute_specs):
                x_var_name = 'pdindex'
                jsons_panda_df[x_var_name] = jsons_panda_df.index
            else:
                pass

    # for here, if list, use x_var_name list otherwise group by would have only subset of results
    # for not integrated, not ge simulation/estimation, group sort by var don't really matter'
    group_by_var_name = x_var_name
    sort_by_var_name = x_var_name
    if ('esti_param_vec_count' in compute_specs):
        sort_by_var_name = 'support_arg.time_start'
    pd_file_equi_out = pd_paramloop.get_agg_stats_param_loop_catesall(
        jsons_panda_df,
        group_by_var_name=group_by_var_name,
        sort_by_var_name=sort_by_var_name,
        wgt_or_max=exo_or_endo_graph_row_select,
        select_r_equi=select_r_equi,
        select_r_equals2=R_INFROM_common_cur)


    # results
    if (select_r_equi):
        '''
        Equilibrium Invokation.
            generate a subset of results with just equilibrium outcomes
            the full results have also non-equilibrium outcomes, outcomes at all other solved for R points.
        '''
        suffix = hardstring.file_suffix(file_type='csv', sub_type='_endo')
        save_file_name = hardstring.main_file_name(combo_type, suffix, save_directory, save_type='simu_csv')
        proj_sys_sup.save_panda(save_file_name, pd_file_equi_out)

    image_folder = save_directory['img_main']
    if (image_save_name == ''):
        image_save_name = image_save_name_prefix + combo_type[1] + ''
        # If in estimation, save also estimationinformation, estimation folder name
        if ('esti_param_vec_count' in compute_specs):
            estitype_folder_name = combo_list[0]['param_update_dict']['support_arg']['compesti_short_name'] + \
                                   combo_list[0]['param_combo_list_ctr_str']
            image_save_name = image_save_name_prefix + combo_type[1] + '_' + estitype_folder_name

    if (x_var_override):
        image_save_name = image_save_name + '-' + x_var_override.replace('.', '-')

    if (isinstance(x_var_name, list)):
        # Generated inside get_agg_stats_param_loop_catesall()
        x_var_name = 'pdindex'

    '''
    Graph
    '''
    if ('graph_agg_j7' in graph_list):
        graphsteadyaggjall.graph_agg_at_equi_allJ(
            pd_file_equi_out, x_var_name,
            title_display, image_save_name, image_folder)

    if ('graph_agg_bj2' in graph_list):
        graphsteadyaggbn.graph_agg_at_equi_bn(
            pd_file_equi_out, x_var_name,
            title_display, image_save_name, image_folder)

    if ('graph_agg_j2' in graph_list):
        graphsteadyaggj2.graph_agg_at_equi(
            pd_file_equi_out, x_var_name,
            title_display, image_save_name, image_folder)

    if ('graph_agg_params' in graph_list):
        if ((combo_type[2] == None) or combo_type[2] == 'None'):
            pass
        else:
            graphsteadyparam.graph_parameters(
                pd_file_equi_out, combo_type[2], combo_list, x_var_name,
                title_display, image_save_name, image_folder)

    if ('graph_agg_moments' in graph_list):
        graphsteadymoments.graph_estiobj(
            pd_file_equi_out, x_var_name,
            title_display, image_save_name, image_folder)

    '''
    Counterfactual CSVs
    '''
    if ((combo_type[2] == None) or (combo_type[2] == 'None') or ('_2j127' in combo_type[1])):
        pass
    else:
        if ('csv' in save_directory.keys()):
            '''
            save_directory does not have csv for globed esti results
            '''
            if (compute_specs['memory'] == '517'):
                '''
                mpoly don't do this
                '''
            else:
                current_policy_column = combo_type[2][0]
                gen_counter3dims.gen_3dims_csv(simulate_csv_directory=save_directory['csv'],
                                               simulate_csv_file_name=image_save_name,
                                               current_policy_column=current_policy_column,
                                               simu_df=pd_file_equi_out,
                                               exo_or_endo_graph_row_select=exo_or_endo_graph_row_select)

    return pd_file_equi_out
