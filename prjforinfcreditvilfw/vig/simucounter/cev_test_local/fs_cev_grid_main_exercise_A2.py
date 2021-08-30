'''
Created on Jan 09, 2021
@author: fan
'''

import os
import logging
import invoke.run_main as invoke_run_main
import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist

"""
Step A2, CEV GRID
"""


def main():
    # Folder
    save_directory_main = 'simu_tst_pege_A2_21Jan11'
    # Possible Parameters
    ls_compute_size = ['x', '']
    ls_model_assumption = ['PE', 'ITG_PE']

    # ng_s_t 3 point test non-parallel
    # local_ng_par_d_cev many more points, parallel
    ls_compute_spec = ['ng_s_t', 'local_ng_par_d_cev']
    compute_spec = ls_compute_spec[1]

    ls_combe_type_date = ['19E1NEp99r99']
    ls_graph_panda_list_name = ['main_aAcsv_graphs']

    dc_invoke_main_args_default = {'speckey': None,
                                   'ge': None,
                                   'multiprocess': False,
                                   'estimate': False,
                                   'graph_panda_list_name': ls_graph_panda_list_name[0],
                                   'save_directory_main': save_directory_main,
                                   'logging_level': logging.WARNING,
                                   'log_file': False,
                                   'log_file_suffix': ''}

    for compute_size in ls_compute_size:
        for model_assumption in ls_model_assumption:
            dc_invoke_main_args_default['speckey'] = 'b_ge_s_t_bis' if 'GE' in model_assumption else compute_spec
            dc_invoke_main_args_default['ge'] = 'GE' in model_assumption
            dc_invoke_main_args_default['multiprocess'] = True if '_par_' in compute_spec else False
            st_combo_type_b = "_".join(
                filter(None, [ls_combe_type_date[0] + compute_size, model_assumption]))
            ls_combo_type = paramcombotypelist.gen_combo_type_list(file='e',
                                                                   date=st_combo_type_b,
                                                                   paramstr_key_list_str=['CEV_PROP_INCREASE'])
            combo_type = ls_combo_type[0]
            invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

    # else:
    #     raise ValueError(f'{sc_step=} specified is not allowed.')


if __name__ == '__main__':
    main()
