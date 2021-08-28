'''
Created on Sep 3, 2018

@author: fan
'''

import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup
import estimation.postprocess.texdo.texdo_gen_distribute as esti_texdo_gendist


def gen_simu_params(top_esti_df, save_directory, update_param_counter_folder=True, compesti_short_name=None,
                    combo_type=None):
    """
    grab current json directory and json filename from df
        - json_directory
        - json_file_name
    grab also region and time vars
        - period_dictkey
    conditional only on estimation results, not data, just model
    
    groupby(period_dictkey) + ctr if data_model == model
    new_file_name = period_dictkey + ctr    

    Parameters
    ----------
    compesti_short_name : str
        string of comp esti name, like *C1E126M4S3*, add these to suffix if this is not None

    Examples
    --------
    import estimation.postprocess.gen_simu_params as gen_simu_params
    top_esti_df = ''
    save_directory = ''
    gen_simu_params(top_esti_df, save_directory)
    """

    '''
    1. Only model rows
    '''
    top_esti_df_model_only = top_esti_df[top_esti_df['data_model'] == 'model']

    '''
    2. unique region time keys
    '''
    period_dictkey_unique = top_esti_df_model_only['period_dictkey'].unique()

    '''
    3. loop over
    '''
    for period_dictkey in period_dictkey_unique:

        '''
        3a. only current region
        '''
        top_esti_df_cur = top_esti_df_model_only[top_esti_df_model_only['period_dictkey'] == period_dictkey]

        copy_json = False
        '''
        3b. grab out columns storing urls json
        '''
        counter = 0
        for index, row in top_esti_df_cur.iterrows():
            counter = counter + 1

            new_file_name = hardstring.main_file_name(period_dictkey, counter,
                                                      compesti_short_name=compesti_short_name,
                                                      combo_type=combo_type,
                                                      save_type='esti_top_json_indi_wth_cpetname')
            next_folder_file = save_directory + new_file_name

            if (copy_json):
                '''
                copy json if json file exists
                '''
                json_directory = row['json_directory']
                json_file_name = row['json_file_name']
                cur_folder_file = json_directory + json_file_name
                next_folder_file = save_directory + new_file_name
                proj_sys_sup.copy_rename(cur_folder_file, next_folder_file)

            else:
                '''
                Convert from csv
                '''
                row_dict_nonan = esti_texdo_gendist.csv_to_dict(df_row=row)

                '''
                4b. Save non-aggregate file with local specific names to non-Aggregate Folder
                '''
                saveFileDirectory = next_folder_file
                proj_sys_sup.save_json(saveFileDirectory, row_dict_nonan, replace=True, s3=True, add_time=False)

                '''
                4b1. Save non-aggregate file with local specific names to Aggregate Folder
                '''
                non_region_specific_esti_directory, append_or_add, last_folder, \
                last_folder_non_region_specific \
                    = hardstring.get_generic_folder(save_directory=save_directory, same_root=True)
                saveFileDirectory = non_region_specific_esti_directory + new_file_name
                proj_sys_sup.save_json(saveFileDirectory, row_dict_nonan, replace=True, s3=True, add_time=False)

                if (update_param_counter_folder):
                    __, __, __, last_folder_non_region_specific = hardstring.get_generic_folder(
                        save_directory=save_directory, add_date=False, same_root=True)
                    parameters_json_folder = proj_sys_sup.get_paths_in_git('parameters.json')
                    parameters_json_subfolder = proj_sys_sup.get_paths(parameters_json_folder,
                                                                       sub_folder_name=last_folder_non_region_specific)
                    folder_file = parameters_json_subfolder + new_file_name
                    proj_sys_sup.save_json(folder_file, row_dict_nonan, replace=True, s3=False, add_time=False)
