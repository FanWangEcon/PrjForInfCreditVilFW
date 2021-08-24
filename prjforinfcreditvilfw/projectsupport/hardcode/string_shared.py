'''
Created on Jun 26, 2018

@author: fan

import projectsupport.hardcode.string_shared as hardstring
'''
import os
import pathlib

import parameters.parse_combo_type as parsecombotype
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.hardcode.str_periodkey as hardcode_periodkey
import projectsupport.systemsupport as proj_sys_sup


def parse_command_line_str2list(combo_type_p3_arg):
    """
    combo_type_p3_arg might look like this: 'esti_param.alpha_k esti_param.beta'
    convert to list
    """
    if isinstance(combo_type_p3_arg, list):

        if len(combo_type_p3_arg) == 1:
            '''
            With batch when there are multiple parameters, they are put in one string:
                ['esti_param.alpha_k esti_param.beta']
            convert this to actual list
            this is from batch if this has space in between
            '''

            if len(combo_type_p3_arg[0].split(" ")) > 1:
                # we are in batch with multiple parameters
                combo_type_p3_arg_list = []
                for param_type_name in combo_type_p3_arg[0].split(" "):
                    combo_type_p3_arg_list.append(param_type_name)
                combo_type_p3_arg = combo_type_p3_arg_list

    return combo_type_p3_arg


def gen_esti_subfolder_name(param_combo, combo_type=None):
    """Generate seed specific estimation subfolder names

    Differentially generate subfolder estimation storage names based on whether results is based
    on prior mpoly estimations.
    """

    # subfolder name, looks like: C1E21M3S3_c3 of esti\e_20201025x_esr_list_tKap_mlt_ce1a2\C1E21M3S3_c3
    estitype_folder_name = param_combo['param_update_dict']['support_arg']['compesti_short_name'] + \
                           param_combo['param_combo_list_ctr_str']

    if combo_type is not None:
        if len(combo_type) == 5:
            # There are five elements, this means we are dealing with mplypostesti
            # subfolder name contains mplypostesti compesti_short_name, but also the mpoly short_name and
            # whether top 1, 2, or 3 etc result is been used.
            # C1E21M3S3_c3_mpolyC1E21M3S3t1: C1E21M3S3 estimation, using c3 3rd seed, and using best estimate top
            # t1 from mpolyC1E21M3S3.
            compesti_short_name_mpoly, esti_top_which_mpoly = \
                parsecombotype.parse_combo_type_e(combo_type_e=combo_type[4])
            estitype_folder_name = estitype_folder_name + '_mpoly' + \
                                   compesti_short_name_mpoly + 't' + str(esti_top_which_mpoly)

    return estitype_folder_name


def gen_compesti_short_name(compute_spec_key='ng_s_t', esti_spec_key='esti_tinytstthin_11', moment_key=3,
                            momset_key=3):
    """Subfolder prefix for esti-rand-simu

    Generating prefix for subfolders to store results for each seed's estimation/simulation.

        \esti\e_20201025x_esr_list_tKap_mlt_ne1a2\C1E126M4S3_c0
        C1E126M4S3_c1
        C1E126M4S3_c2
        C1E126M4S3_c3
        C1E126M4S3_c4
    """
    spec_key_index = computespec.spec_key_counter(compute_spec_key, fargate=False)
    esti_key_index = estispec.esti_key_counter(esti_spec_key)

    compesti_short_name = 'C' + str(spec_key_index) + 'E' + str(esti_key_index) + \
                          'M' + str(moment_key) + 'S' + str(momset_key)

    return compesti_short_name


def combo_type_date_type_combine(combo_type_list_ab, combo_type_list_date):
    """String construction for combo_type
    
    combo_type string determines folder name etc, need to analyze

    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    combo_type_list_ab_date = hardstring.combo_type_date_type_combine(combo_type_list_ab, combo_type_list_date)
    """

    return proj_hardcode_filename.combo_type_date_type_combine(combo_type_list_ab, combo_type_list_date)


