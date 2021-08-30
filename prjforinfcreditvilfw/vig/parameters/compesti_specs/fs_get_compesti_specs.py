"""
Created on oct 29, 2020

@author: fan

generate combo_type
"""

import parameters.runspecs.get_compesti_specs as param_compestispecs
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='parameters',
                                     subsub_folder_name='compesti_specs',
                                     file_name='fs_get_compesti_specs',
                                     it_time_format=8, log_level=logging.INFO)

"""
A1. Generate COMPESTI_SPECS
"""
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('A1')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
speckey = 'ng_s_d'
compesti_specs = param_compestispecs.get_compesti_specs(speckey)

"""
A2. Generate COMPESTI_SPECS
"""
logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
logging.info('A2')
logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
speckey = 'ng_s_d=kap_m0_nld_m_simu=2=3'
compesti_specs = param_compestispecs.get_compesti_specs(speckey)

"""
B. COMPESTI_SPECS with different first component, the compute specifications 
"""
# What can be used for the
speckey_dict = {0: 'mpoly_1',
                1: 'ng_s_t',
                2: 'ng_s_d',
                3: 'ng_p_t',
                4: 'ng_p_d',
                5: 'ge_p_t_mul',
                6: 'ge_p_m_mul',
                7: 'ge_p_d_mul',
                8: 'ge_s_t_bis',
                9: 'ge_p_t_bis',
                10: 'ge_p_m_bis',
                11: 'ge_p_d_bis',
                12: 'b_ng_s_t',  # 12
                13: 'b_ng_s_d',  # 13
                14: 'b_ng_p_t',  # 14
                15: 'b_ng_p_d',  # 15
                16: 'b_ge_p_m_mul',  # 16
                17: 'b_ge_p_d_mul',  # 17
                18: 'b_ge_s_t_bis',  # 18
                19: 'b_ge_p_m_bis',  # 19
                20: 'b_ge_p_d_bis'}  # 20

# Get names from parameters.loop_combo_type_list.param_str_simu.param2str_groups_simu
for speckey_key, speckey_val in speckey_dict.items():
    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info('B' + str(speckey_key) + '. ' + speckey_val)
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    speckey = speckey_val + '=kap_m0_nld_m_simu=2=3'
    compesti_specs = param_compestispecs.get_compesti_specs(speckey)

"""
C. COMPESTI_SPECS with different second component, the estimation specifications 
"""
# What can be used for the
spec_key_bases = ['esti_test', 'esti_testfull', 'esti_main', 'esti_long', 'esti_mpoly',
                  'esti_thin', 'esti_tstthin']
ctr = 0
for spec_key_base in spec_key_bases:
    for cur_esti_spec in [10, 11, 12, 13, 14,
                          20, 21, 22, 23, 24,
                          30, 31, 32, 33, 34]:
        ctr += 1
        estispec_key = spec_key_base + '_' + str(cur_esti_spec)
        logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
        logging.info('C' + str(ctr) + '. ' + estispec_key)
        logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
        speckey = 'ng_s_t=' + estispec_key + '=2=3'
        compesti_specs = param_compestispecs.get_compesti_specs(speckey)

"""
D. COMPESTI_SPEC with different moments and momset integers
"""
# see parameters.runspecs.estimate_specs.moments_and_momsets for options

for moment_key in [0, 1, 2, 3, 4]:
    for momset_key in [0, 1, 2, 3, 4, 5, 6]:
        ctr += 1
        speckey = 'ng_s_t=esti_testfull_11=' + str(moment_key) + '=' + str(momset_key)
        logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
        logging.info('D' + str(ctr) + '. ' + speckey)
        logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
        compesti_specs = param_compestispecs.get_compesti_specs(speckey)

