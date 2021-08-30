'''
Created on Jan 06, 2021
@author: fan

Generate results based on parameters in a particular JSON file.
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
1. Model simulation, one period one region
- speckey with compute_spec only, no moments, no estimate_spec.
- unlike estimation, this is not doing two time-periods at the same time. 
- the JSON file, if it contains time-specific parameters, does not work. 
"""

"""
Example JSON files contents
based on BNI_BORR_P_ne9901 estimate:
    {"esti_param.BNI_BORR_P": 0.16361536960703554}
based on BNF_BORR_P_ne0209 estimate:
    {"esti_param.BNF_BORR_P": 0.01347052410530248}
"""

"""
The four steps change (1) what is the JSON file been called and (2) whether call GE or PE. 

1. GE Simulation at "Original" Parameters to get GE interest

1b. Get GE Interest rates, and put into:
json_bni_borr_p_high.json:
    {"esti_param.BNI_BORR_P": 0.16361536960703554,
     "esti_param.R_INFORM_SAVE": 1.125,
     "esti_param.R_INFORM_BORR": 1.125}
json_bni_borr_p_low.json:
    {"esti_param.BNF_BORR_P": 0.01347052410530248,
     "esti_param.R_INFORM_SAVE": 1.125,
     "esti_param.R_INFORM_BORR": 1.125}

2. Simulate GE at baseline again, now with the fixed GE interest rate
+ this is pretty point-less
+ a little helpful perhaps because (1) has too many results 
+ but (4) has a lot of results as well and does not get its (2)
+ turns out to be very useful to debug, to make sure (2) produces the same result as (1)

3. PE Effect of Lower fixed cost
PE effect because in step 1b, loaded in the interest rate to p_high and p_low files 

4. GE Effect of Lower fixed cost
Same as 3 except change GE price now: ls_model_assumption[1] not [0]

btp_fb_opti_grid_allJ_agg vs btp_ib_opti_grid_allJ_agg

In this simple example, lower informal borrowing cost leads to higher demand for informal loans, which pushes
up the informal borrowing interest rate. 
"""


# Possible Parameters
save_directory_main = 'simu_tst_pege'
ls_compute_size = ['x', '']
ls_model_assumption = ['', 'ITG', 'GE', 'ITG_GE']
ls_graph_panda_list_name = ['min_graphs', 'main_aAcsv_graphs']
ls_json_file_names = ['json_bni_borr_p_high', 'json_bni_borr_p_low']
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


if sc_step in [1, 2, 3, 4]:
    if sc_step in [1, 2]:
        json_file_names = ls_json_file_names[0]
    elif sc_step in [3, 4]:
        json_file_names = ls_json_file_names[1]

    if sc_step in [1, 4]:
        model_assumption = ls_model_assumption[2]
    elif sc_step in [2, 3]:
        model_assumption = ls_model_assumption[0]

    dc_invoke_main_args_default['speckey'] = 'b_ge_s_t_bis' if 'GE' in model_assumption else 'ng_s_t'
    dc_invoke_main_args_default['ge'] = 'GE' in model_assumption
    st_combo_type_b = "_".join(
        filter(None, ['20201025' + st_compute_size, model_assumption, graph_panda_list_name, json_file_names]))
    st_combo_type_e = os.path.join(save_directory_main, json_file_names).replace(os.sep, '/')
    combo_type = ['e', st_combo_type_b, None, None, st_combo_type_e]
    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

else:
    raise ValueError(f'{sc_step=} specified is not allowed.')
