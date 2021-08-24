'''
Created on Dec 7, 2017

@author: fan

Utility from choosing choice j
'''


class LifeTimeUtility_ChoiceJ():

    def __init__(
            self, param_inst,
            utoday_inst, ufuture_inst,
            A=0, eps_tt=0, k_tt=0, b_tt=0,
            k_tp=0,
            b_tp_borr_for=0, b_tp_borr_inf=0,
            b_tp_save_for=0, b_tp_lend_inf=0):
        # instances joint functions         
        self.utoday_inst = utoday_inst
        self.ufuture_inst = ufuture_inst

        # instance parameter
        self.beta = param_inst.beta

        # State data vectors        
        self.A = A
        self.eps_tt = eps_tt
        self.k_tt = k_tt
        self.k_tp = k_tp

        # Choices data vectors
        self.b_tt = b_tt
        self.b_tp_borr_for = b_tp_borr_for
        self.b_tp_borr_inf = b_tp_borr_inf
        self.b_tp_save_for = b_tp_save_for
        self.b_tp_lend_inf = b_tp_lend_inf

    def get_utoday_btp(self):
        utility_today, y, consumption, cash, b_tp = \
            self.utoday_inst.utility_today(
                A=self.A, eps_tt=self.eps_tt, k_tt=self.k_tt, b_tt=self.b_tt,
                k_tp=self.k_tp,
                b_tp_borr_for=self.b_tp_borr_for, b_tp_borr_inf=self.b_tp_borr_inf,
                b_tp_save_for=self.b_tp_save_for, b_tp_lend_inf=self.b_tp_lend_inf,
                out_all_res=True)

        '''
        after one invoke of get_utoday_btp, b_tp is now fixed
        for get_future invokations. 
        '''
        self.b_tp = b_tp

        return utility_today, y, consumption, cash, b_tp

    def get_future(self, interpolant):
        utility_future = self.ufuture_inst.get_integrated_util_future(
            interpolant,
            b_tp=self.b_tp, k_tp=self.k_tp, A=self.A,
            eps_tt=self.eps_tt, eps_tp=0)

        return utility_future

    def utility_lifetime(self, utility_today, utility_future):
        """Today and future utility discounted
        
        Future value party will get updated every VFI round
        
        """
        return utility_today + self.beta * utility_future
