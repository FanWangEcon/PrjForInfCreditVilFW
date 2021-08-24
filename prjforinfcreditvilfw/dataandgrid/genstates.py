'''
Created on Dec 16, 2017

@author: fan

Directly copied over function from /src/ProjectDisertCredit/Simulation.py
    method stateSpaceEmaxRand

'''

import numpy as np
import pyfan.amto.array.geomspace as geomspace

import logging

logger = logging.getLogger(__name__)


def state_grids_fi(param_inst, bdgt_inst, fixed_unif_grid, seed=1230):
    "fi stands for from instance"

    len_states = param_inst.grid_param['len_states']
    len_k_start = param_inst.grid_param['len_k_start']

    max_kapital = param_inst.grid_param['max_kapital']
    min_kapital = param_inst.grid_param['min_kapital']
    max_netborrsave = param_inst.grid_param['max_netborrsave']

    kapital_points, netborrsave_points, param_inst = state_grids(
        param_inst, bdgt_inst,
        max_kapital, min_kapital, max_netborrsave,
        len_states, len_k_start, fixed_unif_grid, seed)

    return kapital_points, netborrsave_points


def state_grids(param_inst, bdgt_inst,
                max_kapital, min_kapital, max_netborrsave,
                len_states, len_k_start,
                fixed_unif_grid=True, seed=1230):
    """Generate State Grid that conforms to model
    
    1. can not have so much borrowing that k is not enough to repay
    2. try to have even states for k and b
    
    Parameters
    ----------
    len_states: integer
        total state grid length, actually just k and b len multiplied
    K_discretePoints_start: integer
        a much smaller number than len_states, the initial len of k vec. 
        
    modelParameters().stateSpaceEmaxRand(useExisting=True,printResults=True)
    """

    #     max_kapital_log = np.log(max_kapital)

    logger.debug('max_kapital %s, min_kapital: %s, max_netborrsave: %s ',
                 max_kapital, min_kapital, max_netborrsave)
    logger.debug('len_states %s, len_k_start: %s, fixed_unif_grid: %s ',
                 len_states, len_k_start, fixed_unif_grid)

    #         if (useExisting == True):
    #             np.random.seed(seed)
    #             normal1 = simuSup.stateSpacePoints().genNormalBase(len_states)
    #             normal2 = simuSup.stateSpacePoints().genNormalBase(len_states)
    #
    #         if (useExisting == False):
    #             normal1 = simuSup.stateSpacePoints().genNormalBase(len_states)
    #             normal2 = simuSup.stateSpacePoints().genNormalBase(len_states)
    #
    #         kapital_points = mean_kapital + normal1 * std_kapital
    #         netborrsave_points = mean_netborrsave + normal2 * std_netborrsave

    if (fixed_unif_grid):
        #         len_K_start = 5
        remainder_cur = 1
        while (remainder_cur != 0):
            K_discretePoints = len_k_start
            B_discretePoints = int(len_states / K_discretePoints)
            remainder_cur = len_states % K_discretePoints
            len_k_start = len_k_start + 1
            logger.debug('K_discretePoints: %s, B_discretePoints: %s, remainder_cur: %s',
                         K_discretePoints, B_discretePoints, remainder_cur)

        'uniform grid for k, few points'
        #         unif1 = np.linspace(0,1,K_discretePoints)

        method_0523 = False
        if (method_0523):
            unif1_lin = np.linspace(0, 1, K_discretePoints - int(K_discretePoints / 2))
            unif1_geom = np.geomspace(unif1_lin[1] / 4, 1, int(K_discretePoints / 2))
            unif1 = np.append(unif1_lin, unif1_geom)
            unif1 = np.sort(unif1)
        else:
            '''Thought more about geospace, understood it, created my version
            with geom_ratio = 1.03:
                starts with 1 percent, then up to 4 percent gap, can see in gen_geom_grid tester file
                geomspace.py - gen_geom_grid - 50 -  2018-05-24 12:11:44,231 - DEBUG geom_base_scaled:
                    [0.    0.009 0.019 0.028 0.039 0.049 0.06  0.071 0.082 0.094 0.106 0.118 0.131 0.144 0.157 0.171
                     0.186 0.2   0.216 0.231 0.248 0.264 0.281 0.299 0.317 0.336 0.355 0.375 0.396 0.417 0.438 0.461
                     0.484 0.507 0.532 0.557 0.583 0.61  0.637 0.666 0.695 0.725 0.756 0.788 0.82  0.854 0.889 0.925
                     0.962 1.   ]
                geomspace.py - gen_geom_grid - 52 -  2018-05-24 12:11:44,232 - DEBUG geom_base_scaled diff:
                    [0.009 0.009 0.01  0.01  0.01  0.011 0.011 0.011 0.012 0.012 0.012 0.013 0.013 0.014 0.014 0.014
                     0.015 0.015 0.016 0.016 0.017 0.017 0.018 0.018 0.019 0.019 0.02  0.02  0.021 0.022 0.022 0.023
                     0.024 0.024 0.025 0.026 0.027 0.028 0.028 0.029 0.03  0.031 0.032 0.033 0.034 0.035 0.036 0.037
                     0.038]            
            '''
            start = 0
            stop = 1
            num = K_discretePoints
            '''this value is a parameter value. It's too deeply nested here, can't reach with params so hard-code. 1.03 hard code all'''
            geom_ratio = 1.03
            unif1, __, __, __, __, = geomspace.gen_geom_grid(start, stop, num, geom_ratio, a=1)

        unif1 = np.repeat(unif1, B_discretePoints, axis=0)

        'b grid'
        #         unif2 = np.linspace(0,1,B_discretePoints)
        start = 0
        stop = 1
        num = B_discretePoints
        geom_ratio = 1.03
        unif2, __, __, __, __, = geomspace.gen_geom_grid(start, stop, num, geom_ratio, a=1)
        #         unif2 = np.geomspace(0.01,1,B_discretePoints-1)
        #         unif2 = np.insert(unif2, 0, 0)

        unif2 = np.tile(unif2, (K_discretePoints, 1))
        # unif2 = np.ravel(unif2, 0)
        unif2 = np.ravel(unif2)

    else:
        np.random.seed(seed)
        unif1 = np.random.uniform(0, 1, len_states)
        np.random.seed(seed + 239)
        unif2 = np.random.uniform(0, 1, len_states)

    '''
        Although this is in K and B space, Emax is in Cash and K space, want Cash and K to be a Box
        Max Cash, given our K and B grid (assuming shock = -inf for produ function):
            (Kmax)*(1-depreciation) + (Bmax)
        Min Cash, zero:
            Bmin = -(Kmax)*(1-depreciation) 
                      
        cash_max = max_kapital*(1 - DELTA_DEPRE) + max_netborrsave
        #=======================================================================
        # unif1[0] = 0
        # unif1[len_states-1] = 1
        # unif2[0] = 0
        # unif2[len_states-1] = 1
        #=======================================================================
        maxNegB = - (kapital_points * (1 - DELTA_DEPRE))
        maxPosB = cash_max - kapital_points*(1 - DELTA_DEPRE)                            

        maxNegB = - (kapital_points * (1 - DELTA_DEPRE))        
        choiceB_tooneg = (netborrsave_points < maxNegB)
        netborrsave_points[choiceB_tooneg] = maxNegB[choiceB_tooneg]
    '''

    cash_max = bdgt_inst.cash(Y=0, k_tt=max_kapital, b_tt=max_netborrsave)
    logger.debug('cash_max: %s', cash_max)

    kapital_points = min_kapital + unif1 * (max_kapital - min_kapital)

    k_depreciate = bdgt_inst.k_depreciate(kapital_points)
    logger.debug('min(kapital_points) %s, max(kapital_points): %s',
                 min(kapital_points), max(kapital_points))

    maxNegB = - k_depreciate
    maxPosB = cash_max - k_depreciate

    netborrsave_points = maxNegB + unif2 * (maxPosB - maxNegB)
    logger.debug('min(netborrsave_points) %s, max(netborrsave_points): %s',
                 min(netborrsave_points), max(netborrsave_points))

    '''
    Return Sequenceis crucial, can not change,
    '''
    logger.debug('kapital_points, netborrsave_points:\n%s',
                 np.column_stack((kapital_points, netborrsave_points)))

    return kapital_points, netborrsave_points, param_inst


def max_min_K_B_sqr(param_inst):
    """
    Based on formula above, what are max K and B, B transformed to rectangle?
    This is what is shown is the KCOH graphs:
        C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_genstates
    """

    K_DEPRECIATION = param_inst.esti_param['K_DEPRECIATION']

    max_kapital = param_inst.grid_param['max_kapital']
    min_kapital = param_inst.grid_param['min_kapital']
    max_netborrsave = param_inst.grid_param['max_netborrsave']

    B_Vepszr_square_max = max_kapital * (1 - K_DEPRECIATION) + max_netborrsave
    B_Vepszr_square_min = 0

    K_Vepszr_square_max = max_kapital
    K_Vepszr_square_min = min_kapital

    return B_Vepszr_square_max, B_Vepszr_square_min, K_Vepszr_square_max, K_Vepszr_square_min
