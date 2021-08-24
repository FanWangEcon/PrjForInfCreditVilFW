'''
Created on Dec 16, 2017

@author: fan

copied over from Function.py previous JMP codes
 
'''

import logging
import numpy as np

import dataandgrid.choices.dynamic.minmaxfunc as minmaxfunc

logger = logging.getLogger(__name__)


def minmax_eachchoice(cash, k_tp,
                      R_INFORM, R_FORMAL_BORR, R_FORMAL_SAVE,
                      DELTA_DEPRE, borr_constraint_KAPPA,
                      BNF_SAVE_P, BNF_SAVE_P_startVal,
                      BNF_BORR_P, BNF_BORR_P_startVal,
                      BNI_LEND_P, BNI_LEND_P_startVal,
                      BNI_BORR_P, BNI_BORR_P_startVal,
                      choice_set_list=[0, 1, 2, 3, 4, 5, 6, 7]):
    #     choice_set_list=[0,1,2,3,4,5,6,7,8]
    #                       choice_set_list=[4]

    """    
    Parameters
    ----------    
    BNI_LEND_P: numeric
        if BNI_LEND_P > cash ==> cash_pos = np.maximum(0.001, cash-credit_fixed_costs)
        so high fixed cost just means for informal lending, you will not be able
        to lend/save anything except 0.001, and capital next period also just 0.001
        higher fixed cost moves the slanted edge of triangle down        
    BNI_LEND_P_startVal: numeric
        this is different than the fixed cost, 
        higher start val requirement moves up the lower triangle bound, and moves
        to the right the left triangle bound
        Given cash_pos from np.maximum(0.001, cash-credit_fixed_costs), 
        BNI_LEND_P_startVal can not exceed save_max, determine save max, then bound save min by save max,
        then determine capital givesn save min and max
        
    
    BNF_SAVE_P_startVal: formal saving minimal savings required
        in multinomial choice logit, every choice is feasible,
        so if a choice is chosen, even if it is optimal to borrow 0 from
        that category, need to pay the category fixed cost and minimal
        borrowing or savings.
    s
    
    """

    #     BNF_SAVE_NP_startVal, BNF_BORR_NP_startVal = 500, -5000
    #     BNI_SAVELEND_NP_startVal, BNI_BORR_NP_startVal = 500, -5000

    '''
    Actually K is a function of B, there is maximum K at maximum B, but given total resources
    available and given current B, there is maximum K.
    
    The maximum for borrowing bounds here are actually not used later, note that need to divide borrowing
    by 1+r to get to maximum K' from borrowing 
    '''

    '''
    Issue with low informal interest rate, can not be more than d  
        see: https://www.evernote.com/shard/s10/nl/1203171/042f20a3-d75a-461d-8188-7c40bcf0800b
        this is just choice bound, does not impact utility 
    '''
    R_INFORM_bounded = max(-DELTA_DEPRE + 0.01, R_INFORM - 1) + 1

    all_minmax = []
    #     all_minmax = [ibf, isLF, fbF, fsF, ibfbF, fbislF, noneF, fbWthInf_BorrCostsF, fbWthInf_SaveCostsF]

    for ctr, j in enumerate(choice_set_list):
        logger.debug('choice_set_list cur:%s, j:%s, list:%s', ctr, j, choice_set_list)

        if (j == 0):
            """
            1. informal borrow
            """
            '''
            ibF Grind            
            '''
            ibf = minmaxfunc.minmax_KB_Informal_Borrow(
                d=DELTA_DEPRE, Y_minCst=cash - BNI_BORR_P,
                Bstart=BNI_BORR_P_startVal, RB=R_INFORM_bounded)
            cur_minmax = ibf
            # =======================================================================
            # ibf = minmax_KB_Borrow(Y_minCst=cash,
            #                             Bstart=BNI_BORR_P_startVal, RB=R_INFORM)
            # =======================================================================

        if (j == 1):
            '''
            2. informal lend
            '''
            isLF = minmaxfunc.minmax_KB_Save(
                DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNI_LEND_P,
                Bstart=BNI_LEND_P_startVal, RB=R_INFORM_bounded)
            cur_minmax = isLF
            # =======================================================================
            # isLF = minmax_KB_Save(DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash,
            #                            Bstart=BNI_LEND_P_startVal, RB=R_INFORM) 
            # =======================================================================

        if (j == 2 or j == 102):
            if (j == 2):
                """
                3. formal borrow
                """
                '''
                fbF Grind, this is the natural borrowing constraint part of the formal borrowinng constraint,
                is bounded in genchoices also by (k_tp * borr_constraint_KAPPA)
                '''
                fbF = minmaxfunc.minmax_KB_Borrow(
                    DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNF_BORR_P,
                    Bstart=BNF_BORR_P_startVal, RB=R_FORMAL_BORR)
                cur_minmax = fbF
                # =======================================================================
                # fbF = minmax_KB_Borrow(DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash,
                #                             Bstart=BNF_BORR_P_startVal, RB=R_FORMAL_BORR)        
                # =======================================================================

            if (j == 102):
                """
                2018-06-13
                    alternative formal borrowing choice, same triangular structure
                    as informal borrowing, but with lower slope determined by not depreciation but by 
                    coollateral or actually here, down-payment, constraint. In contrast
                    to the formal borrowing choice before which is a fraction of current
                    physical capital level, this is a fraction of chosen physical 
                    capital level.  
                    
                    compare this to j == 1, all four parameters for minmax_KB_Informal_Borrow function differs
                """
                fbF = minmaxfunc.minmax_KB_Informal_Borrow(
                    d=(1 - borr_constraint_KAPPA), Y_minCst=cash - BNF_BORR_P,
                    Bstart=BNF_BORR_P_startVal, RB=R_FORMAL_BORR)
                cur_minmax = fbF

        if (j == 3):
            '''
            4. formal save
            '''
            fsF = minmaxfunc.minmax_KB_Save(
                DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNF_SAVE_P,
                Bstart=BNF_SAVE_P_startVal, RB=R_FORMAL_SAVE)
            cur_minmax = fsF
            # =======================================================================
            # fsF = minmax_KB_Save(DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash,
            #                            Bstart=BNF_SAVE_P_startVal, RB=R_FORMAL_SAVE)
            # =======================================================================

        if (j == 4 or j == 104):

            if (j == 4):
                '''
                5, joint formal informal borrow: Maxed formal choices, cts informal choices
                '''
                ibfbF = minmaxfunc.minmax_KB_Borrow(
                    DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNI_BORR_P - BNF_BORR_P,
                    Bstart=BNI_BORR_P_startVal, RB=R_INFORM_bounded,
                    Z=-k_tp * borr_constraint_KAPPA, RZ=R_FORMAL_BORR)
                cur_minmax = ibfbF
                # =======================================================================
                # ibfbF = minmax_KB_Borrow(DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash,
                #                             Bstart=BNI_BORR_P_startVal, RB=R_INFORM,
                #                             Z=-k_tp * borr_constraint_KAPPA, RZ=R_FORMAL_BORR)               
                # =======================================================================

            if (j == 104):
                """
                2018-07-01
                    alternative formal+informal borrowing choice, same triangular structure
                    as informal borrowing:
                        - lower slope controled by collateral or actually here, down-payment, constraint.
                        - upper slope controled by informal borrow interset rate.
                    to the formal borrowing choice before which is a fraction of current
                    physical capital level, this is a fraction of chosen physical 
                    capital level.  
                    
                    compare this to j == 1 and j == 102
                    
                    note:
                        - BNF_BORR_P_startVal + BNI_BORR_P_startVal: ok because have same sign
                        - only makes sense here if DELTA_DEPRE > borr_constraint_KAPPA
                        - this does not provide the correct chocie triangle. A triangle of high k'
                        and high borrow is actually infeasible. The actual choice set top slope
                        first determined by R_FORMAL_BORR, then by R_INFORMAL. But here, by the lower
                        R_FORMAL_BORR. This does not create a problem except to be wasting some choice
                        points in region where consumption will be below zero. 
                """
                ibfbF = minmaxfunc.minmax_KB_Informal_Borrow(
                    d=DELTA_DEPRE,
                    Y_minCst=cash - BNI_BORR_P - BNF_BORR_P,
                    Bstart=BNF_BORR_P_startVal + BNI_BORR_P_startVal,
                    RB=R_FORMAL_BORR)
                cur_minmax = ibfbF

        if (j == 5 or j == 105):

            if (j == 5):
                '''
                6, formal borrow informal lend: Maxed formal choices, lend informally
                    Z includes principle and interest, invoke get borrow constraint function
                '''
                #             Z =  constraints.get_borrow_constraint()
                fbislF = minmaxfunc.minmax_KB_Save(
                    DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNI_LEND_P - BNF_BORR_P,
                    Bstart=BNI_LEND_P_startVal, RB=R_INFORM_bounded,
                    Z=-k_tp * borr_constraint_KAPPA, RZ=R_FORMAL_BORR)
                cur_minmax = fbislF
                # =======================================================================
                # fbislF = minmax_KB_Save(DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash,
                #                              Bstart=BNI_LEND_P_startVal, RB=R_INFORM,
                #                              Z=-k_tp * borr_constraint_KAPPA, RZ=R_FORMAL_BORR)           
                # =======================================================================

            if (j == 105):
                fbis_borr = minmaxfunc.minmax_KB_Informal_Borrow(
                    d=(1 - borr_constraint_KAPPA),
                    Y_minCst=cash - BNI_LEND_P - BNF_BORR_P,
                    Bstart=BNF_BORR_P_startVal,
                    RB=R_FORMAL_BORR)
                fbis_save = minmaxfunc.minmax_KB_Save(
                    DELTA_DEPRE=DELTA_DEPRE,
                    Y_minCst=cash - BNI_LEND_P - BNF_BORR_P,
                    Bstart=BNI_LEND_P_startVal,
                    RB=R_INFORM_bounded)
                cur_minmax = {'fbis_borr': fbis_borr,
                              'fbis_save': fbis_save}

        if (j == 6):
            '''
            7, Cash under Matress
            '''
            kapitalnext_max = cash
            if (isinstance(cash, (int))):
                zeros = 0
            else:
                zeros = np.zeros(cash.shape)

            minmax = [[zeros, kapitalnext_max], [zeros, zeros]]

            bk_sum = cash

            noneF = [minmax, bk_sum, 1]
            cur_minmax = noneF

        if (j == 7):
            '''
            8, joint formal informal borrow:            
                - but no informal choice, only informal choice with informal + formal costs
                
                fbWthInf_BorrCostsF, this is the natural borrowing constraint part of the formal borrowinng constraint,
                is bounded in genchoices also by (k_tp * borr_constraint_KAPPA)
                
                It might seem that From the perspective of finding the choice set, there is no difference between formal borrowing and this choice 
                except that this choice has a higher 'fixed cost' component to be subtracted away, this is not actually true
                because when you borrow also minimal informal credit, your minimal k possible changes. 
            '''
            fbWthInf_BorrCostsF = minmaxfunc.minmax_KB_Borrow(
                DELTA_DEPRE=DELTA_DEPRE, Y_minCst=cash - BNF_BORR_P - BNI_BORR_P,
                Bstart=BNF_BORR_P_startVal, RB=R_FORMAL_BORR,
                Z=BNI_BORR_P_startVal, RZ=R_INFORM_bounded)
            cur_minmax = fbWthInf_BorrCostsF

        if (j != 105):
            logger.debug('cur_minmax[2]=RB:%s', cur_minmax[2])
        else:
            for cur_minmax_105_str in ['fbis_borr', 'fbis_save']:
                cur_minmax_use = cur_minmax[cur_minmax_105_str]
                logger.debug(cur_minmax_105_str + ', [K_min_i, K_max_i,B_min_i, B_max_i, Y_minCst]:\n%s',
                             np.concatenate((cur_minmax_use[0][0][0], cur_minmax_use[0][0][1],
                                             cur_minmax_use[0][1][0], cur_minmax_use[0][1][1],
                                             cur_minmax_use[1]), axis=1))

        try:
            logger.debug('cur_minmax, [K_min_i, K_max_i,B_min_i, B_max_i, Y_minCst]:\n%s',
                         np.concatenate((cur_minmax[0][0][0], cur_minmax[0][0][1],
                                         cur_minmax[0][1][0], cur_minmax[0][1][1],
                                         cur_minmax[1]), axis=1))
        except:
            logger.debug('cur_minmax, [K_min_i, K_max_i,B_min_i, B_max_i, Y_minCst]:\n%s', cur_minmax)

        """
        Collect and Return
        """
        all_minmax.append(cur_minmax)

    return all_minmax
