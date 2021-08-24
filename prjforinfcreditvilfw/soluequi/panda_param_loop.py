'''
Created on May 22, 2018

@author: fan

wheather param_loop or param_r_loop, will generate a big panda file from json. 
The file contains rows for each invokation. 
Need to grab out row values from here to generate aggregate statistics analysis
Whether at equilibrium or not.

    The panda files stored have N sets of rows for each element of policy vector. 
    Each of the N set of rows have M set of rows. each of these m rows is for a 
    particular interest rate. 
    
    M rows from one of the N sets
    aggregate_inf_borrow    aggregate_inf_save    aggregate_netB    esti_param.R_INFORM_BORR    esti_param.R_INFORM_SAVE
    -5.962967664    0.000404893    -5.962562771    0.95    0.95
    -0.662759191    0.107448953    -0.555310238    1.0125    1.0125
    -0.489688621    0.238137232    -0.251551388    1.028125    1.028125
    -0.442758901    0.257501406    -0.185257495    1.030357143    1.030357143
    -0.377676987    0.288937254    -0.088739734    1.032589286    1.032589286
    -0.338082466    0.301314653    -0.036767813    1.034821429    1.034821429
    -0.305445675    0.825092792    0.519647117    1.075    1.075
    -0.292379003    0.317943522    0.025564519    1.037053571    1.037053571
    -0.261079359    0.346304391    0.085225032    1.039285714    1.039285714
    -0.214048403    0.373114815    0.159066412    1.041517857    1.041517857
    -0.182564475    0.443614378    0.261049902    1.04375    1.04375
    -0.070390859    0.633972933    0.563582074    1.059375    1.059375
    -0.002355387    34.38302587    34.38067048    1.1375    1.1375
    -7.85E-08       41.73011849    41.73011841    1.2    1.2
         
    Need to find from the dataset which row has the smallest aggregate_netB.
'''

import logging

import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def get_agg_stats_param_loop_catesall(pd_file,
                                      x_var_name='data_param.A',
                                      group_by_var_name=None,
                                      sort_by_var_name=None,
                                      wgt_or_max='_wgtJ',
                                      select_r_equi=True,
                                      select_r_equals2=None):
    """
    This ses 0 and 1, informal borrow and informal lend, and also all other joint 
    choices that invovle informal

    Parameters
    ----------
    pd_file : panda
        file each row results from one steady state model invoke
        for each param_combo, there is one folder, and the pd_file contains all
        results including those invoked from loop over R and those from just loop
        over x_var_name coefficients. 
    sort_var_name : string
        the name of the column that contains the x-axis variable, the param that
        the current folder files are looping over. 
    wgt_or_max : string
        _wgtJ or _maxJ. maxJ just the max choice no logit shock, wgtJ is weighted
        by logit probabilities
    select_r_equals2 : float
        if select_r_equi is False, select_r_equals2 must not be none 
        the specific interest rate from param_combo invoke paramset

    returns
    -------
    pd_file_equi_out: panda datafile
        a data file containing various variables        

    """

    if (group_by_var_name is None):
        group_by_var_name = x_var_name
    if (sort_by_var_name is None):
        sort_by_var_name = x_var_name

    """
    0. Get Strings
    """
    choice_names = param_model_a.choice_index_names()['choice_names']
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    aggregate_ib_col_name = steady_var_suffixes_dict['btp_ib_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_il_col_name = steady_var_suffixes_dict['btp_il_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]

    """
    A. Select only wgted or maxJ rows
    """
    pd_file.columns
    pd_file = pd_file[pd_file['file_save_suffix'].str.contains(wgt_or_max) == True]

    """
    B. Demand and Supply Gap
    """
    #     pd_file['aggregate_inf_sabr_gap'] = abs(pd_file['aggregate_inf_borrow'] + \
    #                                             pd_file['aggregate_inf_save'])

    '''3. Get Key Vectors'''
    pd_file['aggregate_inf_sabr_gap'] = abs(pd_file[aggregate_ib_col_name] + \
                                            pd_file[aggregate_il_col_name])
    equi_gap_var = 'aggregate_inf_sabr_gap'

    """
    C. Sort File
    if this panda file from json has multiple rows for each x_var_name unique
    that means we are looking at
    """
    pd_file_row_count = pd_file.shape[0]

    if (pd_file_row_count == 1):
        '''
        Single Invocation
        '''
        pd_file = pd_file.reset_index(drop=True)
        pd_file['pdindex'] = pd_file.index
        pd_file_sort_select = pd_file

    else:

        if (isinstance(sort_by_var_name, list)):
            sort_vars = sort_by_var_name + [equi_gap_var]
        else:
            sort_vars = [sort_by_var_name, equi_gap_var]

        pd_file = pd_file.sort_values(sort_vars, ascending=True)
        # Generate Index after sorting
        pd_file = pd_file.reset_index(drop=True)
        pd_file['pdindex'] = pd_file.index
        #     pd_file[[x_var_name, equi_gap_var]]

        """
        D. Selecting rows from panda file
        """
        if (select_r_equi):
            """
            D1. Selecting out the values closest to values that close equilibrium
            """
            pd_file_sort_equi = pd_file.groupby(group_by_var_name).first().reset_index()
            pd_file_sort_select = pd_file_sort_equi
        else:
            if (select_r_equals2 is None):
                """
                Did not specify a parameter value here, just grab all this is coming from param_loop.py. 
                If simulating over two parameters, meshed grid, with 9 combinations overall, this will
                output a dataframe with nine different rows.                 
                """
                pd_file_sort_select = pd_file
            else:
                """
                D2. The only other option, where we select at a specified interest rate
                (informal) this would be the interest rate we the param_combo invokes by
                default without the loop. 
                """
                pd_file_sort_equi = pd_file.groupby(group_by_var_name).first().reset_index()
                pd_file_sort_select = pd_file.loc[pd_file['esti_param.R_INFORM_BORR'] == select_r_equals2]

    return pd_file_sort_select


