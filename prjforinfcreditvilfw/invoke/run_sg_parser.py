"""
Parse inputs for run_sg

import invoke.run_sg_parser as run_sg_parser
"""

import os

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import projectsupport.systemsupport as proj_sys_sup


def run_sg_arg_generator(sg_run,
                         dc_ls_execute_type=None,
                         dc_it_execute_type=None,
                         verbose=True,
                         verbose_sync=False,
                         st_conda_aws_env='wk_aws',
                         st_conda_cgefi_env='wk_cgefi'):
    """Generate input arguments for the run_arg function

    Generate arguments that service a number of functions, including:
    - AWS: \vig\estisimurand\sall_aws_sandbox\template_onefile\sg_s1357_submit_job.py
    - AWSlocal: \vig\estisimurand\sall_aws_sandbox\template_onefile\sg_s2468_sync_gather.cmd
    - VIG: \vig\estisimurand\sall_local\fs_sg_oneparam_lin.py
    - CMD: \vig\estisimurand\sall_local_sandbox\working_cmd\fs_sg_oneparam_lin_cmd.cmd

    Assume the joint estimation of two regions.

    Parameters
    ----------
    sg_run : int
        between 1 and 8 integer values
    dc_it_execute_type : dict
        Dictionary of keys and which element of the specifications should be picked
    dc_ls_execute_type : dict
        Dictionary of lists of possible specifications. These are inputs for run_sg, but basically simplified
    """

    """
    A. Default Values
    """
    if sg_run not in [1]:
        raise ValueError(f'{sg_run=} is not valid, must be integer between 1 and 8')

    if dc_ls_execute_type is None:
        dc_ls_execute_type = {'model_assumption': ['PE', 'ITG_PE', 'GE', 'ITG_GE'],
                              'compute_size': ['x', '', 'd'],
                              'simu_param': ['CEV_PROP_INCREASE', None],
                              'call_type': ['vig', 'cmd', 'aws'],
                              'param_date': ['19E1NEp99r99',  # A1 (GE) 0
                                             '19E1NEp02r99',  # A2a 1
                                             '19E1NEp02per02ger99',  # A2b 2

                                             '19E1NEp02r02',  # B1 (GE) 3

                                             '19E1NEp02r02f11A',  # 4
                                             '19E1NEp02r02f11B',  # 5
                                             '19E1NEp02r02f11C',  # 6

                                             '19E1NEp02r02f12A',  # 7
                                             '19E1NEp02r02f12B',  # 8
                                             '19E1NEp02r02f12C',  # 9

                                             '19E1NEp02r02cltA',  # 10
                                             '19E1NEp02r02cltB',  # 11
                                             '19E1NEp02r02cltC',  # 12
                                             '19E1NEp02r02cltD',  # 13
                                             '19E1NEp02r02cltE',  # 14
                                             '19E1NEp02r02cltF',  # 15

                                             '19E1kapTkTr28',  # 16, this is the GE 28 result
                                             '19E1kapRkTr42',  # 17
                                             '19E1kapRkTr56',  # 18
                                             '19E1kapRkTr70',  # 19
                                             '19E1kapRkTr84',  # 20
                                             '19E1kapRkRr42',  # 21
                                             '19E1kapRkRr56',  # 22
                                             '19E1kapRkRr70',  # 23
                                             '19E1kapRkRr84'  # 24
                                             ]}

        if dc_it_execute_type is None:
            dc_it_execute_type = {'model_assumption': 0,
                                  'compute_size': 0,
                                  'simu_param': 0,
                                  'call_type': 0,
                                  'param_date': 0}

        """
        B. Select key-value pairs for each simplified parameter structure here
        """
        # Default index, assume first element is default
        dc_execute_default = {param_key: val_list[0] for param_key, val_list in dc_ls_execute_type.items()}
        # Non-default
        dc_selected_vals = {param_key: dc_ls_execute_type[param_key][val_idx]
                            for param_key, val_idx in dc_it_execute_type.items()}
        # Override default with externally specified values
        dc_execute_default.update(dc_selected_vals)
        dc_parms = dc_execute_default

        """
        D1. Generate cta
        """
        st_cta = 'e'

        """
        D2. Generate ctb
        """
        st_separator = "_"
        # Region-specific combo_type information
        # st_cta, st_ctb = 'e', '20201025x_sg_medtst'
        st_sgbstfilesuffix = st_separator.join(filter(None, ['sg', dc_parms['call_type']]))
        st_ctb = st_separator.join(filter(None, [dc_parms['param_date'] + dc_parms['compute_size'],
                                                 dc_parms['model_assumption'], st_sgbstfilesuffix]))

        """
        D4. combo_type, region-specific cta, ctb, and ctc
        these are components that will jointly create combo_type with paramcombotypelist.gen_combo_type_list
        """
        combo_type_component = {'cta': st_cta, 'ctb': st_ctb, 'ctc': dc_parms['simu_param']}

        """
        E1. Compute specs 
        see: https://github.com/FanWangEcon/ThaiJMP/blob/master/parameters/runspecs/compute_specs.py
        """
        if dc_parms['compute_size'] == 'x':
            compute_spec_key = "ng_s_t"
            if 'GE' in dc_parms['model_assumption']:
                compute_spec_key = "ge_p_d_bis"
        else:
            if dc_parms['model_assumption'] == 'PE':
                compute_spec_key = "ng_s_t"
            if dc_parms['model_assumption'] == 'ITG_PE':
                compute_spec_key = "local_ng_par_d_cev"
            if dc_parms['model_assumption'] == 'GE':
                compute_spec_key = "ge_p_d_bis"
            if dc_parms['model_assumption'] == 'ITG_GE':
                compute_spec_key = "ge_p_d_bis"

        """
        D3. Generate sgf
        """
        if dc_parms['simu_param'] == 'CEV_PROP_INCREASE':
            sgf = 'simu_cev_' + proj_sys_sup.save_suffix_time(format=1)
        elif dc_parms['simu_param'] is None:
            # V2 changes crra to 2, divides lending costs by 2

            if '19E1kap' in dc_parms['param_date']:
                # sgf = 'simu_polkappa_V1_' + proj_sys_sup.save_suffix_time(format=1)
                """
                V6: 1/14/2021 6:34:58 AM
                Gradient of kappa, finer CEV
                1. moroe kappa levels
                2. 201 cev points
                3. 12 type points
                """
                sgf = 'simu_polkappa_V2_' + proj_sys_sup.save_suffix_time(format=1)
            else:
                # sgf = 'simu_polA1A2B1B2_V4_' + proj_sys_sup.save_suffix_time(format=1)
                """
                V5: 1/13/2021 10:39:04 PM
                using directly reported coefficients, no additional scaling, only increase crra to 1.5
                """
                sgf = 'simu_polA1A2B1B2_V5_' + proj_sys_sup.save_suffix_time(format=1)
        else:
            raise ValueError(f'{dc_parms=} is not allowed, tens violation')

        """
        F. Generate CMD local call strings
        """
        st_cmd_prefix = "python run_sg.py"
        dc_run_sg_args = {st_cmd_prefix: str(sg_run),
                          '-s': compute_spec_key,
                          '-cta': combo_type_component['cta'],
                          '-ctb': combo_type_component['ctb'],
                          '-ctc': combo_type_component['ctc'],
                          '-f': sgf}

        st_sg_args_compose = ' '.join(
            ['activate', st_conda_cgefi_env,
             '&',
             'cd', "/d", "\"" + proj_sys_sup.directory_local_gitrepo(subfolder='invoke') + "\"",
             '&'] +
            [str(key) + ' ' + str(val)
             for key, val in dc_run_sg_args.items()])
        if verbose:
            print(f'{st_sg_args_compose}')

        if dc_parms['simu_param'] is None:
            combo_type = [st_cta, st_ctb]
        else:
            combo_type = paramcombotypelist.gen_combo_type_list(
                file=st_cta,
                date=st_ctb,
                paramstr_key_list_str=[combo_type_component['ctc']])[0]

        """
        G. CMD local and s3 SYNC
        """
        aws_local_sync_cmd = None
        if dc_parms['call_type'] == 'aws':
            spt_awslocal = proj_sys_sup.main_directory(bl_awslocal=True)
            spt_awslocal_sgf = proj_sys_sup.get_paths(spt_awslocal, sub_folder_name=sgf)
            spt_awslocal_subfolders = proj_sys_sup.gen_path(combo_type, st_type='simuesti_subfolder')
            spt_awslocal_sgf_subfolders = proj_sys_sup.get_paths(spt_awslocal_sgf,
                                                                 sub_folder_name=spt_awslocal_subfolders)
            aws_paths = os.path.join('s3://', proj_sys_sup.s3_bucket_name(), sgf, spt_awslocal_subfolders).replace(
                os.sep, '/')

            aws_local_sync_cmd = ['activate', st_conda_aws_env,
                                  '&',
                                  'aws', 's3', 'cp',
                                  aws_paths,
                                  spt_awslocal_sgf_subfolders,
                                  '--recursive', '--exclude', '"*.png"']
            if verbose_sync:
                print(f'{" ".join(aws_local_sync_cmd)}')

        return st_sg_args_compose, aws_local_sync_cmd, \
               combo_type, combo_type_component, \
               sgf, \
               compute_spec_key


if __name__ == '__main__':

    """
    Call to Generate Parameter Combinations
    """
    # dc_it_execute_type = []
    dc_it_execute_type = {'model_assumption': 0,
                          'compute_size': 0,
                          'simu_param': 1,
                          'call_type': 0,
                          'param_date': 0}

    sg_run = 1
    for sg_run in [1]:
        st_sg_args_compose, aws_local_sync_cmd, \
        combo_type, combo_type_component, \
        sgf, \
        compute_spec_key = \
            run_sg_arg_generator(sg_run, dc_it_execute_type=dc_it_execute_type)

    # dc_st_sg_args_compose, dc_spt_awslocal_sgf_subfolders, \
    # dc_combo_type, dc_combo_type_component, \
    # dc_st_speckey, dc_st_speckey_mpoly, sgf, \
    # it_esti_top_which_max, compute_spec_key, esti_spec_key = \
    #     run_sg_arg_generator(2, awslocal=True, dc_it_execute_type=dc_it_execute_type)

    print(f'{st_sg_args_compose=}')
    print(f'{aws_local_sync_cmd=}')
    print(f'{combo_type=}')
    print(f'{combo_type_component=}')
    print(f'{sgf=}')
    print(f'{compute_spec_key=}')
