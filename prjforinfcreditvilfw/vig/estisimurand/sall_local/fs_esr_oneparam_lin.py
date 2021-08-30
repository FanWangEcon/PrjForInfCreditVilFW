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
from copy import deepcopy
import logging
import traceback
import numpy as np

logger = logging.getLogger(__name__)


def main(it_execute_type=11):
    """Core local computer estimation testing function

    Tests estimation over multiple time-periods, partial equilibrium.

    Includes: 1. one time/region specific or mulitple parameters; 2. integrated or not;
    3. limited (5) or more starting seeds.

    Local testing includes several sets of tests for different groups of parameters

    # Parameter Group 1:

    > dc_paramstr_key_list_str = {'ce': ['list_tKap_mlt_ce1a2'], 'ne': ['list_tKap_mlt_ne1a2']}
    > save_directory_main = 'esti_tst_tKap'

    it_execute_type: 11 21
    """
    # Initiate Log
    spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                         main_folder_name='logvig', sub_folder_name='estisimurand',
                                         subsub_folder_name='oneparam_local',
                                         file_name='fs_estisimurand_oneparam_lin',
                                         it_time_format=8, log_level=logging.INFO)

    # if change direct name, update in projectsupport.systemsupport.get_paths
    compute_spec_key_esr137 = 'ng_s_t'
    hardstring.file_suffix(file_type='json', sub_type='partial', integrated=True)

    it_esti_optsalgo_hundreds = int(np.floor(it_execute_type / 100))
    it_esti_optsalgo_tens = int(np.floor(it_execute_type / 10))
    it_esti_optsalgo_digits = it_execute_type % 10
    print(f'{it_esti_optsalgo_hundreds=}, {it_esti_optsalgo_digits=}')

    if it_esti_optsalgo_hundreds == 1:
        dc_paramstr_key_list_str = {'ce': ['list_tKap_mlt_ce1a2'], 'ne': ['list_tKap_mlt_ne1a2']}
        save_directory_main = 'esti_tst_tKap'
    elif it_esti_optsalgo_hundreds == 2:
        dc_paramstr_key_list_str = {'ce': ['list_tvars_mlt_ce1a2'], 'ne': ['list_tvars_mlt_ne1a2']}
        save_directory_main = 'esti_tst_tvars'
    else:
        raise ValueError(f'{it_execute_type=} is not allowed, tens violation')

    if it_esti_optsalgo_digits == 1:
        # quick run test
        # D:\repos\ThaiJMP\esti
        st_xd = 'x'
        st_file_suffix = '_esr_tstN5_vig'
        st_testscale = 'tinytst'
    elif it_esti_optsalgo_digits == 2:
        # quick run test, N100 required for more parameters
        # D:\repos\ThaiJMP\esti
        st_xd = 'x'
        st_file_suffix = '_esr_tstN100_vig'
        st_testscale = 'medtst'
    elif it_esti_optsalgo_digits == 3:
        # takes much longer and is larger in terms of the number of seeds
        # D:\repos\ThaiJMP\esti
        st_xd = ''
        st_file_suffix = '_esr_tstN100_vig'
        st_testscale = 'medtst'
    elif it_esti_optsalgo_digits == 4:
        # Integrated Small
        # NOTE: GE DOES NOT WORK FOR ESTIMATION with MULTIPLE TIME PERIODS
        st_xd = 'x'
        st_file_suffix = '_ITG_esr_tstN5_vig'
        st_testscale = 'tinytst'
        compute_spec_key_esr137 = 'b_ng_p_d'
    elif it_esti_optsalgo_digits == 5:
        # Integrated Small
        # NOTE: GE DOES NOT WORK FOR ESTIMATION with MULTIPLE TIME PERIODS
        st_xd = ''
        st_file_suffix = '_ITG_esr_tstN5_vig'
        st_testscale = 'tinytst'
        compute_spec_key_esr137 = 'b_ng_p_d'
    else:
        raise ValueError(f'{it_execute_type=} is not allowed, digit violation')

    # Specify to estimate
    estimate = True
    # ar_steps meaning
    """
    Eight Elements of Esti-Simu-Rand
    1. Simulate at N sets of parameter combinations
    2. Polynomial approximation surface based on (1) for each outcome of interest, find best
    3. Estimation at N sets of starting points with (2) as objective function
    4. Gather results frorm (3), find M best.
    5. Simulate (estimate once) at the top M best results from (4) actual model, compare objective to approximated from (3)
    6. Gather results from (5), re-rank best of the M best from (4)
    7. Estimate at the top M best results from (4) actual model, (4) M best are M best seeds
    8. Gather results from (7), re-rank best of the final results from the M best seeds
    """

    ar_steps = [1, 2, 3, 4, 5, 6, 7, 8]
    # ar_steps = [2]
    # need to be central first then northeast, by design
    ar_regions = ['ce', 'ne']

    # 1. range of parameter values and other parameter specifications for all the parameters.
    combo_type_list_ab = 'e'
    combo_type_list_date_base = '20201025'

    # 2. over which parameters to estimate the model, which parameters are free Parameters
    # value need to be list, not string

    # 3. how the model should be simulated, GE or not, Integrated or not. Many other decisions related to how the
    # model should be simulated, most related to parameters/model specifications.
    combo_type_list_date = combo_type_list_date_base + st_xd

    # combo_type_list_date = combo_type_list_date + '_ITG_esr'
    combo_type_list_date = combo_type_list_date + st_file_suffix

    # 4. region and time periods for estimation, allowing which parameters to vary, and to jointly try to match
    # outcomes in several regions and/or time periods.
    dc_moment_key = {'ce': 3, 'ne': 4}
    momset_key = 3

    # 5. how many points at which to do ESR draws for simulation
    # the two esti_specs below share the same ESTI_PARAM_VEC_COUNT

    # "_1" = nelder meand and very lax tolerance
    esti_spec_key_esr1 = 'esti_' + st_testscale + '_thin_1'
    esti_spec_key_esr3 = 'esti_' + st_testscale + '_mpoly_13'
    esti_spec_key_esr5 = 'esti_mplypostsimu_1'
    esti_spec_key_esr7 = 'esti_mplypostesti_12'

    # 6. computational structure, if local, or remote, whether parallel processing should be used, and if using
    # remote the compute requirements
    # When local invoke the options don't matter much? except for worker count?
    compute_spec_key_esr1 = compute_spec_key_esr137
    compute_spec_key_esr3 = 'mpoly_1'
    compute_spec_key_esr5 = compute_spec_key_esr137
    compute_spec_key_esr7 = compute_spec_key_esr137

    # 7. where to store results, and what graphs/tables etc to save and to output.
    graph_panda_list_name_esr1 = 'min_graphs'
    graph_panda_list_name_esr3 = 'min_graphs'
    graph_panda_list_name_esr5 = 'min_graphs'
    graph_panda_list_name_esr7 = 'min_graphs'
    log_file = False

    # Top results to keep
    # Random simulate points, grab out top five (objective) for review
    top_estimates_keep_count_esr2 = 5
    # MPOLY estimation all random points, top 5 results
    top_estimates_keep_count_esr4 = 5
    top_estimates_keep_count_esr6 = 5
    # At which'th top result to do full estimation
    ls_it_esti_top_which = [1, 2, 3, 4, 5]
    # Present which full estimation with mpoly best seeds
    top_estimates_keep_count_esr8 = 5

    # A. Common Arguments
    # importantly, ESTI_TEST_11, DOES NOT HAVE SIMU at the end.
    # This means moments will be generated, nad parameter values of beta will be randomly
    # drawn rather than over meshed grid
    dc_combo_type_kwargs = {'file': combo_type_list_ab, 'date': combo_type_list_date,
                            'paramstr_key_list_str': dc_paramstr_key_list_str['ce']}
    combo_type_ce = paramcombotypelist.gen_combo_type_list(**dc_combo_type_kwargs)[0]
    dc_combo_type_kwargs['paramstr_key_list_str'] = dc_paramstr_key_list_str['ne']
    combo_type_ne = paramcombotypelist.gen_combo_type_list(**dc_combo_type_kwargs)[0]
    dc_combo_type = {'ce': combo_type_ce, 'ne': combo_type_ne}

    """
    Step 1, default kwargs for key functions
    """

    dc_speckey_default = {'compute_spec_key': None,
                          'esti_spec_key': None,
                          'moment_key': None,
                          'momset_key': momset_key}
    # MPOLY store separately, because it needs to be reused by postesti
    dc_speckey_mpoly_default = {'compute_spec_key': compute_spec_key_esr3,
                                'esti_spec_key': esti_spec_key_esr3,
                                'moment_key': None,
                                'momset_key': momset_key}

    # generate args
    multiprocess = False
    bl_ge = False
    dc_invoke_main_kwargs = {'speckey': param_compestispecs.get_speckey_string(**dc_speckey_default),
                             'ge': bl_ge,
                             'multiprocess': multiprocess,
                             'estimate': estimate,
                             'graph_panda_list_name': graph_panda_list_name_esr1,
                             'save_directory_main': save_directory_main,
                             'logging_level': logging.WARNING,
                             'log_file': log_file,
                             'log_file_suffix': ''}

    # Kwargs for combine_indi_esti
    dc_search_combine_indi_esti_kwargs = {'moment_key': dc_speckey_default['moment_key'],
                                          'momset_key': dc_speckey_default['momset_key'],
                                          'exo_or_endo_graph_row_select': None,
                                          'image_save_name_prefix': 'AGG_ALLESTI_',
                                          'search_directory': None,
                                          'fils_search_str': None,
                                          'save_file_name': None,
                                          'save_panda_all': True,
                                          'graph_list': None,
                                          'top_estimates_keep_count': 2}
    """
    Step 1,2
    """
    # Update compute and esti specs
    for it_step in ar_steps:

        if it_step == 1 or it_step == 2:
            dc_speckey_default['compute_spec_key'] = compute_spec_key_esr1
            dc_speckey_default['esti_spec_key'] = esti_spec_key_esr1
            top_estimates_keep_count = top_estimates_keep_count_esr2

        if it_step == 3 or it_step == 4:
            dc_speckey_default = deepcopy(dc_speckey_mpoly_default)
            top_estimates_keep_count = top_estimates_keep_count_esr4

        if it_step == 5 or it_step == 6:
            dc_speckey_default['compute_spec_key'] = compute_spec_key_esr5
            dc_speckey_default['esti_spec_key'] = esti_spec_key_esr5
            top_estimates_keep_count = top_estimates_keep_count_esr6

        if it_step == 7 or it_step == 8:
            dc_speckey_default['compute_spec_key'] = compute_spec_key_esr7
            dc_speckey_default['esti_spec_key'] = esti_spec_key_esr7
            top_estimates_keep_count = top_estimates_keep_count_esr8

        # get compute specs: for esti, GE true is not valid
        cur_compute_spec = computespec.compute_set(dc_speckey_default['compute_spec_key'])
        dc_invoke_main_kwargs['ge'] = cur_compute_spec['ge']
        dc_invoke_main_kwargs['multiprocess'] = cur_compute_spec['multiprocess']
        if cur_compute_spec['ge']:
            raise ValueError('ESR estimate routine does not allow for GE calls, '
                             'but {dc_speckey_default["compute_spec_key"]=} requires that')

        """
        Estimatate and Simulate
        """
        if it_step == 1 or it_step == 3 or it_step == 5 or it_step == 7:
            for st_regions in ar_regions:

                # A. combo_type and kwargs for invoke_main
                combo_type = dc_combo_type[st_regions]
                # update moment_key region-specific
                dc_speckey_default['moment_key'] = dc_moment_key[st_regions]
                # update spec-key, region specific and esti and compute spec specifics
                dc_invoke_main_kwargs['speckey'] = param_compestispecs.get_speckey_string(**dc_speckey_default)

                # B. MPOLY estimation before and after loops
                # Determine esr esti/simu loop seed/start points
                if it_step in [1, 3]:
                    # [['e', '20201025x_esr_mlt_all_beta', ['esti_param.beta'], None]]
                    # Number of points to randomly draw and estimate with one iteration at
                    # moment_key and momset_keys are parameters for estimate_set, they do not matter
                    dc_estispec = estispec.estimate_set(dc_speckey_default['esti_spec_key'])
                    esti_param_vec_count = dc_estispec['esti_param_vec_count']
                    ls_esr_start_loop = range(esti_param_vec_count)
                elif it_step in [5, 7]:
                    ls_esr_start_loop = ls_it_esti_top_which
                    dc_speckey_mpoly_default['moment_key'] = dc_moment_key[st_regions]
                    compesti_short_name_mpoly = hardstring.gen_compesti_short_name(**dc_speckey_mpoly_default)
                else:
                    raise ValueError(f'{it_step=} must be 1, 3, 5 or 7')

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
                            esti_top_which=it_esti_ctr)
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
        Step 2, Gather individual folder CSVs together, aggregate Excel with all simulations
        """
        if it_step == 2 or it_step == 4 or it_step == 6 or it_step == 8:
            for st_regions in ar_regions:

                """
                Which rows to select from the gathered JSON inside CSV files
                """
                if '_ITG_' in st_file_suffix:
                    # exo_or_endo_graph_row_select = '_exoitg_wgtJitg'
                    exo_or_endo_graph_row_select = hardstring.file_suffix(
                        file_type='json', integrated=True, ge=cur_compute_spec['ge'])
                else:
                    # exo_or_endo_graph_row_select = '_exo_wgtJ'
                    exo_or_endo_graph_row_select = hardstring.file_suffix(
                        file_type='json', integrated=False, ge=cur_compute_spec['ge'])
                dc_search_combine_indi_esti_kwargs['exo_or_endo_graph_row_select'] = exo_or_endo_graph_row_select

                """
                Various Specifications
                """
                combo_type = dc_combo_type[st_regions]
                search_directory = os.path.join(proj_sys_sup.main_directory(), save_directory_main,
                                                combo_type[0] + '_' + combo_type[1], '')
                dc_search_combine_indi_esti_kwargs['search_directory'] = search_directory
                dc_search_combine_indi_esti_kwargs['moment_key'] = dc_moment_key[st_regions]
                dc_search_combine_indi_esti_kwargs['compute_spec_key'] = dc_speckey_default['compute_spec_key']
                dc_search_combine_indi_esti_kwargs['top_estimates_keep_count'] = top_estimates_keep_count

                """
                Call and Run
                """
                esticomp.search_combine_indi_esti(dc_paramstr_key_list_str[st_regions], combo_type_list_ab,
                                                  combo_type_list_date,
                                                  dc_speckey_default['esti_spec_key'],
                                                  **dc_search_combine_indi_esti_kwargs)


if __name__ == "__main__":
    # This is needed in order to avoid freeze_support() issue for parallel processing.
    # ls_it_execute_type = [11, 21, 12, 22, 13, 23, 14, 24]
    # ls_it_execute_type = [11, 21, 12, 22, 13, 23]
    # ls_it_execute_type = [11, 12, 13]
    ls_it_execute_type = [22]
    for it_execute_type in ls_it_execute_type:
        main(it_execute_type)
