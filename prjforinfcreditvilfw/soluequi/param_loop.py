'''
Created on May 18, 2018

@author: fan

Partial Equilibrium Results, Sets of Results, Steady State Distributional Effects
'''
import logging

import analyze.analyzeequi as analyzeequi
import parameters.combo as paramcombo
import projectsupport.datamanage.data_from_json as datajson
import projectsupport.hardcode.file_name as proj_sup_filename
import solusteady.simu_inner_loop as steadyinnerloop
import solusteady.simu_integrate_loop as steadyintegrateloop

logger = logging.getLogger(__name__)


def policies_steady_states(combo_type, combo_list=None,
                           compute_specs='l-ng-s-x',
                           save_directory='C:',
                           panda_graph_only=False,
                           parallel=False,
                           graph_list=None,
                           export_json=True,
                           save_csv=True):
    """
    Given a range of policy values
    _exo_ files and aggregations
    
    Parameters
    ----------
    graph: boolean
        if graph is true, graph_solu = true
        however, always graph graph_demand_supply = True
        at some point, I wanted to save space on docker image, so created docker
        without matplotlib, but that was only a tiny bit smaller than with matplotlib.
    
    """
    #     if (graph_list is None):
    #         graph_list = ['graph_agg_at_equi']

    if combo_list is None:
        combo_list = paramcombo.get_combo(combo_type, compute_specs)

    #     parallel=False
    max_of_J = True
    weightJ = True

    """
    2. Solve and Simulate (save results to key summary results json)
    """
    if '_ITG_' in combo_type[1]:
        integrated = True
        func_invoke = steadyintegrateloop.steady_loop_integrate
    else:
        integrated = False
        func_invoke = steadyinnerloop.steady_loop_inner

    suf_dict = proj_sup_filename.file_suffix(equilibrium=False, integrated=integrated)
    exo_or_endo = suf_dict['exo_or_endo']
    exo_or_endo_json_search = suf_dict['exo_or_endo_json_search']
    exo_or_endo_graph_row_select = suf_dict['exo_or_endo_graph_row_select']
    image_save_name_prefix = suf_dict['image_save_name_prefix']

    if panda_graph_only is False:
        #         try:
        combo_list_results_list = \
            func_invoke(combo_list, compute_specs,
                        save_directory,
                        parallel=parallel,
                        max_of_J=max_of_J,
                        weightJ=weightJ,
                        graph_list=graph_list,
                        export_json=export_json,
                        exo_or_endo=exo_or_endo)
    #         except:
    #             combo_list_results_list = None

    """
    3. Combine key json summary results
        This will sweep up results also from loop_r invoke if that already happened
        just one big panda file for all results for this param_combo
    """

    export_agg_json_csv = True
    if 'esti_param_vec_count' in compute_specs:
        export_agg_json_csv = False

    if export_agg_json_csv:
        panda_df_save_directory = save_directory['csv']
        panda_df_save_filename = combo_type[1] + exo_or_endo + '.csv'
        panda_df = datajson.json_to_panda(
            directory=save_directory['json'],
            file_str='*' + combo_type[1] + exo_or_endo_json_search,
            agg_df_name_and_directory=panda_df_save_directory + panda_df_save_filename)

        """
        5. Graphing Steady State Aggregate
        """
        select_r_equi = False
        R_INFORM_BORR = panda_df['esti_param.R_INFORM_BORR'].iloc[0]
        title_display = combo_list[0]['title'] + '\n Exogenous Fixed R=' + str(R_INFORM_BORR)
        analyzeequi.equi_graph_main(combo_type, combo_list, compute_specs,
                                    jsons_panda_df=panda_df,
                                    exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                    select_r_equi=select_r_equi,
                                    save_directory=save_directory,
                                    title_display=title_display,
                                    image_save_name_prefix=image_save_name_prefix,
                                    graph_list=graph_list)

    """
    5. Return Results
    """
    return combo_list_results_list


def export_agg_json_or_not(graph_list,
                           compute_specs,
                           save_directory,
                           combo_type,
                           exo_or_endo_json_search):
    export_agg_json_csv = True
    to_count_files = False
    graph_freq = 20
    if ('agg_json_csv' not in graph_list):
        export_agg_json_csv = False

    if ('esti_param_vec_count' in compute_specs):
        # in estimation mode, need to count to see if stopping yet
        to_count_files = True
        export_agg_json_csv = False

        graph_freq = compute_specs['graph_frequncy']
    #             do not graph

    if (to_count_files):
        file_count = datajson.json_to_panda(
            directory=save_directory['json'],
            file_str='*' + combo_type[1] + exo_or_endo_json_search,
            count_file_only=True)
        # times 2 because wgt and max results

    st_solu_size = 'test'
    if '_ITG_' in combo_type[1]:

        # 2 regions, 8 integration points 1 integrated, 2 wgt max
        if st_solu_size == 'standard':
            max_rows_allowed = int(compute_specs['esti_max_func_eval'] * 2 * 9 * 2)

        # 2 regions, 3 integration points 1 integrated, 2 wgt max
        if st_solu_size == 'test':
            max_rows_allowed = int(compute_specs['esti_max_func_eval'] * 2 * 4 * 2)
    else:

        if st_solu_size == 'standard':
            max_rows_allowed = int(compute_specs['esti_max_func_eval'] * 2)

        if st_solu_size == 'test':
            max_rows_allowed = int(compute_specs['esti_max_func_eval'] * 2 * 2)

    # if (max_rows_allowed + 1 <= file_count):
    if max_rows_allowed <= file_count:
        export_agg_json_csv = 'EXCEPTION'

    if (file_count % graph_freq == 0) and (file_count != 0):
        # even for estimation, generate the csv file every 10 csv
        export_agg_json_csv = True
        # if false, only graph at the end of estimation
        export_agg_json_csv = False

    return export_agg_json_csv
