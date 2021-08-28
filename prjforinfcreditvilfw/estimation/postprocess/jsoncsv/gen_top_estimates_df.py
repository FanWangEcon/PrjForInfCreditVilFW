'''
Created on Aug 30, 2018

@author: fan
'''

import os.path

import logging
import pandas as pd
# import pandas.io.readexport as readexport
import pyfan.panda.inout.readexport as readexport

import estimation.moments.momcomp as momcomp
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def top_estimates_df(panda_df, top_estimates_keep_count):
    """Merge top results moments and data together
    
    Find Top estimates, combine model with data, and save
    
    Examples
    --------
    import estimation.postprocess.jsoncsv.gen_top_estimates_df as top_estimate
    top_esti_df = top_estimate.top_estimates_df(panda_df, top_estimates_keep_count)
    """
    moment_csv_strs = hardstring.moment_csv_strs()
    moment_pd_cate_vars = hardstring.moment_csv_strs_cates()

    top_objective = moment_csv_strs['main_allperiods_obj'][1]
    sort_by_col = top_objective
    group_by_col = moment_pd_cate_vars['period_dictkey']['colname']
    unique_periodkeys = list(panda_df[moment_pd_cate_vars['period_dictkey']['colname']].unique())

    for ctr, period_key_str_val in enumerate(unique_periodkeys):
        all_esti_df_cur = panda_df[panda_df[group_by_col] == period_key_str_val]
        all_esti_df_cur = all_esti_df_cur.sort_values(sort_by_col).head(top_estimates_keep_count)
        if (ctr == 0):
            top_esti_df = all_esti_df_cur
        else:
            # drop = true to delete the current index (2020-11-14 21:10)
            top_esti_df = pd.concat([top_esti_df, all_esti_df_cur], axis=0).reset_index(drop=True)

    # Previously drop=FALSE by default, created index column, was deleted, new code below is absolete
    if 'index' in top_esti_df:
        del top_esti_df['index']

    return top_esti_df


