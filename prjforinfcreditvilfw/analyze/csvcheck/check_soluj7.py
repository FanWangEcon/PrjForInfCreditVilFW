"""
The :mod:`prjforinfcreditvilfw.analyze.csvcheck.check_soluj7` checks where solutions
of the household optimization problem satisfy expected conditions.

Includes method :func:`load_and_save`, :func:`get_data_columns`, :func:`test_constraint_formal_collatral`, 

:func:`test_positive_consumption`, :func:`get_subset_table`, :func:`check_ibfbis`
"""

import numpy as np
import pandas as pd

import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup


def load_and_save(load=False, save=False, save_data=None, save_suffix='_morestats'):
    '''
    Import file and save file function
    '''
    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/simu/b_20180702_Aprd/csv_exo/'
    param_combo = '20180702_Aprd_A_10000'

    file_name_prefix = 'solu_' + param_combo + ''
    if (load):
        file_name = file_name_prefix + '.csv'
        csv_file_folder = directory + '/' + file_name
        solu_opti_pd = proj_sys_sup.read_csv(csv_file_folder)

        return solu_opti_pd

    if (save):
        file_name = file_name_prefix + save_suffix + '.csv'
        saveFileDirectory = directory + '/' + file_name
        proj_sys_sup.save_panda(saveFileDirectory, save_data, is_panda=True, s3=False)


def get_data_columns(solu_opti_pd):
    '''
    column names
    '''
    solu_var_suffixes = hardstring.get_solu_var_suffixes()
    choice_names = param_model_a.choice_index_names()['choice_names']

    '''
    For each pair of Kn and Bn, generate kappa fraction of Kn
    '''
    bn_cols = [col for col in solu_opti_pd.columns
               if ((solu_var_suffixes['btp_opti'] in col)
                   and (solu_var_suffixes['btp_opti'] + '_' not in col)
                   )]
    kn_cols = [col for col in solu_opti_pd.columns if solu_var_suffixes['ktp_opti'] in col]
    cc_cols = [col for col in solu_opti_pd.columns if solu_var_suffixes['consumption_opti'] in col]

    btp_matrix = solu_opti_pd[bn_cols].to_numpy()
    ktp_matrix = solu_opti_pd[kn_cols].to_numpy()
    ccc_matrix = solu_opti_pd[cc_cols].to_numpy()

    cash_col = np.reshape(solu_opti_pd[solu_var_suffixes['cash']], (-1, 1))

    '''
    Return Dictionary
    '''
    out_matrix = {'btp_matrix': btp_matrix, 'ktp_matrix': ktp_matrix, 'ccc_matrix': ccc_matrix,
                  'cash': cash_col}
    out_col_name_lists = {'bn_cols': bn_cols, 'kn_cols': kn_cols, 'cc_cols': cc_cols}

    return out_matrix, out_col_name_lists


def test_constraint_formal_collatral(kappa=0.25):
    solu_opti_pd = load_and_save(load=True, save=False)
    out_matrix, out_col_name_lists = get_data_columns(solu_opti_pd)

    ktp_matrix_maxborr = (-1) * out_matrix['ktp_matrix'] * kappa

    '''
    For fraction of Kn, generate if Bn is below or above, and then summarize
    '''
    # btp_exceed_index = np.zeros(np.shape(btp_matrix))
    btp_exceed_max = (out_matrix['btp_matrix'] < ktp_matrix_maxborr)
    # btp_exceed_max = (btp_matrix < ktp_matrix_maxborr)
    np.sum(btp_exceed_max)

    '''
    Add matrix to existing panda file
    '''
    kn_kappa_cols = ['kap ' + strn for strn in out_col_name_lists['kn_cols']]
    bn_exceed_col = ['exceed ' + strn for strn in out_col_name_lists['bn_cols']]

    # Convert matrix to panda dataframe
    varnames = ",".join(map(str, kn_kappa_cols)) + ',' + ",".join(map(str, bn_exceed_col))
    varmat = np.column_stack((ktp_matrix_maxborr, btp_exceed_max))
    solu_data_newcols_pd = proj_sys_sup.debug_panda(varnames, varmat,
                                                    save_directory=False,
                                                    filename='',
                                                    time_suffix=False, export_panda=False, log=False)

    # Combine with old
    solu_opti_pd_morestats = pd.concat([solu_opti_pd, solu_data_newcols_pd], axis=1)

    solu_opti_pd = load_and_save(load=False, save=True, save_data=solu_opti_pd_morestats, save_suffix='_morestats')


