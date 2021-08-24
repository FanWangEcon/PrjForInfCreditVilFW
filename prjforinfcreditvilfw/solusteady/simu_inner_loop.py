'''
Created on Jul 14, 2018

@author: fan
'''

import multiprocessing
import numpy as np

import analyze.analyzesolu as analyzesolu
import analyze.analyzesteady as analyzesteady
import solusteady.simuanalytical as simu_analytical


def steady_loop_inner(combo_list, compute_specs,
                      save_directory,
                      parallel=False,
                      max_of_J=True,
                      weightJ=True,
                      graph_list=None,
                      export_json=True,
                      exo_or_endo='_exo',
                      graph_vec_subset=None):
    """
        
    Parameters
    ----------
    graph_vec_subset: list or None
        which subset of parameters to generate graphs for
        
    Examples
    --------    
    import solusteady.simu_param_loop as steadyinnerloop
    steadyinnerloop.steady_loop_inner(combo_list, compute_specs, save_directory)
    """

    if (graph_vec_subset is None):
        graph_vec_subset = np.arange(len(combo_list))

    args = []
    for param_combo_ctr, param_combo in enumerate(combo_list):
        if (param_combo_ctr in graph_vec_subset):
            graph_list_use = graph_list
        else:
            graph_list_use = []

        args_cur = (param_combo, save_directory,
                    max_of_J, weightJ,
                    graph_list_use, export_json, exo_or_endo)
        args.append(args_cur)

    if (parallel):
        parallel_workers = compute_specs['workers']
        if (multiprocessing.cpu_count() < parallel_workers):
            parallel_workers = multiprocessing.cpu_count()
        p = multiprocessing.Pool(parallel_workers)
        # p.map is ordered, there is another function for not ordered.
        combo_list_results_list = p.map(main_solu_steady, args)
        p.close()
        p.join()

    else:
        counter = 0
        combo_list_results_list = []
        for arg in args:
            counter = counter + 1
            out_dict = main_solu_steady(arg)
            combo_list_results_list.append(out_dict)

    return combo_list_results_list


def main_solu_steady(arg):
    param_combo, save_directory, \
    max_of_J, weightJ, \
    graph_list, export_json, exo_or_endo = arg

    directory_str_dict = {'title': param_combo['title'],
                          'file_save_suffix': param_combo['file_save_suffix'],
                          'combo_desc': param_combo['combo_desc']}
    directory_str_dict.update(save_directory)

    solu_dict, mjall_inst, param_inst = simu_analytical.solve_policy(param_combo,
                                                                     directory_str_dict=directory_str_dict,
                                                                     graph_list=graph_list)

    """
    A. Solution Graphs, will only graph if graph_list has right elements
    """
    analyzesolu.solve_graph_main(solu_dict, mjall_inst, param_inst, directory_str_dict,
                                 graph_list=graph_list)

    param_dict_moments_list = []
    out_dict = {}
    if (max_of_J):
        exo_or_endo_add = exo_or_endo + '_maxJ'
        directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + exo_or_endo_add
        trans_prob, simu_output_pd, simu_moments_output = \
            simu_analytical.solve_dist(
                param_combo, solu_dict, mjall_inst, param_inst,
                max_of_J=True)

        param_dict_moments = analyzesteady.steady_graph_main(trans_prob, simu_output_pd,
                                                             simu_moments_output, param_inst,
                                                             directory_str_dict,
                                                             graph_list=graph_list,
                                                             export_json=export_json)
        param_dict_moments_list.append(param_dict_moments)

        # only get these from weightJ for now
        maxJ_out_dict = {'param_combo': param_combo,
                         'trans_prob': trans_prob,
                         'simu_output_pd': simu_output_pd,
                         'simu_moments_output': simu_moments_output,
                         'param_dict_moments': param_dict_moments}

        out_dict['maxJ_out_dict'] = maxJ_out_dict

    if (weightJ):
        exo_or_endo_add = exo_or_endo + '_wgtJ'
        directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + exo_or_endo_add
        trans_prob, simu_output_pd, simu_moments_output = \
            simu_analytical.solve_dist(
                param_combo, solu_dict, mjall_inst, param_inst,
                max_of_J=False)

        param_dict_moments = analyzesteady.steady_graph_main(trans_prob, simu_output_pd,
                                                             simu_moments_output, param_inst,
                                                             directory_str_dict,
                                                             graph_list=graph_list,
                                                             export_json=export_json)
        param_dict_moments_list.append(param_dict_moments)

        # only get these from weightJ for now
        wgtJ_out_dict = {'param_combo': param_combo,
                         'trans_prob': trans_prob,
                         'simu_output_pd': simu_output_pd,
                         'simu_moments_output': simu_moments_output,
                         'param_dict_moments': param_dict_moments}

        out_dict['wgtJ_out_dict'] = wgtJ_out_dict

    return out_dict
