'''
Created on May 18, 2018

@author: fan

Copied over from the run.py file, so that the core invoke function can be called by itself. The run.py function
only handles command line parameter parsing.
'''

import logging

import invoke.run_estimate as runesti
import invoke.run_simulate as runsimu
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.graph.graph_sets as sup_graphset

logger = logging.getLogger(__name__)


def invoke_main(combo_type,
                speckey='ng_s_x',
                ge=False, multiprocess=False, estimate=False,
                graph_panda_list_name=None,
                save_directory_main='simu',
                logging_level=logging.WARNING,
                log_file=False,
                log_file_suffix=''):
    """
    Parameters
    ----------
    combo_type: list
        ["e", "20201025x_esr_list_tKap_mlt_ce1a2",["esti_param.kappa_ce9901", "esti_param.kappa_ce0209"], 1,
        "C1E31M3S3=1"]
        A potentially six element list, that specifies which combinations of parameters to use for simulation, and
        if looping over a grid of parameter values, which parameters' values to grid loop over, and potentially,
        which element of the parameter list to solve at if there is a long array of potential values to simulate at for
        estimation exercise. (5) the compesti_short_name from previous mpoly estimation, the fifth element is only
        specified for post-mpoly estimation. So that the computer knows files/folders to look for JSON file that has
        the latest estimation results. (6) this corresponds to esti_top_which, which top
    speckey: string
        'NG_S_D=KAP_M0_NLD_M=2=3' or 'NG_S_D'. Former is `estimate` is TRUE, latter if `estimate` is FALSE.
        Even when estimate is FALSE, could in fact also still specify `NG_S_D=KAP_M0_NLD_M_SIMU=2=3`, but note
        the addition of the SIMU term in the second element. This will make sure that moment and momset are included
    ge: boolean
        general equilibrium or not
    """

    graph_list = sup_graphset.graph_panda_sets_names(graph_panda_list_name)

    logger.warning('combo_type:%s', combo_type)
    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')

    if (isinstance(spec_key_dict, str)):
        # speckey has key, compesti_spec is None, simulate
        compesti_specs = None
    else:
        # this is simulate or estimate, both can specify comp+esti keys
        compute_spec_key = spec_key_dict['compute_spec_key']
        esti_spec_key = spec_key_dict['esti_spec_key']
        moment_key = spec_key_dict['moment_key']
        momset_key = spec_key_dict['momset_key']
        cur_compute_spec = computespec.compute_set(compute_spec_key)
        cur_esti_spec = estispec.estimate_set(esti_spec_key, moment_key=moment_key,
                                              momset_key=momset_key)
        compesti_specs = cur_compute_spec.copy()
        compesti_specs.update(cur_esti_spec)
        # combo_type to list and add to compesti, which is added to support_arg for each param_combos

    if estimate and not isinstance(spec_key_dict, str):
        # estimation + has fully specified speckey with separator, meaning speckey=NG_S_D=KAP_M0_NLD_M_SIMU=2=3
        # this would generate dict for spec_key_dict
        runesti.invoke_estimate(combo_type,
                                compute_spec_key=compute_spec_key,
                                esti_spec_key=esti_spec_key,
                                moment_key=moment_key, momset_key=momset_key,
                                ge=ge, multiprocess=multiprocess,
                                graph_list=graph_list,
                                save_directory_main=save_directory_main,
                                logging_level=logging_level, log_file=log_file,
                                log_file_suffix=log_file_suffix)

    elif (estimate is False and isinstance(spec_key_dict, str)) or (
            estimate is False and isinstance(spec_key_dict, dict)):
        # estimate is False and isinstance(spec_key_dict, str):
        #   estimate is False, which means to simulate, and is string instance : speckey=NG_S_D
        # estimate is False and isinstance(spec_key_dict, list):
        #   estimate is False, which means to simulate, and is list instance : speckey=NG_S_T=ESTI_TEST_11_SIMU=2=3

        # this would generate string for spec_key_dict
        # if compesti_spec = NOne, use speckey, no estimate
        runsimu.invoke_soluequi_partial(combo_type, combo_list=None,
                                        speckey=speckey,
                                        compesti_specs=compesti_specs,
                                        ge=ge, multiprocess=multiprocess,
                                        graph_list=graph_list,
                                        save_directory_main=save_directory_main,
                                        logging_level=logging_level, log_file=log_file,
                                        log_file_suffix=log_file_suffix)

    else:
        # if estimate, speckey needs to be multisegmented.
        # if simulate, speckey needs to be single segment.
        st_error = 'speckey=' + speckey + ' and estimate=' + str(estimate)
        raise ValueError(st_error)
