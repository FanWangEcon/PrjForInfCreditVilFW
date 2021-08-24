'''
File and Path names
Created on Sep 13, 2018

import projectsupport.hardcode.file_name as proj_hardcode_filename

@author: fan
'''

import os

import parameters.parse_combo_type as parsecombotype
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup


def sync_glob_esti_file_suffix(file_type, compesti_short_name=None):
    """String construction for combo_type
    
    combo_type string determines folder name etc, need to analyze

    Parameters
    ----------
    compesti_short_name : str
        string of comp esti name, like *C1E126M4S3*, add these to suffix if this is not None

    Examples
    --------
    import projectsupport.hardcode.file_name as proj_hardcode_filename
    combo_type_list_ab_date = proj_hardcode_filename.sync_glob_esti_file_suffix(file_type)
    """

    st_suffix = ''
    if compesti_short_name is not None:
        st_suffix = '_' + compesti_short_name

    if (file_type == '_top_datamodel'):
        # for top results, add suffix. This distinguishes top results from mpoly step 1 and step 3.
        return '_top_datamodel' + st_suffix
    elif (file_type == '_top_json'):
        # JSON like ce9901c2_C2E105M3S3.json, add suffix to make it easier to upload to S3
        return st_suffix + '_top_json'
    elif (file_type == '_main_lhsrhs'):
        return '_main_lhsrhs'
    elif (file_type == '_main_lhsrhs_new'):
        return '_main_lhsrhs_new'
    elif (file_type == '_mpoly_reg_coef'):
        return '_mpoly_reg_coef'
    elif (file_type == '_modelsimu_regress'):
        return '_modelsimu_regress'
    else:
        pass


def combo_type_date_type_combine(combo_type_list_ab, combo_type_list_date):
    """String construction for combo_type
    
    combo_type string determines folder name etc, need to analyze

    Examples
    --------
    combo_type_list_ab_date = hardstring.combo_type_date_type_combine(combo_type_list_ab, combo_type_list_date)
    """

    combo_type_separate = '_'
    return combo_type_list_ab + combo_type_separate + combo_type_list_date


def file_json(file_save_suffix):
    """
    Examples
    --------
    import projectsupport.hardcode.file_name as proj_hardcode_filename
    json_file_name = proj_hardcode_filename.file_json(file_save_suffix)
    """

    json_file_name = 's' + file_save_suffix + '.json'

    return json_file_name


def file_suffix(equilibrium, integrated=False):
    """2. Solve and Simulate (save results to key summary results json)
    
    Examples
    --------
    import projectsupport.hardcode.file_name as proj_hardcode_filename    
    equilibrium = True
    integrated = True
    suf_dict = proj_sup_filename.file_suffix(equilibrium, integrated)
    exo_or_endo = suf_dict['exo_or_endo']
    exo_or_endo_json_search = suf_dict['exo_or_endo_json_search']
    exo_or_endo_graph_row_select = suf_dict['exo_or_endo_graph_row_select']
    image_save_name_prefix = suf_dict['image_save_name_prefix']
    image_save_name_prefix_exo = suf_dict['image_save_name_prefix_exo']    
    """

    if (equilibrium):
        image_DS_curves = 'DS'
        if (integrated):
            exo_or_endo = '_equitg'
            # include only integrated results
            exo_or_endo_json_search = '*' + exo_or_endo + '_*Jitg*'
            # see lines 109 in steady_loop_integrate.steady_loop_integrate.py
            exo_or_endo_graph_row_select = '_wgtJitg'
            image_save_name_prefix = 'AGG_EQU_'
            image_save_name_prefix_exo = 'AGG_equEXO_'

        else:
            exo_or_endo = '_equ'
            exo_or_endo_json_search = '*' + exo_or_endo + '_*'
            # see lines 121, 145 in steadyinnerloop.steady_loop_inner.py
            exo_or_endo_graph_row_select = '_wgtJ'
            image_save_name_prefix = 'AGG_EQU_'
            image_save_name_prefix_exo = 'AGG_equEXO_'
    else:
        image_DS_curves = None
        if (integrated):
            exo_or_endo = '_exoitg'
            exo_or_endo_json_search = '*' + exo_or_endo + '_*'
            # see lines 109 in steady_loop_integrate.steady_loop_integrate.py
            # see lines 226 in invoke.saverun.local_estimate_save line 226
            exo_or_endo_graph_row_select = exo_or_endo + '_wgtJitg'
            # INT already at the end 
            image_save_name_prefix = 'AGG_EXO_'
            image_save_name_prefix_exo = 'AGG_EXO_'

        else:
            exo_or_endo = '_exo'
            exo_or_endo_json_search = '*' + exo_or_endo + '_*'
            # see lines 121, 145 in steadyinnerloop.steady_loop_inner.py
            # see lines 226 in invoke.saverun.local_estimate_save line 226
            exo_or_endo_graph_row_select = exo_or_endo + '_wgtJ'

            image_save_name_prefix = 'AGG_EXO_'
            image_save_name_prefix_exo = 'AGG_EXO_'

    '''
    Return dictionary
    '''
    suf_dict = {}
    suf_dict['exo_or_endo'] = exo_or_endo
    suf_dict['exo_or_endo_json_search'] = exo_or_endo_json_search
    suf_dict['exo_or_endo_graph_row_select'] = exo_or_endo_graph_row_select
    suf_dict['image_save_name_prefix'] = image_save_name_prefix
    suf_dict['image_save_name_prefix_exo'] = image_save_name_prefix_exo
    suf_dict['image_DS_curves'] = image_DS_curves

    return suf_dict


