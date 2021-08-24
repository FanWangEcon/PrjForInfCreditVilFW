'''
Similar to :func:`soluvfi`, if here, means the CEV_PROP_INCREASE>0. Need to first
solve the model as in :func:`soluvfi`, then iterate for the same number of times,
to get the value based on proportional consumption increase holding policy function
fixed. Note that this is needed because thie nesting of shocks with CRRA, which makes
extracting the CEV proportional coefficient out of Value expectation as a multiplicative
term not possible.
'''

import logging
import numpy as np

import soluvalue.optimax as opti_tool
import soluvalue.optimax_cev as opti_tool_cev

logger = logging.getLogger(__name__)


def vfi_todayfixed_cev(mjall_inst, minterp_inst,
                       lgit_inst, param_inst,
                       interpolant=None,
                       solu_dict=None,
                       pool=None, info=False):
    """
    Solve for value function (and policies)
    """

    # see G:\repos\R4Econ\math\func_utility\fs_mlogit_crra.Rmd
    CEV_PROP_INCREASE = param_inst.esti_param['CEV_PROP_INCREASE']
    rho = param_inst.esti_param['rho']
    fl_cev_utoday_shift = (1 + CEV_PROP_INCREASE) ** (1 - rho)

    states_vfi_dim = param_inst.grid_param['len_states']
    shocks_vfi_dim = param_inst.grid_param['len_shocks']
    choices_vfi_dim = param_inst.grid_param['len_choices']
    logger.info('states_vfi_dim:%s, shocks_vfi_dim:%s, choices_vfi_dim:%s'
                , states_vfi_dim, shocks_vfi_dim, choices_vfi_dim)

    if interpolant is None:
        interpolant = param_inst.interpolant

    # To Store Results
    if info:
        interpolant_hist = []

    # Converge Criteria
    maxinter = interpolant['maxinter']

    """
    First Proceed as in :func:`soluvfi`
    """

    # lagged EjV
    EjV_lag = None
    fl_gap = np.inf
    ar_fl_gap = np.zeros([maxinter, 1])
    fl_threshold = 0.00001

    # Today U, Fixed
    utoday_stack = mjall_inst.get_utoday()
    utoday_stack = fl_cev_utoday_shift * utoday_stack

    # do the optimal policies and interpolants already exist?
    if solu_dict is None:
        it_soluvfi_iter = 0
    else:
        argmax_index = solu_dict['argmax_index']
        it_soluvfi_iter = maxinter

    # CEV iter starts at zero
    it_cev_iter = 0
    cur_iter = 0

    while (it_soluvfi_iter < maxinter or it_cev_iter < maxinter) \
            and (fl_gap > fl_threshold):

        # Print iteration Status
        logger.info(f'{cur_iter=}, {it_soluvfi_iter=}, {it_cev_iter=}')

        # Future U, Varies by Interpolant
        ufuture_stack = mjall_inst.get_ufuture(interpolant)

        # Combine for lifetime
        ulife_stack = mjall_inst.get_ulifetime(utoday_stack, ufuture_stack)

        # Max Choice Along Each Borrow Save Cate
        if it_soluvfi_iter < maxinter:
            # Updating policy functions and choices
            util_opti_stack, argmax_index = opti_tool.opti_value_eachj(
                ulife_stack,
                states_vfi_dim * shocks_vfi_dim,
                choices_vfi_dim)
        else:
            # argmax_index is from last iteration from soluvfi above
            # no longer changing optimal policy function choices
            util_opti_stack = opti_tool_cev.opti_value_eachj_cev(
                ulife_stack,
                argmax_index,
                states_vfi_dim * shocks_vfi_dim)

        # get E_{j}(V): Integration Step over J, over Eps
        each_j_prob, EjV = lgit_inst.integrate_prob(util_opti_stack)

        # Interpolate
        interpolant = minterp_inst.update_interpolant(EjV, interpolant)

        # Iterators
        if it_soluvfi_iter < maxinter:
            it_soluvfi_iter = it_soluvfi_iter + 1
        else:
            it_cev_iter = it_cev_iter + 1

        cur_iter = cur_iter + 1

        if EjV_lag is None:
            EjV_lag = EjV
        else:
            fl_gap = np.max(abs(EjV_lag - EjV) ** 2)
            ar_fl_gap[cur_iter - 1, :] = fl_gap
            EjV_lag = EjV

    ar_fl_gap = ar_fl_gap[0:cur_iter - 1, :]
    logger.info(f'{ar_fl_gap=}')

    if info:
        return EjV, interpolant, interpolant_hist
    else:
        return EjV, interpolant
