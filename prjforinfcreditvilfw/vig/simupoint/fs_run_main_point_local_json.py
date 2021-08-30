'''
Created on Jan 07, 2021
@author: fan

This is copied over from *vig/simupoint/fs_run_main_point_local_json.py*
'''

import os
import logging
import invoke.run_main as invoke_run_main
from copy import deepcopy

# A. ALL outputs
save_directory_main = 'simu_tst_pege'
ls_compute_size = ['x', '']
ls_model_assumption = ['', 'ITG', 'GE', 'ITG_GE']
ls_graph_panda_list_name = ['min_graphs', 'main_aAcsv_graphs']
ls_json_file_names = ['json_bni_borr_p_high', 'json_bni_borr_p_low']

for st_compute_size in ls_compute_size:
    for snm_json_file_names in ls_json_file_names:
        for model_assumption in ls_model_assumption[2]:
            for graph_panda_list_name in ls_graph_panda_list_name[1:2]:
                dc_invoke_main_args_default = {'speckey': 'ng_s_t',
                                               'ge': False,
                                               'multiprocess': False,
                                               'estimate': False,
                                               'graph_panda_list_name': graph_panda_list_name,
                                               'save_directory_main': save_directory_main,
                                               'logging_level': logging.WARNING,
                                               'log_file': False,
                                               'log_file_suffix': ''}
                st_combo_type_b = "_".join(
                    filter(None, ['20201025' + st_compute_size,
                                  model_assumption, graph_panda_list_name, snm_json_file_names]))
                st_combo_type_e = os.path.join(save_directory_main, snm_json_file_names).replace(os.sep, '/')
                combo_type = ['e', st_combo_type_b, None, None, st_combo_type_e]
                invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)
