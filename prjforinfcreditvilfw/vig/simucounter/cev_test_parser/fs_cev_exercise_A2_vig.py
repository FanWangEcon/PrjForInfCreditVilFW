'''
Created on Jan 09, 2021
@author: fan
'''

import os
import logging
import invoke.run_main as invoke_run_main
import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import invoke.run_sg_parser as run_sg_parser
import parameters.runspecs.compute_specs as computespec


def main(dc_it_execute_type=None):
    if dc_it_execute_type is None:
        dc_it_execute_type = {'model_assumption': 0,
                              'compute_size': 0,
                              'simu_param': 0,
                              'call_type': 0,
                              'param_date': 0}

    st_sg_args_compose, aws_local_sync_cmd, \
    combo_type, combo_type_component, \
    sgf, \
    compute_spec_key = \
        run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type)

    cur_compute_spec = computespec.compute_set(compute_spec_key)
    bl_ge = cur_compute_spec['ge']
    bl_multiprocess = cur_compute_spec['multiprocess']

    dc_invoke_main_args_default = {'speckey': compute_spec_key,
                                   'ge': bl_ge,
                                   'multiprocess': bl_multiprocess,
                                   'estimate': False,
                                   'graph_panda_list_name': 'main_cev_graphs',
                                   'save_directory_main': sgf,
                                   'logging_level': logging.WARNING,
                                   'log_file': False,
                                   'log_file_suffix': ''}
    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_args_default)

    # else:
    #     raise ValueError(f'{sc_step=} specified is not allowed.')


if __name__ == '__main__':

    ls_st_run_groups = ['test',
                        'sixPExTest',
                        'fourGExTest',
                        'sixPEITG',
                        'V3GExTest',
                        'kappaCounter']

    for st_run_group in ls_st_run_groups[5::]:

        if st_run_group == 'test':
            for it_run in [1, 2]:
                dc_it_execute_type = {'model_assumption': None,
                                      'compute_size': 0,
                                      'simu_param': 0,
                                      'call_type': 0,
                                      'param_date': 0}
                if it_run == 1:
                    dc_it_execute_type['model_assumption'] = 0
                if it_run == 2:
                    dc_it_execute_type['model_assumption'] = 1
            main(dc_it_execute_type)

        elif st_run_group == 'sixPExTest':
            for it_run in [0, 1, 2, 3, 4, 5]:
                dc_it_execute_type = {'model_assumption': 0,  # PE
                                      'compute_size': 0,
                                      'simu_param': 1,  # None, no grid of solutions
                                      'call_type': 0,
                                      'param_date': it_run}
                main(dc_it_execute_type)

        elif st_run_group == 'fourGExTest':
            # 0, 99 GE
            # 3, 02 GE
            # 4, 02 parameters except for 99 savings interest rate, GE
            # 11, 02 parameters except 99 collateral, GE
            for it_run in [0, 3, 4, 11]:
                dc_it_execute_type = {'model_assumption': 2,  # GE
                                      'compute_size': 0,
                                      'simu_param': 1,  # None, no grid of solutions
                                      'call_type': 0,
                                      'param_date': it_run}
                main(dc_it_execute_type)

        elif st_run_group == 'sixPEITG':
            for it_run in [0, 1, 2, 3, 4, 5]:
                dc_it_execute_type = {'model_assumption': 1,  # ITG_PE
                                      'compute_size': 1,
                                      'simu_param': 1,  # None, no grid of solutions
                                      'call_type': 0,
                                      'param_date': it_run}
                main(dc_it_execute_type)

        elif st_run_group == 'V3GExTest':
            for it_run in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                dc_it_execute_type = {'model_assumption': 2,  # GE
                                      'compute_size': 0,
                                      'simu_param': 1,  # None, no grid of solutions
                                      'call_type': 0,
                                      'param_date': it_run}
                main(dc_it_execute_type)

        elif st_run_group == 'kappaCounter':
            # local PE runs (at some equilibrium prices)
            for it_run in [16,
                           17, 18, 19, 20,
                           21, 22, 23, 24]:
                dc_it_execute_type = {'model_assumption': 1,  # ITG_PE
                                      'compute_size': 1,
                                      'simu_param': 1,  # None, no grid of solutions
                                      'call_type': 0,
                                      'param_date': it_run}
                main(dc_it_execute_type)

        else:
            raise ValueError(f'{st_run_group=} is invalid')
