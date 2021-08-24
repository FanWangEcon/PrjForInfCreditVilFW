'''
Created on May 10, 2018

@author: fan

Generate moments, based on marginal dsitribution and choices

Moments could be means and sds, and conditional means. 
Total borrowing, total savings are just conditional means. 

import solusteady.distribution.moments as analyticalmm
'''

import logging
import numpy as np
import pandas as pd

import dataandgrid.genshocks as genshocks
import estimation.moments.momcomp as moments
import modelhh.functions.production as prod
import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def calculate_variance(simu_output_pd, param_inst, calc_list=None, mean_dict=None):
    """Calculate Aggregate Mean and Variance
    
    Examples
    --------
    import solusteady.distribution.moments as analyticalmm
    calc_list = ['mean', 'var']
    simu_moments_output_agg_mean_var = analyticalmm.calculate_variance(simu_output_pd_allj, calc_list = calc_list, mean = None)    
    simu_moments_output.update(simu_moments_output_agg_mean_var)
    """
    if (calc_list is None):
        calc_list = ['mean', 'var']

    simu_output = simu_output_pd.sort_values(by=['cash_grid_centered'])

    """
    0. Strings
    """
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    """
    A0. Marginal Distribution
    """
    marginal_dist = simu_output[['marginal_dist']].to_numpy()

    '''
    A. Panda Table Name prefix and suffix.     
    '''
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()

    '''
    B. Aggregating Prob, Kn and Bn choices
    '''
    prob_cols = [col for col in simu_output.columns if steady_var_suffixes_dict['probJ_opti_grid'] in col]
    prb_matrix = simu_output[prob_cols].to_numpy()

    simu_moments_output = {}

    '''
    C. Looping over b, k, c and sub-bs
    '''
    for steady_var_suffixes_cur in [steady_var_suffixes_dict['btp_opti_grid'],
                                    steady_var_suffixes_dict['ktp_opti_grid'],
                                    steady_var_suffixes_dict['consumption_opti_grid'],
                                    steady_var_suffixes_dict['btp_fb_opti_grid'],
                                    steady_var_suffixes_dict['btp_ib_opti_grid'],
                                    steady_var_suffixes_dict['btp_fs_opti_grid'],
                                    steady_var_suffixes_dict['btp_il_opti_grid'],
                                    steady_var_suffixes_dict['cash_grid_centered'],
                                    steady_var_suffixes_dict['y_opti_grid']]:

        '''
        C1. Keys
        '''
        cur_moment_key_mean = steady_var_suffixes_cur + steady_agg_suffixes['_allJ_agg'][0]
        cur_moment_key_var = cur_moment_key_mean + steady_agg_suffixes['_var'][0]

        '''
        C2. Loop over stats to calculate
        '''
        cur_aggregate = 0
        for cur_stat in calc_list:

            #############################################################
            '''
            D. Process Income, Y, requires one more expectation due to e'
            '''
            #############################################################
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['y_opti_grid']):
                '''
                D1. data for Y does not exist in simu_output, but we will solve for Y from K
                '''
                ktp_cols = [col for col in simu_output.columns
                            if (steady_var_suffixes_dict['ktp_opti_grid'] in col) and
                            (steady_agg_suffixes['_allJ_agg'][0] not in col)]
                # B2. Get data columns, all J based ono column name
                ktp_matrix_allJ = simu_output[ktp_cols].to_numpy()

                if (cur_stat == 'mean'):
                    mean_use = None
                elif (cur_stat == 'var'):
                    # cur_aggregate from first round mean calculation
                    if (mean_dict is None):
                        mean_use = cur_aggregate
                    else:
                        # External Mean, for Type weighted variance calculation
                        mean_use = mean_dict[cur_moment_key_mean]
                else:
                    raise Exception('Bad cur_stat y_opti_grid:' + cur_stat)

                cur_matrix_allJ = monte_carlo_EY(param_inst, K=ktp_matrix_allJ, mean=mean_use)

            else:
                '''
                D2. all other columns' data already exists in simu_output
                    why add: (steady_agg_suffixes['_allJ_agg'][0] not in col)?
                        - cur_cols:
                            ['ib_btp_opti_grid', 'is_btp_opti_grid', 'btp_opti_grid_allJ_agg']
                          otherwise
                        - from each type A, calculated: btp_opti_grid_allJ_agg already                        
                '''
                # B1. Get column names
                cur_cols = [col for col in simu_output.columns
                            if (steady_var_suffixes_cur in col) and
                            (steady_agg_suffixes['_allJ_agg'][0] not in col)]
                # B2. Get data columns, all J based ono column name
                cur_matrix_allJ = simu_output[cur_cols].to_numpy()

            #############################################################
            '''
            E. All except for Y, calculate variance if needed 
            '''
            #############################################################
            if (cur_stat == 'mean' or steady_var_suffixes_cur == steady_var_suffixes_dict['y_opti_grid']):
                '''
                E2. if mean, that means calculating mean, do not need mean to calculate variance
                    if steady_var_suffixes_dict['y_opti_grid'], already calculated variance structure
                '''
                pass
            elif (cur_stat == 'var'):
                '''
                E3. Variance
                '''
                # cur_aggregate from first round mean calculation
                if (mean_dict is None):
                    mean_use = cur_aggregate
                else:
                    # External Mean, for Type weighted variance calculation
                    mean_use = mean_dict[cur_moment_key_mean]
                cur_matrix_allJ = (cur_matrix_allJ - mean_use) ** 2

            else:
                raise Exception('Bad cur_stat:' + cur_stat)

            #############################################################
            '''
            F. Weighting Averaging
            '''
            #############################################################
            # B3. Weight choices by conditional probability for each of the J choices
            if (steady_var_suffixes_cur == steady_var_suffixes_dict['cash_grid_centered']):
                '''
                each of the J has an idential cash column, as well as master table:
                cur_cols = ['ib_cash_grid_centered', 'is_cash_grid_centered', 'fb2_cash_grid_centered', 'fs_cash_grid_centered', 'ibfb2_cash_grid_centered', 'fbis2_cash_grid_cen
                    tered', 'none_cash_grid_centered', 'cash_grid_centered']                
                since identical, just need one column
                cur_wgtsum is N by 1 matrix
                '''
                cur_wgtsum = cur_matrix_allJ[:, 0]
                cur_wgtsum_overJ = cur_wgtsum
            else:
                '''
                cur_wgtsum is a N by 7 matrix
                '''
                cur_wgtsum = cur_matrix_allJ * prb_matrix
                cur_wgtsum_overJ = np.sum(cur_wgtsum, axis=1)

            # B4. Weight additionally by marginal probability
            cur_aggregate = np.sum(np.dot(np.transpose(cur_wgtsum), marginal_dist))

            # B5. Add Aggregate to moment json file
            if (cur_stat == 'mean'):
                simu_moments_output[cur_moment_key_mean] = cur_aggregate
                '''
                Sum up across choices at each coh point, aggregate K, B, etc
                '''
                simu_output_pd[cur_moment_key_mean] = pd.Series(cur_wgtsum_overJ, index=simu_output_pd.index)
            if (cur_stat == 'var'):
                simu_moments_output[cur_moment_key_var] = cur_aggregate
    #                 simu_moments_output[cur_moment_key + '_std'] = np.sqrt(cur_aggregate)

    return simu_moments_output, simu_output_pd


