"""
Parse inputs for run_esr

import invoke.run_esr_parser as run_esr_parser
"""

import os

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import projectsupport.systemsupport as proj_sys_sup


def run_esr_arg_generator(esr_run,
                          dc_ls_execute_type=None,
                          dc_it_execute_type=None,
                          ar_regions=None,
                          dc_moment_key=None,
                          momset_key='3',
                          it_esti_top_which_max=5,
                          awslocal=False,
                          verbose=True,
                          st_conda_aws_env='wk_aws',
                          st_conda_cgefi_env='wk_cgefi'):
    """Generate input arguments for the run_arg function

    Generate arguments that service a number of functions, including:
    - AWS: \vig\estisimurand\sall_aws_sandbox\template_onefile\esr_s1357_submit_job.py
    - AWSlocal: \vig\estisimurand\sall_aws_sandbox\template_onefile\esr_s2468_sync_gather.cmd
    - VIG: \vig\estisimurand\sall_local\fs_esr_oneparam_lin.py
    - CMD: \vig\estisimurand\sall_local_sandbox\working_cmd\fs_esr_oneparam_lin_cmd.cmd

    Assume the joint estimation of two regions.

    Parameters
    ----------
    esr_run : int
        between 1 and 8 integer values
    ar_regions : list
        string list of regions
    dc_it_execute_type : dict
        Dictionary of keys and which element of the specifications should be picked
    dc_ls_execute_type : dict
        Dictionary of lists of possible specifications. These are inputs for run_esr, but basically simplified
    """

    """
    A. Default Values
    """
    if esr_run not in [1, 2, 3, 4, 5, 6, 7, 8]:
        raise ValueError(f'{esr_run=} is not valid, must be integer between 1 and 8')

    if dc_ls_execute_type is None:
        dc_ls_execute_type = {'model_assumption': ['', 'ITG', 'GE', 'ITG_GE'],
                              'compute_size': ['x', '', 'd'],
                              'esti_size': ['tinytst', 'medtst', 'bigtst'],
                              'esti_param': ['esti_tst_tKap',
                                             'esti_tst_tvars',
                                             'esti_tst_tvarsb'],
                              'call_type': ['vig', 'cmd', 'aws'],
                              'param_date': ['20201025']}

    if dc_it_execute_type is None:
        dc_it_execute_type = {'model_assumption': 0, 'compute_size': 0, 'esti_size': 0, 'esti_param': 0,
                              'call_type': 0, 'param_date': 0}

    if ar_regions is None:
        ar_regions = ['ce', 'ne']

    if dc_moment_key is None:
        dc_moment_key = {'ce': '3', 'ne': '4'}

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
    # st_cta, st_ctb = 'e', '20201025x_esr_medtst'
    st_esrbstfilesuffix = st_separator.join(filter(None, ['esr', dc_parms['esti_size'], dc_parms['call_type']]))
    st_ctb = st_separator.join(filter(None, [dc_parms['param_date'] + dc_parms['compute_size'],
                                             dc_parms['model_assumption'], st_esrbstfilesuffix]))

    """
    D3. Generate ctc
    """
    if dc_parms['esti_param'] == 'esti_tst_tKap':
        dc_ctc = {ar_regions[0]: 'list_tKap_mlt_ce1a2', ar_regions[1]: 'list_tKap_mlt_ne1a2'}
        esrf = 'esti_tst_tKap'
    elif dc_parms['esti_param'] == 'esti_tst_tvars':
        dc_ctc = {ar_regions[0]: 'list_tvars_mlt_ce1a2', ar_regions[1]: 'list_tvars_mlt_ne1a2'}
        esrf = 'esti_tst_tvars'
    elif dc_parms['esti_param'] == 'esti_tst_tvarsb':
        dc_ctc = {ar_regions[0]: 'list_tvarsb_mlt_ce1a2', ar_regions[1]: 'list_tvarsb_mlt_ne1a2'}
        esrf = 'esti_tst_tvarsb'
    else:
        raise ValueError(f'{dc_parms=} is not allowed, tens violation')

    """
    D4. combo_type, region-specific cta, ctb, and ctc
    these are components that will jointly create combo_type with paramcombotypelist.gen_combo_type_list
    """
    dc_combo_type_component = {ar_regions[0]: {'cta': st_cta, 'ctb': st_ctb, 'ctc': dc_ctc['ce']},
                               ar_regions[1]: {'cta': st_cta, 'ctb': st_ctb, 'ctc': dc_ctc['ne']}}

    """
    E1. Compute specs 
    see: https://github.com/FanWangEcon/ThaiJMP/blob/master/parameters/runspecs/compute_specs.py
    """
    if dc_parms['compute_size'] == 'x':
        esrscomputespeckey = "ng_s_t"
    elif dc_parms['compute_size'] == '':
        # regular sized
        if dc_parms['model_assumption'] == 'ITG':
            esrscomputespeckey = "b_ng_p_d"
        else:
            esrscomputespeckey = "ng_s_t"

    # Region specific speckey
    st_separator = "_"
    dc_compute_spec_key = {1: esrscomputespeckey, 3: 'mpoly_1',
                           5: esrscomputespeckey, 7: esrscomputespeckey}
    dc_compute_spec_key[2] = dc_compute_spec_key[1];
    dc_compute_spec_key[4] = dc_compute_spec_key[3];
    dc_compute_spec_key[6] = dc_compute_spec_key[5];
    dc_compute_spec_key[8] = dc_compute_spec_key[7];

    """
    E2. Esti specs
    see: https://github.com/FanWangEcon/ThaiJMP/blob/master/parameters/runspecs/estimate_specs.py 
    """
    # 1,13,1,12 specify with estimtion routine/algo to use
    dc_esti_spec_key = {1: st_separator.join(['esti', dc_parms['esti_size'], 'thin', '1']),
                        3: st_separator.join(['esti', dc_parms['esti_size'], 'mpoly', '13']),
                        5: st_separator.join(['esti', 'mplypostsimu', '1']),
                        7: st_separator.join(['esti', 'mplypostesti', '12'])}
    dc_esti_spec_key[2] = dc_esti_spec_key[1];
    dc_esti_spec_key[4] = dc_esti_spec_key[3];
    dc_esti_spec_key[6] = dc_esti_spec_key[5];
    dc_esti_spec_key[8] = dc_esti_spec_key[7];

    """
    E3. Spec keys (compute + esti + moments)
    """
    compute_spec_key, esti_spec_key = dc_compute_spec_key[esr_run], dc_esti_spec_key[esr_run]
    dc_st_speckey = {
        ar_regions[0]: '='.join([compute_spec_key, esti_spec_key, str(dc_moment_key['ce']), str(momset_key)]),
        ar_regions[1]: '='.join([compute_spec_key, esti_spec_key, str(dc_moment_key['ne']), str(momset_key)])}

    """
    E4. MPOLY Spec keys
    Relevant for ESR5 and ESR7
    """
    compute_spec_key_mpoly, esti_spec_key_mpoly = dc_compute_spec_key[3], dc_esti_spec_key[3]
    dc_st_speckey_mpoly = {
        ar_regions[0]: '='.join(
            [compute_spec_key_mpoly, esti_spec_key_mpoly, str(dc_moment_key['ce']), str(momset_key)]),
        ar_regions[1]: '='.join(
            [compute_spec_key_mpoly, esti_spec_key_mpoly, str(dc_moment_key['ne']), str(momset_key)])}

    """
    F. Generate CMD local call strings
    """
    st_cmd_prefix = "python run_esr.py"
    dc_dc_run_esr_args = {ar_regions[0]: {st_cmd_prefix: str(esr_run),
                                          '-s': dc_st_speckey[ar_regions[0]],
                                          '-cta': st_cta,
                                          '-ctb': st_ctb,
                                          '-ctc': dc_combo_type_component[ar_regions[0]]['ctc'],
                                          '-f': esrf},
                          ar_regions[1]: {st_cmd_prefix: str(esr_run),
                                          '-s': dc_st_speckey[ar_regions[1]],
                                          '-cta': st_cta,
                                          '-ctb': st_ctb,
                                          '-ctc': dc_combo_type_component[ar_regions[1]]['ctc'],
                                          '-f': esrf}}
    if awslocal and esr_run in [2, 4, 6, 8]:
        dc_dc_run_esr_args[ar_regions[0]]['--awslocal'] = ''
        dc_dc_run_esr_args[ar_regions[1]]['--awslocal'] = ''

    if esr_run in [5, 7]:
        dc_dc_run_esr_args[ar_regions[0]]['-cte1'] = dc_st_speckey_mpoly[ar_regions[0]]
        dc_dc_run_esr_args[ar_regions[1]]['-cte1'] = dc_st_speckey_mpoly[ar_regions[1]]
        dc_dc_run_esr_args[ar_regions[0]]['-cte2'] = it_esti_top_which_max
        dc_dc_run_esr_args[ar_regions[1]]['-cte2'] = it_esti_top_which_max

    dc_st_esr_args_compose = {st_region: ' '.join(
        ['activate', st_conda_cgefi_env,
         '&',
         'cd', "/d", "\"" + proj_sys_sup.directory_local_gitrepo(subfolder='invoke') + "\"",
         '&'] +
        [str(key) + ' ' + str(val)
         for key, val in dc_dc_run_esr_args[st_region].items()])
        for st_region in ar_regions}
    if verbose:
        print(f'{dc_st_esr_args_compose[ar_regions[0]]}')
        print(f'{dc_st_esr_args_compose[ar_regions[1]]}')

    """
    G. CMD local and s3 SYNC
    """
    spt_awslocal = proj_sys_sup.main_directory(bl_awslocal=True)
    spt_awslocal_esrf = proj_sys_sup.get_paths(spt_awslocal, sub_folder_name=esrf)
    dc_combo_type = {
        ar_regions[0]: paramcombotypelist.gen_combo_type_list(
            file=st_cta,
            date=st_ctb,
            paramstr_key_list_str=[dc_combo_type_component[ar_regions[0]]['ctc']])[0],
        ar_regions[1]: paramcombotypelist.gen_combo_type_list(
            file=st_cta,
            date=st_ctb,
            paramstr_key_list_str=[dc_combo_type_component[ar_regions[1]]['ctc']])[0]}
    dc_spt_awslocal_subfolders = {
        ar_regions[0]: proj_sys_sup.gen_path(dc_combo_type[ar_regions[0]], st_type='simuesti_subfolder'),
        ar_regions[1]: proj_sys_sup.gen_path(dc_combo_type[ar_regions[1]], st_type='simuesti_subfolder')}
    dc_spt_awslocal_esrf_subfolders = {
        ar_regions[0]: proj_sys_sup.get_paths(
            spt_awslocal_esrf, sub_folder_name=dc_spt_awslocal_subfolders[ar_regions[0]]),
        ar_regions[1]: proj_sys_sup.get_paths(
            spt_awslocal_esrf, sub_folder_name=dc_spt_awslocal_subfolders[ar_regions[1]])}
    dc_aws_paths = {
        ar_regions[0]: os.path.join('s3://', proj_sys_sup.s3_bucket_name(), esrf,
                                    dc_spt_awslocal_subfolders[ar_regions[0]]).replace(os.sep, '/'),
        ar_regions[1]: os.path.join('s3://', proj_sys_sup.s3_bucket_name(), esrf,
                                    dc_spt_awslocal_subfolders[ar_regions[1]]).replace(os.sep, '/')}

    dc_aws_local_sync_cmd = {region: ['activate', st_conda_aws_env,
                                      '&',
                                      'aws', 's3', 'cp',
                                      dc_aws_paths[region],
                                      dc_spt_awslocal_esrf_subfolders[region],
                                      '--recursive', '--exclude', '"*.png"'] for region in ar_regions}
    if awslocal and verbose:
        print(f'{" ".join(dc_aws_local_sync_cmd[ar_regions[0]])}')
        print(f'{" ".join(dc_aws_local_sync_cmd[ar_regions[1]])}')

    return dc_st_esr_args_compose, dc_aws_local_sync_cmd, \
           dc_combo_type, dc_combo_type_component, \
           dc_st_speckey, dc_st_speckey_mpoly, esrf, it_esti_top_which_max, \
           compute_spec_key, esti_spec_key


if __name__ == '__main__':
    """
    Call to Generate Parameter Combinations
    """
    # dc_it_execute_type = []
    dc_it_execute_type = {'model_assumption': 0, 'compute_size': 0,
                          'esti_size': 0, 'esti_param': 0,
                          'call_type': 1, 'param_date': 0}

    esr_run = 1
    for esr_run in [1, 2, 3, 4, 5, 6, 7, 8]:
        dc_st_esr_args_compose, dc_spt_awslocal_esrf_subfolders, \
        dc_combo_type, dc_combo_type_component, \
        dc_st_speckey, dc_st_speckey_mpoly, esrf, \
        it_esti_top_which_max, compute_spec_key, esti_spec_key = \
            run_esr_arg_generator(esr_run, dc_it_execute_type=dc_it_execute_type, awslocal=True)