def get_path_to_mpoly_reg_coef(combo_type, main_folder_name='esti'):
    """get the path to mpoly estimation results file

    When called from inside docker, the folder root will be the /data/ folder. This means when this function
    is called to copy a JSON file into container from S3, this is the destination folder path, not the origin.

    The origin folder path is almost identical without the /data/ initial folder, replace that with the S3 bucket
    name.

    return
    ------
    str
        return path to file on docker container. i.e.:
        \data\esti\e_20201025x_esr_medtst_list_tKap_mlt_ce1a2\e_20201025x_esr_medtst_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv
    """

    esti_folder = proj_sys_sup.get_paths(main_folder_name=main_folder_name)
    combo_type_list_ab_date = combo_type_date_type_combine(combo_type[0], combo_type[1])
    folder = esti_folder + combo_type_list_ab_date

    file_name = combo_type_list_ab_date + sync_glob_esti_file_suffix(file_type='_mpoly_reg_coef')
    folder_file_name = os.path.join(folder, file_name + '.csv')

    return folder_file_name


def get_path_to_top_json(combo_type, main_folder_name='esti'):
    """Get the path to a particular TOP JSON file given combo_type
    a file like this: D:\repos\ThaiJMP\esti\e_20201025x_esr_tstN5_vig_list_tKap_mlt_ne1a2\ne9901c1_C2E84M4S3_top_json
    """

    """
    METHOD 1:
    Assume that the JSON file in the same subfolder, meaning in an earlier ESR step of the same call sequence        
    METHOD 2:
    ASSUME that JSON file is in some alternative folder potential then the folder determined by current combo_type                 
    """
    # Folder
    bl_esr_json = parsecombotype.parse_combo_type_e_check(combo_type[4])

    if bl_esr_json:
        spt_main_folder = proj_sys_sup.get_paths(main_folder_name=main_folder_name)
        combo_type_list_ab_date = combo_type_date_type_combine(combo_type[0], combo_type[1])
        folder = spt_main_folder + combo_type_list_ab_date

        # File name components
        period_dictkey = hardstring.momentstype_suffix_regiontype(combo_type[1],
                                                                  type='folder_name_to_9901_period_dict_key')
        compesti_short_name, esti_top_which = parsecombotype.parse_combo_type_e(combo_type_e=combo_type[4])
        # File name
        # file = 'ce9901c1_C1E31M3S3_top_json.json'
        file = hardstring.main_file_name(period_dictkey, esti_top_which,
                                         compesti_short_name=compesti_short_name,
                                         save_type='esti_top_json_indi_wth_cpetname')

        # Overall path
        # local example: 'D:/repos/ThaiJMP\\esti\\e_20201025x_esr_tstN5_vig_list_tKap_mlt_ce1a2\\ce9901c1_C1E31M3S3_top_json.json'
        # docker example: 'data/esti/e_20201025x_esr_tstN5_vig_list_tKap_mlt_ce1a2/ce9901c1_C1E31M3S3_top_json.json'
        folder_file_name = os.path.join(folder, file)
    else:
        spt_master_directory = proj_sys_sup.main_directory()
        # Local example:
        # D:\repos\ThaiJMP\simu_tst\M4S3_top_json.json
        if '.json' in combo_type[4]:
            folder_file_name = os.path.join(spt_master_directory, combo_type[4])
        else:
            folder_file_name = os.path.join(spt_master_directory, combo_type[4] + '.json')

    # return
    folder_file_name = folder_file_name.replace(os.sep, '/')

    return folder_file_name


def get_path_to_top_json_parametersfolder(combo_type):
    """Same as :func:`get_path_to_top_json`, but from parameter folder

    Initially, got information from the parameters folder
    """
    folder_json = proj_sys_sup.get_paths_in_git('parameters.json')
    abc_date = hardstring.combo_type_decompose(combo_type, get_type='simu_from_esti_abc_date')
    sub_folder_name = proj_sys_sup.gen_path([combo_type[0], abc_date], st_type='simuesti_subfolder')
    # 'D:/repos/ThaiJMP\\parameters\\json\\e_20201025x_esr_tstN5_vig_list_tKap/'
    folder = os.path.join(folder_json, sub_folder_name, '')

    # get period_dictkey: 'ce9901'
    period_dictkey = hardstring.momentstype_suffix_regiontype(combo_type[1],
                                                              type='folder_name_to_9901_period_dict_key')
    # Get current estimate file name and import the JSON from best MPOLY
    compesti_short_name, esti_top_which = parsecombotype.parse_combo_type_e(combo_type_e=combo_type[4])
    # file = 'ce9901c1_C1E31M3S3_top_json.json'
    file = hardstring.main_file_name(period_dictkey, esti_top_which,
                                     compesti_short_name=compesti_short_name,
                                     save_type='esti_top_json_indi_wth_cpetname')

    # file_path: 'D:/repos/ThaiJMP\\esti\\e_20201025x_esr_tstN5_vig_list_tKap_mlt_ce1a2\\ce9901c1_C1E31M3S3_top_json.json'
    folder_file_name = os.path.join(folder, file)

    return folder_file_name
