'''
Created on May 17, 2018

@author: fan

Solve for equilibrium interest rate
'''
from copy import deepcopy

import logging
import numpy as np

import analyze.analyzeequi as analyzeequi
import parameters.combo as paramcombo
import projectsupport.datamanage.data_from_json as datajson
import projectsupport.graph.equi_demandsupply as graphdemandsupply
import projectsupport.hardcode.file_name as proj_sup_filename
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup
import soluequi.panda_r_loop as pd_rloop
import solusteady.simu_inner_loop as steadyinnerloop
import solusteady.simu_integrate_loop as steadyintegrateloop

logger = logging.getLogger(__name__)


def policies_steady_states_rloop(combo_type, combo_list=None,
                                 compute_specs='l-ng-s-x',
                                 save_directory='C:',
                                 panda_graph_only=False,
                                 parallel=False,
                                 graph_list=None,
                                 export_json=True):
    """
    Given a range of policy values
    Graphing Plan:
        four types of graphs:
            1. Jsoluprob
            2. solumax
            3. transp
            4. steady
        when to produce?            
            1. do not produce at all interest rate levels.
                - R vec: min and max (with mid point) during first iteration round is sufficient
                - Param vec: also min and max with some middle point enough
                - Jointly, 3 by 3, 9 sets of graphs 
            2. maxJ vs wgtJ
                - Jsoluprob and solumax incorporates both maxJ and wgtJ already
                - transp and steady, do we need maxJ and wgtJ versions? I think so
            
    """

    #     if (graph_list is None):
    #         graph_list = ['graph_agg_at_equi','graph_demand_supply']

    if (combo_list is None):
        combo_list = paramcombo.get_combo(combo_type, compute_specs)

    int_specific_json_suffix = '_r'

    """
    _overall is if we are doing any of these types of graphing at all
    """

    # 3. maxJ or not?
    max_of_J = True
    weightJ = True

    # 6. mmust export json for final graphs, no choice

    # 7. where to graph? achieve 3 by 3 graphing, 3 set of param_combo and 3 r for each of the param_combo
    combo_list_graph_set = [0,
                            int((len(combo_list) - 1) / 2),
                            len(combo_list) - 1]
    min_int = 1.00
    max_int = 1.20
    int_rate_counts = compute_specs['int_rate_counts']
    int_vec = None
    int_vec_graph_set = [0,
                         int((int_rate_counts - 1) / 2),
                         (int_rate_counts - 1)]

    """
    2. Solve and Simulate (save results to key summary results json)s
        panda_graph_only is False, that means proceed like normal
        panda_graph_only is True, already produced results, just trying
        to graph and calculate given json results
    """

    if ('_ITG_' in combo_type[1]):
        integrated = True
        func_invoke = steadyintegrateloop.steady_loop_integrate
    else:
        integrated = False
        func_invoke = steadyinnerloop.steady_loop_inner

    suf_dict = proj_sup_filename.file_suffix(equilibrium=True, integrated=integrated)

    exo_or_endo = suf_dict['exo_or_endo']
    exo_or_endo_json_search = suf_dict['exo_or_endo_json_search']
    exo_or_endo_graph_row_select = suf_dict['exo_or_endo_graph_row_select']
    image_save_name_prefix = suf_dict['image_save_name_prefix']
    image_save_name_prefix_exo = suf_dict['image_save_name_prefix_exo']

    counter = 0
    for param_combo in combo_list:
        if counter in combo_list_graph_set:
            graph_list_use = graph_list
        else:
            graph_list_use = []

        counter = counter + 1
        initial_int_vec = demand_supply_interest(
            func_invoke, exo_or_endo, exo_or_endo_graph_row_select,
            param_combo, compute_specs,
            save_directory,
            min_int=min_int, max_int=max_int, int_rate_counts=int_rate_counts,
            int_specific_json_suffix=int_specific_json_suffix,
            int_vec=int_vec,
            parallel=parallel,
            max_of_J=max_of_J,
            weightJ=weightJ,
            int_vec_graph_set=int_vec_graph_set,
            graph_list=graph_list_use,
            panda_graph_only=panda_graph_only,
            export_json=export_json)

    '''3. Combine key json summary results, all param combos, all interest rates'''
    #     if (search_string is None):
    #         search_string = '*'+combo_type[1]+'*'

    export_agg_json_csv = True
    if 'esti_param_vec_count' in compute_specs:
        export_agg_json_csv = False
    #     export_agg_json_csv = soluequipartial.export_agg_json_or_not(graph_list,
    #                                                                  compute_specs,
    #                                                                  save_directory,
    #                                                                  combo_type,
    #                                                                  exo_or_endo_json_search)

    if export_agg_json_csv:

        try:
            suffix = hardstring.file_suffix(file_type='csv', sub_type='_endoexo')
            save_file_name = hardstring.main_file_name(combo_type, suffix, save_directory, save_type='simu_csv')
            panda_df = datajson.json_to_panda(
                directory=save_directory['json'],
                file_str='*' + combo_type[1] + exo_or_endo_json_search,
                agg_df_name_and_directory=save_file_name)
        except Exception:
            logger.critical('%s', save_directory['csv'] + combo_type[1] + exo_or_endo + '.csv')

        '''4. Equilibrium Graphing'''
        select_r_equi = True
        R_INFROM_common_cur = None
        title_display = combo_list[0]['title']
        analyzeequi.equi_graph_main(combo_type, combo_list, compute_specs,
                                    jsons_panda_df=panda_df,
                                    exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                    select_r_equi=select_r_equi,
                                    R_INFROM_common_cur=R_INFROM_common_cur,
                                    save_directory=save_directory,
                                    title_display=title_display,
                                    image_save_name_prefix=image_save_name_prefix,
                                    graph_list=graph_list)

        if ('graph_inti_int_vec_as_exo' in graph_list):

            for R_INFORM_ctr, R_INFROM_common_cur in enumerate(initial_int_vec):
                select_r_equi = False
                R_INFROM_common_cur_use = R_INFROM_common_cur
                image_save_name = image_save_name_prefix_exo + combo_type[1] + '_iniRINFc' + str(R_INFORM_ctr)
                title_display = combo_list[0]['title'] + '\n Exogenous Fixed R=' + str(R_INFROM_common_cur)
                analyzeequi.equi_graph_main(combo_type, combo_list, compute_specs,
                                            jsons_panda_df=panda_df,
                                            exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                            select_r_equi=select_r_equi,
                                            R_INFROM_common_cur=R_INFROM_common_cur_use,
                                            save_directory=save_directory,
                                            title_display=title_display,
                                            image_save_name=image_save_name,
                                            graph_list=graph_list)


