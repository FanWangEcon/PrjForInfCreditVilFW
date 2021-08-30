"""
Created on Dec 8, 2020

@author: fan

https://github.com/FanWangEcon/ThaiJMP/blob/02fb3360959e59ea6a7f6921343c702a962e9f25/parameters/loop_param_combo_list/loops_gen_json.py#L21

This vig tests grabbing out from an existing JSON file estimated parameters.

After MPOLY estimation, there are JSON result files for top 1,2,3 etc estiamtes from the MPOLY. run. Using
*combo_type_e*, which specifies *compesti_short_name* and *esti_top_which*, we specify the file name to be
used in grabbing out existing estimates.

For the new estimation, it has its own esti and compute specs, which are specified in combo_type's 1st to the 4th
element. Only the 5th element contains information from the previous mpoly run.
"""

import parameters.loop_param_combo_list.loops_gen_json as paramloop_json
import parameters.runspecs.get_compesti_specs as param_compestispecs
import projectsupport.hardcode.string_shared as hardstring
import parameters.parse_combo_type as parsecombotype
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='parameters',
                                     subsub_folder_name='param_combo',
                                     file_name='fs_combo_list_auto_json',
                                     it_time_format=8, log_level=logging.INFO)
print(spn_log)

"""
SPECKEY MPOLY and POSTMPOLY
"""

# Already used for estimation
dc_speckey_mpoly = {'compute_spec_key': 'mpoly_1',
                    'esti_spec_key': 'esti_tinytst_mpoly_13',
                    'moment_key': 3,
                    'momset_key': 3}

# Not used yet for estimation, estimating now
dc_speckey_postmpoly = {'compute_spec_key': 'ng_s_t',
                        'esti_spec_key': 'esti_mplypostesti_13',
                        'moment_key': 3,
                        'momset_key': 3}

# see: parameters.paramset.combo_list_e_main.get_combo_list
st_common_subtype = '20201025'

for it_esti_top_which in [1,2]:
    # Mpoly estimation speckey info
    # compesti_short_name = "C1E21M3S3"
    compesti_short_name = hardstring.gen_compesti_short_name(**dc_speckey_mpoly)

    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info('A. ' + f'{it_esti_top_which=}')
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    # ls_combo_list is a list of dicts, each dict is a param_combo that generates one simulation
    # combo_type[4] looks liek: C1E21M3S3=1
    combo_type_e = parsecombotype.parse_combo_type_e(compesti_short_name=compesti_short_name,
                                                     esti_top_which=it_esti_top_which)
    ls_combo_list = paramloop_json.combo_list_auto(
        combo_type=[
            "e",
            "20201025x_esr_list_tKap_mlt_ce1a2",
            [
                "esti_param.kappa_ce9901", "esti_param.kappa_ce0209"
            ],
            None,
            parsecombotype.parse_combo_type_e(compesti_short_name=compesti_short_name,
                                              esti_top_which=it_esti_top_which)
        ],
        compesti_specs=param_compestispecs.get_compesti_specs_aslist(**dc_speckey_postmpoly),
        grid_f='a', grid_t=st_common_subtype,
        esti_f='a', esti_t=st_common_subtype,
        data_f='a', data_t=st_common_subtype,
        model_f='a', model_t=st_common_subtype,
        interpolant_f='a', interpolant_t=st_common_subtype,
        dist_f='a', dist_t=st_common_subtype,
        minmax_f='a', minmax_t=st_common_subtype)
