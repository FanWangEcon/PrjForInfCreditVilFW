'''
Created on Nov 1, 2020

@author: fan

This simulates individual elements of a meshed grid.

Inside an output folder, as we loop over elements of the grid to be solved over separately, each time,
solving a separate point, a different json file is saved. After saving the file, when ran locally, the
joint graph file in the folder gets updated. So the joint graph file goes from having one point to nine points

As a result, the result of running this each_local file is identical to running the local file.
'''

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.runspecs.compute_specs as computespec
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import invoke.run_main as invoke_run_main
from copy import deepcopy
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='simugridrand',
                                     subsub_folder_name='simugrid',
                                     file_name='fs_run_main_grid_multiparam_each_local',
                                     it_time_format=8, log_level=logging.INFO)

# A. Common Arguments
# 'speckey': 'ng_s_t' can also be 'ng-s-t'
graph_panda_list_name = 'min_graphs'
dc_invoke_main_args_default = {'speckey': 'ng_s_t',
                               'ge': False,
                               'multiprocess': False,
                               'estimate': False,
                               'graph_panda_list_name': 'min_graphs',
                               'save_directory_main': 'simu_test0108_beforechange',
                               'logging_level': logging.WARNING,
                               'log_file': False,
                               'log_file_suffix': ''}

# B. Get the compute set to get COMPUTE_PARAM_VEC_COUNT.
dc_computespecs = computespec.compute_set(dc_invoke_main_args_default['speckey'])
compute_param_vec_count = dc_computespecs['compute_param_vec_count']

# C. Solve over meshed grid of beta and rho, element by element
for it_run in [1, 4]:

    dc_invoke_main_args_default_use = deepcopy(dc_invoke_main_args_default)

    if it_run == 1:
        # vig\parameters\compesti_specs\fs_get_compesti_specs.py
        # results stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_each_beta_rhoo
        # outputs identical to those stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_beta_rhoo

        ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                               date='20201025x_each',
                                                               paramstr_key_list_str=[['beta', 'rho']])
        ls_combo_type_store = [["e", "20201025x_each_beta_rhoo", ["esti_param.beta", "esti_param.rho"], None]]

    if it_run == 4:
        # vig\parameters\compesti_specs\fs_get_compesti_specs.py
        # results stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_each_beta_rhoo
        # outputs identical to those stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_beta_rhoo

        ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                               date='20201025x_ITG_GE_each',
                                                               paramstr_key_list_str=[['beta', 'rho']])
        ls_combo_type_store = [["e", "20201025x_ITG_GE_each_beta_rhoo", ["esti_param.beta", "esti_param.rho"], None]]
        dc_invoke_main_args_default_use = dc_invoke_main_args_default
        dc_invoke_main_args_default_use['speckey'] = 'ge_s_t_bis'
        dc_invoke_main_args_default_use['ge'] = True

    # check
    if ls_combo_type == ls_combo_type_store:
        logging.info('ls_combo_type output is correct')

    # first combo_type of combo_list, only one element
    combo_type = ls_combo_type[0]
    # loop over meshed simu points
    for it_mesh_grid_ctr in range(compute_param_vec_count ** len(combo_type[2])):
        combo_type[3] = it_mesh_grid_ctr
        invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default_use)
