'''


@author: fan

import projectsupport.graph.choices_i_eachj_polygon as choices_ieachj_poly
'''

import logging
import numpy as np
import pyfan.graph.generic.allpurpose as grh_sup
import pylab as pylab

logger = logging.getLogger(__name__)


def graph_mi_polygon_j(choice_set_list,
                       save_directory, save_filename_prefix, save_filename_suffix,
                       A, cash_tt, k_tt,
                       ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
                       ibfb_i_ktp, fbis_i_ktp, \
                       none_ktp, \
                       ibfb_f_imin_ktp, fbis_f_imin_ktp, \
                       ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
                       ibfb_i_btp, fbis_i_btp, \
                       none_btp, \
                       ibfb_f_imin_btp, fbis_f_imin_btp):
    """
    multiple i
    """
    zero_mat = np.zeros(np.shape(ib_i_ktp))
    if (ib_i_ktp is 0):
        ib_i_ktp = zero_mat
    if (is_i_ktp is 0):
        is_i_ktp = zero_mat
    if (fb_f_ktp is 0):
        fb_f_ktp = zero_mat
    if (fs_f_ktp is 0):
        fs_f_ktp = zero_mat
    if (ibfb_i_ktp is 0):
        ibfb_i_ktp = zero_mat
    if (fbis_i_ktp is 0):
        fbis_i_ktp = zero_mat
    if (none_ktp is 0):
        none_ktp = zero_mat

    if (ib_i_btp is 0):
        ib_i_btp = zero_mat
    if (is_i_btp is 0):
        is_i_btp = zero_mat
    if (fb_f_btp is 0):
        fb_f_btp = zero_mat
    if (fs_f_btp is 0):
        fs_f_btp = zero_mat
    if (ibfb_i_btp is 0):
        ibfb_i_btp = zero_mat
    if (fbis_i_btp is 0):
        fbis_i_btp = zero_mat
    if (none_btp is 0):
        none_btp = zero_mat

    np.random.seed(0)
    i_set_use = np.random.randint(cash_tt.shape[0], size=5)

    #     i_set = np.ravel(np.where((cash_tt <= 2) & (cash_tt >= 1))[0])
    #     i_set = np.ravel(np.where(cash_tt <= 2)[0])
    #     i_set_subset = np.random.randint(i_set.size, size=10)
    #     i_set_use = i_set[i_set_subset]

    for ctr_i, cur_i in enumerate(i_set_use):
        cash_i = cash_tt[cur_i, :]
        k_tt_i = k_tt[cur_i, :]

        save_filename = save_filename_prefix + 'A' + str(int((A) * 1000)) + \
                        'c' + str(int(cash_i * 1000)) + \
                        'k' + str(int(k_tt_i * 1000)) + \
                        save_filename_suffix + \
                        'i' + str(cur_i)

        title = 'A=' + '{0:.{1}f}'.format(A, 3) + \
                ', cash=' + '{0:.{1}f}'.format(cash_i[0], 3) + \
                ', ktt=' + '{0:.{1}f}'.format(k_tt_i[0], 3) + \
                ' (' + save_filename_suffix + \
                ', i=' + str(cur_i) + ')'

        graph_i_polygon_j(choice_set_list,
                          save_directory, save_filename, title,
                          ib_i_ktp[cur_i, :], is_i_ktp[cur_i, :], fb_f_ktp[cur_i, :], fs_f_ktp[cur_i, :], \
                          ibfb_i_ktp[cur_i, :], fbis_i_ktp[cur_i, :], \
                          none_ktp[cur_i, :], \
                          ib_i_btp[cur_i, :], is_i_btp[cur_i, :], fb_f_btp[cur_i, :], fs_f_btp[cur_i, :], \
                          ibfb_i_btp[cur_i, :], fbis_i_btp[cur_i, :], \
                          none_btp[cur_i, :])


