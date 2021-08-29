'''
Created on May 18, 2018

@author: fan

Invoke
'''

import logging
import time

import parameters.combo as paramcombo
import parameters.runspecs.compute_specs as computespec
import projectsupport.systemsupport as proj_sys_sup
import soluequi.param_loop as soluequipartial
import soluequi.param_loop_r_loop as soluequiinterest

logger = logging.getLogger(__name__)


def invoke_soluequi_partial(combo_type, combo_list=None,
                            speckey='l-ng-s-x',
                            compesti_specs=None,
                            ge=False, multiprocess=False,
                            graph_list=None,
                            save_directory_main='simu',
                            logging_level=logging.WARNING,
                            log_file=False,
                            log_file_suffix='',
                            gen_subfolder=True):
    """
    From estimation:
        - combo_type: is the initial parameters and fixed non-estimated parameters
        - combo_list: a one element list containing updated dictionaries in param_combo
        reflecting current estimation iteration.
        - estimation does not directly invoke this, but invokes estimation program that
        invokes during each estimation iteration this run.py file
    For looping over vector:
        - combo_type: Parameter specifications that represent looping combo_list list
        - combo_list: None
        - test over vector of parameters directly invokes this
             
    Parameters
    ----------
    combo_type: string
        a string that is associated with combo_list
        used more in parameter group testting
    combo_list: list
        list conditioning dictionary with param_inst updates
        if this is specified, this overrides combo_type. 
        used in estimation. 
    speckey: string
        speckey only needed if cokmpesti_spec not available
        perhaps to distinguish between estimation and simulation speckey could be 
        specified if dealing with simulation, but compest_spec if estimation
    compesti_spec: dictionary
        if estimation, speckey which is really comp_spec_key does not contain estimation_key
        so could use est_spec_key and comp_spec_key to generate compeesti_spec when doing
        estimation. 
    ge: boolean
        general equilibrium or not
        
    Examples
    --------
    import invoke.run as invokerun
    invokerun.invoke_soluequi_partial(combo_type,
                                      speckey=speckey, 
                                        ge=ge, multiprocess=multiprocess,
                                        graph_list=graph_list)
    
    """
    #     soluequipartial.policies_steady_states(combo_type, parallel=True)

    '''
    ESTIMATION FOLDER LEVEL 2
    SIMULATION FOLDER LEVEL 1
    '''
    if (ge):
        logfile_name = 'log_rloop_' + combo_type[1] + log_file_suffix
    else:
        logfile_name = 'log_rexo_' + combo_type[1] + log_file_suffix

    if (gen_subfolder):
        sub_folder_name = proj_sys_sup.gen_path(combo_type, st_type='simuesti_subfolder')
        main_directory = proj_sys_sup.get_paths(save_directory_main, sub_folder_name=sub_folder_name)
        json_directory = proj_sys_sup.get_paths(save_directory_main, sub_folder_name=sub_folder_name,
                                                subsub_folder_name='json')
        log_directory = proj_sys_sup.get_paths(save_directory_main, sub_folder_name=sub_folder_name,
                                               subsub_folder_name='log')
    else:
        # from estimation, already with folder created
        main_directory = save_directory_main
        json_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='json')
        log_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='log')

    save_directory = {'json': json_directory,
                      'csv': main_directory,
                      'img_main': main_directory,
                      'log': log_directory}

    if (log_file):
        log_file_name = log_directory + logfile_name + '.log'
        fileHandler, cur_logger = proj_sys_sup.log_start(log_file_name,
                                                         logging_level=logging_level, log_file=log_file,
                                                         module_name='')
    else:
        fileHandler = None

    startTime = time.time()

    # Do not have to specify in compute_set fargate true or false, at this point
    # already on cloud or local, the fargate true of false is just for task/job
    # submissions    
    if (compesti_specs is None):
        compute_specs = computespec.compute_set(speckey)
    else:
        compute_specs = compesti_specs

    logger.warning(f'{compute_specs=}')

    # Also add save_directory_main to compute_specs, this way can get the parameter name when json is called
    compute_specs['save_directory_main'] = save_directory_main

    if (combo_list is None):
        combo_list = paramcombo.get_combo(combo_type, compute_specs)

    panda_graph_only = False
    if (ge):
        img_indi_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='img_equ_indi')
        img_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='img_equ')
        csv_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='csv_equ')

        save_directory['img_detail_indi'] = img_indi_detail_directory
        save_directory['img_detail'] = img_detail_directory
        save_directory['csv_detail'] = csv_detail_directory

        soluequiinterest.policies_steady_states_rloop(
            combo_type, combo_list=combo_list,
            compute_specs=compute_specs,
            save_directory=save_directory,
            panda_graph_only=panda_graph_only,
            parallel=multiprocess,
            graph_list=graph_list)
        combo_list_results_list = None
    else:
        img_indi_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='img_exo_indi')
        img_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='img_exo')
        csv_detail_directory = proj_sys_sup.get_paths(main_directory, sub_folder_name='csv_exo')

        save_directory['img_detail_indi'] = img_indi_detail_directory
        save_directory['img_detail'] = img_detail_directory
        save_directory['csv_detail'] = csv_detail_directory

        combo_list_results_list = soluequipartial.policies_steady_states(
            combo_type, combo_list=combo_list,
            compute_specs=compute_specs,
            save_directory=save_directory,
            panda_graph_only=panda_graph_only,
            parallel=multiprocess,
            graph_list=graph_list)

    t = time.time() - startTime
    logger.warning('Time Used: %s', t)

    if (fileHandler is not None):
        proj_sys_sup.log_stop(fileHandler, log_file_name=log_file_name)

    return combo_list_results_list
