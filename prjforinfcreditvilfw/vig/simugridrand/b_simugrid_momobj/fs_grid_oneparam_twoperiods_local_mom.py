'''
Created on Dec 4, 2020

@author: fan

Run model, over one single parameter, quick testing. Generate moment objective.
Changed simply with the speckey parameter. from *ng_s_t* to *ng_s_t=esti_test_11_simu=2=3*.
Do not average over moment outcomes, match period by period, for each region.

D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ce1_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ce2_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ne1_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ne2_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ce1_ITG_GE_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ce2_ITG_GE_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ne1_ITG_GE_kapp
D:\repos\ThaiJMP\simu\e_20201025_mo_mlt_ne2_ITG_GE_kapp

1. 'esti_spec_key': 'esti_test_11_simu'
    + must specific esti_spec, otherwise no moment comparison
    + add _simu to the end, so will not randomly do estimation.
        + the _simu added here also adds _simu to the end of moments, used here estimation/moments/moments_a.py:120
2. kappa
    + parameter to simulate over, the parameter's value is been changed. No other
    parameters are region/time specific.
3. 'moment_key': 31
    + this is moment for one location, one period
    + loop over 31, 32, 41, 42, corresponding to region and time periods
    + the change in moment key, for the simulation below, does not change simulation
    outcomes, only the data moment to be matched against. Hence, the test
    below partly is to see 31,32,41,42 generate the same simulation results, as seen in:
    search AGG_EXO_20201025_mo_mlt_*_kapp_J7 type graph outputs. Are these
    outcome changes as expected in direction, are they smooth? Since
    the moments to be matched are single numbers, if these are smooth, the moment gaps
    will be smooth as well.
4. Equilibrium analysis:
    As kappa is relaxed, more borrowing possible from formal sources, drive down the informal
    local equilibrium interest rate. In PE, raising kappa makes people want to borrow informally
    and lend formally. In GE, raising kappa drives down the informal interest rate, making
    this arbitrage option less attractive. Formal borrowing only increase, informal borrow only
    also increases. Many other differences.
5. x vs normal simulation
    Less jumpiness in key outcomes from normal simulation vs x simulation.

Kappa parameter, the borrowing bound, which is region as well as time specific.

These are used to study as we move over meshed grid of parameter values, how do moment objectives change.
'''

import projectsupport.hardcode.string_shared as hardstring
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
                                     file_name='fs_grid_oneparam_twoperiods_local_mom',
                                     it_time_format=8, log_level=logging.INFO)

# A. Common Arguments
# importantly, ESTI_TEST_11_SIMU, has SIMU at the end.
# this means moment differences will be generated based on moment_key and momset_key, however, will not estimate
# the model, just simulate the model at some particular point combinations
graph_panda_list_name = 'min_graphs'
dc_speckey_default = {'compute_spec_key': 'ng_s_d',
                      'esti_spec_key': 'esti_test_11_simu',
                      'moment_key': 31,
                      'momset_key': 3}

# B. Solve over grid of list_tKap_mlt_ce1a2
# rely on parameters/runspecs/estimate_specs.py:126
region_time_suffix = hardstring.region_time_suffix()
for it_run in [1, 4]:
# for it_run in [4]:
    # simumulation size, sparse or regular or dense
    # for st_size in ['x', '', 'd']:
    for st_size in ['x', '']:
    # for st_size in ['x']:
        for moment_key in [31, 32, 41, 42]:
            # for it_run in [1]:

            dc_speckey_default_use = deepcopy(dc_speckey_default)
            dc_speckey_default_use['moment_key'] = moment_key

            # Define base name
            st_date_base = "20201025" + st_size + "_mo"
            if moment_key == 31:
                st_region_time_add = region_time_suffix['_ce1'][0]
            elif moment_key == 32:
                st_region_time_add = region_time_suffix['_ce2'][0]
            elif moment_key == 41:
                st_region_time_add = region_time_suffix['_ne1'][0]
            elif moment_key == 42:
                st_region_time_add = region_time_suffix['_ne2'][0]
            else:
                raise ValueError(f'{moment_key=} not allowed')
            st_date_base = st_date_base + st_region_time_add

            if it_run == 1:
                # NON-INTEGRATED, NON-GE
                # Results stored in:
                #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_beta
                ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                       date=st_date_base,  # mo = moment objective
                                                                       paramstr_key_list_str=['kappa'])
                # dc_speckey_default_use['compute_spec_key'] = 'ng_s_t'
                dc_speckey_default_use['compute_spec_key'] = 'ng_s_d'
                bl_ge = False
                multiprocess = False

            if it_run == 4:
                # INTEGRATED, GE
                # Results stored in:
                #   C:\Users\fan\Documents\Dropbox (UH-ECON)\Project Dissertation\simu\e_20201025x_ITG_GE_beta
                # see 20201025x_ITG_GE_beta_endo.xlsx for GE ITG simu results over beta grid stored in excel
                ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                       date=st_date_base + '_ITG_GE',
                                                                       # mo = moment objective
                                                                       paramstr_key_list_str=['kappa'])
                bl_ge = True
                # dc_speckey_default_use['compute_spec_key'] = 'ge_s_t_bis'
                # multiprocess = False
                dc_speckey_default_use['compute_spec_key'] = 'ge_p_m_bis'
                multiprocess = False

            # generate args
            dc_invoke_main_args = {'speckey': param_compestispecs.get_speckey_string(**dc_speckey_default_use),
                                   'ge': bl_ge,
                                   'multiprocess': multiprocess,
                                   'estimate': False,
                                   'graph_panda_list_name': 'min_graphs',
                                   'save_directory_main': 'simu',
                                   'logging_level': logging.WARNING,
                                   'log_file': False,
                                   'log_file_suffix': ''}
            # run
            combo_type = ls_combo_type[0]
            invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)
