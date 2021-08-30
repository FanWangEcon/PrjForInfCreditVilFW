"""
Created on oct 29, 2020

@author: fan

generate combo_type
"""

import parameters.loop_param_combo_list.loops_gen as paramloop
import parameters.runspecs.get_compesti_specs as param_compestispecs
import projectsupport.systemsupport as proj_sys_sup
import pyfan.devel.flog.logsupport as pyfan_logsup
import logging

# Initiate Log
spn_log = pyfan_logsup.log_vig_start(spt_root=proj_sys_sup.main_directory(),
                                     main_folder_name='logvig', sub_folder_name='parameters',
                                     subsub_folder_name='param_combo',
                                     file_name='fs_combo_list_auto',
                                     it_time_format=8, log_level=logging.INFO)
print(spn_log)

"""
When paramloop.combo_list_auto is called, the first and second element of combo_type do not matter
any more, they were relevant to when calling parameters.combo.get_combo in order to call 
parameters.loop_param_combo_list.loops_gen.combo_list_auto. However, here, we are testing 
parameters.loop_param_combo_list.loops_gen.combo_list_auto directly. 

so below, just testing out how the ST_COMMON_SUBTYPE and DC_SPECKEY matter for generate a list
of param_combos, which is called a combolist

Get compute_spec_key names from parameters.loop_combo_type_list.param_str_simu.param2str_groups_simu

ng_s_t: has "compute_param_vec_count": 3, given two parameters will be 3 by 3, 9 combinations
esti_test_11_simu: has simu at the end, so only moment and momset
esti_test_11: no simu at the end, so only other estimation parameters, including esti_param_vec_count

COMPUTE_PARAM_VEC_COUNT vs ESTI_PARAM_VEC_COUNT:
- ESTI_PARAM_VEC_COUNT: if this is specified will be drawing parameters from within some min and max bounds, randomly.
If len(combo_type[2]) > 1, will draw parameters jointly ESTI_PARAM_VEC_COUNT times. 
- COMPUTE_PARAM_VEC_COUNT: if ESTI_PARAM_VEC_COUNT key does not exist, then draw even ordered grid or meshed grid 
over multiple parameters. If len(combo_type[2]) > 1, total simulations is COMPUTE_PARAM_VEC_COUNT*len(combo_type[2]).

When "compute_param_vec_count" is specified 

see: vig/parameters/combo_type/fs_gen_combo_type_list.py:13
see: vig/parameters/compesti_specs/fs_get_compesti_specs.py:8 
"""
# see: parameters.paramset.combo_list_e_main.get_combo_list
st_common_subtype = '20201025'

esti_spec_key = 'esti_test_11'
for st_esti_simu in ['Simulation', 'Estimation']:

    dc_speckey = {'compute_spec_key': 'ng_s_t',
                  'esti_spec_key': esti_spec_key,
                  'moment_key': 2,
                  'momset_key': 3}

    st_sec = 'B'
    if st_esti_simu == 'Simulation':
        st_sec = 'A'
        dc_speckey['esti_spec_key'] = esti_spec_key + '_simu'

    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info(st_sec + '1. ' + st_esti_simu + ' Call Ordered Grid, One Parameter')
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    # ls_combo_list is a list of dicts, each dict is a param_combo that generates one simulation
    ls_combo_list = paramloop.combo_list_auto(
        combo_type=[
            "x_doesnotmatter",
            "2020XXXX_doesnotmatter",
            [
                "esti_param.rho"
            ],
            None
        ],
        compesti_specs=param_compestispecs.get_compesti_specs_aslist(**dc_speckey),
        grid_f='a', grid_t=st_common_subtype,
        esti_f='a', esti_t=st_common_subtype,
        data_f='a', data_t=st_common_subtype,
        model_f='a', model_t=st_common_subtype,
        interpolant_f='a', interpolant_t=st_common_subtype,
        dist_f='a', dist_t=st_common_subtype,
        minmax_f='a', minmax_t=st_common_subtype)

    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info(st_sec + '2. ' + st_esti_simu + ' Call Ordered Grid, One Parameter, 2nd element only')
    logging.info('this would solve at the 2nd element only')
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    # ls_combo_list is a list of dicts, each dict is a param_combo that generates one simulation
    ls_combo_list = paramloop.combo_list_auto(
        combo_type=[
            "x_doesnotmatter",
            "2020XXXX_doesnotmatter",
            [
                "esti_param.rho"
            ],
            2
        ],
        compesti_specs=param_compestispecs.get_compesti_specs_aslist(**dc_speckey),
        grid_f='a', grid_t=st_common_subtype,
        esti_f='a', esti_t=st_common_subtype,
        data_f='a', data_t=st_common_subtype,
        model_f='a', model_t=st_common_subtype,
        interpolant_f='a', interpolant_t=st_common_subtype,
        dist_f='a', dist_t=st_common_subtype,
        minmax_f='a', minmax_t=st_common_subtype)

    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info(st_sec + '3. ' + st_esti_simu + ' Call Ordered Grid Two Parameters')
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    # ls_combo_list is a list of dicts, each dict is a param_combo that generates one simulation
    ls_combo_list = paramloop.combo_list_auto(
        combo_type=[
            "x_doesnotmatter",
            "2020XXXX_doesnotmatter",
            [
                "esti_param.beta",
                "esti_param.rho"
            ],
            None
        ],
        compesti_specs=param_compestispecs.get_compesti_specs_aslist(**dc_speckey),
        grid_f='a', grid_t=st_common_subtype,
        esti_f='a', esti_t=st_common_subtype,
        data_f='a', data_t=st_common_subtype,
        model_f='a', model_t=st_common_subtype,
        interpolant_f='a', interpolant_t=st_common_subtype,
        dist_f='a', dist_t=st_common_subtype,
        minmax_f='a', minmax_t=st_common_subtype)

    logging.info('\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info(st_sec + '4. ' + st_esti_simu + ' Call Ordered Grid, Two Parameter, 2nd element only,')
    logging.info('this would solve at the 2nd element only')
    logging.info('\nXXXXXXXXXXXXXXXXXXXXXXXXX')
    # ls_combo_list is a list of dicts, each dict is a param_combo that generates one simulation
    ls_combo_list = paramloop.combo_list_auto(
        combo_type=[
            "x_doesnotmatter",
            "2020XXXX_doesnotmatter",
            [
                "esti_param.beta",
                "esti_param.rho"
            ],
            2
        ],
        compesti_specs=param_compestispecs.get_compesti_specs_aslist(**dc_speckey),
        grid_f='a', grid_t=st_common_subtype,
        esti_f='a', esti_t=st_common_subtype,
        data_f='a', data_t=st_common_subtype,
        model_f='a', model_t=st_common_subtype,
        interpolant_f='a', interpolant_t=st_common_subtype,
        dist_f='a', dist_t=st_common_subtype,
        minmax_f='a', minmax_t=st_common_subtype)
