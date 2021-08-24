'''
Created on Mar 30, 2018

@author: fan
'''

import dataandgrid.genshocks as genshocks
import parameters.paraminstpreset as paraminstpreset
import solusteady.iterhist as iterhist
import soluvalue.solu as solu


def simu_solve(param_update_dict=None):
    """    
    data_type: 1, get mean and sd; 2, pick one from tic list
    """
    param_inst_name = 'simu_solve'
    param_inst = paraminstpreset.get_param_inst_preset(
        param_update_dict=param_update_dict,
        title=param_inst_name)

    mean_A = param_inst.data_param['mean_A']
    std_A = param_inst.data_param['std_A']
    len_A = param_inst.data_param['len_A']

    A_solve_tics = genshocks.stateSpaceShocks(
        mean_A, std_A, len_A,
        draw_type=1)

    store_list = []
    cur_data_type = param_update_dict['data_type']
    for ctr, A_cur in enumerate(A_solve_tics):
        data_type = [cur_data_type[0], {'A': A_cur, 'Region': 0, 'Year': 0}]
        param_update_dict['data_type'] = data_type
        store, store_map = simulate_eachA(A_cur, param_update_dict)
        store_list.append(store)

    return store_list, store_map


def simulate_eachA(A_cur, param_update_dict):
    """
    
    Coll = []
    Given unobserved types:
        1. V(A)=VFI(A): solve model for each unobserved type
        2. H(A)=HIST(VFI(A))
        3. G(A)=AGGREGATE(HIST(VFI(A)))        
    
    Coleect V, H, G for different A
    
    What are the proportions of A types?
    
    solve for sd(A) from equilibrium
    
    given sd(A), sum up 
    
    orivude H(A) and G(A) to estimation tool
    """

    interpolant, solu_dict, mjall_inst, param_inst = \
        solu.solve_model(param_update_dict)

    store, store_map = iterhist.simu_history_solve(
        A_cur,
        mjall_inst, interpolant,
        grid_type, esti_type, data_type,
        param_inst)
    return store, store_map