def combo_type_decompose(combo_type, get_type='abc_date'):
    """String construction for combo_type
    
    combo_type string determines folder name etc, need to analyze

    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    abc_date = hardstring.combo_type_decompose(combo_type, get_type='abc_date')
    """

    combo_type_separate = '_'
    if get_type == 'abc_date':
        combo_type_1_str_list = combo_type[1].split(combo_type_separate)
        abc_date = combo_type[0] + combo_type_separate + combo_type_1_str_list[0]

    if get_type == 'simu_from_esti_abc_date':
        '''Already contains'''
        #         combo_type_1_str_list = combo_type[1].split(combo_type_separate)
        #         abc_date = combo_type_1_str_list[0] + combo_type_separate + combo_type_1_str_list[1]

        non_region_specific_esti_directory, append_or_add, save_folder, \
        last_folder_non_region_specific = get_generic_folder(save_directory='',
                                                             save_folder=combo_type[1],
                                                             add_date=False)

        abc_date = last_folder_non_region_specific

    return abc_date


def main_file_name(main_string_compo, suffix,
                   compesti_short_name=None,
                   save_directory=None,
                   combo_type=None,
                   save_type='simu_csv'):
    """Simulation CSV Names

    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    file_name = hardstring.main_file_name(main_string_compo, suffix, save_directory, save_type='csv')
    """
    if save_type == 'simu_csv':
        '''
        20180904x_ITG_kapp_endoexo.csv
        '''
        if (save_directory is None):
            save_file_name = main_string_compo[1] + suffix + '.csv'
        else:
            save_file_name = save_directory['csv'] + main_string_compo[1] + suffix + '.csv'

    elif 'esti_top_json_indi' in save_type:
        '''
        period_dictkey = main_string_compo
        '''

        period_dictkey = main_string_compo
        counter = suffix
        suffixstr = str(counter)

        if save_type == 'esti_top_json_indi' or compesti_short_name is None:
            # previous naming procedure before December 2020
            save_file_name = period_dictkey + 'c' + suffixstr + '.json'
        elif save_type == 'esti_top_json_indi_wth_cpetname':

            # cpet: compute esti short name
            # new naming procedure December 2020
            st_suffix = proj_hardcode_filename.sync_glob_esti_file_suffix(file_type='_top_json',
                                                                          compesti_short_name=compesti_short_name)
            save_file_name = period_dictkey + 'c' + suffixstr + st_suffix

            if combo_type is not None:
                if len(combo_type) == 5:
                    compesti_short_name_mpoly, esti_top_which_mpoly = parsecombotype.parse_combo_type_e(
                        combo_type_e=combo_type[4])
                    suffixstr = str(esti_top_which_mpoly)

                    save_file_name = save_file_name + '_t' + str(esti_top_which_mpoly) + compesti_short_name_mpoly

            save_file_name = save_file_name + '.json'
        else:
            raise TypeError(f'{save_type=} contains esti_top_json_indi, '
                            f'needs to be esti_top_json_indi or esti_top_json_indi_wth_cpetname')

    else:
        raise TypeError(f'{save_type=} needs to be simu_csv or contains esti_top_json_indi')

    return save_file_name


def file_suffix(file_type, sub_type='', integrated=False, ge=False):
    """
    Parameters
    ----------
    ge : bool
        ge boolean was added because specifying sub_type is equilibrium is not how some functions are structured
        so ge overrids sub_type when dealing with json

    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    suffix = hardstring.file_suffix(file_type='', sub_type='')
    """

    if file_type == 'csv':
        if sub_type == 'equilibrium' or sub_type == '_endo':
            suffix = '_endo'
        if sub_type == 'all_bisect_points' or sub_type == '_endoexo':
            suffix = '_endoexo'
        if sub_type == 'partial':
            suffix = '_exo'

    if file_type == 'json':
        if (sub_type == 'equilibrium') or ge:
            suffix = '_equ_wgtJ'
            if integrated:
                suffix = '_equitg_wgtJitg'
        else:
            # elif sub_type == 'partial':
            suffix = '_exo_wgtJ'
            if integrated:
                suffix = '_exoitg_wgtJitg'

    return suffix


