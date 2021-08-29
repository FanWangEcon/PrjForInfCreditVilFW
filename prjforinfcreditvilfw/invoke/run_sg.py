"""
Command line interface, run esti-simu-rand function
cd /d "G:\repos\ThaiJMP\invoke"
conda activate wk_cgefi
cd /d "G:/repos/ThaiJMP/invoke"

See also run_esr.py
This function runs simulation, possibly on AWS Batch
"""

import argparse
import logging
import os
import sys

import invoke.run_main as invoke_run_main
import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.string_shared as hardstring

sys.path.append('g:\\repos\\ThaiJMP')

logger = logging.getLogger(__name__)

# A. Start Parser
parser = argparse.ArgumentParser(description='Run SG cmd',
                                 formatter_class=argparse.RawTextHelpFormatter)

# A1. First positional argument for sgtype:
parser.add_argument('sgtype', type=int,
                    choices=[1],
                    help='1. Simulate at N sets of parameter combinations\n')

# A2. Speckey optional argument
parser.add_argument('-s', dest='speckey', type=str,
                    default='ng_s_t',
                    help="compute key\n"
                         "ng_s_t is the smallest three points test.\n"
                         "local_ng_par_d_cev is the primary cev spec.")

# A3. abc and e of comb_type
parser.add_argument('-cta', dest="combo_type_a",
                    default='e', type=str)
parser.add_argument('-ctb', dest="combo_type_b",
                    default='20201025x_SG', type=str,
                    help='combo type second element generated with gen_combo_type_list() using ctb and ctc')
parser.add_argument('-ctc', dest="combo_type_c",
                    default=['beta'], nargs='+', type=str,
                    help='combo type second element generated with gen_combo_type_list() using ctb and ctc')

# folder name
parser.add_argument('-f', dest="save_directory_main",
                    default='simu', type=str)

# Need to protect within __main__ to avoid freeze issue for parallel
if __name__ == "__main__":

    # A6. parse arguments
    args = parser.parse_args()
    it_sgtype = args.sgtype
    st_speckey = args.speckey
    st_combo_type_a = args.combo_type_a
    st_combo_type_b = args.combo_type_b
    ls_st_combo_type_c = hardstring.parse_command_line_str2list(args.combo_type_c)
    save_directory_main = args.save_directory_main

    # Parsing ls_st_combo_type_c
    logger.warning('ls_st_combo_type_c:%s', ls_st_combo_type_c)
    logger.warning('ls_st_combo_type_c.__class__.__name__:%s',
                   ls_st_combo_type_c.__class__.__name__)
    if (ls_st_combo_type_c == 'none' or
            ls_st_combo_type_c == 'None' or
            ls_st_combo_type_c == 'NONE' or
            ls_st_combo_type_c == ['NONE'] or
            ls_st_combo_type_c == ['None'] or
            ls_st_combo_type_c is None):
        ls_st_combo_type_c = None

    # Error check
    if it_sgtype not in [1]:
        raise ValueError(f'{it_sgtype=} has to be 1')

    # B. Generate combo_type base
    # B1. Given inputs Construct combo_type
    if ls_st_combo_type_c is None:
        combo_type = [st_combo_type_a, st_combo_type_b]
    else:
        combo_type_kwargs = {'file': st_combo_type_a, 'date': st_combo_type_b,
                             'paramstr_key_list_str': ls_st_combo_type_c}
        combo_type = paramcombotypelist.gen_combo_type_list(**combo_type_kwargs)[0]

    # B2a. estimate and compute specs
    # B2b. how the model should be simulated, GE or not, Integrated or not. Many other decisions related to how the
    # model should be simulated, most related to parameters/model specifications.
    # Get compute sepc
    dc_speckey = estispec.compute_esti_spec_combine(spec_key=st_speckey, action='split')
    if isinstance(dc_speckey, str):
        compute_spec_key = dc_speckey
    else:
        compute_spec_key = dc_speckey['compute_spec_key']

    # get compute specs: for esti, GE true is not valid
    cur_compute_spec = computespec.compute_set(compute_spec_key)
    bl_ge = cur_compute_spec['ge']
    bl_multiprocess = cur_compute_spec['multiprocess']
    compute_param_vec_count = cur_compute_spec['compute_param_vec_count']

    # C. Call 1 eval or multiple eval estimation routines
    dc_invoke_main_kwargs = {'speckey': st_speckey,
                             'ge': bl_ge,
                             'multiprocess': bl_multiprocess,
                             'estimate': False,
                             'graph_panda_list_name': 'main_cev_graphs',
                             'save_directory_main': save_directory_main,
                             'logging_level': logging.WARNING,
                             'log_file': False,
                             'log_file_suffix': ''}

    # Simulate
    # first combo_type of combo_list, only one element
    # loop over meshed simu points
    if len(combo_type) <= 2:
        # In effect if ls_st_combo_type_c = None, simulate at one point, as specified by st_combo_type_a and st_combo_type_b
        # AWS Batch is not needed
        # This is done for example, for single GE simulation
        invoke_run_main.invoke_main(combo_type, **dc_invoke_main_kwargs)

    else:
        it_mesh_flat_len = compute_param_vec_count ** len(combo_type[2])

        # loop over
        for it_mesh_grid_ctr in range(it_mesh_flat_len):

            if "AWS_BATCH_JOB_ARRAY_INDEX" in os.environ:
                st_batch_job_index = os.environ['AWS_BATCH_JOB_ARRAY_INDEX']
                it_batch_job_index = int(st_batch_job_index)
            else:
                it_batch_job_index = it_mesh_grid_ctr

            print(f'{it_batch_job_index=} and {it_mesh_grid_ctr=}')

            # run one by one on AWS Batch
            if it_batch_job_index == it_mesh_grid_ctr:
                combo_type[3] = it_mesh_grid_ctr
                invoke_run_main.invoke_main(combo_type, **dc_invoke_main_kwargs)
