'''
@author: fan
'''
import logging
import pyfan.amto.lsdc.lsdcconvert as pyfan_amto_lsdcconvert
import random

import parameters.model.a_model as param_model_a
import parameters.paramset.combo_list_a as combo_a
import parameters.paramset.combo_list_b_FC as combo_b_FC
import parameters.paramset.combo_list_c_esti as combo_c_esti
import parameters.paramset.combo_list_d_bench as combo_d_bench
import parameters.paramset.combo_list_e_main as combo_e_main
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def gen_combo_list_one_elemnt(it_default_group=None, **kwargs):
    """A Dictionary of All Model Parameters in Combo_list form

    Model parameters can be modified as a part of combo_list. Here, modify all
    possible parameters via combo_list. This way, can easily change any model
    parameters. And the way to specify each parameter is clarified and made
    transparent.

    Parameters
    ----------
    it_default_group : int, optional
        Change values for keys
    **kwargs
        A dictionary of key-value paris to update/replace or append to the existing
        dictionaries.

    Returns
    -------
    dict
        An updated dictionary of key value pairs for combo_list specifications.
    """

    # A. Default Grid Parameters
    std = 0.5
    std_eps = std
    mean_eps = (-1) * ((std ** 2) / 2)
    std_eps_E = std
    mean_eps_E = mean_eps
    grid_param_default = {
        'len_k_start': 50,
        'len_states': 2500,
        'len_choices': 900,
        'shape_choice': {'type': 'broadcast', 'shape': [2500, 900], 'row': 2500, 'col': 900},
        'min_steady_coh': 0,
        'max_steady_coh': 50,
        'std_eps': std_eps,
        'mean_eps': mean_eps,
        'std_eps_E': std_eps_E,
        'mean_eps_E': mean_eps_E,
        'max_kapital': 50,
        'max_netborrsave': 50,
        'grid_zoom_rounds': 2,
        'markov_points': 200,
        'BNF_SAVE_P_startVal': 0,
        'BNF_BORR_P_startVal': -0,
        'BNI_LEND_P_startVal': 0,
        'BNI_BORR_P_startVal': -0,
    }

    # B. Default Estimate Parameters
    esti_param_default = {
        'rho': 1,
        'beta': 0.96,
        'alpha_k': 0.36,
        'K_DEPRECIATION': 0.15,
        'logit_sd_scale': 1,
        'BNF_SAVE_P': 0,
        'BNF_BORR_P': 0,
        'BNI_LEND_P': 0,
        'BNI_BORR_P': 0,
        'kappa': 0.25,
        'R_INFORM_SAVE': 1.15,
        'R_INFORM_BORR': 1.15,
        'R_FORMAL_SAVE': 1.02,
        'R_FORMAL_BORR': 1.05,
        'R_AVG_INT': 1.10
    }

    # C. Data Type
    A = 0.25
    std = 0.75
    data_param_default = {
        'mean_A': A - ((std ** 2) / 2),
        'std_A': 0,
        'len_A': 1,
        'A': A - ((std ** 2) / 2),
        'Region': 0,
        'Year': 0
    }

    # D. Model Type
    model_param_default = {
        'VFI_type': 'infinite',
        'choice_set_list': [0, 1, 102, 3, 104, 105, 6],
    }

    # E. Interpolant Type
    bktp_geom_dict_null = param_model_a.choice_index_names()['bktp_geom_dict']
    interpolant_param_default = {
        'interp_type': ['forgegeom'],
        'interp_type_option': {'method': 'linear'},
        'maxinter': 30,
        'econforge_interpolant': None,
        'interp_EV_k_b': {'B_Vepszr_square_max': None,
                          'B_Vepszr_square_min': None,
                          'K_Vepszr_square_max': None,
                          'K_Vepszr_square_min': None,
                          'start': 0,
                          'stop': 1,
                          'geom_ratio': 1.03},
        'bktp_geom': bktp_geom_dict_null,  # have to specify all possible
        'pre_save': True
    }

    # F. Distribution type
    data__A_dict = {'dist': 'normal',
                    'params': {'mu': 0.25 - (0.75 ** 2) / 2,
                               'sd': 0.25},
                    'integrate': {'method': 'grid', 'params': {'points': 10}}
                    }
    dist_param_default = {'data__A': data__A_dict,
                          'epsA_frac_A': 0.5,
                          'epsA_std': 0.5}

    # G. Min Max groups

    '''
    Generate a long list of random integers
    '''
    random.seed(123)
    seeds = random.sample(range(100, 1000), 100)
    esti_type_minmax = {
        'alpha_k': [0.15, 0.75, seeds[0]],
        'beta': [0.88, 0.98, seeds[1]],
        'K_DEPRECIATION': [0.05, 0.17, seeds[2]],
        'rho': [1.1, 1.5, seeds[3]],
        'logit_sd_scale': [0.8, 2.0, seeds[4]],
        'R_INFORM_SAVE': [1.0, 1.20, seeds[5]],
        'R_FORMAL_SAVE': [0.90, 2.00, seeds[11]],
        'R_FORMAL_BORR': [0.95, 1.15, seeds[12]],
        'BNF_SAVE_P': [0, 1.5, seeds[6]],
        'BNF_BORR_P': [0, 3.5, seeds[7]],
        'BNI_LEND_P': [0, 3.5, seeds[8]],
        'BNI_BORR_P': [0, 3.5, seeds[9]],
        'kappa': [0.10, 0.70, seeds[10]]
    }
    data_type_minmax = {
        'A': [-0.65, 1, seeds[13]]
    }
    grid_type_minmax = {
        'BNF_SAVE_P_startVal': [0, 3, seeds[14]],
        'BNF_BORR_P_startVal': [-0.0, -3.0, seeds[15]],
        'BNI_LEND_P_startVal': [0, 3, seeds[16]],
        'BNI_BORR_P_startVal': [-0.0, -3.0, seeds[17]],
        'std_eps': [0.2, 2.0, seeds[18]],
        'max_steady_coh': [50, 450, 9393],
        'markov_points': [20, 300, 9394]
    }
    dist_type_minmax = {
        'data__A.params.mu': [-0.65, 0.65, seeds[19]],
        'data__A.params.sd': [0.10, 1.00, seeds[20]],
        'esti__BNF_SAVE_P.params.max': [1.5, 2.5, seeds[21]],
        'epsA_frac_A': [0.05, 0.95, seeds[22]],
        'epsA_std': [0.2, 2.0, seeds[23]],
        'std_eps': [0.2, 2.0, seeds[24]],
    }
    minmax_param_default = {
        'esti_type': esti_type_minmax,
        'data_type': data_type_minmax,
        'grid_type': grid_type_minmax,
        'dist_type': dist_type_minmax
    }

    # The Parameters together
    dc_param_combo = {
        "param_update_dict": {
            "grid_type": ["a", "20181024", grid_param_default],
            "esti_type": ["a", "20180815", esti_param_default],
            "data_type": ["a", "20180607", data_param_default],
            "model_type": ["a", "20180701", model_param_default],
            "interpolant_type": ["a", "20180607", interpolant_param_default],
            "dist_type": ["a", "NONE", dist_param_default],
            "minmax_type": ["a", "20180925", minmax_param_default],
            "support_arg": {
                "cpu": "1024",
                "memory": "517",
                "workers": 1,
                "compute_param_vec_count": 14,
                "aws_fargate": False,
                "ge": False,
                "multiprocess": False,
                "graph": True,
                "esti_method": "MomentsSimuStates",
                "moments_type": [
                    "a",
                    "20180805a"
                ],
                "momsets_type": [
                    "a",
                    "20180805a"
                ],
                "esti_option_type": 1,
                "esti_func_type": "L-BFGS-B",
                "param_grid_or_rand": "rand",
                "esti_param_vec_count": 1,
                "esti_max_func_eval": 10,
                "graph_frequncy": 20,
                "param_combo_list_ctr_str": "_c0"
            }
        },
        "title": "Default Parameters",
        "combo_desc": "Default Parameters",
        "esti_method": "MomentsSimuStates",
        "moments_type": ["a", "20180805a"],
        "momsets_type": ["a", "20180805a"],
        "esti_option_type": 1,
        "esti_func_type": "L-BFGS-B",
        "param_grid_or_rand": "rand",
        "esti_param_vec_count": 1,
        "param_combo_list_ctr_str": "_c0",
        "file_save_suffix": "_20180925_c0_alpk2386"
    }

    combo_list = [dc_param_combo]

    # C. Update dictionaries with parameter group values
    if it_default_group == 1:
        pass
        # combo_list = [dc_param_combo]

    return combo_list


