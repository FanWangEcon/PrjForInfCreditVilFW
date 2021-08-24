'''
Created on Dec 16, 2017

@author: fan

Code largely from thai Human Capital
'''

import numpy as np

import dataandgrid.fixed.policytics as policytics

#
# def stateshockchoice_expand(statespace_matrix, shockspace_matrix, choicespace_matrix, cont_choice_count=1):
#     
#     #===========================================================================
#     # print 'statespace_matrix:{0},shockspace_matrix:{1},shockspace_matrix:{2}'.format(statespace_matrix.shape, shockspace_matrix.shape, choicespace_matrix.shape)
#     # print 'statespace_matrix:{0},shockspace_matrix:{1},shockspace_matrix:{2}'.format(statespace_matrix, shockspace_matrix, choicespace_matrix)
#     #===========================================================================
#     
#     #only numpy array    
#     statespace_ele_len = len(statespace_matrix[:,0])
#     shockspace_ele_len = len(shockspace_matrix[:,0])
#     # print 'len(choicespace_matrix[:,0]):{0},len(choicespace_matrix):{1}'.format(len(choicespace_matrix[:,0]),len(choicespace_matrix))
#     choicespace_ele_len = len(choicespace_matrix[:,0])     
#     choicespace_ele_cols = len(choicespace_matrix[0,:])
#     
#     total_len = statespace_ele_len*shockspace_ele_len*choicespace_ele_len
#     #===========================================================================
#     # print 'statespace_ele_len:{0},shockspace_ele_len:{1},choicespace_ele_len:{2},choicespace_ele_cols:{3}'.format(statespace_ele_len, shockspace_ele_len, choicespace_ele_len,choicespace_ele_cols)
#     #===========================================================================
#         
#     statespace_matrix_out = np.repeat(statespace_matrix,shockspace_ele_len,axis=0)
#     shockspace_matrix_out = np.tile(shockspace_matrix,(statespace_ele_len,1))
# 
#     statespace_matrix_out = np.repeat(statespace_matrix_out,choicespace_ele_len,axis=0)
#     shockspace_matrix_out = np.repeat(shockspace_matrix_out,choicespace_ele_len,axis=0)
#         
#     # To increase sensitivity of choices and likelihood to changing parameters, turn this into a ratio    
#     choicespace_matrix_out = policytics.gentics()
#         
#     # different tics for each continuous choices: 1, number of continuous choices    
#     
#     return statespace_matrix_out, shockspace_matrix_out, choicespace_matrix_out 


'''
Created on Mar 18, 2017

@author: fan
'''

import numpy as np


class ModelGrids():
    """Grids for model
    
    for these grids, often only needed to be generated once in entire estimation
    procedure    
    """

    def __init__(self, hhp_inst):

        self.b_state_minmaxgrid = hhp_inst.b_state_minmaxgrid
        self.k_state_minmaxgrid = hhp_inst.k_state_minmaxgrid
        self.epsilon_state_meansdminmaxgrid = hhp_inst.epsilon_state_meansdminmaxgrid

        self.bp_policy_minmaxgrid = hhp_inst.bp_policy_minmaxgrid
        self.kp_policy_minmaxgrid = hhp_inst.kp_policy_minmaxgrid
        self.child_work_hour_policy_minmaxgrid = hhp_inst.child_work_hour_policy_minmaxgrid

        self.state_gridtype = hhp_inst.state_gridtype
        self.shock_gridtype = hhp_inst.shock_gridtype
        self.policy_gridtype = hhp_inst.policy_gridtype

        self.child_school_hour_min = hhp_inst.child_school_hour_min

    def states_shock_mesh(self,
                          states_mat=None, states_index=None,
                          shocks_mat=None, shocks_index=None,
                          vfigrid=True,
                          shock_zero=True, return_shk_min_max=False):
        """Permutation States Matrix joint shocks        
        """
        'States can be fed in externally, such as in real data'
        if (states_mat == None):
            states_mat, states_index = \
                meshstates.state_grids(self.b_state_minmaxgrid, self.k_state_minmaxgrid, \
                                       vfigrid, self.state_gridtype)

        if (shock_zero == True and return_shk_min_max == False):
            'Do not Generate Shocks in VFI'
            shocks_mat = np.zeros((len(states_mat[:, 0]), 1))
            shocks_index = ['epsilon']
            states_shock_mat = np.column_stack((states_mat, shocks_mat))
        else:
            if (shock_zero == True and return_shk_min_max == True):
                _, shocks_index, epsilon_f_minmax = \
                    meshshock.shock_grids(self.epsilon_state_meansdminmaxgrid, \
                                          vfigrid, self.shock_gridtype,
                                          return_shk_min_max)
                shocks_mat = np.reshape(epsilon_f_minmax, (-1, 1))
            else:
                if (shocks_mat == None):
                    'Generate Shocks in VFI Integration step, or in estimation policy'
                    shocks_mat, shocks_index = \
                        meshshock.shock_grids(self.epsilon_state_meansdminmaxgrid, \
                                              vfigrid, self.shock_gridtype)

            'Mesh States and Shocks together'
            states_shock_mat = arraycontrol.two_mat_mesh(
                states_mat, shocks_mat, return_joint=True)

        states_shock_index = states_index + shocks_index

        return states_shock_mat, states_shock_index

    def states_shock_policy_mesh(self,
                                 states_mat=None, states_index=None,
                                 shocks_mat=None, shocks_index=None,
                                 policy_mat=None, policy_index=None,
                                 vfigrid=True,
                                 shock_zero=True, return_shk_min_max=False):
        """Permutation States Matrix joint shocks        
        """

        'Get states and Policy'
        states_shock_mat, states_shock_index = self.states_shock_mesh(
            states_mat, states_index,
            shocks_mat, shocks_index,
            vfigrid, shock_zero, return_shk_min_max)

        'policy can be fed in externaly for whatever reason'
        if (policy_mat == None):
            policy_mat, policy_index = \
                meshpolicy.policy_grids(self.bp_policy_minmaxgrid,
                                        self.kp_policy_minmaxgrid,
                                        self.child_work_hour_policy_minmaxgrid,
                                        vfigrid, self.policy_gridtype,
                                        self.child_school_hour_min)

        'Mesh states and policy'
        states_shock_policy_mat = arraycontrol.two_mat_mesh(
            states_shock_mat, policy_mat, return_joint=True)
        states_shock_policy_index = states_shock_index + policy_index

        'return'
        return states_shock_policy_mat, states_shock_policy_index
