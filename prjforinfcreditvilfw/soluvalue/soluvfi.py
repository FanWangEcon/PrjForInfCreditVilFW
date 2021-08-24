'''
Created on Mar 6, 2017 for Thai human capital
Created on Dec 11, 2017 Copied here

@author: fan

Value Function Iteration of Course
'''
import logging
import numpy as np

import soluvalue.optimax as opti_tool

logger = logging.getLogger(__name__)


def vfi_todayfixed(mjall_inst, minterp_inst,
                   lgit_inst, param_inst,
                   pool=None, info=False):
    """
    if param_inst.interpolant['interp_type'] == loginf
        then running through this code does nothing, but we are still teseting the
        loop structure here, with loginf, ufuture follows that deterministic function system
        unless maxinter = 0    
    """
    states_vfi_dim = param_inst.grid_param['len_states']
    shocks_vfi_dim = param_inst.grid_param['len_shocks']
    choices_vfi_dim = param_inst.grid_param['len_choices']
    logger.info('states_vfi_dim:%s, shocks_vfi_dim:%s, choices_vfi_dim:%s'
                , states_vfi_dim, shocks_vfi_dim, choices_vfi_dim)

    interpolant = param_inst.interpolant

    # To Store Results
    if (info):
        interpolant_hist = []

    # Converge Criteria

    maxinter = interpolant['maxinter']
    cur_iter = 0

    # lagged EjV
    EjV_lag = None
    fl_gap = np.inf
    ar_fl_gap = np.zeros([maxinter, 1])
    fl_threshold = 0.00001

    # Today U, Fixed
    utoday_stack = mjall_inst.get_utoday()

    while cur_iter < maxinter and fl_gap > fl_threshold:
        logger.info('cur_iter:%s, maxinter:%s', cur_iter, maxinter)

        # Future U, Varies by Interpolant 
        ufuture_stack = mjall_inst.get_ufuture(interpolant)

        # Combine for lifetime
        ulife_stack = mjall_inst.get_ulifetime(utoday_stack, ufuture_stack)

        # Max Choice Along Each Borrow Save Cate
        util_opti_stack, argmax_index = opti_tool.opti_value_eachj(
            ulife_stack,
            states_vfi_dim * shocks_vfi_dim,
            choices_vfi_dim)

        # get E_{j}(V): Integration Step over J, over Eps
        each_j_prob, EjV = lgit_inst.integrate_prob(util_opti_stack)

        # Interpolate
        interpolant = minterp_inst.update_interpolant(EjV, interpolant)

        # Emax Reg Coef Gap
        if (info):
            interpolant_hist.append(interpolant)

        cur_iter = cur_iter + 1

        if EjV_lag is None:
            EjV_lag = EjV
        else:
            fl_gap = np.max(abs(EjV_lag - EjV) ** 2)
            ar_fl_gap[cur_iter - 1, :] = fl_gap
            EjV_lag = EjV

    ar_fl_gap = ar_fl_gap[0:cur_iter - 1, :]
    logger.info(f'{ar_fl_gap=}')

    if (info):
        return interpolant, interpolant_hist
    else:
        return interpolant