def demand_supply_interest(func_invoke, exo_or_endo, exo_or_endo_graph_row_select,
                           param_combo, compute_specs,
                           save_directory,
                           min_int=0.95, max_int=1.20, int_rate_counts=4,
                           int_vec_graph_set=[0, 1, 3],
                           int_vec=None,
                           parallel=False,
                           max_of_J=True,
                           weightJ=True,
                           int_specific_json_suffix='_r',
                           graph_list=['graph_demand_supply_interest'],
                           panda_graph_only=False,
                           export_json=True):
    """
    Whatever the parameter set is generate grid based on interest rate. 
     
    Given one element from list of param_combo, obtained from: 
        paramcombo.get_combo(combo_type)
    Expand that list by interest rate from some low to some higher number. 
    
    param_combo might be from a combo_list, or might be a single thing. 
    Whatever it is, this code checks on demand and supply curves.
    
    the code below works for monotonically decreasing gap.
    
    Parameters
    ----------
    graph_solu: boolean
        Jsoluprob and solumax type graphs produced during solution for VFI
    graph_main: boolean
        transp and steady graphs produced during finding steady state distribution
    export_json: boolean
        necessary, tracks aggregates and parameters from each parameter set steady state
        values. 
    panda_graph_only: Boolean
        if true, this means json files storing aggregate information already saved
        then aggregate over individual jsons, and draw demand and supply curve
        this is graph only basically. The point is sometimes we have already obtained
        the json data, but want to redo the demand supply curve graph.
        
    Returns
    -------
    initial_int_vec: numeric
        interest rate middle point from initial vector initial bisection loop
        grab this which exists in all GE along vector, and plot when r_inf 
        equals this so from EQU invoke, generate also EXO results
    """

    bisection_iter = compute_specs['bisection_iter']
    # bisection_iter = 4
    # int_rate_counts = 5
    for bisection_ctr in np.arange(bisection_iter):

        """
        1. Generate combo_list from param_combo
        """
        combo_list_R_INFORM = []

        if (int_vec is None):

            int_vec = np.linspace(min_int, max_int, num=int_rate_counts)

            if (bisection_ctr == 0):
                try:
                    '''
                    1b. Include the default interest rate for this combo_list
                    why include this?
                    Find equilibrium r, but also want to see what exogenously constant
                    r results are, over param_vec
                    only relevent in first round
                    '''
                    default_R_INFROM = param_combo['param_update_dict']['esti_type'][2]['R_INFORM_BORR']
                    if (np.isin(int_vec, default_R_INFROM)):
                        pass
                    else:
                        int_vec = np.linspace(min_int, max_int,
                                              num=int_rate_counts - 1)
                        int_vec.append(default_R_INFROM)
                        int_vec = np.sort(int_vec)
                except:
                    '''
                    1b. Vector from min to max
                    there is no specific R_INFORM_BORR specified in esti_type 
                    '''
                    pass

            if (bisection_ctr == 0):
                initial_int_vec = int_vec

        else:
            pass

        title_init = param_combo['title']
        combo_desc_init = param_combo['combo_desc']
        file_save_suffix_init = param_combo['file_save_suffix']
        for cur_rate in int_vec:

            param_combo_cur_rate = deepcopy(param_combo)

            r_dict = {}
            r_dict['R_INFORM_BORR'] = cur_rate
            r_dict['R_INFORM_SAVE'] = cur_rate

            '''1a. File Names Updating Etc'''
            cur_rate_str = str(int(cur_rate * 10000))

            title = title_init + '(R=' + cur_rate_str + ')'
            combo_desc = combo_desc_init + '(R=' + cur_rate_str + ')'
            file_save_suffix = file_save_suffix_init + int_specific_json_suffix + cur_rate_str

            param_combo_cur_rate['title'] = title
            param_combo_cur_rate['combo_desc'] = combo_desc
            param_combo_cur_rate['file_save_suffix'] = file_save_suffix

            '''1B. Parameter Updating'''

            try:
                '''A. Has esti_type 3 elements'''
                esti_type_adjust_dict = param_combo['param_update_dict']['esti_type'][2]
                esti_type_adjust_dict.update(r_dict)
                param_combo_cur_rate['param_update_dict']['esti_type'][2] = esti_type_adjust_dict
            except:
                '''B. has esti_type'''
                esti_type_cur = param_combo_cur_rate['param_update_dict']['esti_type']
                esti_type_cur.append(r_dict)
                param_combo_cur_rate['param_update_dict']['esti_type'] = esti_type_cur

            '''Add Informal R current to list'''
            param_combo_append_rate = deepcopy(param_combo_cur_rate)
            combo_list_R_INFORM.append(param_combo_append_rate)

        """
        2. Solve and Simulate at different interest rates, collect aggregate results
            panda_graph_only is False, that is normal
            panda_graph_only is True, that means the json individual files
            are already created, so just generate panda, generate graphs
        """
        combo_list = combo_list_R_INFORM
        if (panda_graph_only is False):

            proj_sys_sup.jdump(combo_list, 'combo_list', logger=logger.warning)
            if bisection_ctr in [0, (bisection_iter - 1)]:
                graph_list_use = graph_list
            else:
                graph_list_use = []

            # Results are saved to file, which are loaded in below
            func_invoke(combo_list, compute_specs,
                        save_directory,
                        parallel,
                        max_of_J=max_of_J, weightJ=weightJ,
                        graph_list=graph_list_use,
                        export_json=export_json,
                        exo_or_endo=exo_or_endo,
                        graph_vec_subset=int_vec_graph_set)

        """
        3. analyze aggregate results, for files under current param_combo with different
        interest rates.
            Every time, will gather all past rounds results together into new panda file
            then will zoom in to current tighest interest rate gap
            - save csv with ['image_DS_curves'] suffix every time, but do not graph every time
        """
        file_str = '*' + file_save_suffix_init + int_specific_json_suffix + '*'
        agg_df_name_and_directory = save_directory['csv'] + \
                                    proj_sup_filename.file_suffix(equilibrium=True)[
                                        'image_DS_curves'] + file_save_suffix_init + '.csv'
        agg_steadysolu_pd = datajson.json_to_panda(
            directory=save_directory['json'],
            file_str=file_str,
            agg_df_name_and_directory=agg_df_name_and_directory)

        """
        4. Calculate updated interest rate vector 
        """
        R_INFORM_BORR, aggregate_inf_borrow, aggregate_inf_save = \
            pd_rloop.get_demand_supply_vec(agg_steadysolu_pd,
                                           wgt_or_max=exo_or_endo_graph_row_select)
        min_int_new, max_int_new, int_rate_counts, int_vec_new = \
            next_r_bounds(R_INFORM_BORR, int_rate_counts,
                          aggregate_inf_borrow, aggregate_inf_save)
        int_vec = int_vec_new

    """
    5. Graph demand and supply of interest rate 
    """
    if ('graph_demand_supply_interest' in graph_list):
        image_folder = save_directory['img_main']

        image_save_name = proj_sup_filename.file_suffix(equilibrium=True)['image_DS_curves'] + \
                          file_save_suffix_init + ''
        title_display = title_init

        graphdemandsupply.graph_demand_supply_interest(
            R_INFORM_BORR, aggregate_inf_borrow, aggregate_inf_save,
            title_display, image_save_name, image_folder)

    return initial_int_vec


