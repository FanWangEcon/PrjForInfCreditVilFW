'''
Created on Apr 8, 2018
@author: fan
'''

from copy import deepcopy

import logging
import numpy as np
import pyfan.amto.json.json as support_json

import invoke.run_simulate as runsimu
import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def estimate_objective(params_esti, param_esti_group_key_list,
                       moments_type=['a', '20180724_test'], use_states_data=False, use_likelihood=False,
                       combo_type='', param_combo='',
                       compesti_specs=None,
                       return_type='obj',
                       ge=False, multiprocess=False,
                       graph_list=None,
                       save_directory='estisubdirectory',
                       logger=None,
                       **kwargs):
    """
    Update Parameters with Latest Point as determined by algorithm
    """
    if (logger == None):
        logger = logging.getLogger(__name__)

    print('New Estimates:', params_esti)
    support_json.jdump([str(param_esti_group_key) + ':' + str(param)
                        for param_esti_group_key, param in zip(param_esti_group_key_list, params_esti)],
                       'cur-estimate', logger=logger.critical)

    '''
    A. Updating Dictionaries
    Updating dictionaries for each param_group, updating potentially many 
    parameters in many groups concurrently in estimation procedure.
    '''
    grid_param_adjust_dict = {}
    esti_param_adjust_dict = {}
    data_param_adjust_dict = {}
    model_param_adjust_dict = {}
    interpolant_adjust_dict = {}
    dist_param_adjust_dict = {}
    for param_esti_counter in np.arange(len(param_esti_group_key_list)):

        '''A. Current Value of Estimate'''
        params_esti_cur = params_esti[param_esti_counter]

        '''B. Key and paramger group'''
        param_esti_group_key = param_esti_group_key_list[param_esti_counter]
        param_shortname, param_type, param_name = paramloopstr.param_type_param_name(
            param_group_key=param_esti_group_key)

        if (param_type == 'grid_type'):
            grid_param_adjust_dict[param_name] = params_esti_cur
        if (param_type == 'esti_type'):
            esti_param_adjust_dict[param_name] = params_esti_cur
        if (param_type == 'data_type'):
            data_param_adjust_dict[param_name] = params_esti_cur
        if (param_type == 'model_type'):
            model_param_adjust_dict[param_name] = params_esti_cur
        if (param_type == 'interpolant_type'):
            interpolant_adjust_dict[param_name] = params_esti_cur
        if (param_type == 'dist_type'):
            '''
            Nested param_key for dist_param is fine (with many dots) because
            paraminstpreset.py line 152 can replace nesting values
            under the assumption that full nest structure is written out in 
            combo_list_c_esti.py's targeted a_dist group 
            '''
            dist_param_adjust_dict[param_name] = params_esti_cur

    '''
    B. Update Param_combo    
    '''
    # param_combo is the orginal, do not change that
    param_combo_cur_esti = deepcopy(param_combo)

    # Loop over parameter types to update all 
    param_types_adjust_dict = {'grid_type': grid_param_adjust_dict,
                               'esti_type': esti_param_adjust_dict,
                               'data_type': data_param_adjust_dict,
                               'model_type': model_param_adjust_dict,
                               'interpolant_type': interpolant_adjust_dict,
                               'dist_type': dist_param_adjust_dict}

    display_str = ''
    for param_type, param_adjust_dict in param_types_adjust_dict.items():

        if (param_adjust_dict != {}):
            try:
                '''A. Has esti_type 3 elements'''
                cur_type_adjust_dict = param_combo_cur_esti['param_update_dict'][param_type][2]
                cur_type_adjust_dict.update(param_adjust_dict)
                param_combo['param_update_dict'][param_type][2] = cur_type_adjust_dict
            except:
                '''B. has esti_type'''
                cur_type = param_combo_cur_esti['param_update_dict'][param_type]
                cur_type.append(param_adjust_dict)
                param_combo_cur_esti['param_update_dict'][param_type] = cur_type

            display_str = display_str + \
                          ';'.join('{0:s}-{1:.3f}'.format(key, val)
                                   for key, val in sorted(esti_param_adjust_dict.items()))

    param_combo_cur_esti['title'] = param_combo['title'] + display_str
    param_combo_cur_esti['combo_desc'] = param_combo['combo_desc'] + display_str
    param_combo_cur_esti['file_save_suffix'] = param_combo[
                                                   'file_save_suffix'] + '_' + proj_sys_sup.save_suffix_time(2)

    """
    C. Solve Model
    """
    test_quad = False
    if (test_quad):
        '''
            http://www.wolframalpha.com/input/?i=max+1-2*(x%2B2)%5E2
            2 = argmax (1-2*(x+2)^2) 
            does python minimizer provide the correct solution?
        '''
        #         kappa = param_combo_cur_esti['param_update_dict']['esti_type'][2]['kappa']
        kappa = param_combo_cur_esti['param_update_dict']['esti_type'][2]['rho']
        obj = (1 - 2 * (kappa + 2) ** 2)
        func_return = (-1) * obj

    else:
        combo_list = [param_combo_cur_esti]
        log_file_suffix = '_' + proj_sys_sup.save_suffix_time(2)
        # Invoke with compesti_specs specified, not speckey so that can bring in estimation specs
        combo_list_results_list = runsimu.invoke_soluequi_partial(
            combo_type, combo_list=combo_list,
            speckey=None,
            compesti_specs=compesti_specs,
            ge=ge, multiprocess=multiprocess,
            graph_list=graph_list,
            save_directory_main=save_directory,
            logging_level=logging.INFO,
            log_file=False,
            log_file_suffix=log_file_suffix,
            gen_subfolder=False)
        """
        Estimate
        """

        # Estimation, there is only 1 element in each combo_list
        combo_list_results = combo_list_results_list[0]
        wgtJ_out_dict = combo_list_results['wgtJ_out_dict']
        simu_moments_output = wgtJ_out_dict['simu_moments_output']

        if (return_type == 'obj'):
            '''
            Note that the Moment Objective Function's minimum point is 0. 
            Do not do -1 * obj, only do that for likelihood
            '''
            #         if integrated, had to normalize json, so esti_obj.main_obj is key
            if ('esti_obj.main_obj' in simu_moments_output.keys()):
                obj = simu_moments_output['esti_obj.main_obj']
            else:
                obj = simu_moments_output['esti_obj']['main_obj']
            logger.critical('esti_objective:%s\n', obj)
            func_return = obj
        elif (return_type == 'simu_moments_output'):
            func_return = simu_moments_output
        elif (return_type == 'combo_list_results'):
            func_return = combo_list_results
        else:
            raise Exception("Wrong Return Type, return_type:" + return_type)

    return func_return


def estimate_quad(params_esti, params_esti_str,
                  param_inst,
                  moment_set,
                  use_states_data, use_likelihood):
    logger.critical('params_esti:%s', str(params_esti))

    kappa = params_esti[0]
    obj = 1.5 * kappa - 2 * (kappa ** 2)

    logger.critical('obj = 1.5*kappa - 2*(kappa**2):%s', str(1.5 / 4))

    return (-1) * obj