def latex_do_strings(type, **kwargs):
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    moment_csv_strs = hardstring.latex_do_strings(type, **kwargs)
    """
    # structure new_command, to store probability parameters.
    # \newcommand{\DataNEoneIB}{0.092}
    # \newcommand{\DataNEoneIS}{0.03}

    if (type == 'tex.prob.data'):
        return 'Data' + kwargs['region'] + kwargs['period'] + kwargs['jinja_j'] + 'prob'
    if (type == 'tex.prob.simu'):
        return 'Simu' + kwargs['region'] + kwargs['period'] + kwargs['jinja_j'] + 'prob'
    if (type == 'tex.param'):
        period_dictkey_val = kwargs['period_dictkey_val']
        period_str_replacement = region_time_periodkey_stringonly()[period_dictkey_val]

        '''Some parameters have the date region key in name'''
        param_group_dot_name = kwargs['param_group_dot_name']
        for periodkey in list(region_time_periodkey_stringonly().keys()):
            if (periodkey in kwargs['param_group_dot_name']):
                str_replacement = region_time_periodkey_stringonly()[periodkey]
                param_group_dot_name = kwargs['param_group_dot_name'].replace(periodkey, str_replacement)

        param_key = period_str_replacement + kwargs['param_group'].replace("_", "").lower() + \
                    param_group_dot_name. \
                        replace(kwargs['param_group'], ''). \
                        replace(".", ""). \
                        replace("_", ""). \
                        upper()
        return param_key


def momentstype_suffix_regiontype(moments_type_eleone, type='folder_name'):
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    multi_periods, period_keys_esti_set = hardstring.momentstype_suffix_regiontype(moments_type_eleone)
    """

    if (type == 'folder_name'):
        multi_periods = False
        period_keys_esti_set = ''
        if (region_time_suffix()['_all_ne1a1ce1a1'][0] in moments_type_eleone):
            multi_periods = True
            period_keys_esti_set = region_time_suffix()['_all_ne1a1ce1a1'][1]
        elif (region_time_suffix()['_ne1a2'][0] in moments_type_eleone):
            multi_periods = True
            period_keys_esti_set = region_time_suffix()['_ne1a2'][1]
        elif (region_time_suffix()['_ce1a2'][0] in moments_type_eleone):
            multi_periods = True
            period_keys_esti_set = region_time_suffix()['_ce1a2'][1]
        else:
            raise ('Problem in momentstype_suffix_regiontype():' + moments_type_eleone)

        return multi_periods, period_keys_esti_set

    elif (type == 'folder_name_to_9901_period_dict_key'):
        period_keys_esti_set = ''
        if (region_time_suffix()['_all_ne1a1ce1a1'][0] in moments_type_eleone):
            period_keys_esti_set = region_time_dict()['_all_ne1a1ce1a1'][0]
        elif (region_time_suffix()['_ne1a2'][0] in moments_type_eleone):
            '''northeast'''
            period_keys_esti_set = region_time_dict()['ne1'][0]
        elif (region_time_suffix()['_ce1a2'][0] in moments_type_eleone):
            '''central'''
            period_keys_esti_set = region_time_dict()['ce1'][0]
        else:
            raise ('Problem in momentstype_suffix_regiontype():' + moments_type_eleone)

        return period_keys_esti_set

    # def get_generic_name(name_with_region_time_suffix=''):


def get_generic_folder(save_directory='',
                       save_folder=None,
                       add_date=True,
                       main_folder_name='s3local_esti',
                       same_root=False):
    """Non-region time specific sestimation results folder

    Assumes that estimation results are region or time specific, and will try to generate an aggregate folder where
    simulation results from different periods/time are aggregate together. This is done by generating a new folder
    whereever the existing directory is, without the region/time folder suffix.

    Parameters
    ----------
    save_directory : str
        full directory name given full directory name, find last folder and drop region specific components
        'C:/Users/fan/Documents/Dropbox (UH-ECON)\\Project Dissertation\\esti\\e_20201025x_esr_list_tKap_mlt_ce1a2\\'
    save_folder : str
        just the saving folder name saving folder name, keep up to region specific component
    same_root : bool
        If this is set to true, that means will have for example, esti\e_20201025x_esr_list_tKap as the new
        all region/time folder, based on esti\e_20201025x_esr_list_tKap_mlt_ce1a2 folder
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    non_region_specific_esti_directory,  append_or_add, save_folder, \
        last_folder_non_region_specific = hardstring.get_generic_folder(save_directory='', save_folder=None, add_date = True)
    """

    ce_suffix = region_time_suffix()['_ce1a2'][0]
    ne_suffix = region_time_suffix()['_ne1a2'][0]

    if (save_folder is None):
        find_suffix_in = save_directory
    else:
        find_suffix_in = save_folder

    if (ce_suffix in find_suffix_in):
        region_suffix = ce_suffix
        append_or_add = 'w'
    elif (ne_suffix in find_suffix_in):
        region_suffix = ne_suffix
        append_or_add = 'a'
    else:
        raise ValueError(f'{find_suffix_in=} does not contain region substring, do not use this')

    if same_root:
        # Generate new region-time agnostic folder in the same folder branch as the region-time folder

        # Path name without region suffix
        # 'C:/Users/fan/Documents/Dropbox (UH-ECON)\\Project Dissertation\\esti\\e_20201025x_esr_list_tKap'
        non_region_specific_esti_directory = save_directory[:save_directory.index(region_suffix)]

        # Generate new folder if does not exist
        pathlib.Path(non_region_specific_esti_directory).mkdir(parents=True, exist_ok=True)

        # Get new folder name
        # last_folder_non_region_specific = 'e_20201025x_esr_list_tKap'
        __, last_folder_non_region_specific = os.path.split(non_region_specific_esti_directory)
        non_region_specific_esti_directory = non_region_specific_esti_directory + os.sep
    else:

        if save_folder is None:
            save_folder = save_directory.split('/')[-2]

        date_suffix = ''
        if add_date:
            date_suffix = proj_sys_sup.save_suffix_time(format=1, dash=True)
        last_folder_non_region_specific = save_folder[:save_folder.index(region_suffix)] + date_suffix

        non_region_specific_esti_directory = proj_sys_sup.get_paths(main_folder_name,
                                                                    sub_folder_name=last_folder_non_region_specific)

    return non_region_specific_esti_directory, append_or_add, save_folder, last_folder_non_region_specific


