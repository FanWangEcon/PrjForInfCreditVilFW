'''
Created on Jul 15, 2018

@author: fan
'''

from copy import deepcopy

import numpy as np
from pandas.io.json import json_normalize

import analyze.analyzesteady as analyzesteady
import parameters.dist.a_dist as param_dist_a
import parameters.paraminstpreset as param_inst_preset
import projectsupport.hardcode.string_shared as hardstring
import solusteady.distribution.moments as analyticalmm
import solusteady.simu_inner_loop as steadyinnerloop


def steady_loop_integrate(combo_list, compute_specs,
                          save_directory,
                          parallel=False,
                          max_of_J=True,
                          weightJ=True,
                          graph_list=None,
                          export_json=True,
                          exo_or_endo='_exo',
                          graph_vec_subset=None):
    """
    - Same inputs as simu_inner_loop.steady_loop_inner
    - Produce the same set of outputs as simu_inner_loop.steady_loop_inner:
        a list of out_dict: combo_list_results_list
        out_dict = {'param_combo':param_combo,
                    'trans_prob':trans_prob,
                    'simu_output_pd':simu_output_pd,
                    'simu_moments_output':simu_moments_output,
                    'param_dict_moments':param_dict_moments}
    - If here, the parallized loop is the type integration loop

    - Process: each param_combo of combo_list has to be integrated
        1. Generate a combo_list from each param_combo based on the integration
            variable
        2. For each combo_list, invoke simu_inner_loop.py to produce combo_list_results_list for
            each integration point. 
        3. Integrate
        
    Examples
    --------
    import solusteady.simu_integrate_loop as steadyintegrateloop
    steadyintegrateloop.steady_loop_integrate(combo_list, compute_specs, save_directory)
    
    """

    if (graph_vec_subset is None):
        graph_vec_subset = np.arange(len(combo_list))

    combo_list_results_list = []
    for param_combo_ctr, param_combo in enumerate(combo_list):
        if (param_combo_ctr in graph_vec_subset):
            graph_list_use = graph_list
        else:
            graph_list_use = []

        args_cur = (param_combo, compute_specs,
                    save_directory, parallel,
                    max_of_J, weightJ,
                    graph_list_use, export_json, exo_or_endo)

        out_dict = main_integrate_steady(args_cur)
        combo_list_results_list.append(out_dict)

    return combo_list_results_list


def main_integrate_steady(arg):
    """Integrate
    """
    param_combo, compute_specs, \
    save_directory, parallel, \
    max_of_J, weightJ, \
    graph_list, export_json, exo_or_endo = arg

    param_inst, combo_list_integrate = gen_integrate_param_list(param_combo)

    '''
    generates: _exointegrate_,  _equintegrate_
        csv file search string for aggregates: '*'+combo_type[1]+'*_exo_*'       
    '''

    combo_list_integrate_results_list = \
        steadyinnerloop.steady_loop_inner(combo_list_integrate, compute_specs,
                                          save_directory,
                                          parallel=parallel,
                                          max_of_J=max_of_J,
                                          weightJ=weightJ,
                                          graph_list=graph_list,
                                          export_json=export_json,
                                          exo_or_endo=exo_or_endo)

    directory_str_dict = {'title': param_combo['title'],
                          'file_save_suffix': param_combo['file_save_suffix'],
                          'combo_desc': param_combo['combo_desc']}
    directory_str_dict.update(save_directory)

    out_dict_integrated = {}
    for max_or_wgt in ['maxJ_out_dict', 'wgtJ_out_dict']:
        #     for max_or_wgt in ['wgtJ_out_dict']:

        if (max_or_wgt == 'maxJ_out_dict'):
            exo_or_endo_add = exo_or_endo + '_maxJitg'
            directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + exo_or_endo_add

        if (max_or_wgt == 'wgtJ_out_dict'):
            exo_or_endo_add = exo_or_endo + '_wgtJitg'
            directory_str_dict['file_save_suffix'] = param_combo['file_save_suffix'] + exo_or_endo_add

        out_dict_integrated[max_or_wgt] = integration(param_combo, param_inst,
                                                      directory_str_dict, graph_list, export_json,
                                                      max_or_wgt, combo_list_integrate_results_list)

    return out_dict_integrated


