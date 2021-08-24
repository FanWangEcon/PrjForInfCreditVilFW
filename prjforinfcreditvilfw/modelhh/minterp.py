'''
Created on Dec 13, 2017

@author: fan

'''

import modelhh.future.future_forgegeom as u_forgegeom
import modelhh.future.future_forgegeom_reuse as u_forgegeom_reuse
import modelhh.future.future_griddata as u_griddata
import modelhh.future.future_polyquad as u_polyquad


class UlifeInterpolate():

    def __init__(self, bdgt_inst, prod_inst, param_inst,
                 B_V, K_V, eps_V,
                 B_Veps, K_Veps, eps_Veps,
                 B_Vepszr, K_Vepszr):
        """Interpolation Entry point
        
        The method I use here is similar to Imai Keane
        
        Parameters
        ----------
        b_vec: 1d array
            meshes between all statkes, in this case b and k, for b 
        k_vec: 1d array
            meshes between all statkes, in this case b and k, for k             
        """

        self.bdgt_inst = bdgt_inst
        self.prod_inst = prod_inst
        self.param_inst = param_inst

        self.B_V = B_V
        self.K_V = K_V
        self.eps_V = eps_V

        self.B_Veps = B_Veps
        self.K_Veps = K_Veps
        self.eps_Veps = eps_Veps

        self.B_Vepszr = B_Vepszr
        self.K_Vepszr = K_Vepszr
        self.eps_Vepszr = 0

        self.A = param_inst.data_param['A']

    def gen_vecs(self):
        pass

    def update_interpolant(self, EjV, interpolant):
        """Return Integrated Future Value        
        """
        interp_type = interpolant['interp_type']

        if (interp_type[0] == "loginf"):
            'nothing to do here'
            pass

        func_use = None
        if (interp_type[0] == "forgegeom"):
            if (interpolant['pre_save']):
                func_use = u_forgegeom_reuse.get_interpolant
            else:
                func_use = u_forgegeom.get_interpolant
        if (interp_type[0] == "polyquad"):
            func_use = u_polyquad.get_interpolant
        if (interp_type[0] == "griddata"):
            func_use = u_griddata.get_interpolant

        if (func_use is not None):
            interpolant = func_use(
                interpolant,
                self.bdgt_inst, self.prod_inst, self.param_inst,
                EjV,
                self.B_V, self.K_V, self.A, self.eps_V,
                self.B_Veps, self.K_Veps, self.A, self.eps_Veps,
                self.B_Vepszr, self.K_Vepszr, self.A, self.eps_Vepszr)

        return interpolant
