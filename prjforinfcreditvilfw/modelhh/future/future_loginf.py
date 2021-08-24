'''
Created on Dec 7, 2017

@author: fan

'''


def future_loginf(prod_inst, crra_inst, param_inst,
                  b_tp, k_tp, A, eps_tt):
    """Basic Future Approximation
    """
    R = param_inst.esti_param['R_AVG_INT']
    beta = param_inst.esti_param['beta']

    '''
    A. Assume Capital forever the same
    '''
    output_tp_forever = prod_inst.cobb_douglas_nolabor(
        eps_t=eps_tt, A=A, k_t=k_tp, alphaed=False)

    '''
    B. Add to output savings from interest rate
    For each dollar saved today, get 1+R tomorrow
    b_tp is interest and principle
    if negative, this is payment I suppose 
    in reality, this should take into consideration chances of using 
    each type of loan, each interest is different, but just use formal 
    borrow here for now
    '''
    interest_earning_cost_forever = (b_tp * (R / (1 + R)))

    '''
    C. Assume will consume interest rate from savings each t
    '''
    consumption_tp_forever = output_tp_forever + interest_earning_cost_forever
    utilityperiod_forever = crra_inst.utility_consumption_crra(consumption_tp_forever)

    '''
    D. infinity sum
    '''
    utility_forever = (1 / (1 - beta)) * utilityperiod_forever

    return utility_forever
