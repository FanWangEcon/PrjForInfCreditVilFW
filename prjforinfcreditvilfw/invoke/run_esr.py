"""
Command line interface, run esti-simu-rand function
cd /d "G:\repos\ThaiJMP\invoke"
conda activate wk_cgefi
cd /d "G:/repos/ThaiJMP/invoke"
"""

import traceback

import argparse
import logging
import os
import sys

import estimation.postprocess.process_main as esticomp
import invoke.run_main as invoke_run_main
import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.parse_combo_type as parsecombotype
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

sys.path.append('g:\\repos\\ThaiJMP')

logger = logging.getLogger(__name__)

"""
Three broad sets of things to specify.
1. Array of parameters, and bounds on parameters, along with which subset of parameters to estimate
2. Computation and estimation specifications
3. Misc Specifications
"""

# A. Start Parser
parser = argparse.ArgumentParser(description='Run ESR cmd',
                                 formatter_class=argparse.RawTextHelpFormatter)

# A1. First positional argument for esrtype:
parser.add_argument('esrtype', type=int,
                    choices=[1, 2, 3, 4, 5, 6, 7, 8],
                    help='1. Simulate at N sets of parameter combinations\n'
                         '2. Polynomial approximation surface based on (1) '
                         'for each outcome of interest, find best\n'
                         '3. Estimation at N sets of starting points with (2) as objective function\n'
                         '4. Gather results frorm (3), find M best.\n'
                         '5. Simulate (estimate once) at the top M best results from (4) actual model, '
                         'compare objective to approximated from (3)\n'
                         '6. Gather results from (5), re-rank best of the M best from (4)\n'
                         '7. Estimate at the top M best results from (4) actual model, '
                         '(4) M best are M best seeds\n'
                         '8. Gather results from (7), re-rank best of the final results from the M best seeds')

# A2. Speckey optional argument
parser.add_argument('-s', dest='speckey', type=str,
                    default='ng_s_t=esti_tinytst_thin_1=3=3',
                    help="compute and esti keys and omments\n"
                         "esti_tinytst_thin_1 (estimate, tiny test, thin simu 1, minimizer opt 0)")

# A3. abc and e of comb_type
parser.add_argument('-cta', dest="combo_type_a",
                    default='e', type=str)
parser.add_argument('-ctb', dest="combo_type_b",
                    default='20201025x_esr_cmd', type=str,
                    help='combo type second element generated with gen_combo_type_list() using ctb and ctc')
parser.add_argument('-ctc', dest="combo_type_c",
                    default=['list_tKap_mlt_ce1a2'], nargs='+', type=str,
                    help='combo type second element generated with gen_combo_type_list() using ctb and ctc')
parser.add_argument('-cte1', dest="combo_type_e1_speckey_mpoly",
                    default='mpoly_1=esti_tinytst_mpoly_13=3=3', type=str)
parser.add_argument('-cte2', dest="combo_type_e2_max_esti_top_which_max",
                    default=5, type=int)

parser.add_argument('-f', dest="save_directory_main",
                    default='esti', type=str)

# A5. other parameters
parser.add_argument('-top', dest="top_estimates_keep_count",
                    default='5', type=int,
                    help='for esr 2, 4, 6 or 8, the number of top results to '
                         'select out for csv and tex json extractions ')
parser.add_argument('--awslocal', dest="bl_awslocal",
                    action="store_true", default=False,
                    help='if False, assume esti simu results in local folder,'
                         'if True, assume results in locally synced s3 folder')