def gen_compesti_spec(it_default_group=None, **kwargs):
    """A dictionary of all esti and compute parameters

    parameters.runspecs.compute_specs.compute_set specifies compute_specs.
    parameters.runspecs.estimate_specs.estimate_set_gen specifies esti_specs.
    This function provides a list of the possible keys and sample value pairs
    for esti and compute specs. Some explanations are provided here for what
    each of the key specifies and where it is used.

    Parameters
    ----------
    it_default_group : int, optional
        Change values for keys
    **kwargs
        A dictionary of key-value paris to update/replace or append to the existing
        dictionaries.

    Returns
    -------
    dict
        An updated dictionary of key value pairs for compesti specifications.
    """

    # A. Define the default parameter keys and values
    esti_specs = {'esti_method': 'MomentsSimuStates',
                  'moments_type': ['a', '20180805a'],
                  'momsets_type': ['a', '20180805a'],
                  'esti_option_type': 1,
                  'esti_func_type': 'L-BFGS-B',
                  'param_grid_or_rand': 'rand',
                  'esti_param_vec_count': 1,
                  'esti_max_func_eval': 10,
                  'graph_frequncy': 20}

    compute_specs = {'cpu': str(1024 * 1),
                     'memory': str(517),  # only need about 160 mb in reality
                     'workers': 1,
                     'int_rate_counts': 4,
                     'bisection_iter': 3,
                     'compute_param_vec_count': 14,
                     'aws_fargate': False,
                     'ge': False,
                     'multiprocess': False,
                     'graph': True}

    # B. For different
    compesti_specs = {**compute_specs, **esti_specs}

    # C. Update dictionaries with parameter group values
    if it_default_group == 1:
        compesti_specs_updates = {'memory': str(1024 * 55),
                                  'compute_param_vec_count': 6,
                                  'esti_param_vec_count': 640}
        compesti_specs.update(compesti_specs_updates)

    # D. Update with kward, could append new
    compesti_specs.update(kwargs)

    return compesti_specs


