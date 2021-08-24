'''
Created on Dec 18, 2017

@author: fan

this provides simulated data, to be matched, looked at together with actually
observed data.
'''

import pyfan.stats.interpolate.interpolate2d as interp2d

import solusteady.iterhist as iterhist
import soluvalue.solu as solu


def simu_interp(param_update_dict=None):

    interpolant, maxof7_overJ, \
    ktp_opti, btp_opti, mjall_inst, param_inst = \
        solu.solve_model(param_update_dict=param_update_dict)

    k_tt = mjall_inst.k_tt
    b_tt = mjall_inst.b_tt
    eps_tt = mjall_inst.eps_tt

    cash_tt, __ = mjall_inst.utoday_inst.get_cash(A=param_inst.data_param['A'],
                                                  eps_tt=eps_tt,
                                                  k_tt=k_tt, b_tt=b_tt)

    ktp_interpolant = interp2d.interpRbf2D(k_tt, cash_tt, ktp_opti)
    btp_interpolant = interp2d.interpRbf2D(k_tt, cash_tt, btp_opti)

    store, store_map = iterhist.simu_history_interp(mjall_inst,
                                                    ktp_interpolant,
                                                    btp_interpolant,
                                                    param_inst)

    return store, store_map
