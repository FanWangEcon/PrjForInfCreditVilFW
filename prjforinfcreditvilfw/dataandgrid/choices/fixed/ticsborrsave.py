'''
Created on Jan 28, 2018

@author: fan
'''

import logging
import dataandgrid.choices.fixed.tics as policytics

logger = logging.getLogger(__name__)


def gen_polfixed_borr_save_pair(len_choices, cont_choice_count,
                                k_choice_min, k_choice_max,
                                b_borr_choice_min, b_borr_choice_max,
                                b_save_choice_min, b_save_choice_max):
    """
    Mesh K prime and B prime choice grid. 
    
    Unlike genpoldyna, genpolfixed does not need state-space information.         
    """

    logger.debug('gen N choices')
    choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints = \
        policytics.gentics(
            len_states=1,
            len_shocks=1,
            len_choices=len_choices,
            cont_choice_count=2,
            k_choice_min=k_choice_min,
            k_choice_max=k_choice_max,
            b_choice_min=b_borr_choice_min,
            b_choice_max=b_borr_choice_max)

    K_borr_tp = choicegrid_tics_mat[:, 0]
    B_borr_tp = choicegrid_tics_mat[:, 1]

    choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints = \
        policytics.gentics(
            len_states=1,
            len_shocks=1,
            len_choices=len_choices,
            cont_choice_count=2,
            k_choice_min=k_choice_min,
            k_choice_max=k_choice_max,
            b_choice_min=b_save_choice_min,
            b_choice_max=b_save_choice_max)

    K_save_tp = choicegrid_tics_mat[:, 0]
    B_save_tp = choicegrid_tics_mat[:, 1]

    return K_borr_tp, B_borr_tp, K_save_tp, B_save_tp
