'''
Created on Nov 5, 2020

@author: fan

Run model, over one single parameter, quick testing. Generate moment objective.
Changed simply with the speckey parameter. from *ng_s_t* to *ng_s_t=esti_test_11_simu=2=3*.
Data moments are time periods specific. The moments been matched to when time-periods not specified
will be averaged over moments for different time periods in one region

Testing over the beta parameter here, which is shared by all regions and time.

These are used to study as we move over meshed grid of parameter values, how do moment objectives change.
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
                                     subsub_folder_name='simugrid_momobj',
                                     file_name='fs_grid_oneparam_local_mom',
                                     it_time_format=8, log_level=logging.INFO)

# A. Common Arguments
# importantly, ESTI_TEST_11_SIMU, has SIMU at the end.
# this means moment differences will be generated based on moment_key and momset_key, however, will not estimate
# the model, just simulate the model at some particular point combinations
graph_panda_list_name = 'min_graphs'
dc_speckey_default = {'compute_spec_key': 'ng_s_t',
                      'esti_spec_key': 'esti_test_11_simu',
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
                                                               date='20201025x_momobj',
                                                               paramstr_key_list_str=['beta'])
        ls_combo_type_store = [["e", "20201025x_momobj_beta", ["esti_param.beta"], None]]
        dc_speckey_default_use['compute_spec_key'] = 'ng_s_t'
        bl_ge = False

    if it_run == 4:
        # INTEGRATED, GE
        # Results stored in:
        #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_beta
        # see 20201025x_ITG_GE_beta_endo.xlsx for GE ITG simu results over beta grid stored in excel
        ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                               date='20201025x_momobj_ITG_GE',
                                                               paramstr_key_list_str=['beta'])
        ls_combo_type_store = [["e", "20201025x_momobj_ITG_GE_beta", ["esti_param.beta"], None]]
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
                           'save_directory_main': 'simu',
                           'logging_level': logging.WARNING,
                           'log_file': False,
                           'log_file_suffix': ''}
    # run
    combo_type = ls_combo_type[0]
    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)
