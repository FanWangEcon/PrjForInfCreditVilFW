'''
Created on Jan 29, 2018

@author: fan

This is how soluvalue folder contains interacts with modelhh. Only entry point
from here to modellhh. works jointly with gengrids.  
'''
import logging

import modelhh.functions.budget as bdgt
import modelhh.functions.preference as crra
import modelhh.functions.preflogit as lgit
import modelhh.functions.production as prod
import modelhh.minterp as minterp
import modelhh.mjall as mjall
import modelhh.ufuture as ufuture
import modelhh.utoday as utoday
import parameters.paraminstpreset as param_inst_preset
import soluvalue.gengrids as gengrids

logger = logging.getLogger(__name__)


def get_basic_instances(param_combo):
    'A. Param Instance'
    param_inst_name = 'Basic Friendly'
    param_inst = param_inst_preset.get_param_inst_preset_combo(param_combo)

    'B. Functional Instances'
    bdgt_inst = bdgt.BudgetConsumption(param_inst)
    crra_inst = crra.PeriodUtility(param_inst)
    prod_inst = prod.ProductionFunction(param_inst)
    lgit_inst = lgit.MultinomialLogitU(param_inst)

    'C. utoday ufuture Instances'
    utoday_inst = utoday.TodayUtility(
        bdgt_inst, prod_inst,
        crra_inst, param_inst)
    ufuture_inst = ufuture.FutureUtil(
        bdgt_inst, prod_inst,
        crra_inst, param_inst)

    return param_inst, \
           bdgt_inst, crra_inst, prod_inst, lgit_inst, \
           utoday_inst, ufuture_inst


def gen_model_instances(param_combo=None, data=None, data_map=None):
    """
    Instances for mjall
    """

    logger.info('0. Default Parameters')
    param_inst, \
    bdgt_inst, crra_inst, prod_inst, lgit_inst, \
    utoday_inst, ufuture_inst = get_basic_instances(param_combo)

    logger.info('D. gengrid (Data instance)')
    data_inst = gengrids.GenModelData(param_inst, utoday_inst, bdgt_inst)

    logger.info('E1. Generate Data for mjall')
    logger.info('observed state vectors MESHED with shocks:k_tt, b_tt, fb_f_max_btp, and Kp Bp Choices')

    k_tt_v, b_tt_v, fb_f_max_btp_v, \
    eps_tt, k_tt, b_tt, \
    fb_f_max_btp, \
    ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
    ibfb_i_ktp, fbis_i_ktp, \
    none_ktp, \
    ibfb_f_imin_ktp, fbis_f_imin_ktp, \
    ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
    ibfb_i_btp, fbis_i_btp, \
    none_btp, \
    ibfb_f_imin_btp, fbis_f_imin_btp, \
        = data_inst.gen_mjall_data(data, data_map)

    logger.info('E2. Generate mjall Instance')
    mjall_inst = mjall.LifeTimeUtility(
        utoday_inst, ufuture_inst, param_inst,
        eps_tt=eps_tt, k_tt=k_tt, b_tt=b_tt,
        fb_f_max_btp=fb_f_max_btp,
        ib_i_ktp=ib_i_ktp, is_i_ktp=is_i_ktp, fb_f_ktp=fb_f_ktp, fs_f_ktp=fs_f_ktp,
        ibfb_i_ktp=ibfb_i_ktp, fbis_i_ktp=fbis_i_ktp,
        none_ktp=none_ktp,
        ibfb_f_imin_ktp=ibfb_f_imin_ktp, fbis_f_imin_ktp=fbis_f_imin_ktp,
        ib_i_btp=ib_i_btp, is_i_btp=is_i_btp, fb_f_btp=fb_f_btp, fs_f_btp=fs_f_btp,
        ibfb_i_btp=ibfb_i_btp, fbis_i_btp=fbis_i_btp,
        none_btp=none_btp,
        ibfb_f_imin_btp=ibfb_f_imin_btp, fbis_f_imin_btp=fbis_f_imin_btp)

    logger.info('F1. Generate Data for minterp')
    logger.info('observed state vectors MESHED with integration shocks:B_Veps, K_Veps, eps_Veps')
    B_Veps, K_Veps, eps_Veps = data_inst.gen_minterp_data(k_tt_v, b_tt_v, fb_f_max_btp_v)

    logger.info('F2. Generate minterp instance')
    minterp_inst = minterp.UlifeInterpolate(
        bdgt_inst, prod_inst, param_inst,
        B_V=b_tt, K_V=k_tt, eps_V=eps_tt,
        B_Veps=B_Veps, K_Veps=K_Veps, eps_Veps=eps_Veps,
        B_Vepszr=b_tt_v, K_Vepszr=k_tt_v)

    return mjall_inst, minterp_inst, lgit_inst, param_inst
