'''
Created on Jul 7, 2018

@author: fan

finding optimal choices from stacked choices, max cts and, max of J from max cts

import soluvalue.optimax_stack as optimax_stack

'''

import logging

import dataandgrid.genchoices_fbibfsil as fbibfsis
import soluvalue.optimax as optimax

logger = logging.getLogger(__name__)


def max_of_stack(argmax_index, maxof7_overJ, choice_stack, choice_set_list, states_dim, debugstr):
    """
    Parameters
    ----------
    choice_stack: numpy array 3d
        from mjall,where stacks have: 
        self.stack_shape = [self.len_statesshocks, self.choice_set_count, self.len_choices]        
    """

    choice_opti_allJ = optimax.opti_choices_givenargmax(argmax_index, choice_stack, states_dim)
    logger.debug(debugstr, choice_opti_allJ)
    choice_opti = optimax.max_choice_overJ_givenargmax(maxof7_overJ, choice_opti_allJ, choice_set_list, states_dim)

    return choice_opti_allJ, choice_opti


def get_all_optimalchoices(argmax_index, maxof7_overJ,
                           btp_stack, ktp_stack, consumption_stack,
                           b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack,
                           states_dim, choice_set_list, param_inst):
    """
        if (b_tp_borr_for_stack is not None):
            that means in mjall kept each of the four choices, formal informal borrow save
        if (b_tp_borr_for_stack is None):
            means to generate formal informal borrow save based on aggregates from mjall 
    """
    '''
    A. Main ktp, btp and c
    '''
    ktp_opti_allJ, ktp_opti = \
        max_of_stack(argmax_index, maxof7_overJ, ktp_stack, choice_set_list, states_dim, 'ktp_opti_allJ:\n%s')

    btp_opti_allJ, btp_opti = \
        max_of_stack(argmax_index, maxof7_overJ, btp_stack, choice_set_list, states_dim, 'btp_opti_allJ:\n%s')

    consumption_opti_allJ, consumption_opti = \
        max_of_stack(argmax_index, maxof7_overJ, consumption_stack, choice_set_list, states_dim,
                     'consumption_opti_allJ:\n%s')

    '''
    B. optimal b for each j of J
    '''
    if (b_tp_borr_for_stack is not None):
        '''
        B1. if stack of each kept from solumain
        '''
        # this means other 3 are also not None
        btp_fb_opti_allJ, btp_fb_opti = \
            max_of_stack(argmax_index, maxof7_overJ, b_tp_borr_for_stack, choice_set_list, states_dim,
                         'btp_fb_opti_allJ:\n%s')
        btp_ib_opti_allJ, btp_ib_opti = \
            max_of_stack(argmax_index, maxof7_overJ, b_tp_borr_inf_stack, choice_set_list, states_dim,
                         'btp_ib_opti_allJ:\n%s')
        btp_fs_opti_allJ, btp_fs_opti = \
            max_of_stack(argmax_index, maxof7_overJ, b_tp_save_for_stack, choice_set_list, states_dim,
                         'btp_fs_opti_allJ:\n%s')
        btp_il_opti_allJ, btp_il_opti = \
            max_of_stack(argmax_index, maxof7_overJ, b_tp_lend_inf_stack, choice_set_list, states_dim,
                         'btp_fs_opti_allJ:\n%s')
    else:
        """
            Might need these to get the four _opti, for max results, but for weighted results
            don't need to generate anything here, can get fb ib fs il decomposed at interpolating
            over cash grid stage for steady state calculation. 
        """
        btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ = \
            None, None, None, None
        btp_fb_opti, btp_ib_opti, btp_fs_opti, btp_il_opti = \
            None, None, None, None

        '''
        B2. if stack of each not kept from solumain, generate here
        '''
        generate_here = True
        if (generate_here):
            btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ = \
                fbibfsis.genfibs_btpstack(choice_set_list, btp_opti_allJ, ktp_opti_allJ, param_inst)

            btp_fb_opti = optimax.max_choice_overJ_givenargmax(maxof7_overJ, btp_fb_opti_allJ, choice_set_list,
                                                               states_dim)
            btp_ib_opti = optimax.max_choice_overJ_givenargmax(maxof7_overJ, btp_ib_opti_allJ, choice_set_list,
                                                               states_dim)
            btp_fs_opti = optimax.max_choice_overJ_givenargmax(maxof7_overJ, btp_fs_opti_allJ, choice_set_list,
                                                               states_dim)
            btp_il_opti = optimax.max_choice_overJ_givenargmax(maxof7_overJ, btp_il_opti_allJ, choice_set_list,
                                                               states_dim)

    return maxof7_overJ, ktp_opti, btp_opti, consumption_opti, \
           ktp_opti_allJ, btp_opti_allJ, consumption_opti_allJ, \
           btp_fb_opti, btp_ib_opti, btp_fs_opti, btp_il_opti, \
           btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ

