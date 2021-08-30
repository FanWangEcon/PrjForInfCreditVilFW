'''
@author: fan

specific *point* invoke structure, copying largely from b_FC
'''

import numpy as np

import parameters.loop_param_combo_list.loops_gen as paramloops


def get_combo_list(combo_type=['e', '20200901'], compesti_specs=None):
    """
    For ITG integration problems, do not specify each element to be integrated over as
    as param_combo in param_list. These will be auto-generated for each param_combo
    that is contained in the param_list by
    `solusteady.simu_integrate_loop.gen_integrate_param_list`.

    For GE problems, do not specify each interest rate to be looped over during
    bisection as param_combo in param_list. These will be auto-generated for each
    param_combo that is contained in the param_list by
    `soluequi/param_loop_r_loop.py:331` inside function
    `soluequi.param_loop_r_loop.demand_supply_interest`.

    For GE + ITG, first proceeds as GE in description above, and then it will detect
    ITG and use the ITG step described above. So GE + ITG solution at a particular
    combination of parameters is one element in the param_list. In another word,
    the GE and ITG related parameters do not need to be specified as varying elements of
    the param_list loop. However, they could be specified as such, if they are,
    should not add ITG substring to combo_type[1] string. GE is specified as a
        parameter for the run function directly, `invoke

    Parameters
    ----------
    compesti_specs : dict
        see `parameters.combo.gen_compesti_spec` for example for `compesti_specs`.
    """

    module = combo_type[0]
    sub_type = combo_type[1]

    if "20181025" in sub_type:
        """
        20180801 re-testing model, borrowing and savings

        - for integration, needs dist_type, otherwise even add _ITG_ does not integrate
        - need to specify minmax_type, even when no grid, otherwise graph for parameters does not work.

        """
        int_rate_counts = 1
        min_int = 1.05
        max_int = 1.05
        A = 0.25
        std = 0.75
        interpolant_type = ['a', 11, {'maxinter': 15}]

        combo_list = \
            [{'param_update_dict': {'grid_type': ['a', 20200801,
                                                  {'std_eps': std, 'std_eps_E': std}],
                                    'esti_type': ['a', 20180512,
                                                  {'R_INFORM_SAVE': cur_rate,
                                                   'R_INFORM_BORR': cur_rate}],
                                    'data_type': ['b', 20180512,
                                                  {'A': A - ((std ** 2) / 2), 'Region': 0,
                                                   'Year': 0}],
                                    'model_type': ['a', 1],
                                    'dist_type': ['a', 20200801, {'epsA_frac_A': 0.15}],
                                    'minmax_type': ['a', 20180801],
                                    'interpolant_type': interpolant_type,
                                    'support_arg': {}},
              'title': 'Borrow Save Testing ' + str(int(cur_rate * 100)) + ', A=' + str(
                  A) + ',S=' + str(std) + ')',
              'combo_desc': 'Borrow Save Testing' + str(int(cur_rate * 100)),
              'file_save_suffix': '_i15r' + str(int(cur_rate * 100)) + 'A' + str(
                  int(A * 100)) + 's' + str(
                  int(std * 100))}
             for cur_rate in np.linspace(min_int, max_int, num=int_rate_counts)]

    main_type_str_list = ['20201025']
    if any([main_type_str in sub_type for main_type_str in main_type_str_list]):

        # A. Invocation precision, changing grid tyep and interpolant types
        if any([main_type_str + 'x' in sub_type for main_type_str in main_type_str_list]):
            st_common_subtype = '20201025x'
        elif any([main_type_str + 'd' in sub_type for main_type_str in
                  main_type_str_list]):
            st_common_subtype = '20201025d'
        else:
            st_common_subtype = '20201025'

        # B. Integrate or not
        if "_ITG_" in sub_type:
            dist_t = st_common_subtype
        else:
            dist_t = None

        # C. Model type
        if "_1j7" in sub_type:
            model_t = '20181011'
        elif "_1ja7" in sub_type:
            # 1j7 does not work, 1ja7 approximates 1j7 by making fixed cost very high
            # for saving option
            model_t = '20181013j16'
        elif "_2j127" in sub_type:
            model_t = '20181013j016'
        elif "_5j12347" in sub_type:
            model_t = '20180613'
        elif "_7jAll" in sub_type:
            model_t = '20180701'
        else:
            raise Exception('bad _j12347 etc not in sub_type')

        # D. Generate list of param combos and create combo_list
        if len(combo_type) >= 3 and combo_type[2] is not None:
            combo_list = paramloops.combo_list_auto(
                combo_type=combo_type,
                compesti_specs=compesti_specs,
                minmax_f='a', minmax_t=minmax_t,
                data_f='a', data_t='20180607',
                esti_f='a', esti_t='20180815',
                model_f='a', model_t=model_t,
                grid_f='a', grid_t=st_common_subtype,
                interpolant_f='a', interpolant_t=st_common_subtype,
                dist_f='a', dist_t=dist_t)
        else:
            # support_arg below will be filled out by other functions with string other
            # calibration and estimation information.
            combo_list = \
                [{'param_update_dict': {'model_type': ['a', model_t],
                                        'grid_type': ['a', st_common_subtype],
                                        'esti_type': ['a', st_common_subtype],
                                        'data_type': ['b', st_common_subtype],
                                        'dist_type': ['a', dist_t],
                                        'interpolant_type': ['a', st_common_subtype],
                                        'support_arg': {}},
                  'title': '20201025 Single Simu',
                  'combo_desc': 'Base Combo 20201025',
                  'file_save_suffix': ''}]

    return combo_list