def monte_carlo_EY(param_inst, K, mean=None):
    """Calculate Mean of Y

    - handles mean and variance for Y conditional on Productivity type
    - calculates average over epsilon prime shocks for each coh level, each choice j given optimal k'(a, coh, j)
    - k'(a, coh, j) leads to:
        + {k'(a, coh, j, e'_1), ..., k'(a, coh, j, e'_{e_count})}

    Draw Monte Carlo

    [f(K)]^(T)
        - f(K) is N by J, its transpose is J by N
    g(e)
        - g(e) is 1 by M
    Loop over J
        - inside loop, multiply (N by 1) and (1 by M)

    Parameters
    ----------
    K: array
        N by J vector, K' optimal choices at N COH grid points, for J discrete categories
    """

    '''
    1. 
    '''
    J_count = K.shape[1]

    A = param_inst.data_param['A']
    alpha_k = param_inst.esti_param['alpha_k']
    e_mean = param_inst.grid_param['mean_eps_E']
    e_sd = param_inst.grid_param['std_eps_E']
    len_eps_E = param_inst.grid_param['len_eps_E'] * 4
    markov_points = param_inst.grid_param['markov_points']
    e_count = markov_points * len_eps_E * J_count
    draw_type = 2

    '''
    1. Draw M Shocks
    '''
    eps_vec = genshocks.stateSpaceShocks(
        e_mean, e_sd, e_count,
        seed=123, draw_type=draw_type,
        lower_sd=-4, higher_sd=+4)
    eps_tensor = np.reshape(eps_vec, (markov_points, len_eps_E, J_count))

    '''
    2.
    '''
    meanvar_Y = np.zeros(K.shape)
    for j in range(J_count):

        # j's category's optimal K' choices
        K_j = K[:, j]

        # K_j = f(K_j, A, alpha)
        f_K_j = prod.cobb_douglas_nolabor_external(0, A, K_j, alpha_k)
        # EPS_j = g(eps_tt_v)
        f_EPS_j = prod.cobb_douglas_nolabor_external(eps_tensor[:, :, j], A=0, k_t=1, alpha_k=1)

        # Automatically broadcast, EPS_J is a N by M matrix, K_j reshape is N by 1
        Y_mat = np.reshape(f_K_j, (-1, 1)) * f_EPS_j

        if (mean is not None):
            # Calculate Variance Contribution
            Y_mat = (Y_mat - mean) ** 2
        else:
            # Calculate Variance Contribution
            pass

        # Averaging, the Monte Carlo Part
        Y_j = np.mean(Y_mat, axis=1)
        meanvar_Y[:, j] = Y_j

    return meanvar_Y


