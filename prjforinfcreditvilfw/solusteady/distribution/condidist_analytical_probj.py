'''
Created on May 16, 2018

@author: fan
'''

import logging
import numpy as np
import pandas as pd

import dataandgrid.genchoices_fbibfsil as fbibfsis
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup
import solusteady.distribution.condidist_analytical as condianaly

logger = logging.getLogger(__name__)


def semi_analytical_marginal_probj(param_inst, cash_tt, solu_dict,
                                   cur_col_prefix_space='_'):
    """
    Get Marginal Distribution for each j of J
    Then weight each marginal by choice probability for j of J
    
    Returns
    -------
    simu_output_pd_allj: panda dataframe
        each row is a interpolating even grid coh point position
        each column is a different choice or probability interpolated at the coh grid
    trans_prob_wgtJ: numpy array 2d
        transition probability matrix
        
    """

    choice_set_list = param_inst.model_option['choice_set_list']
    choice_names_use = param_inst.model_option['choice_names_full_use']
    choice_names_use = param_inst.model_option['choice_names_use']

    each_j_prob = solu_dict['each_j_prob']
    ktp_opti_allJ = solu_dict['ktp_opti_allJ']
    btp_opti_allJ = solu_dict['btp_opti_allJ']
    consumption_opti_allJ = solu_dict['consumption_opti_allJ']

    #     btp_fb_opti_allJ = solu_dict['btp_fb_opti_allJ']
    #     btp_ib_opti_allJ = solu_dict['btp_ib_opti_allJ']
    #     btp_fs_opti_allJ = solu_dict['btp_fs_opti_allJ']
    #     btp_il_opti_allJ = solu_dict['btp_il_opti_allJ']

    trans_prob_list = []
    simu_output_pd_allj = 0

    for ctr, choicej in enumerate(choice_set_list):

        cur_col_prefix = choice_names_use[ctr]
        logger.info('ctr,choicej,cur_col_prefix:\n%s,%s,%s',
                    str(ctr), str(choicej), str(cur_col_prefix))

        btp_opti = btp_opti_allJ[:, ctr]
        ktp_opti = ktp_opti_allJ[:, ctr]
        prob_cur = each_j_prob[:, ctr]
        consumption_opti = consumption_opti_allJ[:, ctr]

        '''
        Get columns at centered interpolating grid points for:
            'cash_grid_centered'
            'marginal_dist'
            'btp_opti_grid',
            'ktp_opti_grid',
            'consumption_opti_grid'        
        '''
        logger.info('Solve, P(COH|j), P(COH|COH,j), ctr:%s, name:%s', str(ctr), cur_col_prefix)
        simu_output_pd_curj, trans_prob_curj = condianaly.semi_analytical_marginal(
            param_inst,
            cash_tt, ktp_opti, btp_opti, consumption_opti,
            each_j_prob=prob_cur,
            trans_prob_only=True,
            cur_col_prefix=cur_col_prefix + cur_col_prefix_space)

        '''Store Choice J Transition Prob'''
        trans_prob_list.append(trans_prob_curj)

        '''Update Column Names'''
        if (ctr == 0):
            simu_output_pd_allj = simu_output_pd_curj
        else:
            '''Cumulate'''
            simu_output_pd_allj = pd.concat([simu_output_pd_allj,
                                             simu_output_pd_curj], axis=1)

    """
    D. Add columns for each j of J for fbibfsil
    """
    # D1. Get Columns from just created panda files, j specific columns
    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    btp_opti_grid_allJ_cols = [col for col in simu_output_pd_allj.columns if
                               cur_col_prefix_space + steady_var_suffixes_dict['btp_opti_grid'] in col]
    ktp_opti_grid_allJ_cols = [col for col in simu_output_pd_allj.columns if
                               cur_col_prefix_space + steady_var_suffixes_dict['ktp_opti_grid'] in col]

    # D2. Matrix from columns
    btp_opti_grid_allJ = simu_output_pd_allj[btp_opti_grid_allJ_cols].to_numpy()
    ktp_opti_grid_allJ = simu_output_pd_allj[ktp_opti_grid_allJ_cols].to_numpy()

    # D3. Get fb ib fs il specific matrixes
    btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ = \
        fbibfsis.genfibs_btpstack(choice_set_list, btp_opti_grid_allJ, ktp_opti_grid_allJ, param_inst)

    # D4. Add to simu_output_pd_allj panda
    fb_ib_fs_il_steady_var_key_list = ['btp_fb_opti_grid', 'btp_ib_opti_grid',
                                       'btp_fs_opti_grid', 'btp_il_opti_grid']
    varnames_list = [choice_names_use[ctr] + cur_col_prefix_space + steady_var_suffixes_dict[fbibfsil_stdykey]
                     for fbibfsil_stdykey in fb_ib_fs_il_steady_var_key_list
                     for ctr, choicej in enumerate(choice_set_list)]

    # D5. Additional Panda columns with fb ib fs il information
    varnames = ",".join(map(str, varnames_list))
    varmat = np.column_stack((btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ))
    simu_output_pd_allj_fbibfsil = proj_sys_sup.debug_panda(varnames, varmat, export_panda=False, log=False)

    # D6. Concatenate together, join more columns together. 
    simu_output_pd_allj = pd.concat([simu_output_pd_allj, simu_output_pd_allj_fbibfsil], axis=1)

    """
    E0. Grid Column
    """
    cash_grid_centered_cols = [col for col in simu_output_pd_allj.columns
                               if steady_var_suffixes_dict['cash_grid_centered'] in col]
    simu_output_pd_allj['cash_grid_centered'] = simu_output_pd_allj[cash_grid_centered_cols[0]]

    """
    E1. Adjust Probabilities due to Interpolation issue over J choices
    """
    logger.info('simu_output_pd_allj.columns:\n%s', simu_output_pd_allj.columns)
    prob_cols = [col for col in simu_output_pd_allj.columns if 'probJ_opti_grid' in col]
    logger.info('prob_cols:\n%s', prob_cols)
    probJ_matrix = simu_output_pd_allj[prob_cols].to_numpy()
    logger.info('probJ_matrix:\n%s', probJ_matrix)

    '''These are actually not needed, perfect symmatery'''
    probJ_matrix_rowsum = np.reshape(np.sum(probJ_matrix, axis=1), (-1, 1))
    logger.info('probJ_matrix_rowsum:\n%s', probJ_matrix_rowsum)
    probJ_matrix_rescale_sum1 = probJ_matrix / probJ_matrix_rowsum
    logger.info('probJ_matrix_rescale_sum1:\n%s', probJ_matrix_rescale_sum1)

    """
    E2. Overall Conditional probabilities
    """
    trans_prob_wgtJ = 0
    trans_prob_dict_allj = {}
    for ctr, choicej in enumerate(choice_set_list):
        '''E2a. Transition Probability current j'''
        trans_prob_curj = trans_prob_list[ctr]

        '''E2b. Choice Probability over J'''
        prob_opti_grid = probJ_matrix_rescale_sum1[:, ctr]

        '''E2c. Update current column with reweighted sum to 1 choice J prob'''
        simu_output_pd_allj[prob_cols[ctr]] = prob_opti_grid

        '''E2d. Weighted Discrete Transition Probability'''
        trans_prob_curj_wgted = trans_prob_curj * np.reshape(prob_opti_grid, (-1, 1))
        logger.debug('trans_prob_curj:\n%s', trans_prob_curj)
        logger.debug('prob_opti_grid:\n%s', prob_opti_grid)
        logger.debug('trans_prob_curj_wgted:\n%s', trans_prob_curj_wgted)

        '''E2e. Update Column Names'''
        trans_prob_dict_allj[choicej] = trans_prob_curj
        if (ctr == 0):
            trans_prob_wgtJ = trans_prob_curj_wgted
        else:
            '''Cumulate'''
            trans_prob_wgtJ = trans_prob_wgtJ + trans_prob_curj_wgted

    logger.info('trans_prob_wgtJ:\n%s', trans_prob_wgtJ)
    logger.info('np.sum(trans_prob_wgtJ):\n%s', np.sum(trans_prob_wgtJ, axis=1))

    return simu_output_pd_allj, trans_prob_wgtJ, trans_prob_dict_allj
