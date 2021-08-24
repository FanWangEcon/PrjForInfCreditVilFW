'''
Created on Mar 7, 2017 for Thai Human Capital
Created on Dec 11, 2017 Copied here
@author: fan

Given Data Matrix, Find Optimal Continuous Choices within each of 7 categories
the value at each of 7th optimal is treated that as choices speicific utility
Integrated over logistic shocks, the output is first step integrated utility.
'''

import logging
import parameters.model.a_model as param_model_a
import soluvalue.genmodelinner as genmodelinner
import soluvalue.optimax as optimax
import soluvalue.optimax_stack as optimax_stack

logger = logging.getLogger(__name__)


def solve_optimal_manage(mjall_inst, lgit_inst, param_inst,
                         interpolant,
                         pool=None, info=False,
                         directory_str_dict=None,
                         graph_list=None):
    mjall_inst_cur = mjall_inst

    """
    0 to N, zooming in after VFI. If 'CEV_PROP_INCREASE' is not None, this is overridedn to be 0. 
        This leads to policy function that is inconsistent with value function results.
    """
    if 'CEV_PROP_INCREASE' in param_inst.esti_param:
        CEV_PROP_INCREASE = param_inst.esti_param['CEV_PROP_INCREASE']
    else:
        CEV_PROP_INCREASE = None

    if CEV_PROP_INCREASE is None:
        grid_zoom_rounds = param_inst.grid_param['grid_zoom_rounds']
    else:
        grid_zoom_rounds = 0
    inner_iter_loop = range(grid_zoom_rounds + 1)

    for inner_iter in inner_iter_loop:

        return_mid = True
        info_cur = False
        if graph_list is not None:
            if ('graph_choices_i_eachj_polygon' in graph_list):
                '''
                This means we are doing some sort of deep testing
                Want to see grid zooming in getting smaller
                info should be true
                '''
                info_cur = info

        if (inner_iter == inner_iter_loop[-1]):
            info_cur = info
            return_mid = False

        if (inner_iter != 0 and
                interpolant['interp_type'][0] == 'forgegeom' and
                interpolant['pre_save'] == True):
            # Update choice grids
            bktp_geom_dict_null = param_model_a.choice_index_names()['bktp_geom_dict']
            interpolant['bktp_geom'] = bktp_geom_dict_null

        if (directory_str_dict is not None):
            directory_str_dict['graph_mi_polygon_j_suffix'] = '_zm' + str(inner_iter)
        solu_dict = solve_optimal(mjall_inst_cur, lgit_inst, param_inst,
                                  interpolant,
                                  pool=pool, info=info_cur,
                                  return_mid=return_mid,
                                  directory_str_dict=directory_str_dict,
                                  graph_list=graph_list)
        if (return_mid):
            argmax_index = solu_dict['argmax_index']
            mjall_inst_cur = genmodelinner.gen_model_instances_inner(argmax_index, mjall_inst_cur, param_inst)

    return solu_dict


def solve_optimal(mjall_inst, lgit_inst, param_inst,
                  interpolant,
                  pool=None, info=False, return_mid=False,
                  directory_str_dict=None,
                  graph_list=None):
    """Obtain Optimal choices
    
    Parameter
    ---------
    return_mid: Boolean
        return max index for each of 7 choices results
    
    Returns
    -------
    dictionary of arrays
        solu_dict flexible return depending on needs, intermediate, final, info
    """

    states_dim = param_inst.grid_param['len_states']
    shocks_dim = param_inst.grid_param['len_shocks']
    choices_dim = param_inst.grid_param['len_choices']
    choice_set_list = param_inst.model_option['choice_set_list']

    #     proj_sys_sup.jdump(interpolant, 'interpolant', logger=logger.info)

    logger.info('2. Get Total Utility')
    if (info):
        utoday_stack, b_tp_principle_stack, consumption_stack, cash, y, \
        ufuture_stack, btp_stack, ktp_stack, \
        ulifetime_stack, \
        b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack = \
            mjall_inst.get_all_outputs(interpolant=interpolant, check_scalar=False,
                                       directory_str_dict=directory_str_dict,
                                       graph_list=graph_list)
    else:
        utoday_stack = mjall_inst.get_utoday(False)
        ufuture_stack = mjall_inst.get_ufuture(interpolant, False)
        ulifetime_stack = mjall_inst.get_ulifetime(utoday_stack, ufuture_stack)

    logger.info('3. Max over Choices for each j of J')
    util_opti_eachj, argmax_index = optimax.opti_value_eachj(ulifetime_stack,
                                                             ulifetime_stack.shape[0],
                                                             choices_dim)
    if (return_mid):
        solu_dict = {'util_opti_eachj': util_opti_eachj,
                     'argmax_index': argmax_index}
    else:

        logger.info('4. Max over J')
        each_j_prob, EjV = lgit_inst.integrate_prob(util_opti_eachj)
        maxof7_overJ = optimax.max_value_overJ(util_opti_eachj, choice_set_list)

        if (info):

            maxof7_overJ, ktp_opti, btp_opti, consumption_opti, \
            ktp_opti_allJ, btp_opti_allJ, consumption_opti_allJ, \
            btp_fb_opti, btp_ib_opti, btp_fs_opti, btp_il_opti, \
            btp_fb_opti_allJ, btp_ib_opti_allJ, btp_fs_opti_allJ, btp_il_opti_allJ = \
                optimax_stack.get_all_optimalchoices(
                    argmax_index, maxof7_overJ,
                    btp_stack, ktp_stack, consumption_stack,
                    b_tp_borr_for_stack, b_tp_borr_inf_stack, b_tp_save_for_stack, b_tp_lend_inf_stack,
                    ulifetime_stack.shape[0], choice_set_list, param_inst)

            solu_dict = {'EjV': EjV, 'util_opti_eachj': util_opti_eachj,
                         'maxof7_overJ': maxof7_overJ, 'each_j_prob': each_j_prob, 'ktp_opti': ktp_opti,
                         'btp_opti': btp_opti, 'consumption_opti': consumption_opti,
                         'ktp_opti_allJ': ktp_opti_allJ, 'btp_opti_allJ': btp_opti_allJ,
                         'consumption_opti_allJ': consumption_opti_allJ, 'btp_fb_opti_allJ': btp_fb_opti_allJ,
                         'btp_fb_opti': btp_fb_opti, 'btp_ib_opti_allJ': btp_ib_opti_allJ,
                         'btp_ib_opti': btp_ib_opti, 'btp_fs_opti_allJ': btp_fs_opti_allJ,
                         'btp_fs_opti': btp_fs_opti, 'btp_il_opti_allJ': btp_il_opti_allJ,
                         'btp_il_opti': btp_il_opti,
                         'argmax_index': argmax_index}


        else:
            solu_dict = {'maxof7_overJ': maxof7_overJ}

    return solu_dict
