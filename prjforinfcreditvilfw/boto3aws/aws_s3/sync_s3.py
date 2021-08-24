'''
Created on Aug 30, 2018

@author: fan
'''

import logging
from subprocess import call

import parameters.loop_combo_type_list.param_combo_type_list as paramloopstr
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

aws_sync_command = 'aws s3 sync'


def sync_s3_local_s3_folders():
    """
    Examples
    --------
    import boto3aws.aws_s3.sync_s3 as sync_s3
    folders = sync_s3.sync_s3_local_s3_folders()
    s3_directory_main = folders['s3_directory_main']
    local_sync_directory_main = folders['local_sync_directory_main']
    """
    folders = {}
    '''
        i.e.: C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation EC2/
    '''
    d_root = proj_sys_sup.s3_local_sync_folder()
    '''
        bucket in use, i.e.: 'thaijmp201809j8var'
    '''
    bucket_name = proj_sys_sup.s3_bucket_name()
    folders['s3_directory_main'] = 's3://' + bucket_name
    '''
        local sync folder full name
    '''
    folders['local_sync_directory_main'] = '' + d_root + bucket_name

    return folders


def gen_sync_str(s3_directory=None,
                 local_directory=None,
                 main_folder='',
                 sub_folder='',
                 aws_sync_command=aws_sync_command,
                 sync_condi='png'):
    """
    Examples    
    --------
    import boto3aws.aws_s3.sync_s3 as sync_s3
    sync_s3.gen_sync_str(main_folder = '', sync_condi = 'png')
    """

    folders = sync_s3_local_s3_folders()
    if (s3_directory is None):
        s3_directory = folders['s3_directory_main']
    if (local_directory is None):
        local_directory = folders['local_sync_directory_main']

    main_sub_folder = main_folder
    if ((main_folder != '') and (sub_folder != '')):
        main_sub_folder = main_folder + '/' + sub_folder

    if (main_sub_folder != ''):
        s3_directory = '\"' + s3_directory + '/' + main_sub_folder + '\"'
    if (main_sub_folder != ''):
        local_directory = '\"' + local_directory + '/' + main_sub_folder + '\"'

    if (sync_condi == 'png'):
        sync_condi_str = '--exclude \"*\" --include \"*.png\"'
    if (sync_condi == 'csv'):
        sync_condi_str = '--exclude \"*\" --include \"*.csv\"'

    estisimu_command_line_list = [aws_sync_command, s3_directory, local_directory, sync_condi_str]
    s3_sync_estisimu = " ".join(estisimu_command_line_list)

    return s3_sync_estisimu


def sync_loop_paramstr_key_list(combo_type_list_ab,
                                combo_type_list_date,
                                save_directory_main,
                                paramstr_key_list,
                                sync_condi='png'):
    combo_type_list = paramloopstr.gen_combo_type_list(file=combo_type_list_ab,
                                                       date=combo_type_list_date,
                                                       paramstr_key_list_str=paramstr_key_list)
    for combo_type in combo_type_list:
        combo_type_list_ab_date = proj_hardcode_filename.combo_type_date_type_combine(combo_type[0], combo_type[1])
        s3_sync_str = gen_sync_str(s3_directory=None,
                                   local_directory=None,
                                   main_folder=save_directory_main,
                                   sub_folder=combo_type_list_ab_date,
                                   aws_sync_command=aws_sync_command,
                                   sync_condi=sync_condi)

        logger.critical('sync, s3_sync_estisimu:\n%s', s3_sync_str)
        call(s3_sync_str, shell=True)


def sync_s3(estisimu_save_directory_main,
            estisimu_combo_type_list_ab,
            estisimu_combo_type_list_date,
            run_size, ITG, folder_param_name,
            s3_directory_main, local_sync_directory_main,
            esti_or_simu='esti'):
    """import estimation.postprocess.p1_sync_s3 as sync_s3
    """

    '''
    Directories specific to the current estimation run. p
    '''
    estisimu_sub_direct = estisimu_save_directory_main + '/' + estisimu_combo_type_list_ab + '_' \
                          + estisimu_combo_type_list_date + run_size + ITG + folder_param_name
    s3_subdirect_estisimu = '\"' + s3_directory_main + '/' + estisimu_sub_direct + '\"'
    local_sync_subdirect_estisimu = '\"' + local_sync_directory_main + '/' + estisimu_sub_direct + '\"'

    '''
    Join Sync Commands
    '''

    def sub_process_call(sync_cur):
        estisimu_command_line_list = [aws_sync_command, s3_subdirect_estisimu, local_sync_subdirect_estisimu,
                                      sync_cur]

        s3_sync_estisimu = " ".join(estisimu_command_line_list)

        logger.critical('sync, s3_sync_estisimu:\n%s\n%s', esti_or_simu, s3_sync_estisimu)
        call(s3_sync_estisimu, shell=True)

    '''
    File Sync Type
    '''
    logger.critical('sync, s3_subdirect_estisimu:\n%s', s3_subdirect_estisimu)
    if (esti_or_simu == 'esti'):
        #         sub_process_call(sync_cur = '--exclude \"*\" --include \"*.png\"')
        sub_process_call(sync_cur='--exclude \"*\" --include \"*.csv\"')

    if (esti_or_simu == 'simu'):
        sub_process_call(sync_cur='--exclude \"*\" --include \"*.png\"')
        sub_process_call(sync_cur='--exclude \"*\" --include \"*.csv\"')