# Need to protect within __main__ to avoid freeze issue for parallel
if __name__ == "__main__":

    # A6. parse arguments
    args = parser.parse_args()
    it_esrtype = args.esrtype
    st_speckey = args.speckey
    st_combo_type_a = args.combo_type_a
    st_combo_type_b = args.combo_type_b
    ls_st_combo_type_c = hardstring.parse_command_line_str2list(args.combo_type_c)
    st_speckey_mpoly = args.combo_type_e1_speckey_mpoly
    it_esti_top_which_max = args.combo_type_e2_max_esti_top_which_max
    save_directory_main = args.save_directory_main
    # steps 2,4,6,8 only:
    top_estimates_keep_count = args.top_estimates_keep_count
    bl_awslocal = args.bl_awslocal

    # Error check
    if it_esrtype not in [1, 2, 3, 4, 5, 6, 7, 8]:
        raise ValueError(f'{it_esrtype=} has to be 1 to 8')

    # B. Generate combo_type base
    # B1. Given inputs Construct combo_type
    combo_type_kwargs = {'file': st_combo_type_a, 'date': st_combo_type_b,
                         'paramstr_key_list_str': ls_st_combo_type_c}
    combo_type = paramcombotypelist.gen_combo_type_list(**combo_type_kwargs)[0]

    # B2a. estimate and compute specs
    # B2b. how the model should be simulated, GE or not, Integrated or not. Many other decisions related to how the
    # model should be simulated, most related to parameters/model specifications.
    estimate = True
    # Get compute sepc
    dc_speckey = estispec.compute_esti_spec_combine(spec_key=st_speckey, action='split')
    # get compute specs: for esti, GE true is not valid
    cur_compute_spec = computespec.compute_set(dc_speckey['compute_spec_key'])
    bl_ge = cur_compute_spec['ge']
    bl_multiprocess = cur_compute_spec['multiprocess']
    if cur_compute_spec['ge']:
        raise ValueError('ESR estimate routine does not allow for GE calls, '
                         'but {dc_speckey_default["compute_spec_key"]=} requires that')

    # B3. MISC specifications
    graph_panda_list_name_esr = 'min_graphs'
    log_file = False
    if it_esrtype == 1:
        graph_panda_list_name = 'min_graphs'
    if it_esrtype == 3:
        graph_panda_list_name = 'min_graphs'
    if it_esrtype == 5:
        graph_panda_list_name = 'min_graphs'
    if it_esrtype == 7:
        graph_panda_list_name = 'min_graphs'

    # C. Call 1 eval or multiple eval estimation routines
    if it_esrtype in [1, 3, 5, 7]:

        dc_invoke_main_kwargs = {'speckey': st_speckey,
                                 'ge': bl_ge,
                                 'multiprocess': bl_multiprocess,
                                 'estimate': estimate,
                                 'graph_panda_list_name': graph_panda_list_name,
                                 'save_directory_main': save_directory_main,
                                 'logging_level': logging.WARNING,
                                 'log_file': log_file,
                                 'log_file_suffix': ''}

        # C1. MPOLY estimation before and after loops
        ls_esr_start_loop = []
        if it_esrtype in [1, 3]:
            # [['e', '20201025x_esr_mlt_all_beta', ['esti_param.beta'], None]]
            dc_estispec = estispec.estimate_set(dc_speckey['esti_spec_key'])
            esti_param_vec_count = dc_estispec['esti_param_vec_count']
            ls_esr_start_loop = range(esti_param_vec_count)
        if it_esrtype in [5, 7]:
            ls_esr_start_loop = range(it_esti_top_which_max)
            dc_speckey_mpoly = estispec.compute_esti_spec_combine(spec_key=st_speckey_mpoly, action='split')
            compesti_short_name_mpoly = hardstring.gen_compesti_short_name(**dc_speckey_mpoly)

        # C2. Loop and run estimation and simulation
        for it_esti_ctr in ls_esr_start_loop:

            # AWS Batch Index
            if "AWS_BATCH_JOB_ARRAY_INDEX" in os.environ:
                st_batch_job_index = os.environ['AWS_BATCH_JOB_ARRAY_INDEX']
                it_batch_job_index = int(st_batch_job_index)
            else:
                it_batch_job_index = it_esti_ctr
            print(f'{it_batch_job_index=} and {it_esti_ctr=}')

            # run one by one on AWS Batch
            if it_batch_job_index == it_esti_ctr:

                # C3. Update combo_type
                # C3a. Simulation randomly and MPOLY approximation estimation
                if it_esrtype in [1, 3]:
                    combo_type[3] = it_esti_ctr
                # C3b. Simulate at MPOLY best, and estimate model using MPOLY as seeds
                if it_esrtype in [5, 7]:
                    combo_type[3] = 0
                    # it_esti_ctr + 1, it_esti_ctr starts at 0, esti_top_which starts at 1
                    combo_type_e = parsecombotype.parse_combo_type_e(compesti_short_name=compesti_short_name_mpoly,
                                                                     esti_top_which=it_esti_ctr + 1)
                    if len(combo_type) == 5:
                        combo_type[4] = combo_type_e
                    else:
                        combo_type.append(combo_type_e)

                # C3c. Estimate and Simulate the Model
                # if proj_sys_sup.check_is_on_aws_docker():
                # see error message if running on docker
                # invoke_run_main.invoke_main(combo_type, **dc_invoke_main_kwargs)
                # else:
                # try and except even on EC2, so that container task will proceed to be under succeed column rather than
                #     the fail column
                try:
                    invoke_run_main.invoke_main(combo_type, **dc_invoke_main_kwargs)
                except Exception:
                    traceback.print_exc()
                    logging.critical(f'Finished this {it_esti_ctr=} of {len(ls_esr_start_loop)=}')

    # D. Gather Results, find Top estimates.
    if it_esrtype in [2, 4, 6, 8]:

        """
        Which rows to select from the gathered JSON inside CSV files
        """
        if '_ITG_' in combo_type[1]:
            # exo_or_endo_graph_row_select = '_exoitg_wgtJitg'
            exo_or_endo_graph_row_select = hardstring.file_suffix(file_type='json', integrated=True, ge=bl_ge)
        else:
            # exo_or_endo_graph_row_select = '_exo_wgtJ'
            exo_or_endo_graph_row_select = hardstring.file_suffix(file_type='json', integrated=False, ge=bl_ge)

        # Search path
        search_directory = os.path.join(proj_sys_sup.main_directory(bl_awslocal),
                                        save_directory_main, combo_type[0] + '_' + combo_type[1], '')
        # kwargs for search_combine_indi_esti
        dc_search_combine_indi_esti_kwargs = {'moment_key': dc_speckey['moment_key'],
                                              'momset_key': dc_speckey['momset_key'],
                                              'exo_or_endo_graph_row_select': exo_or_endo_graph_row_select,
                                              'image_save_name_prefix': 'AGG_ALLESTI_',
                                              'search_directory': search_directory,
                                              'fils_search_str': None,
                                              'save_file_name': None,
                                              'save_panda_all': True,
                                              'graph_list': None,
                                              'top_estimates_keep_count': top_estimates_keep_count,
                                              'compute_spec_key': dc_speckey['compute_spec_key']}
        # Call search combine function
        esticomp.search_combine_indi_esti(combo_type_kwargs['paramstr_key_list_str'],
                                          combo_type_kwargs['file'],
                                          combo_type_kwargs['date'],
                                          dc_speckey['esti_spec_key'],
                                          **dc_search_combine_indi_esti_kwargs)
