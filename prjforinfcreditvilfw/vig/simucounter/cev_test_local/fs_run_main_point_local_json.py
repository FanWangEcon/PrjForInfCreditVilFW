'''
Created on Jan 06, 2021
@author: fan

Generate results based on parameters in a particular JSON file.

Compare CEV Zero and CEV Small and CEV share change Null. Point Simulations
'''

import os
import logging
import invoke.run_main as invoke_run_main
from copy import deepcopy

"""
SC: Simulate Counterfactual
"""
sc_step = 3

"""
json_cev_null, with CEV_PROP_INCREASE = None, will have grid_zoom_rounds = 1 (based on a_grid) specs, so V and C are not consistent
json_cev_zr, with CEV_PROP_INCREASE not None, have grid_zoom_rounds = 0.
"""
# Possible Parameters
save_directory_main = 'simu_tst_pege'
ls_compute_size = ['x', '']
ls_model_assumption = ['', 'ITG', 'GE', 'ITG_GE']
ls_graph_panda_list_name = ['min_graphs', 'main_aAcsv_graphs']
ls_json_file_names = ['json_cev_null', 'json_cev_zr', 'json_cev_sm']
st_compute_size, graph_panda_list_name = ls_compute_size[0], ls_graph_panda_list_name[1]

dc_invoke_main_args_default = {'speckey': None,
                               'ge': None,
                               'multiprocess': False,
                               'estimate': False,
                               'graph_panda_list_name': graph_panda_list_name,
                               'save_directory_main': save_directory_main,
                               'logging_level': logging.WARNING,
                               'log_file': False,
                               'log_file_suffix': ''}

for sc_step in [1, 2]:
    json_file_names = ls_json_file_names[sc_step]
    model_assumption = ls_model_assumption[0]

    dc_invoke_main_args_default['speckey'] = 'b_ge_s_t_bis' if 'GE' in model_assumption else 'ng_s_t'
    dc_invoke_main_args_default['ge'] = 'GE' in model_assumption
    st_combo_type_b = "_".join(
        filter(None, ['20201025' + st_compute_size, model_assumption, graph_panda_list_name, json_file_names]))
    st_combo_type_e = os.path.join(save_directory_main, json_file_names).replace(os.sep, '/')
    combo_type = ['e', st_combo_type_b, None, None, st_combo_type_e]
    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# else:
#     raise ValueError(f'{sc_step=} specified is not allowed.')