def next_r_bounds(int_vec, int_rate_counts,
                  borr_vec, save_vec, algorithm_old=False):
    """
    Parameters
    ----------
    int_vec: 1d array
        int_vec = np.array([0.95,
                        1.0125,
                        1.075,
                        1.1375,
                        1.2])
    borr_vec: 1d array
        same len as int_vec
        borr_vec = np.array([-24.50784453,
                        -2.639024908,
                        -0.247764452,
                        -0.001920397,
                        -8.79E-08])
    save_vec: 1d array    
        same len as int_vec
        save_vec = np.array([0.000528161,
                        0.316690569,
                        3.508032947,
                        22.17614478,
                        36.32750355])
    algorithm_old: Boolean
        True or False
        old algorithm was wasting many evaluation points, suppose 4 points
            - 1,2,3,4
            - then 2,2.33,2.66,3, don't need to evaluate at 2 and 3
        for updated new algortihm: 
            - 1,2,3,4
            - 1,2--4 points here--3,4
        
    """

    min_int = int_vec[0]
    max_int = int_vec[-1]

    gap_vec = borr_vec + save_vec
    less_than = (0 > gap_vec)

    less_than_count = np.where(less_than)[0]

    '''
    Test if less_than_count is sequential, whether there are jumps
    '''
    has_jump = False
    for gap in np.diff(less_than_count):
        if (gap > 1):
            has_jump = True
            less_than_first = np.argmax(0 < gap_vec)
            less_than_count[less_than_first - 1]
            break

    # old
    #     int_vec_len = len(int_vec)
    # updated
    int_vec_len = int_rate_counts

    if (len(less_than_count) == 0):
        '''
        Interest Rate was not low enough before:
            So we should move interest rate downwards more in new iteration
            not sure if this works
            I will do a half size downshift. 
            originally: A to B for N points
            new: A-(1/2)(B-A) to A for N points
            
            Then do linspace with N+1 elements, then take away final, so do not calculate
            twice at r=A
            
            max_int = 1.2
            min_int = 0.8875
            min_int_new = min_int - (max_int-min_int)/4
            max_int_new = min_int
        '''

        min_int_new = min_int - (max_int - min_int) / 4
        max_int_new = min_int

        if (int_vec_len == 3):
            # BISECTION EXTEND ONE POINT TO LEFT
            int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len - 1)
        else:
            int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len + 1)

        int_vec_new = int_vec_new[:-1]

    elif (len(less_than_count) == len(int_vec)):
        '''
            min_int_new = max_int 
            max_int_new = max_int + (max_int-min_int)/4        
        '''
        min_int_new = max_int
        max_int_new = max_int + (max_int - min_int) / 4

        if (int_vec_len == 3):
            # BISECTION EXTEND ONE POINT TO RIGHT
            int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len + 1)
        else:
            int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len + 1)

        int_vec_new = int_vec_new[1:]

    else:
        '''
        Can zoom into one of the 'middle' element of interest rate vector
        '''
        if (has_jump):
            new_min_int_idx = less_than_first - 1
        else:
            new_min_int_idx = np.where(less_than)[0][-1]

        new_max_int_idx = new_min_int_idx + 1

        min_int_new = int_vec[new_min_int_idx]
        try:
            max_int_new = int_vec[new_max_int_idx]
        except IndexError:
            1

        # Drop first and Last element of array, where we already solved model
        if (algorithm_old == True):
            int_vec_new = np.linspace(min_int_new, max_int_new, len(int_vec))
        else:
            if (int_vec_len == 3):
                #                 BISECTION
                #                 this means when zooming in generate only 1 new point
                int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len)
            else:
                #                 this means when zooming in generate only int_vec_len new point
                int_vec_new = np.linspace(min_int_new, max_int_new, int_vec_len + 2)
            int_vec_new = int_vec_new[1:-1]

    min_int_new = int_vec_new[0]
    max_int_new = int_vec_new[-1]
    int_rate_counts = len(int_vec_new)

    return min_int_new, max_int_new, int_rate_counts, int_vec_new
