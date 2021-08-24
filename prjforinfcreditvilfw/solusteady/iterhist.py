'''
Created on Dec 18, 2017

@author: fan

Given value function interpolant, and initial states, iterate over time, either
using interpolated policy function, or resolving every period

'''

import numpy as np
import pyfan.stats.interpolate.interpolate2d as interp2d

import dataandgrid.genshocks as genshocks
import soluvalue.solu as solu


def simu_history_interp(mjall_inst,
                        ktp_interpolant, btp_interpolant,
                        param_inst):
    k_tt = mjall_inst.k_tt
    b_tt = mjall_inst.b_tt

    iter_periods = param_inst.model_option['simu_iter_periods']
    simu_indi_count = param_inst.model_option['simu_indi_count']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']

    store_map = {'id': 0, 't': 1, 'k': 2, 'b': 3, 'eps': 4, 'y': 5, 'cash': 6}
    store = np.zeros((simu_indi_count, iter_periods, len(store_map)))

    period_not_save = 10
    strctr = 0
    for itercur in np.arange(iter_periods):

        epsvec_cur = genshocks.stateSpaceShocks(
            mean_eps, std_eps, simu_indi_count,
            seed=itercur + 123,
            draw_type=2)

        if (itercur == 0):
            k_cur = np.zeros(epsvec_cur.shape) + np.mean(k_tt)
            b_cur = np.zeros(epsvec_cur.shape) + np.mean(b_tt)

        cash_tt, y = mjall_inst.utoday_inst.get_cash(
            A=param_inst.data_param['A'],
            eps_tt=epsvec_cur,
            k_tt=k_cur, b_tt=b_cur)

        if (itercur >= period_not_save):
            store[:, strctr, store_map['id']] = np.arange(0, simu_indi_count)
            store[:, strctr, store_map['t']] = itercur
            store[:, strctr, store_map['k']] = k_cur
            store[:, strctr, store_map['b']] = b_cur
            store[:, strctr, store_map['eps']] = epsvec_cur
            store[:, strctr, store_map['y']] = y
            store[:, strctr, store_map['cash']] = cash_tt
            strctr = strctr + 1

        k_cur = interp2d.interpRbf2D(k_cur, cash_tt, interpolant=ktp_interpolant)
        b_cur = interp2d.interpRbf2D(k_cur, cash_tt, interpolant=btp_interpolant)

    return store, store_map


def simu_history_solve(A_cur, mjall_inst, interpolant,
                       grid_type, esti_type, data_type,
                       param_inst):
    k_tt = mjall_inst.k_tt
    b_tt = mjall_inst.b_tt

    iter_periods = param_inst.model_option['simu_iter_periods']
    simu_indi_count = param_inst.model_option['simu_indi_count']
    std_eps = param_inst.grid_param['std_eps']
    mean_eps = param_inst.grid_param['mean_eps']

    store_map = {'id': 0, 't': 1, 'A': 2,
                 'k': 3, 'b': 4, 'eps': 5, 'y': 6, 'cash': 7,
                 'j': 8, 'k_opti': 9, 'b_opti': 10}

    store = np.zeros((simu_indi_count, iter_periods, len(store_map)))

    period_not_save = 10
    strctr = 0
    for itercur in np.arange(period_not_save + iter_periods):
        #  do not store the first 10 periods
        epsvec_cur = genshocks.stateSpaceShocks(
            mean_eps, std_eps, simu_indi_count,
            seed=itercur + 123,
            draw_type=2)

        if (itercur == 0):
            k_cur = np.zeros(epsvec_cur.shape) + np.mean(k_tt)
            b_cur = np.zeros(epsvec_cur.shape) + np.mean(b_tt)

        period_states_data = np.zeros((simu_indi_count, 3))
        period_states_data[:, 0] = k_cur
        period_states_data[:, 1] = b_cur
        period_states_data[:, 2] = epsvec_cur
        period_states_data_map = {'k': 0, 'b': 1, 'eps': 2}

        optimal_choices, ktp_opti, btp_opti, __ = \
            solu.solve_model_with_interpolant(
                interpolant,
                grid_type=grid_type, esti_type=esti_type, data_type=data_type,
                data=period_states_data, data_map=period_states_data_map)

        cash_tt, y = mjall_inst.utoday_inst.get_cash(
            A=param_inst.data_param['A'],
            eps_tt=epsvec_cur,
            k_tt=k_cur, b_tt=b_cur)

        if (itercur >= period_not_save):
            store[:, strctr, store_map['id']] = np.arange(0, simu_indi_count)
            store[:, strctr, store_map['t']] = itercur
            store[:, strctr, store_map['A']] = A_cur

            store[:, strctr, store_map['k']] = k_cur
            store[:, strctr, store_map['b']] = b_cur
            store[:, strctr, store_map['eps']] = epsvec_cur
            store[:, strctr, store_map['y']] = y
            store[:, strctr, store_map['cash']] = cash_tt

            store[:, strctr, store_map['j']] = optimal_choices
            store[:, strctr, store_map['k_opti']] = ktp_opti
            store[:, strctr, store_map['b_opti']] = btp_opti
            strctr = strctr + 1

        k_cur = ktp_opti
        b_cur = btp_opti

    #         store[:, itercur, store_map['eps']]= mjall_inst
    #         store[:, itercur, store_map['y']]  = cash_tt

    return store, store_map