def gen_file_save_suffix(param_update_dict, fiel_save_suffix_more,
                         combo_name_only=True, combo_name=''):
    grid_type = param_update_dict['grid_type']
    esti_type = param_update_dict['esti_type']
    data_type = param_update_dict['data_type']
    model_type = param_update_dict['model_type']
    interpolant_type = param_update_dict['interpolant_type']

    if (combo_name_only):
        file_save_suffix = '_' + combo_name + fiel_save_suffix_more
    else:
        file_save_suffix = '_G' + grid_type[0] + str(grid_type[1]) + \
                           'E' + esti_type[0] + str(esti_type[1]) + \
                           'M' + model_type[0] + str(model_type[1]) + \
                           'I' + interpolant_type[0] + str(interpolant_type[1]) + \
                           'D' + data_type[0] + fiel_save_suffix_more

    return file_save_suffix


def get_combo(combo_type=None, compesti_specs=None):
    """
    Parameters
    ----------
    compesti_specs: dictionary
        this is either compute_spec alone, or this is compute_spec + esti_spec for
        run_estimate invokes.
    """
    if (combo_type is not None):
        logger.info('combo_type:%s\n', combo_type)

        if (combo_type[0] == 'a'):
            combo_list = combo_a.get_combo_list(combo_type, compesti_specs)
        if (combo_type[0] == 'b'):
            combo_list = combo_b_FC.get_combo_list(combo_type, compesti_specs)
        if (combo_type[0] == 'c'):
            # compute_esti_specs should include compute_specs + esti_specs, if no esti_specs, defaults used
            combo_list = combo_c_esti.get_combo_list(combo_type, compesti_specs)
        if (combo_type[0] == 'd'):
            # compute_esti_specs should include compute_specs + esti_specs, if no esti_specs, defaults used
            combo_list = combo_d_bench.get_combo_list(combo_type, compesti_specs)
        if combo_type[0] == 'e':
            combo_list = combo_e_main.get_combo_list(combo_type, compesti_specs)

    # combo_type convert to dict to be stored in support_arg
    dc_combo_type = pyfan_amto_lsdcconvert.ff_ls2dc(combo_type)

    # Update file Save String Name
    for ctr, param_combo in enumerate(combo_list):
        param_update_dict = param_combo['param_update_dict']
        file_save_suffix = param_combo['file_save_suffix']
        file_save_suffix = gen_file_save_suffix(param_update_dict, file_save_suffix,
                                                combo_name_only=True,
                                                combo_name=combo_type[1])
        combo_list[ctr]['file_save_suffix'] = file_save_suffix

        '''
        Add compesti_specs to support_arg of combo
        '''
        if ('support_arg' in combo_list[ctr]['param_update_dict']):
            if compesti_specs is not None:
                combo_list[ctr]['param_update_dict']['support_arg'].update(compesti_specs)
        else:
            if compesti_specs is not None:
                combo_list[ctr]['param_update_dict']['support_arg'] = compesti_specs

        combo_list[ctr]['param_update_dict']['support_arg'].update(dc_combo_type)

        if ('param_combo_list_ctr_str' in combo_list[ctr].keys()):
            combo_list[ctr]['param_update_dict']['support_arg']['param_combo_list_ctr_str'] = \
                combo_list[ctr]['param_combo_list_ctr_str']

    proj_sys_sup.jdump(combo_list, 'get_combo_list', logger=logger.info)

    return combo_list
