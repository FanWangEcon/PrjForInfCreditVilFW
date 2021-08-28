'''
Created on Sep 13, 2018

@author: fan
'''

import analyze.analyzeequi as analyzeequi
import estimation.postprocess.jsoncsv.gen_top_estimates_df as top_estimate
import projectsupport.datamanage.data_from_json as datajson
import projectsupport.hardcode.file_name as proj_sup_filename
import projectsupport.systemsupport as proj_sys_sup


def gen_agg_csv_from_json(combo_type, param_combo,
                          ge, compute_specs,
                          save_directory_dict,
                          graph_list,
                          panda_df_save_best=False):
    """Obtain CSV file from JSONs in JSON folder
    
    1. invoked when estimation is finished (so capture all jsons if estimation is done)
    2. invoked at M estimation iteration intervals (so if for some reason, estimation breaks down, will have kept most results)
    3. invoked when estimation max iteration I set has been reached (this means we will not reach 1, there will be exception)
    
    main_directory = save_directory_sub
    json_directory = proj_sys_sup.get_paths(save_directory, sub_folder_name=estitype_folder_name,
                                            subsub_folder_name='json') 
    save_directory_dict = {}
    save_directory_dict['json'] = json_directory
    save_directory_dict['img_main'] = main_directory
    save_directory_dict['csv'] = main_directory
    
    Examples
    --------
    import estimation.postprocess.jsoncsv.gen_agg_csv_from_json as gen_csvaggjson
    gen_csvaggjson.gen_agg_csv_from_json(combo_type, param_combo,
                                         ge, compute_specs,
                                         save_directory_dict, 
                                         graph_list)
    """

    integrated = False
    if ('_ITG_' in combo_type[1]):
        integrated = True

    suf_dict = proj_sup_filename.file_suffix(equilibrium=ge, integrated=integrated)

    exo_or_endo = suf_dict['exo_or_endo']
    exo_or_endo_json_search = suf_dict['exo_or_endo_json_search']
    exo_or_endo_graph_row_select = suf_dict['exo_or_endo_graph_row_select']
    image_save_name_prefix = suf_dict['image_save_name_prefix']
    image_save_name_prefix_exo = suf_dict['image_save_name_prefix_exo']

    panda_df_save_filename = combo_type[1] + exo_or_endo + '.csv'
    agg_df_name_and_directory = save_directory_dict['img_main'] + panda_df_save_filename
    panda_df = datajson.json_to_panda(
        directory=save_directory_dict['json'],
        file_str='*' + combo_type[1] + exo_or_endo_json_search,
        agg_df_name_and_directory=agg_df_name_and_directory)

    """
    5. Graphing Steady State Aggregate
    """
    if (ge):
        select_r_equi = True
        R_INFORM_BORR = None
        title_display = param_combo['title']
    else:
        select_r_equi = False
        R_INFORM_BORR = panda_df['esti_param.R_INFORM_BORR'].iloc[0]
        title_display = param_combo['title'] + '\n Exogenous Fixed R=' + str(R_INFORM_BORR)

    combo_list = [param_combo]
    #     compute_specs = compesti_specs
    analyzeequi.equi_graph_main(combo_type, combo_list, compute_specs,
                                jsons_panda_df=panda_df,
                                exo_or_endo_graph_row_select=exo_or_endo_graph_row_select,
                                select_r_equi=select_r_equi,
                                save_directory=save_directory_dict,
                                title_display=title_display,
                                image_save_name_prefix=image_save_name_prefix,
                                graph_list=graph_list)

    '''
    6. Resave to keep only top
        but do this after graphs have been made
    '''
    if (panda_df_save_best):
        '''
        see: 
            estimate.py:l356
            estimate_objective_multiperiods:l86
        panda_df already saved to:
            save_directory_dict['img_main'] + panda_df_save_filename
        re-save only a subset of file, the top estimate by objective
            codes copied over basically from gen_top_estimates_df
        '''
        top_estimates_keep_count = 1
        panda_df = top_estimate.top_estimates_df(panda_df, top_estimates_keep_count)
        proj_sys_sup.save_panda(agg_df_name_and_directory, panda_df)
