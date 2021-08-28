'''
Created on Sep 4, 2018

Generate a dataset with these variables based on simulation results

    each file needs to have:
        interestinf
        shr_inf_clone
        shr_for_clone
        shr_joint_clone
        shr_none_m_avg_clone

    Along these Five Parameter Dimensions:
    bnf_borr_p_r1 bnf_save_p_r1 kappa_r1 int_formal_borr int_formal_save

@author: fan
'''

import ast
import numpy as np
import pandas as pd

import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup


def gen_3dims_csv_fromcsv(simulate_csv_file_name,
                          simulate_csv_directory,
                          current_policy_column,
                          exo_or_endo_graph_row_select,
                          csv_name_suffix):
    """
    Examples
    --------
    import estimation.postprocess.gen_counter_3dims_data as gen_counter3dims
    simulate_csv_file_name = ''
    simulate_csv_directory = ''
    current_policy_column = ''
    exo_or_endo_graph_row_select = ''
    csv_name_suffix = ''
    gen_counter3dims.gen_3dims_csv_fromcsv(simulate_csv_file_name,
                          simulate_csv_directory,
                          current_policy_column, 
                          exo_or_endo_graph_row_select,
                          csv_name_suffix)
    """
    for_stata_save_file_name = gen_3dims_csv(simulate_csv_directory,
                                             simulate_csv_file_name,
                                             current_policy_column,
                                             simu_df=None,
                                             exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                             csv_name_suffix=csv_name_suffix)

    return for_stata_save_file_name


def gen_3dims_csv(simulate_csv_directory,
                  simulate_csv_file_name,
                  current_policy_column,
                  simu_df=None,
                  exo_or_endo_graph_row_select='_equ_wgtJ',
                  csv_name_suffix='_ctr3d'):
    """
    Examples
    --------
    import estimation.postprocess.gen_counter_3dims_data as gen_counter3dims
    simulate_csv_directory = ''
    simulate_csv_file_name = ''
    current_policy_column = ''
    gen_counter3dims.gen_3dims_csv(simulate_csv_directory,
                                   simulate_csv_file_name,
                                   current_policy_column)
    """

    simulate_csv_file_name_for_stata = simulate_csv_file_name + csv_name_suffix
    for_stata_save_file_name = simulate_csv_directory + simulate_csv_file_name_for_stata + '.csv'

    file_path = simulate_csv_directory + simulate_csv_file_name + '.csv'
    if (simu_df is None):
        simu_df = proj_sys_sup.read_csv(csv_file_folder=file_path)

    '''
    1. Include Only Wgt Main Results
    '''
    simu_df = simu_df[simu_df['file_save_suffix'].str.contains(exo_or_endo_graph_row_select) == True]

    '''
    2. Obtain columns for credit market choices
    '''
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    translate_jinja_name = param_model_a.choice_index_names()['translate_jinja_name']
    moment_csv_strs = hardstring.moment_csv_strs()

    choice_set_list = simu_df['model_option.choice_set_list'].iloc[0]
    choice_names_use = simu_df['model_option.choice_names_use'].iloc[0]
    if (isinstance(choice_set_list, list)):
        pass
    else:
        choice_names_use = ast.literal_eval(choice_names_use)
        choice_set_list = ast.literal_eval(choice_set_list)

    pf_col_name_dict = {}
    for ctr, j in enumerate(choice_set_list):
        jinja_j = translate_jinja_name[j]
        pf_col_name = choice_names_use[ctr] + '_' + \
                      steady_var_suffixes_dict['probJ_opti_grid'] + \
                      steady_agg_suffixes['_j_agg'][0]
        pf_col_name_dict[jinja_j] = pf_col_name

    #     print(pf_col_name_dict)

    '''
    3. Add add probabilities to go from 7 to 4
    '''
    shr_zeros = np.zeros(len(simu_df.index))
    if 'IB' in pf_col_name_dict:
        shr_inf = simu_df[pf_col_name_dict['IB']] + simu_df[pf_col_name_dict['IS']]
    else:
        shr_inf = shr_zeros
    if 'FB' in pf_col_name_dict:
        shr_for = simu_df[pf_col_name_dict['FB']] + simu_df[pf_col_name_dict['FS']]
    else:
        shr_for = shr_zeros
    if 'FBIB' in pf_col_name_dict:
        shr_joint = simu_df[pf_col_name_dict['FBIB']] + simu_df[pf_col_name_dict['FBIS']]
    else:
        shr_joint = shr_zeros
    if 'NONE' in pf_col_name_dict:
        shr_none_m_avg = simu_df[pf_col_name_dict['NONE']]
    else:
        shr_none_m_avg = shr_zeros

    '''
    4. Include Interest Rate Column and other column names
    '''
    R_INFORM = simu_df[moment_csv_strs['R_INFORM'][1]]
    BNF_SAVE_P = simu_df[moment_csv_strs['BNF_SAVE_P'][1]]
    BNF_BORR_P = simu_df[moment_csv_strs['BNF_BORR_P'][1]]
    kappa = simu_df[moment_csv_strs['kappa'][1]]
    R_FORMAL_SAVE = simu_df[moment_csv_strs['R_FORMAL_SAVE'][1]]
    R_FORMAL_BORR = simu_df[moment_csv_strs['R_FORMAL_BORR'][1]]

    '''
    5. Export: converting to stata do file graphing variable names
    '''
    simu_df['shr_inf'] = pd.Series(shr_inf, index=simu_df.index)
    simu_df['shr_for'] = pd.Series(shr_for, index=simu_df.index)
    simu_df['shr_joint'] = pd.Series(shr_joint, index=simu_df.index)
    simu_df['shr_none_m_avg'] = pd.Series(shr_none_m_avg, index=simu_df.index)
    simu_df['interestinf'] = pd.Series(R_INFORM, index=simu_df.index)

    simu_df['bnf_save_p_r1'] = pd.Series(BNF_SAVE_P, index=simu_df.index)
    simu_df['bnf_borr_p_r1'] = pd.Series(BNF_BORR_P, index=simu_df.index)
    simu_df['kappa_r1'] = pd.Series(kappa, index=simu_df.index)
    simu_df['int_formal_save'] = pd.Series(R_FORMAL_SAVE, index=simu_df.index)
    simu_df['int_formal_borr'] = pd.Series(R_FORMAL_BORR, index=simu_df.index)

    '''
    6. Export
    '''
    varkeep_list = ['bnf_save_p_r1', 'bnf_borr_p_r1', 'kappa_r1', 'int_formal_save', 'int_formal_borr',
                    'interestinf', 'shr_inf', 'shr_for', 'shr_joint', 'shr_none_m_avg']

    if (current_policy_column in varkeep_list):
        pass
    else:
        varkeep_list.insert(0, current_policy_column)

    counter_3dims = simu_df[varkeep_list]
    proj_sys_sup.save_panda(for_stata_save_file_name, counter_3dims)

    return for_stata_save_file_name
