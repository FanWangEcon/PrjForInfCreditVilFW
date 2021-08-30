'''
Created on Oct 27, 2020

@author: fan

Test the run function. This is not a unitest. This is an "Actual Test".

Test calling invoke.run.invoke_main with different types of combo_type input structures.

Single point simulation, GE and PE, and/or Integerated or Not runs.

This is the TESTING if things work file

Eight folders/results are generated from this vig.

- \simu\e_20201025x
- \simu\e_20201025x_GE
- \simu\e_20201025x_ITG_
- \simu\e_20201025x_ITG_GE
- \simu\e_20201025
- \simu\e_20201025_GE
- \simu\e_20201025_ITG_
- \simu\e_20201025_ITG_GE
'''

import logging
import invoke.run_main as invoke_run_main
from copy import deepcopy

# A. Common Arguments
# 'speckey': 'ng_s_t' can also be 'ng-s-t'
graph_panda_list_name = 'min_graphs'
dc_invoke_main_args_default = {'speckey': 'ng_s_t',
                               'ge': False,
                               'multiprocess': False,
                               'estimate': False,
                               'graph_panda_list_name': 'min_graphs',
                               'save_directory_main': 'simu_test0108_beforechange',
                               'logging_level': logging.WARNING,
                               'log_file': False,
                               'log_file_suffix': ''}

# B1. Testing the Invoke Run function
# need to specify ** or other options to determine how many choices to simulatee
# 20201025x = 7 discrete choices, small simulation, not GE, one type
# 20201025x_ITG = 7 discrete choices, small simulation, not GE, integrate over types
# 20201025x_ITG_GE = 7 discrete choices, small simulation, GE, integrate over types
# put in *20201025x* vs *20201025* to run small rather than normal
# put in *20201025d* vs *20201025* to run dense rather than normal
# put in *20201025_ITG_* vs *20201025* to run integrated version over different types
# \Project Dissertation\simu\e_20201025x
combo_type = ['e', '20201025x']
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# \Project Dissertation\simu\20201025x_GE
combo_type = ['e', '20201025x_GE']
dc_invoke_main_args = deepcopy(dc_invoke_main_args_default)
dc_invoke_main_args['speckey'] = 'b_ge_s_t_bis'
dc_invoke_main_args['ge'] = True
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)

# \Project Dissertation\simu\e_20201025x_ITG_
combo_type = ['e', '20201025x_ITG_']
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# \Project Dissertation\simu\e_20201025x_ITG_GE
combo_type = ['e', '20201025x_ITG_GE']
dc_invoke_main_args = deepcopy(dc_invoke_main_args_default)
dc_invoke_main_args['speckey'] = 'b_ge_s_t_bis'
dc_invoke_main_args['ge'] = True
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)

# 20201025x = 7 discrete choices, regular run simulation, not GE, one type
# 20201025x_ITG = 7 discrete choices, regular run simulation, not GE, integrate over types
# 20201025x_ITG_GE = 7 discrete choices, regular run simulation, GE, integrate over types
# \Project Dissertation\simu\e_20201025
combo_type = ['e', '20201025']
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# \Project Dissertation\simu\20201025_GE
combo_type = ['e', '20201025_GE']
dc_invoke_main_args = deepcopy(dc_invoke_main_args_default)
dc_invoke_main_args['speckey'] = 'b_ge_s_t_bis'
dc_invoke_main_args['ge'] = True
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)

# \Project Dissertation\simu\e_20201025_ITG_
combo_type = ['e', '20201025_ITG_']
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

# \Project Dissertation\simu\e_20201025_ITG_GE
combo_type = ['e', '20201025_ITG_GE']
dc_invoke_main_args = deepcopy(dc_invoke_main_args_default)
dc_invoke_main_args['speckey'] = 'b_ge_s_t_bis'
dc_invoke_main_args['ge'] = True
invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args)