def test_positive_consumption(kappa=0.25, save=True):
    """
    Given COH, is optimal choice exceeding feasible choice range?
    Really this is asking if the feasible choice range constructed has weird values
    that are beyond feasible.

    """
    solu_opti_pd = load_and_save(load=True, save=False)
    out_matrix, out_col_name_lists = get_data_columns(solu_opti_pd)

    '''
    Check Consumption
    '''
    # should use j specific rate, but to
    check_c_negative = True
    if (check_c_negative):
        btp_matrix = out_matrix['btp_matrix']

    btp_matrix_principle = np.zeros(np.shape(btp_matrix))
    any_r_max_borr = 1.05
    btp_matrix_principle[btp_matrix < 0] = btp_matrix[btp_matrix < 0] / any_r_max_borr
    any_r_max_save = 1.08
    btp_matrix_principle[btp_matrix > 0] = btp_matrix[btp_matrix > 0] / any_r_max_save

    bkn_max_c = (out_matrix['cash'] - out_matrix['ktp_matrix'] - btp_matrix_principle)
    #         bkn_max_c = (out_matrix['cash'] - out_matrix['ktp_matrix'] - btp_matrix)
    c_negative = (bkn_max_c < -0.01)

    ktp_matrix_maxborr = (-1) * out_matrix['ktp_matrix'] * kappa

    '''
    For fraction of Kn, generate if Bn is below or above, and then summarize
    '''
    # btp_exceed_index = np.zeros(np.shape(btp_matrix))
    btp_exceed_max = (out_matrix['btp_matrix'] < ktp_matrix_maxborr)
    # btp_exceed_max = (btp_matrix < ktp_matrix_maxborr)
    np.sum(btp_exceed_max)

    '''
    Add matrix to existing panda file
    '''
    kn_kappa_cols = ['kap ' + strn for strn in out_col_name_lists['kn_cols']]
    bn_exceed_col = ['exceed ' + strn for strn in out_col_name_lists['bn_cols']]
    bkn_max_c_col = ['bkn_max_c ' + strn for strn in out_col_name_lists['bn_cols']]
    c_neg_col = ['cneg ' + strn for strn in out_col_name_lists['bn_cols']]

    # Convert matrix to panda dataframe
    varnames = ",".join(map(str, kn_kappa_cols)) + ',' + \
               ",".join(map(str, bn_exceed_col)) + ',' + \
               ",".join(map(str, bkn_max_c_col)) + ',' + \
               ",".join(map(str, c_neg_col))

    varmat = np.column_stack((ktp_matrix_maxborr, btp_exceed_max, bkn_max_c, c_negative))
    solu_data_newcols_pd = proj_sys_sup.debug_panda(varnames, varmat,
                                                    save_directory=False,
                                                    filename='',
                                                    time_suffix=False,
                                                    export_panda=False, log=False)

    # Combine with old
    solu_opti_pd_morestats = pd.concat([solu_opti_pd, solu_data_newcols_pd], axis=1)

    if (save):
        load_and_save(load=False, save=True, save_data=solu_opti_pd_morestats, save_suffix='_morestats')

    return solu_opti_pd_morestats


