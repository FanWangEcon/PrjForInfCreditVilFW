'''
Created on Jun 24, 2018

@author: fan

import projectsupport.graph.graph_sets as sup_graphset

'''


def graph_analyzeaggequi_set():
    """
    These are aggregate graphs looping over a grid of parameter values, or estimation iteration
    graphing at the combo_type level
    """
    graph_analyzeaggequi_list = ['graph_agg_j7',  # 8
                                 'graph_agg_bj2',  # 9
                                 'graph_agg_j2',  # 10
                                 'graph_agg_params',  # 11
                                 'graph_agg_moments']  # 12
    return graph_analyzeaggequi_list


def graph_analyzesolu_set():
    """
    graphs 0 1 2 3 4 5
    graphing at param_combo level
    """
    graph_analyzesolu_list = ['solu_data_pd',
                              # add here to allow for output of solution csv files for CEV without graphs
                              'graph_maxj_nologit',  # 0
                              'graph_solu_dist',  # 1
                              'graph_eachj_prob',  # 2
                              'graph_optimalChoice7Cates',  # 3
                              'graph_optimal_continuous_ktp',  # 4
                              'graph_optimal_continuous_btp']  # 5
    return graph_analyzesolu_list


def graph_panda_sets_names(graph_panda_list_name=None):
    """
    List of graph and panda table names. 
    each name correspond to a different graph, table, including these images
    and table in the list leads to their production and saving. 
    
    """
    #     timesufx = ''

    graph_all = graph_analyzesolu_set() \
                + ['graph_transprob',  # 6
                   'graph_marginal_dist'] \
                + graph_analyzeaggequi_set() \
                + ['graph_inti_int_vec_as_exo',  # 13 (9)
                   'graph_demand_supply_interest',  # 14 (10)

                   'graph_choices_i_eachj_polygon']  # 15 (11)

    panda_all = ['solu_data_pd',
                 'steady_trans_prob',
                 'steady_marginal',
                 'agg_json_csv']

    graph_list_idx = []
    panda_list_idx = []

    agg = [8, 9, 11, 12]
    if '_esti' in graph_panda_list_name:
        agg = [11, 12]

    if graph_panda_list_name is None:
        graph_list_idx = [0, 2]
        panda_list_idx = [3]

    if 'all_graphs_tables' in graph_panda_list_name:
        graph_list_idx = [0, 1, 2, 3, 4, 5, 6, 7] + agg + [13, 14, 15]
        panda_list_idx = [0, 1, 2, 3]
    #         graph_list_idx = [10]
    #         panda_list_idx = []

    if 'all_solu_graphs_tables' in graph_panda_list_name:
        graph_list_idx = [0, 1, 2, 3, 4, 5, 6, 7] + agg + [13, 14]
        panda_list_idx = [0, 1, 2, 3]
    #         graph_list_idx = [10]
    #         panda_list_idx = []

    if 'main_aAcsv_graphs' in graph_panda_list_name:
        '''
        Include also csv file that includes policy prob aggregates at (a=coh,A)
        '''
        graph_list_idx = [0, 2, 3, 6, 7] + agg + [13, 14]
        panda_list_idx = [0, 1, 2, 3]

    if 'main_aA_graphs' in graph_panda_list_name:
        '''
        subset of main_aAcsv_graphs, more important main files
        '''
        graph_list_idx = [0, 6, 7] + agg + [13, 14]
        panda_list_idx = [2, 3]

    if 'main_aAmin_graphs' in graph_panda_list_name:
        '''
        subset of main_aAcsv_graphs, more important main files
        '''
        graph_list_idx = agg + [13, 14]
        panda_list_idx = [2, 3]

    if 'main_graphs' in graph_panda_list_name:
        graph_list_idx = [0, 2, 3, 6, 7] + agg + [13, 14]
        panda_list_idx = [3]

    if 'min_graphs' in graph_panda_list_name:
        graph_list_idx = agg + [13, 14]
        panda_list_idx = [3]

    if 'main_cev_graphs' in graph_panda_list_name:
        # for cev outputs, just need to store the solu file, otherwise same as min_graphs
        graph_list_idx = agg + [13, 14]
        panda_list_idx = [0, 3]

    if 'no_graphs' in graph_panda_list_name:
        graph_list_idx = []
        panda_list_idx = []

    graph_list = [graph_all[ctr] for ctr in graph_list_idx]
    panda_list = [panda_all[ctr] for ctr in panda_list_idx]

    graph_panda_list = graph_list + panda_list

    return graph_panda_list


if __name__ == "__main__":
    print(graph_panda_sets_names(graph_panda_list_name=None))
    print(graph_panda_sets_names(graph_panda_list_name='all_solu_graphs'))