def region_time_suffix(return_common_suffix=False, moment_key=None):
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    region_time_suffix = hardstring.region_time_suffix()
    """
    common_suffix_start = '_mlt'
    region_time_suffix = {'_ce1a2': [common_suffix_start + '_ce1a2', [1, 2]],
                          '_ne1a2': [common_suffix_start + '_ne1a2', [3, 4]],
                          '_all_ne1a1ce1a1': [common_suffix_start + '_all_ne1a2ce1a2', [1, 2, 3, 4]],
                          '_ce1': [common_suffix_start + '_ce1', [1]],
                          '_ce2': [common_suffix_start + '_ce2', [2]],
                          '_ne1': [common_suffix_start + '_ne1', [3]],
                          '_ne2': [common_suffix_start + '_ne2', [4]]}

    if moment_key is not None:
        # see: parameters/runspecs/estimate_specs.py:122
        if moment_key == 2:
            return region_time_suffix['_all_ne1a1ce1a1'][0]
        elif moment_key == 3:
            return region_time_suffix['_ce1a2'][0]
        elif moment_key == 4:
            return region_time_suffix['_ne1a2'][0]

    elif (return_common_suffix):
        return common_suffix_start
    else:
        return region_time_suffix


def region_time_next(cur_var='kappa_ce9901', both_periods=False, period_dictkey=None):
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    next_period_param = hardstring.region_time_next(early_period_param)
    """
    ce1 = peristr(period=1, action='str')
    ce2 = peristr(period=2, action='str')
    ne1 = peristr(period=3, action='str')
    ne2 = peristr(period=4, action='str')

    if both_periods:
        if period_dictkey in ce1:
            '''
            period_dictkey = 'ne9901'
            ce1 = '_ne9901'
            '''
            early_period_param = cur_var + ce1
            later_period_param = cur_var + ce2

            return early_period_param, later_period_param

        if period_dictkey in ne1:
            early_period_param = cur_var + ne1
            later_period_param = cur_var + ne2

            return early_period_param, later_period_param
    else:
        if ce1 in cur_var:
            return cur_var.replace(ce1, ce2)
        elif ne1 in cur_var:
            return cur_var.replace(ne1, ne2)
        else:
            raise ('bad region_time_next:%s', early_period_param)


