'''
Created on Jun 26, 2017

@author: fan
'''

import numpy as np


class PeriodUtility():
    """Calculates per period utility.
    
    invoke this separately from future because sometimes future utility might
    be dealt with differently depending on 
    """

    def __init__(self, param_inst):
        """Gets all model parametesr and disects data vectors.            
        """

        # Preference
        self.rho = param_inst.esti_param['rho']
        self.c_min_bound = param_inst.esti_param['c_min_bound']

    def utility_consumption_crra(self, consumption):
        """Utility from consumption.
        """

        if np.isscalar(consumption):
            if consumption < self.c_min_bound:
                consumption = self.c_min_bound
        else:
            consumption[consumption < self.c_min_bound] = self.c_min_bound

        if 0.982 <= self.rho <= 1e-3:
            u_c = np.log(consumption)
        else:
            u_c = (consumption ** (1 - self.rho)) / (1 - self.rho)
        #         u_c = np.log(consumption)
        return u_c
