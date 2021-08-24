"""
The :mod:`prjforinfcreditvilfw.analyze.analyzesteady` provides steady state solution visualizations.

Includes method :func:`steady_graph_main`, and :func:`gen_param_dict_moment`
"""

from copy import deepcopy

import logging

import projectsupport.graph.stationary_dist as graph_station
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def steady_graph_main(trans_prob, simu_output_pd,
                      simu_moments_output, param_inst,
                      directory_str_dict,
                      graph_list=None, export_json=True):
    """
    Function returns param_dict_moments, these results if export_json is true
    could be saved.
    
    Parameters
    ----------
    export_panda: boolean
        export simulation transition probability matrix as well as marginal 
        distribution along with choices at each marginal distribution grid points
    export_json: boolean
        export param_dict_moments: model parameters, and model equilibrium aggregate outcomes.
        if. These are just a few numbers very summary form of results. 
        export_panda exports deeper detailed full distributional results. 
        
    Returns
    -------
    param_dict_moments: dictionary
        nested dictionary with all invokation parameters and aggregation results
        for k, b, output etc, that are needed for equilibrium analysis and analyzing
        effects of parameters on equilibrium aggregates.  
    
    Examples
    --------
    import analyze.analyzesteady as analyzesteady
    param_dict_moments_integrated = analyzesteady.steady_graph_main(
                                        trans_prob=trans_prob_integrated,
                                        simu_output_pd=simu_output_pd_integrated,
                                        simu_moments_output=simu_moments_output_integrated,
                                        param_inst=param_inst,
                                        directory_str_dict=directory_str_dict,
                                        graph_list=graph_list,
                                        export_json=export_json)
    """

    log_directory = directory_str_dict['log']
    csv_directory = directory_str_dict['csv_detail']
    json_directory = directory_str_dict['json']
    image_directory = directory_str_dict['img_detail']

    title = directory_str_dict['title']
    file_save_suffix = directory_str_dict['file_save_suffix']
    combo_desc = directory_str_dict['combo_desc']

    cash_grid_centered = simu_output_pd['cash_grid_centered']
    marginal_dist = simu_output_pd['marginal_dist']

    '''
    json
    '''
    '''Equilibrium Results (and all parameters)'''
    #     json_file_name = 's' + file_save_suffix + '.json'

    param_dict_moments = gen_param_dict_moment(param_inst,
                                               simu_moments_output,
                                               file_save_suffix,
                                               json_directory,
                                               export_json)

    '''
    Store Distributional Results
    '''
    if ('steady_trans_prob' in graph_list):
        '''Transition Probability'''
        csv_file_name = 'transp' + file_save_suffix + '.csv'
        trans_prob_row_idx = cash_grid_centered
        trans_prob_header = cash_grid_centered
        proj_sys_sup.save_panda(csv_directory + csv_file_name, trans_prob,
                                header=trans_prob_header,
                                rowindex=trans_prob_row_idx,
                                is_panda=False)

    if ('steady_marginal' in graph_list):
        '''Steady State Distributions'''
        csv_file_name = 'steady' + file_save_suffix + '.csv'
        proj_sys_sup.save_panda(csv_directory + csv_file_name, simu_output_pd, header='', is_panda=True)

    '''
    Graph
    '''
    if ('graph_transprob' in graph_list):
        '''Transition Probability'''
        save_file_name = 'transp' + file_save_suffix
        graph_station.graph_transprob(cash_grid_centered, trans_prob,
                                      title + ' ' + file_save_suffix,
                                      image_directory, save_file_name)

    if ('graph_marginal_dist' in graph_list):
        '''Steady State Distributions'''
        save_file_name = 'steady' + file_save_suffix
        graph_station.graph_marginal_dist(cash_grid_centered, marginal_dist, trans_prob,
                                          title + ' ' + file_save_suffix,
                                          image_directory, save_file_name)

    return param_dict_moments


def gen_param_dict_moment(param_inst,
                          simu_moments_output,
                          file_save_suffix,
                          json_directory,
                          export_json=True):
    """
    import analyze.analyzesteady as analyzesteady
    analyzesteady.gen_param_dict_moment(param_inst, 
                          simu_moments_output,
                          file_save_suffix,
                          json_directory,
                          json_file_name,
                          export_json=True):
    """

    json_file_name = proj_hardcode_filename.file_json(file_save_suffix)

    param_inst_copy = deepcopy(param_inst)
    param_dict_moments = vars(param_inst_copy)

    logger.debug('param_dict_moments:\n%s', param_dict_moments)

    # Code below only keeps 3 parameters from interpolant, others dropped
    interpolant = param_dict_moments['interpolant']
    interpolant_subset = {k: interpolant[k]
                          for k in interpolant.keys() &
                          {'interp_type',
                           'interp_type_option',
                           'maxinter'}}
    param_dict_moments['interpolant'] = interpolant_subset

    param_dict_moments.update(simu_moments_output)
    param_dict_moments['file_save_suffix'] = file_save_suffix

    param_dict_moments['json_directory'] = json_directory
    param_dict_moments['json_file_name'] = json_file_name
    if (export_json):
        proj_sys_sup.save_json(json_directory + json_file_name,
                               param_dict_moments, replace=True)

    return param_dict_moments
