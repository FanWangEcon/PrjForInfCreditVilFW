'''
Created on May 22, 2018

@author: fan

This deals with panda files that just has interest rate loop, all parameters
the same, except for interest rate differences
'''

import numpy as np

import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring


def get_demand_supply_vec(pd_file, wgt_or_max='_wgtJ'):
    """
    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/simu/a_20180517_A'
    file_name = '_20180517_A_A-650.csv'
    csv_file_folder = directory + '/' + file_name
    pdfile = proj_sys_sup.read_csv(csv_file_folder)
    """

    """
    0. Get Strings
    """
    choice_names = param_model_a.choice_index_names()['choice_names']
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    aggregate_ib_col_name = steady_var_suffixes_dict['btp_ib_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_il_col_name = steady_var_suffixes_dict['btp_il_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]

    '''1. Select only wgtJ'''
    pd_file = pd_file[pd_file['file_save_suffix'].str.contains(wgt_or_max) == True]

    '''2. Sort'''
    pd_file = pd_file.sort_values(by=['esti_param.R_INFORM_BORR'])

    '''3. Get Key Vectors'''
    aggregate_inf_borrow = pd_file[aggregate_ib_col_name].to_numpy()
    aggregate_inf_save = pd_file[aggregate_il_col_name].to_numpy()
    R_INFORM_BORR = pd_file[['esti_param.R_INFORM_BORR']].to_numpy()

    aggregate_inf_borrow = np.ravel(aggregate_inf_borrow)
    aggregate_inf_save = np.ravel(aggregate_inf_save)
    R_INFORM_BORR = np.ravel(R_INFORM_BORR)

    return R_INFORM_BORR, aggregate_inf_borrow, aggregate_inf_save