def get_agg_stats_param_loop_cates01(pd_file,
                                     x_var_name='data_param.A',
                                     wgt_or_max='_wgtJ',
                                     select_r_equi=True,
                                     select_r_equals2=None):
    """
    This only uses 0 and 1, informal borrow and informal lend, no joint categories

    Parameters
    ----------
    pd_file: panda 
        file each row results from one steady state model invoke
        for each param_combo, there is one folder, and the pd_file contains all
        results including those invoked from loop over R and those from just loop
        over x_var_name coefficients. 
    x_var_name: string
        the name of the column that contains the x-axis variable, the param that
        the current folder files are looping over. 
    wgt_or_max: string
        _wgtJ or _maxJ. maxJ just the max choice no logit shock, wgtJ is weighted
        by logit probabilities
    select_r_equals2: float
        if select_r_equi is False, select_r_equals2 must not be none 
        the specific interest rate from param_combo invoke paramset
    
    returns
    -------
    pd_file_equi_out: panda datafile
        a data file containing various variables        

    Invoke
    ------
    Sample File/Invoke:
        import numpy as np
        import pandas as pd
        import projectsupport.systemsupport as proj_sys_sup
            
        directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/simu/a_20180517_A'
        file_name = '20180517_A.csv'
        csv_file_folder = directory + '/' + file_name
        pd_file = proj_sys_sup.read_csv(csv_file_folder)
        
       x_var = 'data_param.A'

    """

    """
    0. Get Strings
    """
    choice_names = param_model_a.choice_index_names()['choice_names']
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    inf_borr_col_name_prefix = choice_names[0] + '_' + steady_var_suffixes_dict['btp_opti_grid']
    aggregate_inf_borrow_col_name = inf_borr_col_name_prefix + steady_agg_suffixes['_j_agg'][0]
    avg_inf_borrow_ifborr_col_name = inf_borr_col_name_prefix + steady_agg_suffixes['_j_agg_ifj'][0]

    inf_save_col_name_prefix = choice_names[1] + '_' + steady_var_suffixes_dict['btp_opti_grid']
    aggregate_inf_save_col_name = inf_save_col_name_prefix + steady_agg_suffixes['_j_agg'][0]
    avg_inf_save_ifinfsave_col_name = inf_save_col_name_prefix + steady_agg_suffixes['_j_agg_ifj'][0]

    """
    A. Select only wgted or maxJ rows
    """
    pd_file.columns
    pd_file = pd_file[pd_file['file_save_suffix'].str.contains(wgt_or_max) == True]

    """
    B. Demand and Supply Gap
    """
    #     pd_file['aggregate_inf_sabr_gap'] = abs(pd_file['aggregate_inf_borrow'] + \
    #                                             pd_file['aggregate_inf_save'])

    logger.debug('aggregate_inf_borrow_col_name:%s', aggregate_inf_borrow_col_name)
    logger.debug('aggregate_inf_save_col_name:%s', aggregate_inf_save_col_name)

    pd_file['aggregate_inf_sabr_gap'] = abs(pd_file[aggregate_inf_borrow_col_name] + \
                                            pd_file[aggregate_inf_save_col_name])
    equi_gap_var = 'aggregate_inf_sabr_gap'

    """
    C. Sort File
    if this panda file from json has multiple rows for each x_var_name unique
    that means we are looking at
    """
    pd_file = pd_file.sort_values([x_var_name, equi_gap_var], ascending=[True, True])
    #     pd_file[[x_var_name, equi_gap_var]]

    """
    D. Selecting rows from panda file
    """
    if (select_r_equi):
        """
        D1. Selecting out the values closest to values that close equilibrium
        """
        pd_file_sort_equi = pd_file.groupby(x_var_name).first().reset_index()
        pd_file_sort_select = pd_file_sort_equi
    else:
        if (select_r_equals2 is None):
            """
            Did not specify a parameter value here, just grab all
            this is coming from param_loop.py
            """
            pd_file_sort_select = pd_file
        else:
            """
            D2. The only other option, where we select at a specified interest rate
            (informal) this would be the interest rate we the param_combo invokes by
            default without the loop. 
            """
            pd_file_sort_equi = pd_file.groupby(x_var_name).first().reset_index()
            pd_file_sort_select = pd_file.loc[pd_file['esti_param.R_INFORM_BORR'] == select_r_equals2]

    """
    E. Vector of output columns, whatever needed for aggregate analysis. 
    """

    aggregate_netB_col_name = steady_var_suffixes_dict['btp_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    aggregate_K_col_name = steady_var_suffixes_dict['ktp_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    p_inf_borrow_col_name = choice_names[0] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                            steady_agg_suffixes['_j_agg'][0]
    p_inf_save_col_name = choice_names[1] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                          steady_agg_suffixes['_j_agg'][0]


    return pd_file_sort_select
