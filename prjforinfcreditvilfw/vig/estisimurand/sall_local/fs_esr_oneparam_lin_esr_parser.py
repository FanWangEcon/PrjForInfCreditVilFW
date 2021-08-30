import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.runspecs.get_compesti_specs as param_compestispecs
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import invoke.run_main as invoke_run_main
import estimation.postprocess.process_main as esticomp
import os as os
import projectsupport.hardcode.string_shared as hardstring
import parameters.parse_combo_type as parsecombotype
import invoke.run_esr_parser as run_esr_parser
from copy import deepcopy
import logging
import traceback
import numpy as np

logger = logging.getLogger(__name__)


def main(ar_steps=None, it_execute_type=11, dc_it_execute_type=None, **kwargs):
    """Core local computer estimation testing function

    Tests estimation over multiple time-periods, partial equilibrium.

    Includes: 1. one time/region specific or mulitple parameters; 2. integrated or not;
    3. limited (5) or more starting seeds.

    Local testing includes several sets of tests for different groups of parameters

    # Parameter Group 1:

    > dc_paramstr_key_list_str = {'ce': ['list_tKap_mlt_ce1a2'], 'ne': ['list_tKap_mlt_ne1a2']}
    > save_directory_main = 'esti_tst_tKap'

    it_execute_type: 11 21

    Eight Elements of Esti-Simu-Rand
    1. Simulate at N sets of parameter combinations
    2. Polynomial approximation surface based on (1) for each outcome of interest, find best
    3. Estimation at N sets of starting points with (2) as objective function
    4. Gather results frorm (3), find M best.
    5. Simulate (estimate once) at the top M best results from (4) actual model, compare objective to approximated from (3)
    6. Gather results from (5), re-rank best of the M best from (4)
    7. Estimate at the top M best results from (4) actual model, (4) M best are M best seeds
    8. Gather results from (7), re-rank best of the final results from the M best seeds

    Parameters
    ----------
    it_execute_type : int
        integer, several basic estimation type hard-coded
    dc_it_execute_type : dict
        dict of specficiations, if this is not None, then this overrides dc_it_execute_type
    """

    """
    A1. Log
    """
    # Initiate Log
    spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                         main_folder_name='logvig', sub_folder_name='estisimurand',
                                         subsub_folder_name='oneparam_local',
                                         file_name='fs_estisimurand_oneparam_lin',
                                         it_time_format=8, log_level=logging.INFO)
    """
    A2. Defaults
    """
    if ar_steps is None:
        ar_steps = [1, 2, 3, 4, 5, 6, 7, 8]
    if dc_it_execute_type is None and it_execute_type is None:
        dc_it_execute_type = {'model_assumption': 0,
                              'compute_size': 0,
                              'esti_size': 0,
                              'esti_param': 0,
                              'call_type': 0,
                              'param_date': 0}

    """
    A3. Fixed Parameters
    """
    ar_regions = ['ce', 'ne']
    # generate args
    dc_invoke_main_kwargs = {'speckey': None,
                             'ge': False,
                             'multiprocess': False,
                             'estimate': True,
                             'graph_panda_list_name': 'min_graphs',
                             'save_directory_main': None,
                             'logging_level': logging.WARNING,
                             'log_file': False,
                             'log_file_suffix': ''}

    # Kwargs for combine_indi_esti
    dc_search_combine_indi_esti_kwargs = {'moment_key': None,
                                          'momset_key': None,
                                          'exo_or_endo_graph_row_select': None,
                                          'image_save_name_prefix': 'AGG_ALLESTI_',
                                          'search_directory': None,
                                          'fils_search_str': None,
                                          'save_file_name': None,
                                          'save_panda_all': True,
                                          'graph_list': None,
                                          'top_estimates_keep_count': 2}

    """
    B. Call esr parser to get non-esr-run specific outputs
    """
    # Call (1) get results common for all
    __, __, \
    dc_combo_type, dc_combo_type_component, \
    __, __, esrf, \
    __, __, __ = \
        run_esr_parser.run_esr_arg_generator(1,
                                             awslocal=False,
                                             dc_it_execute_type=dc_it_execute_type,
                                             **kwargs)
    dc_invoke_main_kwargs['save_directory_main'] = esrf

    """
    C. esr-run step specific operations 
    """
    # Update compute and esti specs
    for it_step in ar_steps:

        """
        D1. Call esr parser to get esr-run specific outputs
        """
        __, __, \
        __, __, \
        dc_st_speckey, dc_st_speckey_mpoly, __, \
        it_esti_top_which_max, __, __ = \
            run_esr_parser.run_esr_arg_generator(it_step, awslocal=False,
                                                 dc_it_execute_type=dc_it_execute_type)
        top_estimates_keep_count = it_esti_top_which_max

        """
        D2. esr-step specific speckey dict components
        """
        # first only need values common to both regions
        dc_speckey_default = estispec.compute_esti_spec_combine(spec_key=dc_st_speckey[ar_regions[0]],
                                                                action='split')


        """
        D3. GE and Multiprocess based on compute specification
        """
        cur_compute_spec = computespec.compute_set(dc_speckey_default['compute_spec_key'])
        dc_invoke_main_kwargs['ge'] = cur_compute_spec['ge']
        dc_invoke_main_kwargs['multiprocess'] = cur_compute_spec['multiprocess']
        if cur_compute_spec['ge']:
            raise ValueError('ESR estimate routine does not allow for GE calls, '
                             'but {dc_speckey_default["compute_spec_key"]=} requires that')

        """
        E1. esr-run 1, 3, 5, or 7, Estimatate and Simulate
        """
        if it_step in [1, 3, 5, 7]:
            for st_regions in ar_regions:

                """
                F1. esr-step and region specific speckey dict components and combo_type
                """
                combo_type = dc_combo_type[st_regions]
                dc_speckey_default = estispec.compute_esti_spec_combine(spec_key=dc_st_speckey[st_regions],
                                                                        action='split')

                """
                F2. Update invoke args
                """
                # update spec-key, region specific and esti and compute spec specifics
                dc_invoke_main_kwargs['speckey'] = param_compestispecs.get_speckey_string(**dc_speckey_default)

                """
                F3. Simulate and Estimate Loop Count, AWS parallelized with batch
                """
                # B. MPOLY estimation before and after loops
                if it_step in [1, 3]:
                    dc_estispec = estispec.estimate_set(dc_speckey_default['esti_spec_key'])
                    esti_param_vec_count = dc_estispec['esti_param_vec_count']
                    ls_esr_start_loop = range(esti_param_vec_count)
                elif it_step in [5, 7]:
                    ls_esr_start_loop = range(top_estimates_keep_count)
                    dc_speckey_mpoly_default = estispec.compute_esti_spec_combine(
                        spec_key=dc_st_speckey_mpoly[st_regions],
                        action='split')
                    compesti_short_name_mpoly = hardstring.gen_compesti_short_name(**dc_speckey_mpoly_default)
                else:
                    raise ValueError(f'{it_step=} must be 1, 3, 5 or 7')

                """
                F4. Loop over seeds and top results
                """
                # C. Loop and run estimation and simulation
                for it_esti_ctr in ls_esr_start_loop:

                    # D. Update combo_type
                    # D1. Simulation randomly and MPOLY approximation estimation
                    if it_step in [1, 3]:
                        combo_type[3] = it_esti_ctr
                    # D2. Simulate at MPOLY best, and estimate model using MPOLY as seeds
                    if it_step in [5, 7]:
                        combo_type[3] = 0
                        combo_type_e = parsecombotype.parse_combo_type_e(
                            compesti_short_name=compesti_short_name_mpoly,
                            esti_top_which=it_esti_ctr + 1)
                        if len(combo_type) == 5:
                            combo_type[4] = combo_type_e
                        else:
                            combo_type.append(combo_type_e)

                    # E. Estimate and Simulate the Model
                    try:
                        invoke_run_main.invoke_main(combo_type, **dc_invoke_main_kwargs)
                    except Exception:
                        traceback.print_exc()
                        logging.critical(f'Finished this {it_esti_ctr=} of {len(ls_esr_start_loop)=}')

        """
        E2. esr-run 2, 4, 6, or 8, Gather individual folder CSVs together, aggregate Excel with all simulations
        """
        if it_step in [2, 4, 6, 8]:
            for st_regions in ar_regions:

                """
                F5. Which rows to select from the gathered JSON inside CSV files
                """
                if '_ITG_' in dc_combo_type[st_regions][1]:
                    # exo_or_endo_graph_row_select = '_exoitg_wgtJitg'
                    exo_or_endo_graph_row_select = hardstring.file_suffix(
                        file_type='json', integrated=True, ge=cur_compute_spec['ge'])
                else:
                    # exo_or_endo_graph_row_select = '_exo_wgtJ'
                    exo_or_endo_graph_row_select = hardstring.file_suffix(
                        file_type='json', integrated=False, ge=cur_compute_spec['ge'])
                dc_search_combine_indi_esti_kwargs['exo_or_endo_graph_row_select'] = exo_or_endo_graph_row_select

                dc_speckey_default = estispec.compute_esti_spec_combine(spec_key=dc_st_speckey[st_regions],
                                                                        action='split')
                """
                F6. Various Specifications
                """
                combo_type = dc_combo_type[st_regions]
                search_directory = os.path.join(proj_sys_sup.main_directory(),
                                                dc_invoke_main_kwargs['save_directory_main'],
                                                combo_type[0] + '_' + combo_type[1], '')
                dc_search_combine_indi_esti_kwargs['search_directory'] = search_directory
                dc_search_combine_indi_esti_kwargs['moment_key'] = dc_speckey_default['moment_key']
                dc_search_combine_indi_esti_kwargs['momset_key'] = dc_speckey_default['momset_key']
                dc_search_combine_indi_esti_kwargs['compute_spec_key'] = dc_speckey_default['compute_spec_key']
                dc_search_combine_indi_esti_kwargs['top_estimates_keep_count'] = top_estimates_keep_count

                """
                F7. Call and Run
                """
                combo_type_list_ab = dc_combo_type_component[st_regions]['cta']
                combo_type_list_date = dc_combo_type_component[st_regions]['ctb']
                paramstr_key_list_str = dc_combo_type_component[st_regions]['ctc']
                esticomp.search_combine_indi_esti([paramstr_key_list_str], combo_type_list_ab,
                                                  combo_type_list_date,
                                                  dc_speckey_default['esti_spec_key'],
                                                  **dc_search_combine_indi_esti_kwargs)


if __name__ == "__main__":
    # Base Default Call
    dc_it_execute_type = {'model_assumption': 0, 'compute_size': 0,
                          'esti_size': 0, 'esti_param': 2,
                          'call_type': 0, 'param_date': 0}
    main(dc_it_execute_type=dc_it_execute_type)