def region_time_periodkey_stringonly():
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    period_keys_stringonly = hardstring.region_time_periodkey_stringonly()
    """
    period_keys_stringonly = {region_time_dict()['ce1'][0]: 'ceNNZO',
                              region_time_dict()['ce2'][0]: 'ceZTZN',
                              region_time_dict()['ne1'][0]: 'neNNZO',
                              region_time_dict()['ne2'][0]: 'neZTZN'}

    return period_keys_stringonly


def region_time_dict(return_periods_keys=False):
    """
    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    periods_keys = hardstring.region_time_dict()
    """
    periods_keys_dict = {'ce1': ['ce9901', 1],
                         'ce2': ['ce0209', 2],
                         'ne1': ['ne9901', 3],
                         'ne2': ['ne0209', 4]}

    if (return_periods_keys):
        periods_keys = {1: periods_keys_dict['ce1'][0],
                        2: periods_keys_dict['ce2'][0],
                        3: periods_keys_dict['ne1'][0],
                        4: periods_keys_dict['ne2'][0]}
        return periods_keys
    else:
        return periods_keys_dict


def peristr(period=None, action='str'):
    """Combined string of the two for command line invoke

    period string control

    import parameters.runspecs.estimate_specs as estispec
    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')
    compute_spec_key = spec_key_dict['compute_spec_key']
    esti_spec_key = spec_key_dict['esti_spec_key']

    Examples
    --------
    import parameters.loop_combo_type_list.param_str as paramloopstr
    period_str = paramloopstr.peristr(period=0, action='period_name')
    periods = paramloopstr.peristr(action='list')
    """

    return hardcode_periodkey.peristr(period=period, action=action)


def moment_csv_strs_cates():
    """
    """
    period_dict_key_cates = {}
    for key, val in region_time_dict().items():
        period_dict_key_cates[key] = [val[0], val[1]]

    moment_pd_cate_vars = \
        {'data_model':
             {'colname': 'data_model',
              'cates': {'data': ['data', 0],
                        'model': ['model', 1]}},
         'period_dictkey':
             {'colname': 'period_dictkey',
              'cates': period_dict_key_cates}}

    return moment_pd_cate_vars


def moment_csv_strs():
    """
    used in several places:
    1. solu_20180701_basicJ7_basic.csv
        - generated by analyzesolu.py
        - storing all optimal choics at all solved for state space points
    2. reviewed in: check_soluj7.py

    note these are not on interpolation grid, just the solution grid

    Examples
    --------
    import projectsupport.hardcode.string_shared as hardstring
    moment_csv_strs = hardstring.moment_csv_strs()
    period_dictkey = hardstring.moment_csv_strs()['period_dictkey'][1]
    """
    moment_pd_col_names = \
        {'esti_obj': ['esti_obj',
                      'esti_obj',
                      'key name for where all moments objectives are stored'],
         'main_obj': ['main_obj',
                      'esti_obj.main_obj',
                      'key name for period specific objectives'],
         'main_allperiods_obj': ['main_allperiods_obj',
                                 'esti_obj.main_allperiods_obj',
                                 'key that stores moment objective summed up all periods'],
         'agg_prob_obj': ['agg_prob',
                          'esti_obj.subsets_other.agg_prob',
                          'always calcualte how well just the probabilities match up'],
         'BI_obj': ['BI_obj',
                    'esti_obj.subsets_main.equi_BI',
                    'just the equilibrium BI diff gap'],
         'period_dictkey': ['period_dictkey',
                            'period_dictkey',
                            'key that stores which period the results are for, this is parallel to esti_obj key'],
         'R_INFORM': ['R_INFORM_BORR',
                      'esti_param.R_INFORM_BORR',
                      'Interest rate might be equilibrium or not'],
         'BNF_SAVE_P': ['BNF_SAVE_P',
                        'esti_param.BNF_SAVE_P',
                        'formal saving fixed cost'],
         'BNF_BORR_P': ['BNF_BORR_P',
                        'esti_param.BNF_BORR_P',
                        'formal borrowing fixed cost'],
         'kappa': ['kappa',
                   'esti_param.kappa',
                   'Interest rate might be equilibrium or not'],
         'R_FORMAL_SAVE': ['R_FORMAL_SAVE',
                           'esti_param.R_FORMAL_SAVE',
                           'Formal saving interest rate'],
         'R_FORMAL_BORR': ['R_FORMAL_BORR',
                           'esti_param.R_FORMAL_BORR',
                           'Formal borrowing interest rate'],
         }

    return moment_pd_col_names


def get_solu_var_suffixes():
    """
    used in several places:
    1. solu_20180701_basicJ7_basic.csv
        - generated by analyzesolu.py
        - storing all optimal choics at all solved for state space points
    2. reviewed in: check_soluj7.py

    note these are not on interpolation grid, just the solution grid

    Sample
    ------
        import projectsupport.hardcode.string_shared as hardstring
        solu_var_suffixes = hardstring.get_solu_var_suffixes()
    """

    '''For steady state, names for storing results, append choice_names to each'''

    solu_var_suffixes = {'cash': 'cash_tt',
                         'k_tt': 'k_tt',
                         'b_tt': 'b_tt',
                         'eps_tt': 'eps_tt',
                         'ktp_opti': 'kn',
                         'btp_opti': 'bn',
                         'btp_fb_opti': 'bn_fb',
                         'btp_ib_opti': 'bn_ib',
                         'btp_fs_opti': 'bn_fs',
                         'btp_il_opti': 'bn_il',
                         'consumption_opti': 'cc',
                         'probJ_opti': 'prob',
                         'EjV': 'EjV',
                         'util_opti_eachj': 'jV'}

    return solu_var_suffixes


def get_steady_var_suffixes():
    """
    used in several places:
    1. condidist_analytical.py
        - column names, combined with choice_names for simu_output_pd panda file,
        stored in files like: steady_20180623_Aprd_A_0_exo_wgtJ.csv
    2. momenst.py
        - get columns from simu_output_pd, aggregate to generate moments
    3.

    Sample
    ------
        import projectsupport.hardcode.string_shared as hardstring
        steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    """

    '''For steady state, names for storing results, append choice_names to each'''

    steady_var_suffixes = {'marginal_dist': 'marginal_dist',
                           'cash_grid_centered': 'cash_grid_centered',
                           'btp_opti_grid': 'btp_opti_grid',
                           'ktp_opti_grid': 'ktp_opti_grid',
                           'consumption_opti_grid': 'consumption_opti_grid',
                           'y_opti_grid': 'y_opti_grid',
                           'probJ_opti_grid': 'probJ_opti_grid',
                           'btp_fb_opti_grid': 'btp_fb_opti_grid',
                           'btp_ib_opti_grid': 'btp_ib_opti_grid',
                           'btp_fs_opti_grid': 'btp_fs_opti_grid',
                           'btp_il_opti_grid': 'btp_il_opti_grid',
                           'btp_fbfsloggap_opti_grid': 'btp_fbfsloggap_opti_grid',
                           'btp_ibilloggap_opti_grid': 'btp_ibilloggap_opti_grid',
                           'btp_ibilgap_opti_grid': 'btp_ibilgap_opti_grid'}

    return steady_var_suffixes


def get_steady_var_cts_desc():
    """
    Sample
    ------
        import projectsupport.hardcode.string_shared as hardstring
        steady_var_cts_desc = hardstring.get_steady_var_cts_desc()
    """
    steady_var_cts_desc = {'marginal_dist': ['Marginal Distribution', 'long'],
                           'cash_grid_centered': ['cur cash', 'Cash Steady State Interpolation Points'],
                           'btp_opti_grid': ['b next', 'Optimal Bn choice at Steady State Interpolation point'],
                           'ktp_opti_grid': ['k next', 'Optimal Kn choice at Steady State Interpolation point'],
                           'consumption_opti_grid': ['c curr',
                                                     'Optimal current consumption choice at Steady State Interpolation point'],
                           'y_opti_grid': ['E[y(k,esp)]', 'Integrating over eps given k choice, expected income'],
                           'probJ_opti_grid': ['prob j', 'probJ_opti_grid probability'],
                           'btp_fb_opti_grid': ['borr formal', 'btp_fb_opti_grid'],
                           'btp_ib_opti_grid': ['borr informal', 'btp_ib_opti_grid'],
                           'btp_fs_opti_grid': ['save formal', 'btp_fs_opti_grid'],
                           'btp_il_opti_grid': ['lend informal', 'btp_il_opti_grid'],
                           'btp_fbfsloggap_opti_grid': ['log(abs(fb-fs))', 'log(Capital outflow)'],
                           'btp_ibilloggap_opti_grid': ['log(abs(ib-il))', 'log(Informal Market Excess Borrow)'],
                           'btp_ibilgap_opti_grid': ['(ib-il)', '(Informal Market Excess Borrow)']}

    return steady_var_cts_desc


def steady_aggregate_suffixes():
    """
    Can aggregate:
        1. for each j of J: aggregate conditionally, marginally, over cc, kn, bn, prob choices
        2. for all j of J: aggregate all c, kn, bn, choices

    Sample
    ------
        import projectsupport.hardcode.string_shared as hardstring
        steady_agg_suffixes = hardstring.steady_aggregate_suffixes()
    """
    steady_agg_suffixes = {'_allJ_agg': ['_allJ_agg', 'All J Aggregating'],
                           '_j_agg': ['_j_agg', 'each j aggregating'],
                           '_j_agg_ifj': ['_j_agg_ifj', 'each j aggregating, if j chosen'],
                           '_var': ['_var', 'variance key']}

    return steady_agg_suffixes
