'''
Created on Aug 6, 2016

@author: fan
'''

import modelhh.future.future_forgegeom as u_forgegeom
import modelhh.future.future_forgegeom_reuse as u_forgegeom_reuse
import modelhh.future.future_griddata as u_griddata
import modelhh.future.future_loginf as u_loginf
import modelhh.future.future_polyquad as u_polyquad


class FutureUtil():
    """Future Utility Main Class
    Return future value given state space known in the last period
    """

    default_interpolant = {'interp_type': 'loginf'}

    def __init__(self,
                 bdgt_inst, prod_inst,
                 crra_inst, param_inst):
        """Constructor
        this is as with others initiated outside of utilitylifetime
        """
        self.bdgt_inst = bdgt_inst
        self.prod_inst = prod_inst
        self.crra_inst = crra_inst
        self.param_inst = param_inst

    def get_integrated_util_future(self, interpolant,
                                   b_tp=0, k_tp=0, A=0, eps_tt=0, eps_tp=0, choice_set_list_j=None):
        """Return Integrated Future Value        
        """

        interp_type = interpolant['interp_type']

        if (interp_type[0] == "loginf"):
            utility_future = u_loginf.future_loginf(
                self.prod_inst, self.crra_inst, self.param_inst,
                b_tp, k_tp, A, eps_tt)

        if (interp_type[0] == "polyquad"):
            EV_type = interp_type[2]
            utility_future = (u_polyquad.func_polyquad_EV_predict(
                interpolant,
                b_tp, k_tp, A,
                approx_type=EV_type))

        if (interp_type[0] == "griddata"):
            utility_future = u_griddata.func_griddata_EV_predict(
                self.param_inst, interpolant, b_tp, k_tp)

        if (interp_type[0] == "forgegeom"):
            if (interpolant['pre_save']):
                utility_future = u_forgegeom_reuse.func_forgegeom_EV_predict(
                    self.param_inst, interpolant,
                    b_tp, k_tp, choice_set_list_j)
            else:
                utility_future = u_forgegeom.func_forgegeom_EV_predict(
                    self.param_inst, interpolant,
                    b_tp, k_tp)

        return utility_future