def top_results_merge_moments_data(combo_type_list,
                                   esti_specs,
                                   all_esti_df,
                                   top_estimates_keep_count=4,
                                   search_directory='',
                                   save_file_name='',
                                   save_file_name_regress='',
                                   multiperiod=True,
                                   save_panda_top=True,
                                   return_panda_top=False,
                                   exo_or_endo_graph_row_select='_exo_wgtJ'):
    """Merge top results moments and data together
    
    Find Top estimates, combine model with data, and save to CSV
    
    Parameters
    ----------
    return_panda_top: boolean
        return existing, do not save new or find new if already has file
        
    Examples
    --------
    import estimation.postprocess.jsoncsv.gen_top_estimates_df as top_estimate
    """

    '''
    0. File Full Directory + Name
    '''
    save_directory = search_directory
    if (save_file_name.endswith('.csv')):
        file_name = save_file_name
    else:
        file_name = save_file_name + '.csv'
    save_directory_file_name = save_directory + file_name

    file_exists = False
    if (os.path.isfile(save_directory_file_name)):
        file_exists = True

    if (file_exists and return_panda_top):
        top_esti_df = readexport.read_csv(save_directory_file_name)

    else:
        '''
        1. Top Estimate and Moments 
        '''
        moment_pd_cate_vars = hardstring.moment_csv_strs_cates()
        moment_csv_strs = hardstring.moment_csv_strs()

        '''
        1b. CAN NOT have other top_objective, CAN ONLY HAVE the main_allperiods_obj
            other objectives are period specific, not common to all periods. 
        '''
        top_objective = moment_csv_strs['main_allperiods_obj'][1]

        '''
        unique period keys
        '''
        unique_periodkeys = list(all_esti_df[moment_pd_cate_vars['period_dictkey']['colname']].unique())
        unique_periodkeys = [x for x in unique_periodkeys if str(x) != 'nan']

        if (multiperiod):
            esti_obj_main_obj = [top_objective,
                                 moment_csv_strs['period_dictkey'][1]]

            '''
            1. separate to sub-groups
            2. each subgroup select top
            3. combine back
            '''

            top_esti_df = top_estimates_df(all_esti_df, top_estimates_keep_count)

        else:
            esti_obj_main_obj = [moment_csv_strs['main_obj'][1]]
            all_esti_df = all_esti_df.sort_values(esti_obj_main_obj, ascending=True)

            '''
            2. Top estimates
            '''
            top_esti_df = all_esti_df.iloc[0:top_estimates_keep_count * 2]

        '''
        3. add string variable for model or data, all model simulation results are model 
        '''
        data_model_col = moment_pd_cate_vars['data_model']['colname']

        data_model_col_model_cate = moment_pd_cate_vars['data_model']['cates']['model'][0]
        data_model_col_data_cate = moment_pd_cate_vars['data_model']['cates']['data'][0]
        top_esti_df[data_model_col] = data_model_col_model_cate

        '''
        Unique Period Keys In current Results
        '''
        moments_type = esti_specs['moments_type']
        momsets_type = esti_specs['momsets_type']
        moments_data, __, __ = momcomp.get_moments_momsets(moments_type, momsets_type)

        periods_keys = hardstring.region_time_dict(True)
        for period_key_str_val in unique_periodkeys:
            period_moments_data_dict = moments_data[period_key_str_val]

            '''
            Add to CSV
            '''
            period_moments_data_dict[moment_csv_strs['period_dictkey'][0]] = period_key_str_val
            period_moments_data_dict[data_model_col] = data_model_col_data_cate
            df_period_moments_data = pd.DataFrame([period_moments_data_dict],
                                                  columns=period_moments_data_dict.keys())
            top_esti_df = pd.concat([top_esti_df, df_period_moments_data], axis=0).reset_index(drop=True)

        '''
        4. Re-order column names 
        '''
        steady_agg_suffixes = hardstring.steady_aggregate_suffixes()
        moment_key_list = list(period_moments_data_dict.keys())
        moment_key_list_wth_var = []
        for mom_key in moment_key_list:
            moment_key_list_wth_var.append(mom_key)
            moment_key_list_wth_var.append(mom_key + steady_agg_suffixes['_var'][0])

        '''
        4b. include priority columns that are also in all_cols, this is for variance, earlier calculation did nothave variance
            also deletes vars from the data/model key var as well as date var
        '''
        all_cols = list(top_esti_df.columns.values)
        priority_cols = [top_objective] + moment_key_list_wth_var
        priority_cols_include = [col_priority for col_priority in priority_cols if (col_priority in all_cols)]
        non_priority_cols = [col for col in all_cols if (col not in priority_cols_include)]
        resorted_cols = priority_cols_include + non_priority_cols
        top_esti_df = top_esti_df[resorted_cols]

        '''
        4c. Sort by time, data vs model, by objective    
        '''
        sort_cols = [moment_pd_cate_vars['data_model']['colname'], moment_csv_strs['main_obj'][1]]
        if (multiperiod):
            sort_cols = [moment_csv_strs['period_dictkey'][0],
                         moment_pd_cate_vars['data_model']['colname'],
                         top_objective]
        top_esti_df = top_esti_df.sort_values(by=sort_cols, ascending=True)

        '''
        5. Save Results in single file under main folder
        '''
        if (save_panda_top):
            save_directory = search_directory
            if (save_file_name.endswith('.csv')):
                file_name = save_file_name
            else:
                file_name = save_file_name + '.csv'

            top_esti_df.to_csv(save_directory + file_name, header=True, index=False)

        '''
        6. Top with only estimation parameters
        '''
        save_panda_top_regress = False
        if (save_panda_top_regress):
            '''
            if save panda_top, save a separate file where we have estimation objective 
            as well as all parameters that were randomly drawn, that were allowed to be different
                - keep only one time period, because parameters and objectives are the same
            '''
            regress_use_cols = [moment_csv_strs['main_allperiods_obj'][1],
                                moment_csv_strs['agg_prob_obj'][1],
                                moment_csv_strs['BI_obj'][1]] + combo_type_list[0][2]

            '''
            select only one time period rows
                all_esti_df only has model rows, top has data rows as well
                unique_periodkeys[0] or unique_periodkeys[1] should give identical results
            '''
            all_esti_df_modelrows_oneperiod = all_esti_df[
                all_esti_df[moment_csv_strs['period_dictkey'][0]] == unique_periodkeys[0]]

            '''
            regression table
            '''
            top_esti_df_regress = all_esti_df_modelrows_oneperiod[regress_use_cols]
            save_directory = search_directory
            if (save_file_name_regress.endswith('.csv')):
                file_name = save_file_name_regress
            else:
                file_name = save_file_name_regress + '.csv'

            top_esti_df_regress.to_csv(save_directory + file_name, header=True, index=False)

    return top_esti_df