'''
Created on May 7, 2018

@author: fan
'''

import logging
import pandas as pd

import projectsupport.systemsupport as proj_sys_sup
import solusteady.distribution.condidist_analytical as condianaly
import solusteady.distribution.condidist_analytical_probj as condianalyprobj
import solusteady.distribution.marginaldist as marginaldist
import solusteady.distribution.moments as analyticalmm
import soluvalue.solu as solu

logger = logging.getLogger(__name__)


def solve_policy(param_combo, directory_str_dict, graph_list=None):
    """    
    Parameters
    ----------
    solu_dict: dict of arrays from solumain.py line 106
        solu_dict = {'maxof7_overJ':maxof7_overJ,
                     'each_j_prob':each_j_prob,
                     'ktp_opti':ktp_opti,
                     'btp_opti':btp_opti,
                     'consumption_opti':consumption_opti,
                     'ktp_opti_allJ':ktp_opti_allJ,
                     'btp_opti_allJ':btp_opti_allJ,
                     'consumption_opti_allJ':consumption_opti_allJ}        
    """

    interpolant, solu_dict, mjall_inst, param_inst = solu.solve_model(param_combo,
                                                                      directory_str_dict=directory_str_dict,
                                                                      graph_list=graph_list)

    return solu_dict, mjall_inst, param_inst


def solve_dist(param_combo, solu_dict, mjall_inst, param_inst, max_of_J=True):
    """
    
    Parameters
    ----------
    solu_dict: dict of arrays from solumain.py line 106
        optinal choices and probability for each continuous choice max of J
        optinal choices and probability for each j of J
        solu_dict = {'maxof7_overJ':maxof7_overJ,
                     'each_j_prob':each_j_prob,
                     'ktp_opti':ktp_opti,
                     'btp_opti':btp_opti,
                     'consumption_opti':consumption_opti,
                     'ktp_opti_allJ':ktp_opti_allJ,
                     'btp_opti_allJ':btp_opti_allJ,
                     'consumption_opti_allJ':consumption_opti_allJ}
        
                     
    Returns
    -------
    simu_output_pd: panda dataframe
        each row is a interpolating even grid coh point position
        each column is a different choice or probability interpolated at the coh grid
        from semi_analytical_marginal_probj.py
        same as simu_output_pd = simu_output_pd_allj EXCEPT:
            simu_output_pd contains *marginal_dist* column
    trans_prob: numpy array 2d
        transition probability matrix
        from semi_analytical_marginal_probj.py
        same as trans_prob = trans_prob_wgtJ 
    simu_moments_output: dictionary of numerics
        store aggregate moments based on simu_output_pd    
    """

    cash_tt = mjall_inst.cash_tt

    """
    A. get Parameters
    """
    choice_set_list = param_inst.model_option['choice_set_list']
    choice_names_use = param_inst.model_option['choice_names_full_use']

    '''
    A. Max of J
    Relying on the same policy functions below, ignorning or not choice J probabilities 
    '''
    if (max_of_J):
        logger.warning('start max_of_J')
        """No Shock, just choose max of J choices"""

        '''A. Get Conditional + Marginal Distribution'''
        ktp_opti = solu_dict['ktp_opti']
        btp_opti = solu_dict['btp_opti']
        consumption_opti = solu_dict['consumption_opti']
        simu_output_pd, trans_prob = \
            condianaly.semi_analytical_marginal(param_inst,
                                                cash_tt, ktp_opti, btp_opti,
                                                consumption_opti)

        '''B. Get Marginal Distribution'''
        simu_moments_output = analyticalmm.simu_moments_noshock(simu_output_pd)

    else:
        logger.warning('start weightJ')
        """all J choices possible, need to weight by choice probabilities"""

        """
        A1. Get weighted Conditional Distribution
            This also gets choice j specific conditional
            but those are not really useful, unless one choice has 100 percent prob
        """
        simu_output_pd, trans_prob, trans_prob_dict_allj = \
            condianalyprobj.semi_analytical_marginal_probj(
                param_inst, cash_tt, solu_dict)

        '''A2. Get Marginal Distribution'''
        state_count = trans_prob.shape[0]
        logger.warning('WgtJ, E_{j}(P(COH,j))')
        marginal_dist = marginaldist.marginal_dist_from_conditional(
            trans_prob, state_count)

        '''A3. Add overall weighted marginal distribution into data storage'''
        simu_output_pd['marginal_dist'] = \
            pd.Series(marginal_dist, index=simu_output_pd.index)

        '''B. Generate Moments'''
        simu_moments_output, simu_output_pd = analyticalmm.simu_moments_shock(
            choice_set_list,
            simu_output_pd,
            trans_prob_dict_allj,
            param_inst, solu_dict=solu_dict)

    '''
    Print Results
    '''
    logger.warning('param_combo:%s', param_combo)
    proj_sys_sup.jdump(simu_moments_output, 'simu_moments_output', logger=logger.warning)

    return trans_prob, simu_output_pd, simu_moments_output