def gen_integrate_param_list(param_combo):
    """Generate param_list integration points based on param_combo
    
    Within a_dist.py, for current param_combo, a list of parameters for distribution
    
    Returns
    -------
    param_inst: object
        param_inst for param_combo, without the integration stuff stuff
    combo_list_integrate: list 
        list of param_combo, each at a particular integration point
    """

    param_inst = param_inst_preset.get_param_inst_preset_combo(param_combo)

    combo_list_integrate = []

    title_init = param_combo['title']
    combo_desc_init = param_combo['combo_desc']
    file_save_suffix_init = param_combo['file_save_suffix']

    if 'dist_param_integrate_points' in param_inst.dist_param.keys():
        dist_param_integrate_points = param_inst.dist_param['dist_param_integrate_points']
    else:
        dist_param_integrate_points = param_dist_a.gen_dist_param_integrate_points_sample()

    title_integrate_loop = dist_param_integrate_points['title_integrate_loop']
    file_save_suffix_integrate_loop = dist_param_integrate_points['file_save_suffix_integrate_loop']
    combo_desc_integrate_loop = dist_param_integrate_points['combo_desc_integrate_loop']

    param_types = dist_param_integrate_points['param_types']
    param_names = dist_param_integrate_points['param_names']
    param_values_keys = dist_param_integrate_points['param_values_keys']

    param_weights = dist_param_integrate_points['param_weights']
    param_values = dist_param_integrate_points['param_values']
    param_descs = dist_param_integrate_points['param_descs']
    param_save_suffixs = dist_param_integrate_points['param_save_suffixs']

    '''
    creates empty: {'data_type':{},
                    'esti_type':{}}
    '''
    val_dict = {}
    for param_type, param_name in zip(param_types, param_names):
        val_dict[param_type] = {}

    '''
    Generate new combo_list
    '''
    for integrate_point_ctr, integrate_point_wgt in enumerate(param_weights):

        param_combo_cur = deepcopy(param_combo)

        '''
        Generate new combo_list
        creates: {'data_type':{'A':1.1},
                  'esti_type':{'BNF_SAVE_P':2.3}}
        '''
        for param_type, param_name, param_values_key in zip(param_types, param_names, param_values_keys):
            param_value = param_values[param_values_key][integrate_point_ctr]
            val_dict[param_type][param_name] = param_value

        '''
        some string like p11 for example
        '''
        param_desc = param_descs[integrate_point_ctr]
        param_save_suffix = param_save_suffixs[integrate_point_ctr]

        '''
        Integrating point specific title
        '''
        title = title_init + title_integrate_loop + '(' + param_desc + ')'
        combo_desc = combo_desc_init + combo_desc_integrate_loop + '(' + param_desc + ')'
        file_save_suffix = file_save_suffix_init + file_save_suffix_integrate_loop + param_save_suffix

        param_combo_cur['title'] = title
        param_combo_cur['combo_desc'] = combo_desc
        param_combo_cur['file_save_suffix'] = file_save_suffix
        param_combo_cur['integrate_weight'] = integrate_point_wgt

        '''
        1B. Parameter Updating
        '''
        for param_type_key, param_type_update_val in val_dict.items():
            try:
                '''
                A. check if each of the param_type has 3rd elements
                '''
                cur_type_adjust_dict = param_combo_cur['param_update_dict'][param_type_key][2]
                cur_type_adjust_dict.update(param_type_update_val)
                param_combo_cur['param_update_dict'][param_type_key][2] = cur_type_adjust_dict

            except:
                '''
                B. has param_type but not the 3rd element (so should always have this)
                '''
                esti_type_cur = param_combo_cur['param_update_dict'][param_type_key]
                esti_type_cur.append(param_type_update_val)
                param_combo_cur['param_update_dict'][param_type_key] = esti_type_cur

        '''
        Add Informal R current to list
        '''
        param_combo_cur_to_append = deepcopy(param_combo_cur)
        combo_list_integrate.append(param_combo_cur_to_append)

    return param_inst, combo_list_integrate