def get_subset_table(save_suffix='_is_fbis2'):
    #     test_constraint_formal_collatral()
    """
    Too many choices, too many columns, hard to read, generate a table with just columns from one of the choices
    """

    #     solu_opti_pd_morestats = load_and_save(load=True, save=False)

    '''
    A. Get all columns with collateral binding or not columns appended
    '''
    solu_opti_pd_morestats = test_positive_consumption(kappa=0.25,
                                                       save=True)

    '''
    B. Grab out only FBIS columns
    '''
    solu_var_suffixes = hardstring.get_solu_var_suffixes()
    choice_names = param_model_a.choice_index_names()['choice_names']

    #     solu_opti_pd = load_and_save(load=True)

    if (save_suffix == '_fb'):
        select_cols = [col for col in solu_opti_pd_morestats.columns
                       if ((choice_names[102] in col)
                           and (choice_names[104] not in col)
                           and (choice_names[105] not in col)
                           )]

    if (save_suffix == '_is_fbis2'):
        select_cols = [col for col in solu_opti_pd_morestats.columns
                       if (((choice_names[105] in col) or (choice_names[1] in col))
                           and (choice_names[102] not in col)
                           and (choice_names[104] not in col)
                           )]

    if (save_suffix == '_fbis2'):
        select_cols = [col for col in solu_opti_pd_morestats.columns
                       if choice_names[105] in col]

    fbis_cols = [solu_var_suffixes['cash'],
                 solu_var_suffixes['k_tt'],
                 solu_var_suffixes['b_tt'],
                 solu_var_suffixes['eps_tt']] + select_cols
    solu_opti_pd_fbis = solu_opti_pd_morestats[fbis_cols]

    '''
    C. Save a table with just FBIS
    '''
    solu_opti_pd_fbis = solu_opti_pd_fbis.sort_values(by=[solu_var_suffixes['cash']])

    load_and_save(load=False, save=True, save_data=solu_opti_pd_fbis, save_suffix=save_suffix)


def check_ibfbis():
    """
    I do not want to store columns like 'bn_fb ibfb2' and 'bn_ib ibfb2', creates
    memory jump, takes too much space.

    so will only have 'kn ibfb2' and 'bn ibfb2', the point is to generate
    correct 'bn_fb ibfb2' and 'bn_ib ibfb2'from 'kn ..' and 'bn ..'

    For example:
        'bn ibfb2' = 'bn_fb ibfb2' + 'bn_ib ibfb2'
        then check, how to get
    """

    '''
    A. sum check, all choices
    '''

    full_choice_set_list = [0, 1, 102, 3, 104, 105, 6]

    solu_var_suffixes = hardstring.get_solu_var_suffixes()
    choice_names = param_model_a.choice_index_names()['choice_names']

    solu_opti_pd = load_and_save(load=True, save=False)

    # A1
    fbibfsil_list = ['btp_fb_opti', 'btp_ib_opti', 'btp_fs_opti', 'btp_il_opti']
    for cur_choice_j in full_choice_set_list:
        cur_fibs_col_name_list = []
        for cur_fibs in fbibfsil_list:
            cur_fibs_col_name = solu_var_suffixes[cur_fibs] + ' ' + choice_names[cur_choice_j]
            cur_fibs_col_name_list.append(cur_fibs_col_name)

        # A2 Current fibs 4 columns
        cur_fibs_mat = solu_opti_pd[cur_fibs_col_name_list]

        # A3 Sum up
        cur_fibs_mat_sum = np.sum(cur_fibs_mat, axis=1)

        # A4 get btp aggregate
        cur_btp = solu_opti_pd[solu_var_suffixes['btp_opti'] + ' ' + choice_names[cur_choice_j]]

        # A5 check for equality
        #         check_close = np.allclose(cur_fibs_mat_sum, cur_btp, atol=1e-05)
        not_equal_frac = (np.size(np.where(
            np.abs(cur_fibs_mat_sum - cur_btp) <= 1e-05
        ))) / np.size(cur_fibs_mat_sum)

        # Print results
        print(choice_names[cur_choice_j] + ': ' + str(not_equal_frac))

    '''
    B. Decompose check, can I go from bn to bn_for, bn_inf?
    '''


if __name__ == "__main__":
    #     check_ibfbis()
    get_subset_table(save_suffix='_is_fbis2')
