"""
The :mod:`prjforinfcreditvilfw.analyze.analyzesolu` provides optimization and dynamic programming solution visualizations.

Includes method :func:`solve_graph_main`, and :func:`graph_main`
"""

import logging
import numpy as np

import projectsupport.graph.graph_sets as sup_graphset
import projectsupport.graph.optimal_cates7 as opti7graph
import projectsupport.graph.optimal_continuous as opticts
import projectsupport.graph.optimal_eachj_phase as graphphaseeachj
import projectsupport.graph.optimal_eachj_policy as grapheachj
import projectsupport.graph.optimal_maxj_policyphase as graphphase
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def solve_graph_main(solu_dict, mjall_inst, param_inst,
                     directory_str_dict, graph_list=None):
    """Generate Data file and Graph to analyze Model Solution

    
    During any stage of VFI or afterwards, given current optimal choices etc.
    This does not have functions inside, but invokes graphing and potentially other
    codes, this is central location for processing results from solving model    
    
    Functionalities:
    1. Phase diagram related graphs.
        + state today, and choices
        + state today, state tomorrow distribution 
    2. 2D, 3D color graphs of other types
    3. save to log
    
    Parameters
    ----------
    param_combo: dictionary
        relevant paraemters for current invokation 
    solu_dict: dict of arrays
         storing current optimal choices    
    """

    """
    A. What Graphs to Graph?
    """
    #     timesufx = ''
    graph_analyzesolu_list_all = sup_graphset.graph_analyzesolu_set()

    """
    B. Graph if there is anything to graph
    """

    if bool(set(graph_analyzesolu_list_all) & set(graph_list)):

        log_directory = directory_str_dict['log']
        csv_directory = directory_str_dict['csv_detail']
        image_directory = directory_str_dict['img_detail']

        title = directory_str_dict['title']
        file_save_suffix = directory_str_dict['file_save_suffix']
        combo_desc = directory_str_dict['combo_desc']

        EjV = solu_dict['EjV']
        util_opti_eachj = solu_dict['util_opti_eachj']

        maxof7_overJ = solu_dict['maxof7_overJ']
        ktp_opti = solu_dict['ktp_opti']
        btp_opti = solu_dict['btp_opti']
        consumption_opti = solu_dict['consumption_opti']

        each_j_prob = solu_dict['each_j_prob']
        ktp_opti_allJ = solu_dict['ktp_opti_allJ']
        btp_opti_allJ = solu_dict['btp_opti_allJ']
        consumption_opti_allJ = solu_dict['consumption_opti_allJ']

        #     interpolant, \
        #         maxof7_overJ, ktp_opti, btp_opti, consumption_opti, mjall_inst, param_inst = \
        #             solu.solve_model(param_combo=param_combo)

        #         k_tt = np.reshape(mjall_inst.k_tt, (-1, 1))
        #         b_tt = np.reshape(mjall_inst.b_tt, (-1, 1))
        #         eps_tt = np.reshape(mjall_inst.eps_tt, (-1, 1))

        k_tt = mjall_inst.k_tt
        b_tt = mjall_inst.b_tt
        eps_tt = mjall_inst.eps_tt
        cash_tt = mjall_inst.cash_tt
        choice_names_use = param_inst.model_option['choice_names_use']
        choice_names_full_use = param_inst.model_option['choice_names_full_use']
        solu_var_suffixes = hardstring.get_solu_var_suffixes()
        cash_min = param_inst.grid_param['min_steady_coh']
        cash_max = param_inst.grid_param['max_steady_coh']

        choice_each_prob = [solu_var_suffixes['probJ_opti'] +
                            ' ' + strn for strn in choice_names_use]
        choice_each_kn = [solu_var_suffixes['ktp_opti'] + ' ' +
                          strn for strn in choice_names_use]
        choice_each_bn = [solu_var_suffixes['btp_opti'] +
                          ' ' + strn for strn in choice_names_use]
        choice_each_c = [solu_var_suffixes['consumption_opti'] +
                         ' ' + strn for strn in choice_names_use]
        choice_each_jv = [solu_var_suffixes['util_opti_eachj'] +
                          ' ' + strn for strn in choice_names_use]

        '''
        Store File
        '''
        csv_file_name = 'solu' + file_save_suffix
        varnames = 'EjV, k_tt, b_tt, eps_tt, cash_tt, maxof7_overJ, ktp_opti, btp_opti, consumption_opti' + \
                   ',' + ",".join(map(str, choice_each_prob)) + \
                   ',' + ",".join(map(str, choice_each_kn)) + \
                   ',' + ",".join(map(str, choice_each_bn)) + \
                   ',' + ",".join(map(str, choice_each_c)) + \
                   ',' + ",".join(map(str, choice_each_jv))

        varmat = np.column_stack((np.ravel(EjV),
                                  np.ravel(k_tt), np.ravel(b_tt),
                                  np.ravel(eps_tt), np.ravel(cash_tt),
                                  np.ravel(maxof7_overJ),
                                  np.ravel(ktp_opti), np.ravel(btp_opti), np.ravel(consumption_opti),
                                  each_j_prob,
                                  ktp_opti_allJ,
                                  btp_opti_allJ,
                                  consumption_opti_allJ,
                                  util_opti_eachj))

        '''
        fb ib fs il, specific choices, to better understand joint choices
        see: solumain.py, end of function solve_optimal
        '''
        borr_4choices_list = ['btp_fb_opti', 'btp_ib_opti', 'btp_fs_opti', 'btp_il_opti']
        for btp_opti_allJ_cur in borr_4choices_list:
            if btp_opti_allJ_cur in solu_dict:
                choice_each_bn_cur = [solu_var_suffixes[btp_opti_allJ_cur] + ' ' + strn for strn in
                                      choice_names_use]
                varnames = varnames + ',' + btp_opti_allJ_cur + ',' + ",".join(map(str, choice_each_bn_cur))

                btp_opti_allJ_cur_data = solu_dict[btp_opti_allJ_cur + '_allJ']
                btp_opti_cur_data = solu_dict[btp_opti_allJ_cur]
                varmat = np.column_stack((varmat, np.ravel(btp_opti_cur_data), btp_opti_allJ_cur_data))

        export_panda = False
        if ('solu_data_pd' in graph_list):
            export_panda = True
        solu_data_pd = proj_sys_sup.debug_panda(varnames, varmat,
                                                save_directory=csv_directory,
                                                filename=csv_file_name,
                                                time_suffix=False, export_panda=export_panda, log=False)

        '''
        Unique Optimal Choices
        '''
        maxof7_overJ = np.reshape(maxof7_overJ, (-1, 1))
        [unique_choices, unique_counts] = np.unique(maxof7_overJ, return_counts=True)
        logger.info("unique_choices:\n%s", np.column_stack((unique_choices, unique_counts)))

        choice_set_list = mjall_inst.choice_set_list

        # Some what fancier phase diagram
        if 'graph_maxj_nologit' in graph_list:
            img_file_name = 'solumax' + file_save_suffix
            title_display = title + ' ' + file_save_suffix
            image_save_name = img_file_name
            graphphase.graph_maxj_nologit(solu_data_pd, param_inst,
                                          title_display,
                                          image_save_name, image_directory)

        # Each Category, Own Graphs
        if 'graph_solu_dist' in graph_list:
            img_file_name = 'Jdistsolu' + file_save_suffix
            x_var_label = ''
            y_var_label = ''
            title_display = title + ' ' + file_save_suffix
            image_save_name = img_file_name
            graphphaseeachj.graph_solu_dist(solu_data_pd, param_inst,
                                            title_display,
                                            image_save_name, image_directory)

        if 'graph_eachj_prob' in graph_list:
            img_file_name = 'Jsoluprob' + file_save_suffix
            x_var_label = ''
            y_var_label = ''
            title_display = title + ' ' + file_save_suffix
            image_save_name = img_file_name
            grapheachj.graph_eachj_prob(solu_data_pd, param_inst,
                                        title_display,
                                        image_save_name, image_directory)

        # First Generation Graph    
        for graph_type in [1]:

            if (graph_type == 0):
                logger.info("K and B Graphs")
                x_var = k_tt
                y_var = b_tt
                x_var_label = 'k'
                y_var_label = 'b'
                z_var_label = 'opti over 7'
                z_discrete_var = maxof7_overJ
                x_min = None
                x_max = None

            if (graph_type == 1):
                logger.info("cash sand K graphs")
                x_var = k_tt
                y_var = cash_tt
                x_var_label = 'k'
                y_var_label = 'cash'
                z_var_label = 'opti over 7'
                z_discrete_var = maxof7_overJ
                x_min = cash_min
                x_max = cash_max

            graph_main(x_var, y_var, x_var_label, y_var_label, z_var_label, z_discrete_var,
                       ktp_opti, btp_opti, title, file_save_suffix,
                       choice_set_list, image_directory,
                       x_min, x_max, graph_list)


