'''
Created on Jan 09, 2021
@author: fan
'''

import os
import logging
import invoke.run_main as invoke_run_main
from copy import deepcopy

"""
SC: Simulate Counterfactual
json_cev_null, with CEV_PROP_INCREASE = None, will have grid_zoom_rounds = 1 (based on a_grid) specs, so V and C are not consistent
json_cev_zr, with CEV_PROP_INCREASE not None, have grid_zoom_rounds = 0.
"""
# Folder
# M10 = fl_cost_multiple = 10 form a_esti.py
# for each M, go shift thie manually inside a_esti.py
save_directory_main = 'simu_tst_pege_A1_21Jan11_M10'
# Possible Parameters
ls_combe_type_date = ['19E1NEp99r99', '19E1NEp02r99', '19E1NEp02per02ger99', '19E1NEp02r02']
ls_compute_size = ['x', '']
ls_model_assumption = ['PE', 'ITG_PE', 'GE', 'ITG_GE']
ls_graph_panda_list_name = ['min_graphs', 'main_aAcsv_graphs', 'main_cev_graphs']

dc_invoke_main_args_default = {'speckey': None,
                               'ge': None,
                               'multiprocess': False,
                               'estimate': False,
                               'graph_panda_list_name': ls_graph_panda_list_name[2],
                               'save_directory_main': save_directory_main,
                               'logging_level': logging.WARNING,
                               'log_file': False,
                               'log_file_suffix': ''}

for compute_size in ls_compute_size[0:1]:
    for model_assumption in ls_model_assumption[0:2]:
        for combe_type_date in ls_combe_type_date:
            dc_invoke_main_args_default['speckey'] = 'b_ge_s_t_bis' if 'GE' in model_assumption else 'ng_s_t'
            dc_invoke_main_args_default['ge'] = 'GE' in model_assumption
            st_combo_type_b = "_".join(
                filter(None, [combe_type_date + compute_size, model_assumption]))
            combo_type = ['e', st_combo_type_b]
            invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# else:
#     raise ValueError(f'{sc_step=} specified is not allowed.')