def integration(param_combo, param_inst,
                directory_str_dict, graph_list, export_json,
                max_or_wgt, combo_list_integrate_results_list):
    """
    Creates same outputs as main_solu_steady() from simu_inner_loop.py
    and uses analyzesteady.steady_graph_main() to save json/graph etc. 
    
    Parameters
    ----------
    param_inst: object with dictionaries
        param_inst for main param_combo
    combo_list_integrate: list of param_combo 
        each param_combo at a different integration point
    """

    '''
    simu_moments_output_integrated:
        Aggregating over all
        make sure weights and moments columns match up    
    '''
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    '''
    A. Mean and Variance for Key Aggregates
    '''
    simu_moments_output_agg_mean_wgted = {}
    simu_moments_output_agg_var_wgted = {}
    calc_list = ['mean', 'var']
    for cur_stat in calc_list:
        for pc_ctr, pc_out_dict_wgtmax in enumerate(combo_list_integrate_results_list):
            pc_out_dict = pc_out_dict_wgtmax[max_or_wgt]
            cur_weight = pc_out_dict['param_combo']['integrate_weight']

            if (max_or_wgt == 'wgtJ_out_dict'):
                simu_output_pd = pc_out_dict['simu_output_pd']
                calc_list = [cur_stat]

                if (cur_stat == 'mean'):
                    mean_dict = None
                    simu_moments_output_agg_mean, __ = analyticalmm.calculate_variance(
                        simu_output_pd,
                        param_inst,
                        calc_list=calc_list,
                        mean_dict=mean_dict)
                    if (pc_ctr == 0):
                        simu_moments_output_agg_mean_wgted = {key: simu_moments_output_agg_mean[key] * cur_weight
                                                              for key, val in simu_moments_output_agg_mean.items()}
                    else:
                        simu_moments_output_agg_mean_wgted = {
                            key: simu_moments_output_agg_mean[key] * cur_weight +
                                 simu_moments_output_agg_mean_wgted[
                                     key]
                            for key, val in simu_moments_output_agg_mean.items()}
                if (cur_stat == 'var'):
                    mean_dict = simu_moments_output_agg_mean_wgted
                    simu_moments_output_agg_var, __ = analyticalmm.calculate_variance(
                        simu_output_pd,
                        param_inst,
                        calc_list=calc_list,
                        mean_dict=mean_dict)
                    if (pc_ctr == 0):
                        simu_moments_output_agg_var_wgted = {key: simu_moments_output_agg_var[key] * cur_weight
                                                             for key, val in simu_moments_output_agg_var.items()}
                    else:
                        simu_moments_output_agg_var_wgted = {
                            key: simu_moments_output_agg_var[key] * cur_weight + simu_moments_output_agg_var_wgted[
                                key]
                            for key, val in simu_moments_output_agg_var.items()}

    '''
    B1. Mean of Other Keys: Obtain Data
    '''
    simu_moments_output_list = []
    for pc_ctr, pc_out_dict_wgtmax in enumerate(combo_list_integrate_results_list):
        pc_out_dict = pc_out_dict_wgtmax[max_or_wgt]
        simu_moments_output_cur = pc_out_dict['simu_moments_output']
        cur_weight = pc_out_dict['param_combo']['integrate_weight']
        simu_moments_output_cur['integrate_weight'] = cur_weight
        simu_moments_output_list.append(simu_moments_output_cur)

    simu_moments_output_df = json_normalize(simu_moments_output_list)
    all_numeric_columns = simu_moments_output_df.select_dtypes(include=['number']).columns

    '''
    B2. Mean of Other Keys: Mean
    '''
    mean_cols = [col for col in all_numeric_columns if steady_agg_suffixes['_var'][0] not in col]
    simu_moments_output_df_wgt_mean = simu_moments_output_df[mean_cols].multiply(
        simu_moments_output_df["integrate_weight"], axis="index")
    simu_moments_output_integrated_means_others = simu_moments_output_df_wgt_mean.sum(numeric_only=True)

    '''
    C. Together
    '''
    simu_moments_output_integrated = simu_moments_output_integrated_means_others
    if (max_or_wgt == 'wgtJ_out_dict'):
        simu_moments_output_integrated = simu_moments_output_integrated.to_dict()
        simu_moments_output_integrated.update(simu_moments_output_agg_mean_wgted)
        simu_moments_output_integrated.update(simu_moments_output_agg_var_wgted)

    '''
    D. Calculate moment estimation objectives 
    '''
    if ('moments_type' in param_inst.support_arg):
        pass

    '''
    E. trans_prob_integrated and simu_output_pd_integrated
    '''
    for pc_ctr, pc_out_dict_wgtmax in enumerate(combo_list_integrate_results_list):
        pc_out_dict = pc_out_dict_wgtmax[max_or_wgt]
        trans_prob_cur = pc_out_dict['trans_prob']
        simu_output_pd_cur = pc_out_dict['simu_output_pd']

        integrate_weight = pc_out_dict['param_combo']['integrate_weight']

        if (pc_ctr == 0):
            trans_prob_integrated = trans_prob_cur * integrate_weight
            simu_output_pd_integrated = simu_output_pd_cur * integrate_weight
        else:
            trans_prob_integrated += trans_prob_cur * integrate_weight
            simu_output_pd_integrated += simu_output_pd_cur * integrate_weight

    '''
    F. param_dict_moments_integrated:
    '''
    param_dict_moments_integrated = analyzesteady.steady_graph_main(
        trans_prob=trans_prob_integrated,
        simu_output_pd=simu_output_pd_integrated,
        simu_moments_output=simu_moments_output_integrated,
        param_inst=param_inst,
        directory_str_dict=directory_str_dict,
        graph_list=graph_list,
        export_json=export_json)

    '''
    returns
    '''
    out_dict_integrated = {'param_combo': param_combo,
                           'trans_prob': trans_prob_integrated,
                           'simu_output_pd': simu_output_pd_integrated,
                           'simu_moments_output': simu_moments_output_integrated,
                           'param_dict_moments': param_dict_moments_integrated}

    return out_dict_integrated