def simu_moments_shock(choice_set_list, simu_output_pd_allj,
                       trans_prob_dict_allj,
                       param_inst,
                       cur_col_prefix_space='_', solu_dict=None):
    """For model without logit shock
    ktp and bpt here max over each J choice's max over each J cts
    no logit shock considerations.

    solu_dict = {'maxof7_overJ':maxof7_overJ,
                 'each_j_prob':each_j_prob,
                 'ktp_opti':ktp_opti,
                 'btp_opti':btp_opti,
                 'consumption_opti':consumption_opti,
                 'ktp_opti_allJ':ktp_opti_allJ,
                 'btp_opti_allJ':btp_opti_allJ,
                 'consumption_opti_allJ':consumption_opti_allJ}
    """
    logger.info('simu_output_pd_allj.columns:\n%s', simu_output_pd_allj.columns)
    logger.info('simu_output_pd_allj:\n%s', simu_output_pd_allj)

    simu_output = simu_output_pd_allj.sort_values(by=['cash_grid_centered'])

    """
    0. Strings
    """
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    """
    A0. Marginal Distribution
    """
    marginal_dist = simu_output[['marginal_dist']].to_numpy()

    """
    A1. Panda Table Name prefix and suffix.     
    """
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    choice_names = param_model_a.choice_index_names()['choice_names']

    """
    B. Aggregating Prob, Kn and Bn choices
    """
    prob_cols = [col for col in simu_output.columns if steady_var_suffixes_dict['probJ_opti_grid'] in col]
    prb_matrix = simu_output[prob_cols].to_numpy()
    aggregate_prob = np.sum(np.dot(np.transpose(prb_matrix), marginal_dist))  # suppose to be 1

    agg_prob_key = steady_var_suffixes_dict['probJ_opti_grid'] + steady_agg_suffixes['_allJ_agg'][0]
    simu_moments_output = {agg_prob_key: aggregate_prob}

    calc_list = ['mean', 'var']
    simu_moments_output_agg_mean_var, simu_output_pd_allj = \
        calculate_variance(simu_output_pd_allj,
                           param_inst,
                           calc_list=calc_list,
                           mean_dict=None)
    simu_moments_output.update(simu_moments_output_agg_mean_var)

    """
    C. Probability and Kn, Bn, for each J, Marginal prob of each j. 
    Aggregate Probabilities
        Simplest case, two cash grid points, each point different marginal asset
        probability, and each point different conditional probability of choice. 
        The total probability of choosing X, is the marginal multiplied by the conditional 
        then summed up.
        add to moment list: 
            1. probabilities for each of j 
            2. aggregate choices for c, kn, bn for each j (conditional and unconditional) 
    """
    agg_choice_eachJ = {}
    # Loop over each of the J choices
    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):

        '''Probability'''
        prob_col_name = choice_names[choiceJ_index] + cur_col_prefix_space + steady_var_suffixes_dict[
            'probJ_opti_grid']
        cur_j_prb_grid = simu_output[[prob_col_name]].to_numpy()
        cur_j_prob_agg = np.sum(np.dot(np.transpose(cur_j_prb_grid), marginal_dist))

        '''Add to Dictionary, each j prob'''
        moment_dict_key_prefix = prob_col_name + steady_agg_suffixes['_j_agg'][0]
        agg_choice_eachJ[moment_dict_key_prefix] = cur_j_prob_agg

        '''Aggregate each J b asset'''
        # 0. loop over: 'btp_opti_grid':2, 'ktp_opti_grid':3, 'consumption_opti_grid':4
        for steady_var_suffixes_cur in [steady_var_suffixes_dict['btp_opti_grid'],
                                        steady_var_suffixes_dict['ktp_opti_grid'],
                                        steady_var_suffixes_dict['consumption_opti_grid'],
                                        steady_var_suffixes_dict['btp_fb_opti_grid'],
                                        steady_var_suffixes_dict['btp_ib_opti_grid'],
                                        steady_var_suffixes_dict['btp_fs_opti_grid'],
                                        steady_var_suffixes_dict['btp_il_opti_grid']]:
            #         ib_btp_opti_grid = simu_output[['ib_btp_opti_grid']].to_numpy()
            #         is_btp_opti_grid = simu_output[['is_btp_opti_grid']].to_numpy()
            #
            #         ib_prob_opti_grid = simu_output[['ib_probJ_opti_grid']].to_numpy()
            #         is_prob_opti_grid = simu_output[['is_probJ_opti_grid']].to_numpy()
            #
            #         p_inf_borrow = np.sum(np.dot(np.transpose(ib_prob_opti_grid),
            #                                              marginal_dist))
            #         ib_btp_opti_jwgt = ib_btp_opti_grid*ib_prob_opti_grid
            #         aggregate_inf_borrow = np.sum(np.dot(np.transpose(ib_btp_opti_jwgt),
            #                                              marginal_dist))

            # 1. conditional on cash optimal choice for j:
            # column names generate in condidist_analytical.py, line 169
            cur_j_opti_col_name = choice_names[choiceJ_index] + cur_col_prefix_space + steady_var_suffixes_cur
            cur_j_opti_grid = simu_output[[cur_j_opti_col_name]].to_numpy()
            # 2. conditional aggregate choice for j
            cur_j_opti_jwgt = cur_j_opti_grid * cur_j_prb_grid

            # 3. aggregate choice for j, integrating over cash states
            cur_j_opti_agg = np.sum(np.dot(np.transpose(cur_j_opti_jwgt), marginal_dist))
            # 4. aggregate choice for j, for those choosing j, choice conditional on choosing
            cur_j_opti_agg_ifj = np.sum(np.dot(np.transpose(cur_j_opti_grid), marginal_dist))

            '''Add to Dictionary, each j, each cts choice'''
            moment_dict_key_prefix = cur_j_opti_col_name + steady_agg_suffixes['_j_agg'][0]
            agg_choice_eachJ[moment_dict_key_prefix] = cur_j_opti_agg

            moment_dict_key_prefix = cur_j_opti_col_name + steady_agg_suffixes['_j_agg_ifj'][0]
            agg_choice_eachJ[moment_dict_key_prefix] = cur_j_opti_agg_ifj

    """
    D. P(j'|j), given that there are 7 Js, produce 47 numbers. each of them added in nested dict to overall moments 
    """
    P_jp_j_dict = {}
    # Loop over each of the J choices
    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):

        '''
        D1. P(j), aggregate probability of choice type j
        '''
        prob_col_name = choice_names[choiceJ_index] + cur_col_prefix_space + steady_var_suffixes_dict[
            'probJ_opti_grid']
        moment_dict_key_prefix = prob_col_name + steady_agg_suffixes['_j_agg'][0]
        P_j_condi_coh = simu_output[prob_col_name].to_numpy()
        P_j = agg_choice_eachJ[moment_dict_key_prefix]

        '''
        D2. P(Z|j), distribution of Z (COH) conditional on j
            aggregate probabiliyt of choice type
            np.sum(P_coh_condi_j) should = 1
            P_coh_condi_j is M by 1 
        '''
        P_coh_condi_j = (P_j_condi_coh * np.ravel(marginal_dist)) / P_j

        '''
        D3. P(Z'|Z,j)*P(Z|j), M by M 
        '''
        trans_prob_j = trans_prob_dict_allj[choiceJ_index]
        P_zp_condi_z_j = np.matmul(np.reshape(P_coh_condi_j, (1, -1)),
                                   trans_prob_j)

        '''
        D4. P(j'|j) is 1 by 1
        '''
        P_jp_j = np.matmul(P_zp_condi_z_j, prb_matrix)
        P_jp_j = np.ravel(P_jp_j)

        '''
        D5. Save Results P(j'|j=j)
        '''
        P_jp_j_dict_curj = {}
        for choiceJ_p_counter, choiceJ_p_index in enumerate(choice_set_list):
            P_jp_j_dict_curj[str(choiceJ_p_index)] = P_jp_j[choiceJ_p_counter]

        '''
        D6. Save Results P(j'|j) matrix
        '''
        P_jp_j_dict[str(choiceJ_index)] = P_jp_j_dict_curj

    '''
    Save Outputs    
    '''
    simu_moments_output.update(agg_choice_eachJ)
    simu_moments_output['P_jp_j'] = P_jp_j_dict

    '''
    D. Add Estimation Specific Moments if we are doing estimation
    '''
    if ('moments_type' in param_inst.support_arg):
        '''
        '''
        moments_type = param_inst.support_arg['moments_type']
        momsets_type = param_inst.support_arg['momsets_type']
        moments_dict = moments.compare_moments(model_moments=simu_moments_output,
                                               moments_type=moments_type,
                                               momsets_type=momsets_type)
        if (moments_dict is None):
            '''
            Happens in multi-period estimation intentionally.
            Data moments have added time specific suffix, simulated meoments do not, 
            can not be matched up. This is intential, matching to be done within
            estimate_objective_multiperiods.py
            '''
            pass
        else:
            simu_moments_output['esti_obj'] = moments_dict

    """
    E. Add Aggregate EV
    """
    if solu_dict is not None:
        # do not weight these, no need to weight, just get some key statistics
        # unweighted summ stats for EjV
        EjV = solu_dict['EjV']
        dc_EjV = pd.DataFrame(EjV, columns=['EjV_unweighted_stats']).describe().to_dict()
        simu_moments_output.update(dc_EjV)

    return simu_moments_output, simu_output_pd_allj


