'''
Created on Sep 23, 2018

@author: fan

Predict at parameter points not solved for
'''

import logging
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

import estimation.moments.momsets_a as momsetsa
import parameters.loop_param_combo_list.loops_gen as paramloop
import projectsupport.datamanage.data_from_json as datajson
import projectsupport.hardcode.str_estimation as hardcode_estimation
import projectsupport.hardcode.str_periodkey as hardcode_periodkey
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def gen_predict_obj(combo_type_list, all_esti_df,
                    minmax_f='a', minmax_t='20180917',
                    param_vec_count=36,
                    param_vec_predict_count=36,
                    save_directory='',
                    save_main_name='',
                    save_name_mpoly_reg_coef='',
                    exo_or_endo_graph_row_select='_exo_wgtJ'):
    """
    Examples
    --------
    import estimation.postprocess.jsoncsv.gen_predict_more_points as gen_predict
    gen_predict.gen_predict_obj(combo_type_list, all_esti_df,
                                   minmax_f = 'a', minmax_t = '20180917', param_vec_count = 36,
                                   exo_or_endo_graph_row_select = '_exo_wgtJ)    
    """

    '''
    1a. Get Strings etc
    '''
    moment_csv_strs = hardstring.moment_csv_strs()
    moment_pd_cate_vars = hardstring.moment_csv_strs_cates()
    unique_periodkeys = list(all_esti_df[moment_pd_cate_vars['period_dictkey']['colname']].unique())
    unique_periodkeys = [x for x in unique_periodkeys if str(x) != 'nan']
    all_feasible_key_list = hardcode_periodkey.period_key_list()

    '''
    2. Subset of data
    '''
    all_esti_df = all_esti_df[all_esti_df['file_save_suffix'].str.contains(
        exo_or_endo_graph_row_select) == True]

    '''
    Gen DF with all possible RHS LHS
    '''
    param_group_key_list = combo_type_list[0][2]
    regress_rhs_all = param_group_key_list

    regress_lhs_all_moments = momsetsa.momsets_all_moments()  # Potential Moments
    regress_lhs_all_obj = [col for col in all_esti_df.columns
                           if 'esti_obj' in col]
    regress_lhs_all = regress_lhs_all_obj + regress_lhs_all_moments

    other_vars = [hardcode_estimation.string_estimation()['param_combo_list_ctr_str']['str_full'],
                  moment_pd_cate_vars['period_dictkey']['colname'],
                  'model_option.choice_set_list',
                  'model_option.choice_names_use']

    all_esti_main_df = all_esti_df[regress_lhs_all + regress_rhs_all + other_vars]

    '''
    1c, Additional initial parameters
    '''
    param_grid_or_rand = 'rand'
    df_more_parameters = paramloop.gen_initial_params_df(param_group_key_list,
                                                         minmax_f, minmax_t,
                                                         param_vec_count + param_vec_predict_count,
                                                         param_grid_or_rand)

    '''
    add on parameters only those not simulated
    '''
    df_more_parameters = df_more_parameters[param_vec_count:param_vec_predict_count]

    regress_rhs_all = param_group_key_list
    regress_lhs_all_moments = momsetsa.momsets_all_moments()  # Potential Moments

    '''
    1c, Additional initial parameters
    '''
    param_grid_or_rand = 'rand'
    df_simu_params = paramloop.gen_initial_params_df(param_group_key_list,
                                                     minmax_f, minmax_t,
                                                     param_vec_count + param_vec_predict_count,
                                                     param_grid_or_rand)

    '''
    add on parameters only those not simulated
    '''
    df_simu_params = df_simu_params[param_vec_count:]
    logger.info('df_simu_params:\n%s', df_simu_params)

    '''
    3. Select Period
    '''
    mpoly_coef_list = []
    counter = 0
    for unique_periodkey in unique_periodkeys:
        counter = counter + 1

        df_period = all_esti_main_df[all_esti_main_df[moment_csv_strs['period_dictkey'][0]] == unique_periodkey]

        '''
        Stack df together, make sure all have region/time key
        '''
        df_period_all = pd.concat([df_period, df_simu_params])
        df_period_all[moment_csv_strs['period_dictkey'][0]] = unique_periodkey
        df_period_all['model_option.choice_set_list'] = df_period['model_option.choice_set_list'].iloc[0]
        df_period_all['model_option.choice_names_use'] = df_period['model_option.choice_names_use'].iloc[0]

        logger.info('df_period_all:\n%s', df_period_all)

        '''
        4. construct RHS
        '''
        columns_rhs = []
        for columns in regress_rhs_all:
            if (unique_periodkey in columns):
                '''
                Includes current relevant key
                '''
                columns_rhs.append(columns)
            elif (any([key in columns for key in all_feasible_key_list])):
                '''
                Includes coefficients for other periods
                '''
                pass
            else:
                '''
                not time specific variables
                '''
                columns_rhs.append(columns)

        poly = PolynomialFeatures(3)
        logger.info('df_period_all[columns_rhs]:\n%s', columns_rhs)
        logger.info('regress_lhs_all_moments:\n%s', regress_lhs_all_moments)
        logger.info('df_period_all[columns_rhs].iloc(0):\n%s', df_period_all[columns_rhs].iloc[0])
        X = poly.fit_transform(df_period_all[columns_rhs])
        logger.info('X[0,:]\n%s', X[0, :])
        logger.info('X.shape:\n%s', X.shape)

        logger.info('df_period_all[regress_lhs_all_moments].iloc[0]:\n%s',
                    df_period_all[regress_lhs_all_moments].iloc[0])

        '''
        5. Loop over LHS
            - store estimation coefficients in matrix
        '''
        for row_ctr, cur_moment in enumerate(regress_lhs_all_moments):
            y = df_period_all[cur_moment]
            ols_results = sm.OLS(y, X, missing="drop").fit()
            esti_params = ols_results.params

            '''
            5a. Dictionary to store coefficients for the moment
            '''
            esti_params_dict = dict(esti_params)
            moment_lhs_col_name = hardcode_estimation.esti_predict_moment_csv()['moment_lhs']['str']
            prd_dictkey_col_name = hardcode_estimation.esti_predict_moment_csv()['period_dictkey']['str']
            esti_params_dict[moment_lhs_col_name] = cur_moment
            esti_params_dict[prd_dictkey_col_name] = unique_periodkey
            mpoly_coef_list.append(esti_params_dict)

            '''
            save estimation
            '''
            logger.info('ols_results.summary():\n%s', ols_results.summary())
            logger.info('ols_results.rsquared(), rsquared_adj():\n%s, %s, %s',
                        cur_moment, ols_results.rsquared, ols_results.rsquared_adj)

            y_pred = ols_results.predict(X)

            df_period_all.loc[(df_period_all[cur_moment].notnull()), 'predict'] = 0
            df_period_all.loc[(df_period_all[cur_moment].isnull()), 'predict'] = 1

            df_period_all.loc[(df_period_all[cur_moment].isnull()), cur_moment] = y_pred[
                df_period_all[cur_moment].isnull()]

        '''
        Stack dataframe
        '''
        if (counter == 1):
            df_simu_predict = df_period_all
        else:
            df_simu_predict = pd.concat([df_simu_predict, df_period_all])

    '''
    Save Multivariate Coefficient Regression Matris
    '''
    if (save_name_mpoly_reg_coef.endswith('.csv')):
        file_name = save_name_mpoly_reg_coef
    else:
        file_name = save_name_mpoly_reg_coef + '.csv'
    datajson.json_to_panda_nofile(mpoly_coef_list,
                                  agg_df_name_and_directory=save_directory + file_name,
                                  s3=True)

    return df_simu_predict
