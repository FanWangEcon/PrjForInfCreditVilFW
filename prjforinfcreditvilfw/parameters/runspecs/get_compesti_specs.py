"""
@author: fan
"""

import logging
import pyfan.amto.json.json as support_json

import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def get_speckey_string(compute_spec_key='ng_s_d', esti_spec_key='kap_m0_nld_m_simu',
                       moment_key=2, momset_key=3):
    """Generate speckey string with four elements, joined by connector equality sign
    """
    st_speckey = '='.join(list(map(lambda x: str(x), [compute_spec_key, esti_spec_key, moment_key, momset_key])))

    return st_speckey


def get_compesti_specs_aslist(compute_spec_key='ng_s_d', esti_spec_key='kap_m0_nld_m_simu',
                              moment_key=2, momset_key=3):
    """Generate compesti_specs from four parameters explicitly defined

    these parameters are defined as a string under speckey parameter when run.py is called
    from command line. This function is to clarify the four separate input elements.
    """

    st_speckey = get_speckey_string(compute_spec_key, esti_spec_key, moment_key, momset_key)
    compesti_specs = get_compesti_specs(st_speckey)
    return compesti_specs


def get_compesti_specs(speckey='ng_s_d=kap_m0_nld_m_simu=2=3'):
    """Generate compesti from run.py string commandline input

    When the program is called from commandline, need to parse parameters, the first parameter from command
    line is args.speckey, the -A optional parameter for run.py in invoke.run_main.invoke_main.

    For the second element of the speckey, crucial whether *_SIMU* is the suffix. The *_SIMU*
    estispecs will adjust the output compest specs such that when processsed by
    parameters.loop_param_combo_list.loops_gen.combo_list_auto, a combo_list for grid simulation
    will be generated, in particular, this will not include key ESTI_PARAM_VEC_COUNT, which
    means COMPUTE_PARAM_VEC_COUNT will be the length of the output COMBO_LIST.

    Parameters
    ----------
    speckey : str
        A string composed of four elements joined together by some separator. The first
        element are *compute_spec_key*, the second element *esti_spec_key*, the third element
        is *moment_key*, the fourth element is *momset_key*.
    """

    logger.warning('speckey:%s', speckey)
    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')
    support_json.jdump(spec_key_dict, 'spec_key_dict', logger=logger.warning)

    if isinstance(spec_key_dict, str):
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
        # estimation routine specific subfolder name/prefix
        compesti_short_name = hardstring.gen_compesti_short_name(compute_spec_key, esti_spec_key, moment_key,
                                                                 momset_key)
        compesti_specs['compesti_short_name'] = compesti_short_name

        # logging
        support_json.jdump(cur_compute_spec, 'cur_compute_spec', logger=logger.info)
        support_json.jdump(cur_esti_spec, 'cur_esti_spec', logger=logger.info)
        support_json.jdump(compesti_specs, 'compesti_specs', logger=logger.warning)

    return compesti_specs
