'''
Created on Jan 2, 2018

@author: fan

https://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class

create this so that 
'''

import logging

logger = logging.getLogger(__name__)

import projectsupport.systemsupport as proj_sys_sup
import soluvalue.genmodel as genmodel
import pyfan.graph.generic.allpurpose as grh_sup

import pylab as pylab

import modelhh.mjall as mjall
import numpy as np
import PIL
import os


class TestMjall():
    """
    One meaning one choice one state
    """

    def __init__(self, param_combo=None):
        logger.debug('setup class')

        if (param_combo is None):
            param_combo = {'grid_type': ['a', 1, 1], 'esti_type': ['a', 1]}

        self.saveDirectory = proj_sys_sup.get_paths('model_test', sub_folder_name='test_mjall')
        self.param_inst, \
        self.bdgt_inst, self.crra_inst, self.prod_inst, self.lgit_inst, \
        self.utoday_inst, self.ufuture_inst \
            = self.get_mjall_dep_inst(param_combo)

    def get_mjall_dep_inst(self, param_combo=None):
        """
        use this to mimic what value function evlauated at K and B would look like
        """

        if (param_combo is None):
            param_combo = {'grid_type': ['a', 1, 1], 'esti_type': ['a', 1]}

        param_inst, bdgt_inst, crra_inst, prod_inst, lgit_inst, utoday_inst, ufuture_inst = \
            genmodel.get_basic_instances(param_combo)

        return param_inst, bdgt_inst, crra_inst, prod_inst, lgit_inst, utoday_inst, ufuture_inst

    def invoke_mjall_inst(
            self,
            interpolant=None,
            eps_tt=0,
            k_tt=12,
            b_tt=3,
            fb_f_max_btp=-2,
            ib_i_ktp=0, is_i_ktp=0, fb_f_ktp=0, fs_f_ktp=0,
            ibfb_i_ktp=0, fbis_i_ktp=0,
            none_ktp=0,
            ibfb_f_imin_ktp=0, fbis_f_imin_ktp=0,
            ib_i_btp=0, is_i_btp=0, fb_f_btp=0, fs_f_btp=0,
            ibfb_i_btp=0, fbis_i_btp=0,
            none_btp=0,
            ibfb_f_imin_btp=0, fbis_f_imin_btp=0,
            choice_list=np.arange(0, 9, 1),
            check_scalar=True,
            solve=False,
            graph=False, save_suffix='', title_suffix=''):
        """
        use this to mimic what value function evlauated at K and B would look like
        """

        mjall_inst = mjall.LifeTimeUtility(
            self.utoday_inst, self.ufuture_inst, self.param_inst,
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

        if (solve):

            utility_today_stack, b_tp_principle_stack, consumption_stack, cash, y, \
            utility_future_stack, btp_stack, ktp_stack, \
            ulifetime = \
                mjall_inst.get_all_outputs(interpolant=interpolant,
                                           check_scalar=check_scalar)

            self.print_ulifetime(
                ktp_stack, btp_stack,
                utility_today_stack, b_tp_principle_stack, consumption_stack, cash, y,
                utility_future_stack, btp_stack,
                ulifetime)

            if (graph):
                self.graph_mjall_manage(self.param_inst, mjall_inst,
                                        ktp_stack, btp_stack,
                                        utility_today_stack, b_tp_principle_stack, consumption_stack,
                                        cash, y,
                                        utility_future_stack, btp_stack,
                                        ulifetime,
                                        save_suffix, title_suffix)

            return utility_today_stack, \
                   b_tp_principle_stack, consumption_stack, cash, y, \
                   utility_future_stack, \
                   btp_stack, \
                   ulifetime
        else:
            return mjall_inst

    def print_ulifetime(self,
                        ktp_stack, btp_stack,
                        utility_today_stack, b_tp_principle_stack, consumption_stack, cash, y,
                        utility_future_stack, b_tp_stack,
                        ulifetime):

        logger.debug('ktp_stack:%s', ktp_stack)
        logger.debug('btp_stack:%s', btp_stack)

        logger.debug('utility_today_stack:%s', utility_today_stack)
        logger.debug('b_tp_principle_stack:%s', b_tp_principle_stack)
        logger.debug('consumption_stack:%s', consumption_stack)
        logger.debug('cash:%s', cash)
        logger.debug('y:%s', y)

        logger.debug('utility_future_stack:%s', utility_future_stack)
        logger.debug('b_tp_stack:%s', b_tp_stack)

        logger.debug('ulifetime:%s', ulifetime)

    def graph_mjall_manage(self, param_inst, mjall_inst,
                           ktp_stack, btp_stack,
                           utility_today_stack, b_tp_principle_stack, consumption_stack, cash, y,
                           utility_future_stack, b_tp_stack,
                           ulifetime,
                           save_suffix, title_suffix):

        color_mat_list = [[consumption_stack, 'cons', 'consump'],
                          [utility_today_stack, 'utoday', 'utoday'],
                          [utility_future_stack, 'ufuture', 'ufuture'],
                          [ulifetime, 'ulife', 'ulife']
                          ]

        shape_choice_type = self.param_inst.grid_param['shape_choice']['type']
        if (shape_choice_type in ('broadcast', 'broadcast_kron')):
            states_len = utility_today_stack.shape[0]
        else:
            states_len = 1
        logger.info('shape_choice_type:%s', shape_choice_type)
        logger.info('utility_today_stack.shape:%s', utility_today_stack.shape)
        logger.info('ktp_stack.shape:%s', ktp_stack.shape)
        logger.info('states_len:%s', states_len)

        eps_tt = mjall_inst.eps_tt
        k_tt = mjall_inst.k_tt
        b_tt = mjall_inst.b_tt
        cash_tt = mjall_inst.cash_tt

        for cur_state in np.arange(states_len):

            if (shape_choice_type == ('broadcast')):
                'stacks are stored as: state x discrete_choice x cts_choice_grid'
                btp_stack_use = np.transpose(btp_stack[cur_state, :, :])
                ktp_stack_use = np.transpose(ktp_stack[cur_state, :, :])
                eps_tt_use = eps_tt[cur_state, :]
                k_tt_use = k_tt[cur_state, :]
                b_tt_use = b_tt[cur_state, :]
                cash_tt_use = cash_tt[cur_state, :]

            if (shape_choice_type == ('broadcast_kron')):
                'stacks are stored as: cts_choice_grid x discrete_choice'
                btp_stack_use, ktp_stack_use = btp_stack, ktp_stack
                eps_tt_use = eps_tt[cur_state, :]
                k_tt_use = k_tt[cur_state, :]
                b_tt_use = b_tt[cur_state, :]
                cash_tt_use = cash_tt[cur_state, :]

            if (shape_choice_type == ('1to1')):
                break

            list_image = []
            for color_mat_vals in color_mat_list:

                if (shape_choice_type in ('broadcast', 'broadcast_kron')):
                    color_mat = np.transpose(color_mat_vals[0][cur_state, :, :])
                    save_suffix_use = save_suffix + color_mat_vals[1] + '_S' + str(cur_state)
                    title_suffix_use = title_suffix + color_mat_vals[2] + ', S' + str(cur_state)
                else:
                    color_mat = color_mat_vals[0]
                    save_suffix_use = save_suffix + color_mat_vals[1]
                    title_suffix_use = title_suffix + color_mat_vals[2]

                saveFileName = self.graph_mjall(
                    param_inst, color_mat_vals,
                    eps_tt_use, k_tt_use, b_tt_use, cash_tt_use,
                    btp_stack_use, ktp_stack_use, color_mat,
                    xLabel_str='b prime', yLabel_str='k prime',
                    save_suffix=save_suffix_use, title_suffix=title_suffix_use)

                list_image.append(saveFileName)

            """
            Combine Images
            """
            try:
                # https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
                imgs = [PIL.Image.open(self.saveDirectory + file_name + '.png')
                        for file_name in list_image]

                # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
                min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
                imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

                # for a vertical stacking it is simple: use vstack
                imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
                imgs_comb = PIL.Image.fromarray(imgs_comb)
                imgs_comb.save(self.saveDirectory + save_suffix + '_S' + str(cur_state) + '.png')

                imgs = [os.remove(self.saveDirectory + file_name + '.png')
                        for file_name in list_image]
            except:
                """
                Code above has worked, but there might be different PIL versions
                re-testing, says:
                    AttributeError: module 'PIL' has no attribute 'Image'
                """
                pass

    def graph_mjall(self, param_inst, color_mat_vals,
                    eps_tt_use, k_tt_use, b_tt_use, cash_tt_use,
                    x_mat, y_mat, color_mat,
                    xLabel_str='', yLabel_str='',
                    save_suffix='', title_suffix=''):

        """
        Graphing, if satisfy requirement above
        """
        grapher = grh_sup.graphFunc()
        pylab.clf()
        # ===============================================================
        # fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')
        # loopColl = [[0,1],[2,3],[0,4],[1,5],[4,5],[0,1,2,3,4,5]]
        # axisList = [ax1,ax2,ax3,ax4,ax5,ax6]
        # ===============================================================
        choice_set_list = param_inst.model_option['choice_set_list']
        choice_names_use = param_inst.model_option['choice_names_use']

        fig, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10)) = \
            pylab.subplots(2, 5, figsize=(10, 5), sharex=True, sharey=True)
        # fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')                
        loopColl = [[0], [1],
                    [2], [3],
                    [4], [5],
                    [7], [8],
                    [6]]
        loopCollStr = ['borr', 'save',
                       'borr', 'save',
                       'borr', 'save',
                       'borr', 'save',
                       'cash']

        axisList = [ax1, ax6, ax2, ax7, ax3, ax8, ax4, ax9, ax5]

        '''
        Get Min Max Bounds
        '''
        xlim = [np.nanmin(x_mat), np.nanmax(x_mat)]
        ylim = [np.nanmin(y_mat), np.nanmax(y_mat)]
        clim = [np.nanmin(color_mat), np.nanmax(color_mat)]

        '''
        Draw Polygons
        '''
        for loopidx, loopCur in enumerate(loopColl):
            logger.debug('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx loopidx:%s, loopCollStr[loopidx]:%s', loopidx,
                         loopCollStr[loopidx])

            pylab.sca(axisList[loopidx])

            for ctr_cur in loopCur:

                ''' If Current Invoke has the choice'''
                if ctr_cur in choice_set_list:
                    data_col_cur = choice_set_list.index(ctr_cur)
                    y_vec = y_mat[:, data_col_cur]
                    x_vec = x_mat[:, data_col_cur]
                    c_vec = color_mat[:, data_col_cur]

                    'nan index'
                    #                 c_vec = ary_sup.replace_nan_by_lowest(c_vec, lowest=True)

                    logger.debug('y_vec:%s', y_vec)
                    logger.debug('x_vec:%s', x_vec)
                    logger.debug('c_vec:%s', c_vec)

                    xLabel = xLabel_str
                    c_min = '{0:.{1}f}'.format(min(c_vec), 1)
                    c_max = '{0:.{1}f}'.format(max(c_vec), 1)
                    yLabel = yLabel_str + '; c min:' + str(c_min) + ', c max:' + str(c_max)

                    #     pylab.ylim([np.min(yDataMat),np.max(yDataMat)])
                    #     pylab.xlim([np.min(xData),np.max(xData)])
                    grapher.xyPlotMultiYOneX(
                        yDataMat=y_vec, xData=x_vec, colorVar=c_vec, scattersize=50,
                        saveOrNot=False, graphType='scatter',
                        basicTitle=choice_names_use[data_col_cur],
                        ylim=ylim, xlim=xlim,
                        basicXLabel=xLabel, basicYLabel=yLabel, saveDPI=100)

        """title_suffix
        Aggregate Up Graphs
        """
        saveFileName = 'mjall_' + save_suffix
        title_display = color_mat_vals[2] + \
                        ' [eps,k,b,cash]=' + \
                        str(np.concatenate((eps_tt_use, k_tt_use, b_tt_use, cash_tt_use))) + \
                        ' ' + title_suffix
        pylab.suptitle(title_display, fontsize=8)
        grapher.savingFig(saveDirectory=self.saveDirectory,
                          saveFileName=saveFileName,
                          saveDPI=200, pylabUse=fig)
        pylab.clf()
        fig.clf()

        return saveFileName
