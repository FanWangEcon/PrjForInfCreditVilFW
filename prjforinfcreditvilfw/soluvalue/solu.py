'''
Created on Mar 7, 2017 for Thai Human Capital
Created on Dec 11, 2017 Copied here
@author: fan

Given Data Matrix, Find Optimal Continuous Choices within each of 7 categories
the value at each of 7th optimal is treated that as choices speicific utility
Integrated over logistic shocks, the output is first step integrated utility.
'''

import logging

import soluvalue.genmodel as genmodel
import soluvalue.solumain as solumain
import soluvalue.soluvfi as soluvfi
import soluvalue.soluvfi_cev as soluvfi_cev

logger = logging.getLogger(__name__)


def solve_model(param_combo=None,
                param_update_dict_solu=False,
                pool=None, info=False,
                directory_str_dict=None,
                graph_list=None):
    """Obtain Optimal choices
    
    Parameters
    ----------
    grid_type: list
        for grid Paramter: [filename, fileoption]: ['a',1]
        if grid_solu_type == None, grid_type applies to both vfi and solu
    esti_type
        for esti parameters: [filename, fileoption]: ['a',1]
        if solu_esti_type == None, esti_type applies to both vfi and solu
    grid_solu_type
        if this is true, grid_type applies to vfi, grid_solu_type to solu    
    solu_esti_type
        if this is true, esti_type applies to vfi, solu_esti_type to solu
    """

    logger.info('1. vfi')

    mjall_inst, minterp_inst, lgit_inst, param_inst = \
        genmodel.gen_model_instances(param_combo=param_combo,
                                     data=None, data_map=None)
    interpolant = soluvfi.vfi_todayfixed(mjall_inst, minterp_inst,
                                         lgit_inst, param_inst,
                                         pool, info=False)

    logger.info('2. Solution if')
    if param_update_dict_solu:
        # if grid for vfi and solu are the same       
        solu_dict = solumain.solve_optimal_manage(mjall_inst, lgit_inst, param_inst,
                                                  interpolant,
                                                  pool=pool, info=True,
                                                  directory_str_dict=directory_str_dict,
                                                  graph_list=graph_list)
    else:
        solu_dict, mjall_inst = solve_model_with_interpolant(
            interpolant=interpolant,
            param_combo=param_combo,
            pool=pool, info=True,
            directory_str_dict=directory_str_dict,
            graph_list=graph_list)

    if 'CEV_PROP_INCREASE' in param_inst.esti_param:
        CEV_PROP_INCREASE = param_inst.esti_param['CEV_PROP_INCREASE']
        EjV, *_ = soluvfi_cev.vfi_todayfixed_cev(mjall_inst, minterp_inst,
                                                 lgit_inst, param_inst,
                                                 interpolant=interpolant,
                                                 solu_dict=solu_dict)
        solu_dict['EjV'] = EjV

    return interpolant, solu_dict, mjall_inst, param_inst


def solve_model_with_interpolant(interpolant,
                                 param_combo=None,
                                 data=None, data_map=None,
                                 pool=None, info=False,
                                 directory_str_dict=None,
                                 graph_list=None):
    mjall_inst, __, lgit_inst, param_inst = \
        genmodel.gen_model_instances(param_combo=param_combo,
                                     data=data,
                                     data_map=data_map)

    solu_dict = solumain.solve_optimal_manage(mjall_inst, lgit_inst, param_inst,
                                              interpolant,
                                              pool=pool, info=info,
                                              directory_str_dict=directory_str_dict,
                                              graph_list=graph_list)

    return solu_dict, mjall_inst
