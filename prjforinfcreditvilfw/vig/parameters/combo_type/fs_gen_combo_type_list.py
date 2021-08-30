"""
Created on oct 30, 2020

@author: fan

generate combo_type
"""

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='parameters',
                                     subsub_folder_name='combo_type',
                                     file_name='fs_gen_combo_type_list',
                                     it_time_format=8, log_level=logging.INFO)
print(spn_log)

"""
A. generate combo_type for (1) list of parameters (2) list of list of parameters
"""
# Get names from parameters.loop_combo_type_list.param_str_simu.param2str_groups_simu
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('A1. loop over values of beta')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['beta'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('A2. loop over values of beta, then separately, loop over values of A')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['beta', 'rho'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('A3. loop over combinations of beta and A values')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=[['beta', 'rho']])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info(
    'A4. loop over combinations of beta and A values, then combinations of rho, R_INFORM_SAVE and logit_sd_scale')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=[['beta', 'A'],
                                                                              ['rho', 'R_INFORM_SAVE',
                                                                               'logit_sd_scale']])

"""
B. Generate COMBO_TYPE based on string name or list of string names that correspond to list of parameters.
"""
# Get names from parameters/loop_combo_type_list/param_str_simu.py:67
# Get names from parameters/loop_combo_type_list/param_str_esti.py:174
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('B1. loop separately, for each parameter in list_solu')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str='list_solu')
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('B2. loop jointly, over parameters in list_solu, all combinations')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['list_solu'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info(
    'B3. loop jointly, first over combinations of element sin list_solu, then combinations in list_preference')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['list_solu', 'list_preference'])

"""
C. REGION AND TIME SPECIFIC
"""
# Get names from parameters/loop_combo_type_list/param_str_simu.py:67
# Get names from parameters/loop_combo_type_list/param_str_esti.py:174
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('C1. loop separately, for each parameter in list_tKap_ce1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str='list_tKap_mlt_ce1a2')
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('C2. loop jointly, over parameters in list_tKap_ce1a2, all combinations')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['list_tKap_mlt_ce1a2'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info(
    'C3. loop jointly, first over combinations of element sin list_tKap_ce1a2, then combinations in list_tKap_ne1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='a',
                                                       date='20180607',
                                                       paramstr_key_list_str=['list_tKap_mlt_ce1a2', 'list_tKap_mlt_ne1a2'])

"""
D. JOINT multiple Parameters
"""
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('D1. key estimation parameters multiple, central, list_tvars_mlt_ce1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                       date='20201025',
                                                       paramstr_key_list_str=['list_tvars_mlt_ce1a2'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('D2. key estimation parameters multiple, northeast, list_tvars_mlt_ne1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                       date='20201025',
                                                       paramstr_key_list_str=['list_tvars_mlt_ne1a2'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('D3. key estimation parameters multiple, central, list_Afx3_mlt_ce1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                       date='20201025',
                                                       paramstr_key_list_str=['list_Afx3_mlt_ce1a2'])
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('D4. key estimation parameters multiple, northeast, list_Afx3_mlt_ne1a2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                       date='20201025',
                                                       paramstr_key_list_str=['list_Afx3_mlt_ne1a2'])