def graph_main(x_var, y_var, x_var_label, y_var_label, z_var_label, z_discrete_var,
               ktp_opti, btp_opti, title, file_save_suffix,
               choice_set_list, image_directory,
               x_min, x_max, graph_list):
    '''C. Optimal Choices across 7 Categories'''
    if ('graph_optimalChoice7Cates' in graph_list):
        opti7graph.graph_optimalChoice7Cates(
            choice_set_list,
            x_var, y_var, z_discrete_var,
            x_var_label, y_var_label, z_var_label, title,
            file_save_suffix, image_directory)

    '''D. Kapital Continuous Choice'''
    if ('graph_optimal_continuous_ktp' in graph_list):
        opticts.graph_optimal_continuous(
            y_var, ktp_opti, x_var,
            y_var_label, 'ktp_opti', x_var_label,
            title + ' \n color is ' + x_var_label + '',
            file_save_suffix, image_directory,
            x_min, x_max, line45Deg=True)

    '''E. Safe Asset Continuous Choice'''
    if ('graph_optimal_continuous_btp' in graph_list):
        opticts.graph_optimal_continuous(
            y_var, btp_opti, x_var,
            y_var_label, 'btp_opti', x_var_label,
            title + ' \n color is ' + x_var_label + '',
            file_save_suffix, image_directory,
            x_min, x_max, line45Deg=True)

    graph3d = False
    if (graph3d):
        opticts.graph_xyz_3D(x_var, y_var, ktp_opti,
                             x_var_label, y_var_label, 'ktp',
                             graphTitleDisp='ktp cts choices',
                             save_suffix=file_save_suffix,
                             subpath_img_save=image_directory,
                             angleType=[1, [1, 2, 3, 4, 5, 6]])

        opticts.graph_xyz_3D(x_var, y_var, btp_opti,
                             x_var_label, y_var_label, 'btp',
                             graphTitleDisp='btp cts choices',
                             save_suffix=file_save_suffix,
                             subpath_img_save=image_directory,
                             angleType=[1, [1, 2, 3, 4, 5, 6]])
