'''
Created on Jun 26, 2017

@author: fan
import modelhh.functions.production as prod
'''
import numpy as np
import pyfan.devel.obj.classobjsupport as Clsobj_Sup


def cobb_douglas_nolabor_external(eps, A, k_t, alpha_k, alphaed=False):
    """
    import modelhh.functions.production as prod
    cobb_douglas_nolabor_external(eps, A, k_t, alpha_k, alphaed=True)
    """
    esti_param = {'alpha_k': alpha_k}
    attribute_array = ['esti_param']
    attribute_values_array = [esti_param]
    param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
    prod_inst = ProductionFunction(param_inst)

    Y_partial = prod_inst.cobb_douglas_nolabor(eps, A, k_t, alphaed=alphaed)
    return Y_partial


class ProductionFunction():

    def __init__(self, param_inst):
        """Gets all model parametesr and disects data vectors
    
        invoke this separately from future because sometimes future utility might
        be dealt with differently depending on 
        """

        # Production Function
        self.alpha_k = param_inst.esti_param['alpha_k']

    def cobb_douglas_nolabor(self, eps_t, A, k_t, alphaed=True):
        """ 
        """
        k_alpha = self.k_alpha(k_t, alphaed)
        k_alpha_ae = self.k_alpha_ae(eps_t, A, k_alpha)
        y = k_alpha_ae

        return y

    def k_alpha(self, k_t, alphaed=True):
        """K to the power of alpha_k
        Perhaps values for k grid are already alphaed, as is the case during VFI
        if we are outside of VFI, data could be in the form of k, not k to 
        alpha_k power
        """

        if (alphaed):
            return k_t
        else:
            return k_t ** self.alpha_k

    def k_alpha_ae(self, eps_t, A, k_alpha):
        return np.exp(A + eps_t) * k_alpha
