'''
Created on Jun 26, 2017

@author: fan

constraints need to change choice set, not just utility function value. 
'''

import logging

import numpy as np

logger = logging.getLogger(__name__)


# def borrow_constraint():
#     COLLATERAL_RATIO = self.parameters_dict['borr_constraint_KAPPA']        
#     index_too_much_borrow = self.b_formal_prime < (-1)*(COLLATERAL_RATIO*self.k_dupchoice)
#     self.b_formal_prime[index_too_much_borrow] = (-1)*(COLLATERAL_RATIO*self.k_dupchoice)

def get_borrow_constraint(borr_constraint_KAPPA, k_tt, Formal_Borr_Interest_Rate):
    #
    #     becareful with this
    #     the output is going into the budget constraint and will be divided by formal interest rate there,
    #     so this contains princpiles and interest.
    #     the collateral coefficient can not capture both interest rate and collatearl.
    #     otherwise collateral coefficient is a function of interest rate.

    formal_borr_bound = (-1) * (borr_constraint_KAPPA * k_tt) * Formal_Borr_Interest_Rate
    return formal_borr_bound


def get_consumption_constraint(cash, credit_fixed_costs=True):
    """
    Consumption should be non-negative:
        this means several things:
            1. there needs to be enough K such that it can pay back B fully if Y=0
            2. given fixed costs, say fc=10, if Y+B+(1-d)*K < fc, can't pay fc
                pay fixed cost if can, otheriwse reduce fixed cost, which is the
                same as increasing cash
                - b' and k' choices are chosen given this condition, 
                    if cash =0, b' and k' both can only be 0
                - c should also be 0
                - if cash is too low, everything sets to zero. 
                - this means that when cash gets to low enough level, lower cash
                does not do anything, the fc is like a minimal consumption 
                requirement in some tangential sense
    """

    if (credit_fixed_costs):
        cash_pos = np.maximum(0, cash - credit_fixed_costs)
    else:
        'cash already has fixed costs included'
        cash_pos = np.maximum(0, cash)

    return cash_pos
