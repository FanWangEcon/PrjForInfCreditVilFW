'''
Created on Nov 5, 2020

@author: fan

Run model, over one single parameter, quick testing.

Simulate for Estimate:

1. While solving generate moment objective.
2. Simulate at random points within min and max ranges

Changes in comparison to *fs_run_main_grid_oneparam_local*:

1. spekey: 'esti_spec_key': 'esti_test_11', rather than 'esti_test_11_simu'
2. main_args: 'save_directory_main': 'esti', rather than 'simu'
3. folder name changes.

In contrast to the simu folder results, the results here will output no graphs. This is because
at soluequi/param_loop.py:93, we specify that, if 'esti_param_vec_count' in compute_specs:,
do not proceed to generate to export json to csv, and also do not generate any graphs.

This is simulation for estimation, to generate results for the first step for estimation over AWS.
'''

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.runspecs.get_compesti_specs as param_compestispecs
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import invoke.run_main as invoke_run_main
from copy import deepcopy
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='simugridrand',
                                     subsub_folder_name='simurand_momobj',
                                     file_name='fs_run_main_rand_oneparam_local_mom',
                                     it_time_format=8, log_level=logging.INFO)

# A. Common Arguments
# importantly, ESTI_TEST_11, DOES NOT HAVE SIMU at the end.
# This means moments will be generated, nad parameter values of beta will be randomly
# drawn rather than over meshed grid
graph_panda_list_name = 'min_graphs'
dc_speckey_default = {'compute_spec_key': 'ng_s_t',
                      'esti_spec_key': 'esti_test_11',
                      'moment_key': 2,
                      'momset_key': 3}

# B. Solve over grid of beta
for it_run in [1, 4]:

    dc_speckey_default_use = deepcopy(dc_speckey_default)

    if it_run == 1:
        # NON-INTEGRATED, NON-GE
        # Results stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_beta
        ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                               date='20201025x_rand',
                                                               paramstr_key_list_str=['beta'])
        ls_combo_type_store = [["e", "20201025x_rand_beta", ["esti_param.beta"], None]]
        dc_speckey_default_use['compute_spec_key'] = 'ng_s_t'
        bl_ge = False

    if it_run == 4:
        # INTEGRATED, GE
        # Results stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_beta
        # see 20201025x_ITG_GE_beta_endo.xlsx for GE ITG simu results over beta grid stored in excel
        ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                               date='20201025x_ITG_GE_rand',
                                                               paramstr_key_list_str=['beta'])
        ls_combo_type_store = [["e", "20201025x_ITG_GE_rand_beta", ["esti_param.beta"], None]]
        dc_speckey_default_use['compute_spec_key'] = 'ge_s_t_bis'
        bl_ge = True

    # check
    if ls_combo_type == ls_combo_type_store:
        logging.info('ls_combo_type output is correct')

    # generate args
    dc_invoke_main_args = {'speckey': param_compestispecs.get_speckey_string(**dc_speckey_default_use),
                           'ge': bl_ge,
                           'multiprocess': False,
                           'estimate': False,
                           'graph_panda_list_name': 'min_graphs',
                           'save_directory_main': 'esti',
                           'logging_level': logging.WARNING,
                           'log_file': False,
                           'log_file_suffix': ''}
    # run
    combo_type = ls_combo_type[0]
    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)
