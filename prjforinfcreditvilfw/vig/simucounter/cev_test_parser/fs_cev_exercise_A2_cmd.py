import invoke.run_sg_parser as run_sg_parser


# ls_st_run_groups = ['test', 'GE99']
# st_run_group = ls_st_run_groups[1]
#
# if st_run_group == 'test':
#
#     dc_it_execute_type = {'model_assumption': None,
#                           'compute_size': 0,
#                           'simu_param': 0,
#                           'call_type': 1,
#                           'param_date': 0}
#     for it_run in [1, 2]:
#         if it_run == 1:
#             dc_it_execute_type['model_assumption'] = 0
#         if it_run == 2:
#             dc_it_execute_type['model_assumption'] = 1
#
#         st_sg_args_compose, aws_local_sync_cmd, \
#         combo_type, combo_type_component, \
#         sgf, \
#         compute_spec_key = run_sg_parser.run_sg_arg_generator(
#             1, dc_it_execute_type=dc_it_execute_type, verbose=True)
#
# if st_run_group == 'GE99':
#     for it_run in [1, 2, 3]:
#         dc_it_execute_type = {'model_assumption': 2,
#                               'compute_size': None,
#                               'simu_param': 1,
#                               'call_type': 1,
#                               'param_date': 0}
#         if it_run == 1:
#             # GE x
#             dc_it_execute_type['compute_size'] = 0
#         if it_run == 2:
#             # GE
#             dc_it_execute_type['compute_size'] = 1
#         if it_run == 3:
#             # GE x ITG
#             dc_it_execute_type['compute_size'] = 0
#             dc_it_execute_type['model_assumption'] = 3
#         run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)

ls_st_run_groups = ['test',
                    'sixPExTest',
                    'fourGExTest',
                    'sixPEITG',
                    'fourGE']

for st_run_group in ls_st_run_groups[4::]:

    if st_run_group == 'test':
        for it_run in [1, 2]:
            dc_it_execute_type = {'model_assumption': None,
                                  'compute_size': 0,
                                  'simu_param': 0,
                                  'call_type': 1,
                                  'param_date': 0}
            if it_run == 1:
                dc_it_execute_type['model_assumption'] = 0
            if it_run == 2:
                dc_it_execute_type['model_assumption'] = 1
        run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)

    elif st_run_group == 'sixPExTest':
        for it_run in [0, 1, 2, 3, 4, 5]:
            dc_it_execute_type = {'model_assumption': 0,  # PE
                                  'compute_size': 0,
                                  'simu_param': 1,  # None, no grid of solutions
                                  'call_type': 1,
                                  'param_date': it_run}
            run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)

    elif st_run_group == 'fourGExTest':
        for it_run in [0, 3, 4, 5]:
            dc_it_execute_type = {'model_assumption': 2,  # GE
                                  'compute_size': 0,
                                  'simu_param': 1,  # None, no grid of solutions
                                  'call_type': 1,
                                  'param_date': it_run}
            run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)

    elif st_run_group == 'fourGE':
        for it_run in [0, 3, 4, 5]:
            dc_it_execute_type = {'model_assumption': 3,  # GE
                                  'compute_size': 1,
                                  'simu_param': 1,  # None, no grid of solutions
                                  'call_type': 1,
                                  'param_date': it_run}
            run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)


    elif st_run_group == 'sixPEITG':
        for it_run in [0, 1, 2, 3, 4, 5]:
            dc_it_execute_type = {'model_assumption': 1,  # ITG_PE
                                  'compute_size': 1,
                                  'simu_param': 1,  # None, no grid of solutions
                                  'call_type': 1,
                                  'param_date': it_run}
            run_sg_parser.run_sg_arg_generator(1, dc_it_execute_type=dc_it_execute_type, verbose=True)

    else:
        raise ValueError(f'{st_run_group=} is invalid')
