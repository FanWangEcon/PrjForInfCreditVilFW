'''
Created on Dec 12, 2017

@author: fan
'''
import logging
import numpy as np
import pyfan.stats.multinomial.multilogit as multilogit

logger = logging.getLogger(__name__)


class MultinomialLogitU():
    '''
    classdocs
    
    In model, across choices, there is a logit based integration. This is not
    optimal choice. 
    Anything related to adding things up for multinomial logit
    '''

    def __init__(self, param_inst):
        '''
        Constructor
        
        do not rescale in mlogit, because tha tmight double divide future_u
        by scale.
        '''
        self.logit_sd_scale = param_inst.esti_param['logit_sd_scale']
        self.mlogit_inst = multilogit.UtilityMultiNomial(scale_coef=self.logit_sd_scale)

    def integrate_prob(self, all_J_indirect_utility):
        """
        can't do this for utotal because would be dividing twice 
        """
        each_j_prob, optiV_Exp7 = self.mlogit_inst.get_outputs(all_J_indirect_utility)

        logger.debug('optiV_Exp7, each_j_prob:\n%s', np.column_stack((optiV_Exp7, each_j_prob)))

        return each_j_prob, optiV_Exp7