def simu_moments_noshock(simu_output):
    """For model without logit shock
    ktp and bpt here max over each J choice's max over each J cts
    no logit shock considerations.
    """

    simu_output = simu_output.sort_values(by=['cash_grid_centered'])

    """
    A. Get Relevant Parameters
    """
    marginal_dist = simu_output[['marginal_dist']].to_numpy()
    cash_grid_centered = simu_output[['cash_grid_centered']].to_numpy()
    btp_opti_grid = simu_output[['btp_opti_grid']].to_numpy()
    ktp_opti_grid = simu_output[['ktp_opti_grid']].to_numpy()
    consumption_opti_grid = simu_output[['consumption_opti_grid']].to_numpy()

    '''
    Sum Up Assets
    '''
    aggregate_borrow = np.sum(np.dot(btp_opti_grid[btp_opti_grid < 0],
                                     marginal_dist[btp_opti_grid < 0]))
    aggregate_save = np.sum(np.dot(btp_opti_grid[btp_opti_grid >= 0],
                                   marginal_dist[btp_opti_grid >= 0]))
    aggregate_netB = np.sum(np.dot(np.transpose(btp_opti_grid),
                                   marginal_dist))
    aggregate_K = np.sum(np.dot(np.transpose(ktp_opti_grid),
                                marginal_dist))

    '''
    Outputs    
    '''
    simu_moments_output = {'aggregate_borrow': aggregate_borrow,
                           'aggregate_save': aggregate_save,
                           'aggregate_netB': aggregate_netB,
                           'aggregate_K': aggregate_K,
                           'aggregate_KnetB': aggregate_K + aggregate_netB}

    return simu_moments_output
