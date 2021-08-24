'''
Created on Jan 29, 2018

@author: fan

This is how soluvalue folder contains interacts with modelhh. Only entry point
from here to modellhh. works jointly with gengrids.  
'''
import logging

import dataandgrid.genchoicesinner as genchoicesinner
import modelhh.mjall as mjall

logger = logging.getLogger(__name__)


def gen_model_instances_inner(argmax_index, mjall_inst, param_inst):
    """
    Instances for mjall_inner
    When zooming in to new grid, simple method, generate new model instance. 
    """

    logger.debug('0. copy over mjall_inst instances')

    ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
    ibfb_i_ktp, fbis_i_ktp, \
    none_ktp, \
    ibfb_f_imin_ktp, fbis_f_imin_ktp, \
    ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
    ibfb_i_btp, fbis_i_btp, \
    none_btp, \
    ibfb_f_imin_btp, fbis_f_imin_btp \
        = genchoicesinner.choices_kb_each_inner(argmax_index, mjall_inst, param_inst)

    logger.info('E2. Generate mjall Instance')
    mjall_inst_inner = mjall.LifeTimeUtility(
        mjall_inst.utoday_inst, mjall_inst.ufuture_inst, param_inst,
        eps_tt=mjall_inst.eps_tt, k_tt=mjall_inst.k_tt, b_tt=mjall_inst.b_tt,
        fb_f_max_btp=mjall_inst.fb_f_max_btp,
        ib_i_ktp=ib_i_ktp, is_i_ktp=is_i_ktp, fb_f_ktp=fb_f_ktp, fs_f_ktp=fs_f_ktp,
        ibfb_i_ktp=ibfb_i_ktp, fbis_i_ktp=fbis_i_ktp,
        none_ktp=none_ktp,
        ibfb_f_imin_ktp=ibfb_f_imin_ktp, fbis_f_imin_ktp=fbis_f_imin_ktp,
        ib_i_btp=ib_i_btp, is_i_btp=is_i_btp, fb_f_btp=fb_f_btp, fs_f_btp=fs_f_btp,
        ibfb_i_btp=ibfb_i_btp, fbis_i_btp=fbis_i_btp,
        none_btp=none_btp,
        ibfb_f_imin_btp=ibfb_f_imin_btp, fbis_f_imin_btp=fbis_f_imin_btp)

    return mjall_inst_inner
