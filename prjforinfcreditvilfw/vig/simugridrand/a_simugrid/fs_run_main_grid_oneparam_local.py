'''
Created on Nov 1, 2020

@author: fan

Run model, over one single parameter, quick testing.
'''

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import invoke.run_main as invoke_run_main
from copy import deepcopy
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='simugridrand',
                                     subsub_folder_name='simugrid',
                                     file_name='fs_run_main_grid_oneparam_local',
                                     it_time_format=8, log_level=logging.INFO)

# A. Common Arguments
# 'speckey': 'ng_s_t' can also be 'ng-s-t'
graph_panda_list_name = 'min_graphs'
dc_invoke_main_args_default = {'speckey': 'ng_s_t',
                               'ge': False,
                               'multiprocess': False,
                               'estimate': False,
                               'graph_panda_list_name': 'min_graphs',
                               'save_directory_main': 'simu_test0108',
                               'logging_level': logging.WARNING,
                               'log_file': False,
                               'log_file_suffix': ''}
# possible strings/parameters
ls_paramstr_key_list_str = ['beta', 'CEV_PROP_INCREASE']

# B. Solve over grid of beta
for paramstr_key_list_str in ls_paramstr_key_list_str[1::]:
    for it_run in [1, 2, 3]:

        dc_invoke_main_args_default_use = deepcopy(dc_invoke_main_args_default)

        if it_run == 1:
            # NON-INTEGRATED, NON-GE
            # Results stored in:
            #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_beta
            ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                   date='20201025',
                                                                   paramstr_key_list_str=[paramstr_key_list_str])
            # Example output for ls_combo_type:
            # ls_combo_type_store = [["e", "20201025x_beta", ["esti_param.beta"], None]]
            dc_invoke_main_args_default_use['speckey'] = 'ng_s_t'
            dc_invoke_main_args_default_use['ge'] = False

        if it_run == 2:
            # NON-INTEGRATED, GE
            # Results stored in:
            #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_GE_beta
            ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                   date='20201025_GE',
                                                                   paramstr_key_list_str=[paramstr_key_list_str])
            # Example output for ls_combo_type:
            # ls_combo_type_store = [["e", "20201025x_GE_beta", ["esti_param.beta"], None]]
            dc_invoke_main_args_default_use['speckey'] = 'ge_s_t_bis'
            dc_invoke_main_args_default_use['ge'] = True

        if it_run == 3:
            # INTEGRATED, NON-GE
            # Results stored in:
            #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_beta
            ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                   date='20201025_ITG',
                                                                   paramstr_key_list_str=[paramstr_key_list_str])
            # Example output for ls_combo_type:
            # ls_combo_type_store = [["e", "20201025x_ITG_beta", ["esti_param.beta"], None]]
            dc_invoke_main_args_default_use['speckey'] = 'ng_s_t'
            dc_invoke_main_args_default_use['ge'] = False

        if it_run == 4:
            # INTEGRATED, GE
            # Results stored in:
            #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_beta
            # see 20201025x_ITG_GE_beta_endo.xlsx for GE ITG simu results over beta grid stored in excel
            ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                   date='20201025_ITG_GE',
                                                                   paramstr_key_list_str=[paramstr_key_list_str])
            # Example output for ls_combo_type:
            # ls_combo_type_store = [["e", "20201025x_ITG_GE_beta", ["esti_param.beta"], None]]
            dc_invoke_main_args_default_use['speckey'] = 'ge_s_t_bis'
            dc_invoke_main_args_default_use['ge'] = True

        # check
        # if ls_combo_type == ls_combo_type_store:
        #     logging.info('ls_combo_type output is correct')

        # run
        combo_type = ls_combo_type[0]
        invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)
