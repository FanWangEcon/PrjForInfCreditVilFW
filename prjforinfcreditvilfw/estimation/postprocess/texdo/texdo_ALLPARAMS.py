'''
Created on Aug 30, 2018

@author: fan
'''

import ast

import estimation.postprocess.texdo.texdo_gen_distribute as esti_texdo_gendist
import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

def fill_template(df,
                  save_name='',
                  save_directory='',
                  save_tex=True,
                  save_agg_tex=True,
                  update_compile_folder=True,
                  esti_obj_rank=0):
    """for producing NECEcreditShares7m.tex
    
    Parameters
    ----------
    df: panda dataframe
        panda data frame where each row is a different data or model result
        each column is a different parameter. 
        this should have already been sorted, and grouped by, so there is only one
        row for data for each region each period.
        
    Examples
    --------
    import projectsupport.table_latex.jinja_NECEcreditShares7m as jinja_NECEcreditShares7m
    jinja_NECEcreditShares7m.fill_template(df,
                                           save_name = '',
                                           save_directory = '',
                                           save_tex = True)
    """

    '''
    A0. Default Values
    '''
    PROB_OBSV_DATA = {}

    '''
    A1. Load in various strings
    '''
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    translate_jinja_name = param_model_a.choice_index_names()['translate_jinja_name']

    '''
    B. Process Panda File, sort group
        group by region and time, sort by 
    '''
    moment_csv_strs_cates = hardstring.moment_csv_strs_cates()
    data_model_col = moment_csv_strs_cates['data_model']['colname']
    data_model_col_val_data = moment_csv_strs_cates['data_model']['cates']['data'][0]
    data_model_col_val_model = moment_csv_strs_cates['data_model']['cates']['model'][0]

    period_dictkey_col = moment_csv_strs_cates['period_dictkey']['colname']
    period_dictkey_col_val_ne1 = moment_csv_strs_cates['period_dictkey']['cates']['ne1'][0]
    period_dictkey_col_val_ne2 = moment_csv_strs_cates['period_dictkey']['cates']['ne2'][0]
    period_dictkey_col_val_ce1 = moment_csv_strs_cates['period_dictkey']['cates']['ce1'][0]
    period_dictkey_col_val_ce2 = moment_csv_strs_cates['period_dictkey']['cates']['ce2'][0]

    '''
    D. Get Data
    '''
    df_data_only = df[df[data_model_col] == data_model_col_val_data]
    df_simu_only = df[df[data_model_col] == data_model_col_val_model]
    # have to come here, only model rows have these info
    #     df_simu_only['esti_obj.main_allperiods_obj']
    '''
    iloc[0] because all rows are the same
    '''
    choice_set_list = df_simu_only['model_option.choice_set_list'].iloc[0]
    choice_set_list = ast.literal_eval(choice_set_list)
    choice_names_use = df_simu_only['model_option.choice_names_use'].iloc[0]
    choice_names_use = ast.literal_eval(choice_names_use)

    '''
    E. Fill up Probabilities
    '''
    jinja_key_list_region = ['NE', 'CE']
    jinja_key_list_period = ['one', 'two']
    #     jinja_key_list_period = ['one'] # Relevant Parameters

    for region in jinja_key_list_region:
        for period in jinja_key_list_period:

            # get string
            if (region == 'NE' and period == 'one'):
                period_dictkey_val = period_dictkey_col_val_ne1
            if (region == 'NE' and period == 'two'):
                period_dictkey_val = period_dictkey_col_val_ne2
            if (region == 'CE' and period == 'one'):
                period_dictkey_val = period_dictkey_col_val_ce1
            if (region == 'CE' and period == 'two'):
                period_dictkey_val = period_dictkey_col_val_ce2

            # ALl Columns
            all_columns = df_simu_only.columns

            # fill in MODEL
            cur_rows = df_simu_only[df[period_dictkey_col] == period_dictkey_val]
            if (len(cur_rows.index) != 0):
                '''
                There will be multiple rows here, depending on how many were kept
                iloc[esti_obj_rank]
                '''
                '''
                F1. Get Desired ranked Row
                '''
                cur_row = cur_rows.iloc[esti_obj_rank]

                '''
                F2. Convert Row to Dictionary File
                '''

                '''                
                F3. Unflatten Dict: DO NOT UNFLATTEN, NESTED NESTED keys can't get out
                '''

                '''
                F4. Get Key Params
                '''
                param_group_list = ['grid_param', 'esti_param', 'data_param', 'data_param', 'dist_param']
                for param_group in param_group_list:
                    grid_param_cols = [col for col in all_columns if param_group in col]
                    for param_group_dot_name in grid_param_cols:
                        texdo_key = hardstring.latex_do_strings(type='tex.param',
                                                                **{'region': region,
                                                                   'period_dictkey_val': period_dictkey_val,
                                                                   'param_group': param_group,
                                                                   'param_group_dot_name': param_group_dot_name})
                        PROB_OBSV_DATA[texdo_key] = cur_row[param_group_dot_name]

    '''
    F. save
    '''
    if (save_tex):
        DATA_PARAM_DICT = PROB_OBSV_DATA
        esti_texdo_gendist.save_to_tex_do(save_directory, save_name, DATA_PARAM_DICT,
                                          save_agg_tex=save_agg_tex, update_compile_folder=update_compile_folder,
                                          format_str=proj_sys_sup.decimals(type='params'))
