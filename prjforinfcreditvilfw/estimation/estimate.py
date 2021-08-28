'''
Created on Apr 8, 2018

@author: fan

import estimation.estimate as esti
'''

import logging
import numpy as np
import scipy.optimize as scipy_opti

import estimation.estimate_objective as estiobjective
import estimation.estimate_objective_multiperiods as estiobjmulti
import estimation.postprocess.jsoncsv.gen_agg_csv_from_json as gen_csvaggjson
import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.minmax.a_minmax as param_minmax_a
import parameters.paraminstpreset as param_inst_preset
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def estimate(combo_type, param_combo,
             esti_method='MomentsSimuStates',
             moments_type=None,
             esti_option_type=2,
             esti_func_type='nldmd',
             compesti_specs=None,
             ge=False, multiprocess=False,
             graph_list=None, save_directory='estisubfolder'):
    """
    Parameters
    ----------
    param_combo : :obj:`dict` of :obj:`dict`
        A dictionary with information for one simulation. In this case,
        the information not for the initial parameters for estimation. The
        first simulation in the estimation process. For each type of parameters,
        default group, and including updates
    speckey : string
        compute_specs_key
    param_esti_list_key : string
        should be one of the keys in list_all dictionary
        determines which one estimated

    Examples
    --------
    import estimation.estimate as esti

    """

    if (moments_type == None):
        moments_type = ['a', '20180805a']

    '''
    ESTIMATION FOLDER LEVEL 2
    '''
    estitype_folder_name = hardstring.gen_esti_subfolder_name(param_combo=param_combo, combo_type=combo_type)
    # estitype_folder_name = param_combo['param_update_dict']['support_arg']['compesti_short_name'] + \
    #                         param_combo['param_combo_list_ctr_str']
    # sub_folder_name = combo_type[0] + '_' + combo_type[1] + param_combo['param_combo_list_ctr_str']
    save_directory_sub = proj_sys_sup.get_paths(save_directory, sub_folder_name=estitype_folder_name)
    if (ge):
        # param_combo['file_save_suffix'][1:] contains initial starting points value
        logfile_name = 'log_esti_rloop_' + param_combo['file_save_suffix'][1:]
    else:
        # param_combo['file_save_suffix'][1:] contains initial starting points value
        logfile_name = 'log_esti_rexo_' + param_combo['file_save_suffix'][1:]

    log_file_name = save_directory_sub + logfile_name + '.log'
    fileHandler, esti_logger = proj_sys_sup.log_start(log_file_name,
                                                      logging_level=logging.INFO, log_file=False,
                                                      module_name='estimator' + proj_sys_sup.save_suffix_time(
                                                          format=2))

    """
    B. Get Parameter Values (Fixed and Initial)
    """
    param_inst = param_inst_preset.get_param_inst_preset_combo(param_combo)

    if (esti_method is None):
        esti_method = param_combo['esti_method']
    if (moments_type is None):
        moments_type = param_combo['moments_type']
    if (esti_option_type is None):
        esti_option_type = param_combo['esti_option_type']
    if (esti_func_type is None):
        esti_func_type = param_combo['esti_func_type']

    """
    A. Generate Conditions and Strings
    """
    if (esti_method == 'likelihood'):
        use_states_data = True
        use_likelihood = True
        estimethod_folder_str = '_Like'
    elif (esti_method == 'MomentsDataStates'):
        use_states_data = True
        use_likelihood = False
        estimethod_folder_str = '_MDataS'
    elif (esti_method == 'MomentsSimuStates'):
        use_states_data = False
        use_likelihood = False
        estimethod_folder_str = '_MSimuS'

    '''
    B. Get Parameter Bounds
    same bounds used to generate the random initial parameters inside loop_param_combo_list package
    '''
    minmax_type = param_combo['param_update_dict']['minmax_type']
    minmax_file = minmax_type[0]
    if (minmax_file == 'a'):
        minmax_param, minmax_subtitle = param_minmax_a.param(minmax_type)

    """
    C. Which Parametesr to Estimate
    """
    param_esti_group_key_list = combo_type[2]
    params_esti_init = np.zeros((len(param_esti_group_key_list)))
    params_esti_bnds = []
    for ctr, param_esti_group_key in enumerate(param_esti_group_key_list):
        param_val, param_type, param_name = paramloopstr.get_current_init_param_values(param_esti_group_key,
                                                                                       param_inst)
        params_esti_init[ctr] = param_val

        '''
        C3. Get Parameter Bounds
        '''
        param_bound = minmax_param[param_type][param_name]
        params_esti_bnds.append((param_bound[0], param_bound[1]))

    logger.debug('params_esti_str:%s', str(param_esti_group_key_list))
    logger.debug('params_esti_init:%s', str(params_esti_init))

    """
    D. Estimate Option
    """
    if esti_option_type == 0:
        opts = {'xtol': 1e-01, 'ftol': 1e-01, 'gtol': 1e-01,
                'eps': (1e-01) / 2,
                'maxiter': 4}
        # 'maxiter':2, 'maxls':5, 'maxfun':10}
        logger.debug('opts:%s', str(opts))
    elif esti_option_type == 1:
        opts = {'xtol': 1e-02, 'ftol': 1e-02, 'gtol': 1e-02,
                'eps': (1e-02) / 2,
                'maxiter': 8}
        # 'maxiter':7, 'maxls':20, 'maxfun':200}
        logger.debug('opts:%s', str(opts))
    elif esti_option_type == 2:
        opts = {'xtol': 1e-03, 'ftol': 1e-03, 'gtol': 1e-03,
                'eps': (1e-03) / 2,
                'maxiter': 15}
        logger.debug('opts:%s', str(opts))
    elif esti_option_type == 3:
        opts = {'xtol': 1e-04, 'ftol': 1e-04, 'gtol': 1e-04,
                'eps': (1e-04) / 2,
                'maxiter': 30}
        logger.debug('opts:%s', str(opts))
    elif esti_option_type == 4:
        # use default values
        opts = None
        logger.debug('opts:%s', str(opts))
    else:
        raise ('bad')

    '''
    F. Start Logging to Record Estimates Changes
    '''

    """
    E. Function Handle
    """
    moments_type_eleone = moments_type[1]
    # by default, always going to "multi_period" option, which is the polynomial approximation method
    multi_periods, period_keys_esti_set = hardstring.momentstype_suffix_regiontype(moments_type_eleone)
    esti_kwargs = {}
    esti_kwargs['period_keys_esti_set'] = period_keys_esti_set

    if (multi_periods):
        # this uses polynomial approximator
        esti_func = estiobjmulti.estimate_objective_multiperiods
    else:
        # this uses atual function, not approximated it seems.
        esti_func = estiobjective.estimate_objective

    def estimate_objective(params_esti):
        return esti_func(params_esti, param_esti_group_key_list,
                         moments_type, use_states_data, use_likelihood,
                         combo_type=combo_type, param_combo=param_combo,
                         compesti_specs=compesti_specs,
                         ge=ge, multiprocess=multiprocess,
                         graph_list=graph_list,
                         save_directory=save_directory_sub,
                         logger=esti_logger, **esti_kwargs)

    """
    F. Estimate
    """

    if (esti_logger is not None):
        esti_logger.info('start estimation, types:%s', esti_func_type)

    if esti_func_type in ['Nelder-Mead', 'L-BFGS-B', 'TNC', 'SLSQP']:

        if esti_func_type == 'Nelder-Mead':

            if opts is None:
                # others use default
                options_here = {'disp': True}
            else:
                options_here = {'disp': True,
                                'fatol': opts['ftol'],
                                'xatol': opts['gtol'],
                                'maxiter': opts['maxiter'],
                                'maxfev': opts['maxiter'] ** 2}

            results = scipy_opti.minimize(estimate_objective, params_esti_init,
                                          method='Nelder-Mead',
                                          options=options_here)

        if esti_func_type == 'L-BFGS-B':

            if opts is None:
                options_here = {'disp': True}
            else:
                options_here = {'disp': True,
                                'ftol': opts['ftol'],
                                'gtol': opts['gtol'],
                                'eps': opts['eps'],
                                'maxiterint': opts['maxiter'],
                                'maxfunint': opts['maxiter'] ** 2}

            results = scipy_opti.minimize(estimate_objective, params_esti_init,
                                          method='L-BFGS-B',
                                          options=options_here,
                                          bounds=params_esti_bnds)

        if esti_func_type == 'SLSQP':

            if opts is None:
                # others use default
                options_here = {'disp': True}
            else:
                options_here = {'disp': True,
                                'ftol': opts['ftol'],
                                'eps': opts['eps'],
                                'maxiter': opts['maxiter']}

            results = scipy_opti.minimize(estimate_objective, params_esti_init,
                                          method='SLSQP',
                                          options=options_here,
                                          bounds=params_esti_bnds)

        if esti_func_type == 'TNC':
            if opts is None:
                # others use default
                options_here = {'disp': True}
            else:
                options_here = {'disp': True,
                                'ftol': opts['ftol'],
                                'xtol': opts['xtol'],
                                'gtol': opts['gtol'],
                                'eps': opts['eps'],
                                'maxiter': opts['maxiter']}

            results = scipy_opti.minimize(estimate_objective, params_esti_init,
                                          method='TNC',
                                          options=options_here,
                                          bounds=params_esti_bnds)

    else:
        results = scipy_opti.minimize(estimate_objective, params_esti_init, method=esti_func_type,
                                      options={'disp': True, 'maxiter': 20})

    if (esti_logger is not None):
        esti_logger.critical('end estimation, types:%s', esti_func_type)
        esti_logger.critical('estimation results:\n%s', results)

    if (fileHandler is not None):
        proj_sys_sup.log_stop(fileHandler, log_file_name=log_file_name, logger=esti_logger)

    export_agg_json_csv = True
    if (export_agg_json_csv):
        main_directory = save_directory_sub
        json_directory = proj_sys_sup.get_paths(save_directory, sub_folder_name=estitype_folder_name,
                                                subsub_folder_name='json')
        save_directory_dict = {}
        save_directory_dict['json'] = json_directory
        save_directory_dict['img_main'] = main_directory
        save_directory_dict['csv'] = main_directory

        compute_specs = compesti_specs
        panda_df_save_best = True
        gen_csvaggjson.gen_agg_csv_from_json(combo_type, param_combo,
                                             ge, compute_specs,
                                             save_directory_dict,
                                             graph_list,
                                             panda_df_save_best)