def graph_i_polygon_j(choice_set_list,
                      saveDirectory, saveFileName, title,
                      ib_i_ktp, is_i_ktp, fb_f_ktp, fs_f_ktp, \
                      ibfb_i_ktp, fbis_i_ktp, \
                      none_ktp, \
                      ib_i_btp, is_i_btp, fb_f_btp, fs_f_btp, \
                      ibfb_i_btp, fbis_i_btp, \
                      none_btp):
    """
    Graph seven choice polygons grids:    
        see: https://www.evernote.com/shard/s10/nl/1203171/9f61fc91-268f-4c45-b45e-9750cc7a0b4d        
    """

    'B. Generate Choice Vectors'
    grapher = grh_sup.graphFunc()
    pylab.clf()
    # ===============================================================
    # fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')
    # loopColl = [[0,1],[2,3],[0,4],[1,5],[4,5],[0,1,2,3,4,5]]
    # axisList = [ax1,ax2,ax3,ax4,ax5,ax6]
    # ===============================================================

    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = \
        pylab.subplots(2, 4, sharex=True, sharey=True, figsize=(12, 6))
    # fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = pylab.subplots(2, 3,sharex='col', sharey='row')                
    axisList = [ax1, ax5, ax2, ax6, ax3, ax7, ax4, ax8]

    #         '''
    #         Get Min Max Bounds
    #         '''
    #         all_k = []
    #         all_b = []
    #         for ctr_cur in choice_set_list:
    #             [[[minKprime, maxKprime], [minBprime, maxBprime]], Y_minCst, _] = all_minmax[ctr_cur]
    #             all_k.append(minKprime)
    #             all_k.append(maxKprime)
    #             all_b.append(minBprime)
    #             all_b.append(maxBprime)
    #
    #         # np.min and np.max twice in case all_k is 2d matrix
    #         ylim = [np.minimum(np.min(np.min(all_k)),-10), np.maximum(np.max(np.max(all_k)),40)]
    #         xlim = [np.minimum(np.min(np.min(all_b)),-30), np.maximum(np.max(np.max(all_b)),15)]

    '''
    Draw Polygons
    '''
    for loopidx, loopCur in enumerate(choice_set_list):
        pylab.sca(axisList[loopidx])

        logger.debug('Cur loopidx:%s, loopCur:%s', loopidx, loopCur)

        # Informal Borrow
        if (loopCur == 0):
            K_vec, B_vec = ib_i_ktp, ib_i_btp
            title_suffix = 'inf borr'

        # Informal Save/Lend
        if (loopCur == 1):
            K_vec, B_vec = is_i_ktp, is_i_btp
            title_suffix = 'inf lend'

        # Formal Borrow
        if (loopCur == 2 or loopCur == 102):
            if (loopCur == 2):
                K_vec, B_vec = fb_f_ktp, fb_f_btp
                title_suffix = 'for borr (2)'
            if (loopCur == 102):
                K_vec, B_vec = fb_f_ktp, fb_f_btp
                title_suffix = 'for borr (102)'

        # Formal Save
        if (loopCur == 3):
            K_vec, B_vec = fs_f_ktp, fs_f_btp
            title_suffix = 'for save'

        # Informal and Formal Borrow            
        if (loopCur == 4 or loopCur == 104):
            if (loopCur == 4):
                K_vec, B_vec = ibfb_i_ktp, ibfb_i_btp
                title_suffix = 'fbib'
            if (loopCur == 104):
                K_vec, B_vec = ibfb_i_ktp, ibfb_i_btp
                title_suffix = 'fbib (104)'

        # Formal Borrow and Informal Save/Lend
        if (loopCur == 5 or loopCur == 105):
            if (loopCur == 5):
                K_vec, B_vec = fbis_i_ktp, fbis_i_btp
                title_suffix = 'fbis'
            if (loopCur == 105):
                K_vec, B_vec = fbis_i_ktp, fbis_i_btp
                title_suffix = 'fbis (105)'

        # Mattress          
        if (loopCur == 6):
            K_vec, B_vec = none_ktp, none_btp
            title_suffix = 'mattress'

        #         # Informal Borrow Formal Borrow, but formal borrow at minimal not max
        #         if (loopCur == 7):
        #             K_vec, B_vec = ibfb_f_imin_ktp, ibfb_f_imin_btp
        #             title_suffix = 'inf (min) for borr (cts)'
        #             title_suffix = 'fb(min)ib'
        #
        #         # Informal Borrow Formal save, but formal borrow at minimal not max
        #         # THIS CHOICE IS INVALID, can't possibly happen
        #         if (loopCur == 8):
        #             K_vec, B_vec = fbis_f_imin_ktp, fbis_f_imin_btp
        #             title_suffix = 'fb(min)is'

        """
        K and B are M by N matrix, where M are States, N are Choices'
        For Graphing here, turn into MxN by 1 vector, all scatter plots,
        see how multiple states' choice polygons overlap if M > 1             
        """

        K_vec = np.reshape(K_vec, (-1, 1))
        B_vec = np.reshape(B_vec, (-1, 1))

        grapher.xyPlotMultiYOneX(
            yDataMat=K_vec, xData=B_vec, saveOrNot=False,
            showOrNot=False, graphType='scatter', scattersize=3,
            basicTitle=title_suffix,
            basicXLabel='', basicYLabel='')

    """
    Aggregate Up Graphs
    """
    fig.subplots_adjust(wspace=0, hspace=1)
    pylab.suptitle(title, fontsize=5)

    fig.text(0.5, 0, 'B choice', ha='center')
    fig.text(0, 0.5, 'K choice', va='center', rotation='vertical')
    #     saveFileName='choice_'+save_suffix
    grapher.savingFig(saveDirectory=saveDirectory,
                      saveFileName=saveFileName,
                      saveDPI=200, pylabUse=fig)

    pylab.clf()
    fig.clf()
