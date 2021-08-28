'''
Created on Aug 30, 2018

@author: fan
'''

import ast

import estimation.postprocess.texdo.texdo_gen_distribute as esti_texdo_gendist
import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup


def default_values():
    """Values from previous draft of paper
    """

    PROB_OBSV_DATA = {}
    PROB_OBSV_DATA['DataNEoneFB'] = 14.9
    PROB_OBSV_DATA['DataNEoneFS'] = 6.2
    PROB_OBSV_DATA['DataNEoneIB'] = 25.0
    PROB_OBSV_DATA['DataNEoneIS'] = 7.0
    PROB_OBSV_DATA['DataNEoneFBIB'] = 24.1
    PROB_OBSV_DATA['DataNEoneFBIS'] = 7.4
    PROB_OBSV_DATA['DataNEoneNONE'] = 15.5

    PROB_OBSV_DATA['DataNEtwoFB'] = 29.0
    PROB_OBSV_DATA['DataNEtwoFS'] = 14.0
    PROB_OBSV_DATA['DataNEtwoIB'] = 6.2
    PROB_OBSV_DATA['DataNEtwoIS'] = 4.90
    PROB_OBSV_DATA['DataNEtwoFBIB'] = 32.5
    PROB_OBSV_DATA['DataNEtwoFBIS'] = 7.8
    PROB_OBSV_DATA['DataNEtwoNONE'] = 5.6

    PROB_OBSV_DATA['DataCEoneFB'] = 21.5
    PROB_OBSV_DATA['DataCEoneFS'] = 30.0
    PROB_OBSV_DATA['DataCEoneIB'] = 9.2
    PROB_OBSV_DATA['DataCEoneIS'] = 3.0
    PROB_OBSV_DATA['DataCEoneFBIB'] = 5.0
    PROB_OBSV_DATA['DataCEoneFBIS'] = 1.7
    PROB_OBSV_DATA['DataCEoneNONE'] = 29.7

    PROB_OBSV_DATA['DataCEtwoFB'] = 24.2
    PROB_OBSV_DATA['DataCEtwoFS'] = 34.1
    PROB_OBSV_DATA['DataCEtwoIB'] = 6.1
    PROB_OBSV_DATA['DataCEtwoIS'] = 3.8
    PROB_OBSV_DATA['DataCEtwoFBIB'] = 14.3
    PROB_OBSV_DATA['DataCEtwoFBIS'] = 3.8
    PROB_OBSV_DATA['DataCEtwoNONE'] = 13.8

    return PROB_OBSV_DATA


def fill_template(df,
                  save_name='',
                  save_directory='',
                  save_tex=True,
                  save_agg_tex=True,
                  update_compile_folder=True,
                  esti_obj_rank=0,
                  gen_graph_stata=True):
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
    PROB_OBSV_DATA = default_values()
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

    for region in jinja_key_list_region:
        for period in jinja_key_list_period:
            for ctr, j in enumerate(choice_set_list):

                # Jinja Key:  ['FB', 'FS', 'IB', 'IS', 'FBIB', 'FBIS', 'NONE']                
                jinja_j = translate_jinja_name[j]
                tex_newcommand_var_key_data = hardstring.latex_do_strings(type='tex.prob.data',
                                                                          **{'region': region, 'period': period,
                                                                             'jinja_j': jinja_j})
                tex_newcommand_var_key_simu = hardstring.latex_do_strings(type='tex.prob.simu',
                                                                          **{'region': region, 'period': period,
                                                                             'jinja_j': jinja_j})

                # value from df: fbis2_probJ_opti_grid_j_agg
                pf_col_name = choice_names_use[ctr] + '_' + \
                              steady_var_suffixes_dict['probJ_opti_grid'] + \
                              steady_agg_suffixes['_j_agg'][0]

                # get string
                if (region == 'NE' and period == 'one'):
                    period_dictkey_val = period_dictkey_col_val_ne1
                if (region == 'NE' and period == 'two'):
                    period_dictkey_val = period_dictkey_col_val_ne2
                if (region == 'CE' and period == 'one'):
                    period_dictkey_val = period_dictkey_col_val_ce1
                if (region == 'CE' and period == 'two'):
                    period_dictkey_val = period_dictkey_col_val_ce2

                cur_row = df_data_only[df[period_dictkey_col] == period_dictkey_val]
                if (len(cur_row.index) != 0):
                    '''
                    There can only be one row here, this is the data row
                    one row for early period, one row for later period, with == period_dictkey_val
                    '''
                    cur_val = cur_row[pf_col_name].iloc[0]
                    PROB_OBSV_DATA[tex_newcommand_var_key_data] = cur_val * 100

                # fill in MODEL
                cur_row = df_simu_only[df[period_dictkey_col] == period_dictkey_val]
                if (len(cur_row.index) != 0):
                    '''
                    There will be multiple rows here, depending on how many were kept
                    iloc[esti_obj_rank]
                    '''
                    cur_val = cur_row[pf_col_name].iloc[esti_obj_rank]
                    PROB_OBSV_DATA[tex_newcommand_var_key_simu] = cur_val * 100

    '''
    F. save
    '''
    if (save_tex):
        DATA_PARAM_DICT = PROB_OBSV_DATA
        esti_texdo_gendist.save_to_tex_do(save_directory, save_name, DATA_PARAM_DICT,
                                          save_agg_tex=save_agg_tex, update_compile_folder=update_compile_folder,
                                          format_str=proj_sys_sup.decimals(type='prob'))
