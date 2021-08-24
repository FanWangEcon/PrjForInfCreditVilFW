'''
Created on Aug 1, 2016

@author: fan

import projectsupport.systemsupport as proj_sys_sup

'''

import boto3
import platform as platform
import pyfan.util.inout.iosupport as IOSup
import datetime as datetime

import logging

import pyfan.util.inout.exportpanda as exportpanda

import pyfan.amto.json.json as support_json
import pandas as pd
import json as json
import numpy as np
import time
import os as os

import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

if 'amzn' in platform.release():
    s3_status = True
else:
    s3_status = False


def log_start_name(logfile_directory='', logfile_name='',
                   logging_level=logging.WARNING, log_file=True,
                   module_name=__name__):
    fileHandler, __ = log_start(logfile_directory_name=logfile_directory + logfile_name,
                                logging_level=logging_level,
                                log_file=log_file,
                                module_name=module_name)
    return fileHandler


def log_stop(fileHandler, log_file_name, logger=logging.getLogger(''), s3=s3_status):
    logger.removeHandler(fileHandler)
    if (s3):
        s3_upload(log_file_name)


def log_start(logfile_directory_name='',
              logging_level=logging.WARNING,
              log_file=True, module_name=''):
    """
    Parameters
    ----------
    module_name: module name
        actually '' is base logger root logger
        Default module name __name__ is the module name of systemsupport module.
        if different calls use the same module_name, only one log file created.
        If I want multiple log files, need to use the module name from
        each module that is generating the logs.
    """

    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    # np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=np.nan)
    np.set_printoptions(precision=4, linewidth=100, suppress=True, threshold=1000)
    cur_logger = logging.getLogger(module_name)

    if (log_file):
        fileHandler = logging.FileHandler(logfile_directory_name, mode='w')
        formatter = logging.Formatter(FORMAT)
        fileHandler.setFormatter(formatter)
        cur_logger.addHandler(fileHandler)
        cur_logger.setLevel(logging_level)


    #         logging.basicConfig(filename= logfile_directory_name,
    #                             filemode='w',
    #                             level=logging_level, format=FORMAT)
    else:
        logging.basicConfig(level=logging_level, format=FORMAT)
        fileHandler = None
        cur_logger = None

    return fileHandler, cur_logger


def debug_panda(varnames, varmat, folder='', subfolder='', save_directory=False,
                filename='', time_suffix=False, export_panda=False, log=True, s3=s3_status):
    '''Several Possibilities

    Parameters
    ----------
    varmat: 2d array
        array of data, each column a different variable
    varnames: string
        comma separated string names for each column of varmat
    export_panda: Boolean
        if export to csv file
    log: Boolean
        if store results in log

    Returns
    -------
    panda dataframe:
        varnames + varmat combined together as Panda

    '''

    store_map = {}
    for col_ctr, curname in enumerate([x.strip() for x in varnames.split(',')]):
        store_map[curname] = col_ctr

    if (save_directory):
        pass
    else:
        if (folder == ""):
            folder = 'model_test'
        if (subfolder == ""):
            subfolder = 'other'
        save_directory = get_paths(folder, sub_folder_name=subfolder)

    if (filename == ''):
        time_suffix = True
    else:
        save_suffix_name = filename

    if (time_suffix):
        timesufx = save_suffix_time()
        save_suffix_name = filename + timesufx

    panda_df = exportpanda.export_history_csv(varmat, store_map,
                                              save_directory, save_suffix_name,
                                              export_panda)

    if log:
        logger.debug(folder + ',' + subfolder + ',' + filename + ':\n' + varnames + ':\n%s', varmat)

    if s3 and export_panda:
        saveFileDirectory = os.path.join(save_directory, save_suffix_name + '.csv').replace(os.sep, '/')
        s3_upload(saveFileDirectory)

    return panda_df


def save_panda(saveFileDirectory, dataToSave, header='', rowindex=False, is_panda=True, s3=s3_status):
    """
    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_solu/'
    param_combo = '20180701_basicJ7_basic'
    file_name = 'solu_'+param_combo+'_morestats.csv'
    saveFileDirectory = directory + '/' + file_name
    proj_sys_sup.save_panda(saveFileDirectory, solu_opti_pd_morestats,
                            is_panda=True, s3=False)
    """
    panda_df = exportpanda.saveCSV(saveFileDirectory, dataToSave, header,
                                   rowindex, is_panda, replace=True, export=True)
    if (s3):
        s3_upload(saveFileDirectory)

    return panda_df


def save_json(saveFileDirectory, dataToSave, replace=True, s3=s3_status, add_time=True):
    if (('support_arg' in dataToSave) and add_time):
        dataToSave['support_arg']['time_end'] = save_suffix_time(3)
        dataToSave['support_arg']['time_run'] = save_suffix_time(3) - dataToSave['support_arg']['time_start']
        dataToSave['support_arg']['time_end_date'] = save_suffix_time(0)

    json_out = exportpanda.saveJSON(saveFileDirectory, dataToSave, replace)

    if (s3):
        s3_upload(saveFileDirectory)

    return json_out


def load_json(file_name_and_directory, keep_int=False):
    with open(file_name_and_directory) as f:
        json_data = json.load(f)

    if (keep_int):
        for key, val in json_data.items():
            try:
                if (val == int(val)):
                    json_data[key] = int(val)
            except:
                pass

    return json_data


def save_img(plt, cur_img_directory_name, dpi=300, papertype='a4',
             orientation='horizontal', s3=s3_status):
    cur_img_directory_name = cur_img_directory_name + '.png'
    plt.savefig(cur_img_directory_name,
                dpi=dpi, papertype=papertype,
                orientation=orientation)
    if (s3):
        s3_upload(cur_img_directory_name)


def s3_download(local_download_to_directory_file):
    '''
    current s3 bucket
    '''
    s3 = boto3.client('s3')

    '''
    local root a part of: local_download_to_directory_file
    '''
    local_root = main_directory()
    s3_source_directory_file = local_download_to_directory_file[len(local_root):]

    s3.download_file(s3_bucket_name(), s3_source_directory_file, local_download_to_directory_file)


def s3_download_to_docker_mpoly(spn_docker_path_mpoly_reg_coef):
    """Download file from s3 to docker for mpoly_reg_coef csv files
    While docker container executes estimation and simulation tasks, files
    auto uploaded to S3. Need to download the mpoly_reg_coef file from S3 for ESR3
    MPOLY estimation.

    1. constructure correctly the path to the mpoly file on s3
    2. assume that the path is identical for docker container, except append to /data/ folder

    The file not only applies to MPOLY but also other files that are stored in the same hierachy structure,
    including json top.

    Parameters
    ----------
    spn_s3_path_file_name : str
        i.e., esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv

    """
    s3 = boto3.client('s3')

    # esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv
    # spn_s3_path_file_name = "_data/iris_s3.dta"

    # /data/esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv
    spn_s3_path_mpoly_reg_coef = spn_docker_path_mpoly_reg_coef[len(main_directory()):]

    # download command
    s3.download_file(s3_bucket_name(), spn_s3_path_mpoly_reg_coef, spn_docker_path_mpoly_reg_coef)

    return spn_s3_path_mpoly_reg_coef


def s3_upload(cur_file_directory_name):
    """
    Upload to AWS for tasks done on AWS, not for local tasks
    """
    if ('amzn' in platform.release()):
        s3 = boto3.client('s3')
        str_root = main_directory()
        str_full = cur_file_directory_name

        root_len = len(str_root)
        #         folder_wth_file_name = 'D' + save_suffix_time(format=1) + '/' + str_full[root_len:]
        folder_wth_file_name = str_full[root_len:]

        #     file_name = str_full[ (str_full.rfind('/')+1) :]
        #     folder_name = str_full[root_len:(str_full.rfind('/') +1)]

        s3.upload_file(str_full, s3_bucket_name(), folder_wth_file_name)

    else:

        # This means working locally, while working locally, upload just the *mpoly_reg_coef* file to s3
        # after esr1, this file is needed for esr3.
        # Do this only if working inside the local mirro of s3_bucket.
        # Do not if working purely locally.
        # Check if bucket name is in local directory + if file is mpoly_reg_coef
        # upload also top estimation results from ESR1 and ESR2 to S3

        if (s3_bucket_name() in cur_file_directory_name) \
                and (('_mpoly_reg_coef' in cur_file_directory_name) or
                     ('_top_json' in cur_file_directory_name)):
            local_s3_directory = s3_local_sync_folder() + s3_bucket_name()
            root_len = len(local_s3_directory)
            str_full = cur_file_directory_name
            folder_wth_file_name = str_full[(root_len + 1):]

            s3 = boto3.client('s3')

            # 'thaijmp201809j8vara/esti/c_20180925_ITG_list_Afx3_mlt_ce1a2/c_20180925_ITG_list_Afx3_mlt_ce1a2_mpoly_reg_coef.csv'
            # Note the SLASH conversion below:
            # SLASH conversion needed otherwise windows has \\, which becomes \ on S3.
            s3.upload_file(str_full, s3_bucket_name(), folder_wth_file_name.replace(os.sep, '/'))

        pass


def s3_bucket_name():
    """
    thaijmp201808j7itgesti: 2018-08-13 13:57
        with estimation using "real" data
    thaijmp201808j8var: 2018-08-22 23:16
        estimation where moments now include conditional probability P(j'|j) and variances
    thaijmp201809j8vara: 2018-09-18 06:10
        after several debugging and adjustment
        crucially, A type mean and sd fully work with simulation now.
    fin201810: 2018-12-11 16:06
        stores Benchmark Table 1 and 2 Results
    thaijmp202010: 2020-10-19 18:09

    """
    bucket_name = 'thaijmp202010'
    return bucket_name


def s3_local_sync_folder():
    """local_sync_folder
    """
    local_sync_folder = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation EC2/'
    local_sync_folder = 'G:/S3/'
    return local_sync_folder


def local_stata_exe_directory():
    local_sync_folder = 'C:/Program Files (x86)/Stata14/StataMP-64bit.exe'
    return local_sync_folder


def directory_local_gitrepo(subfolder='invoke'):
    """
    Currently locally synced git repo
    """

    if os.path.exists('G:/repos'):
        # Precision
        # spn_dropbox = 'G:/Dropbox (UH-ECON)'
        # D:/repos/ThaiJMP on precision, local D drive folder, not synced
        spt_return_directory = 'G:/repos/ThaiJMP'
    else:
        spt_return_directory = 'C:/users/fan/repos/ThaiJMP'

    if subfolder == 'invoke':
        spt_return_directory = os.path.join(spt_return_directory, 'invoke')

    spt_return_directory = spt_return_directory.replace(os.sep, '/')

    return spt_return_directory


def main_directory_gitrepo():
    if ('amzn' in platform.release()):
        gitrepo_directory = '/ThaiJMP/'
    else:

        gitrepo_directory = main_directory()

        # if os.path.exists('G:/Dropbox (UH-ECON)/repos/ThaiJMP'):
        #     spn_project_src = 'G:/Dropbox (UH-ECON)/repos/'
        # elif os.path.exists('C:/Users/fan/Documents/Dropbox (UH-ECON)/repos/ThaiJMP'):
        #     spn_project_src = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/repos/'
        # elif os.path.exists('C:/Users/fan/ThaiJMP/'):
        #     spn_project_src = 'c:/Users/fan/'
        #
        # gitrepo_directory = os.path.join(spn_project_src, 'ThaiJMP')

    return gitrepo_directory


def check_is_on_aws_docker():
    bl_in_aws_docker = False
    if 'amzn' in platform.release():
        bl_in_aws_docker = True

    return bl_in_aws_docker


def main_directory(bl_awslocal=False):
    """Determines where simulation, estimation results are stored locally.

    Note that this does not determine code location. All code is packaged up with package
    reference.

    """
    if 'amzn' in platform.release():
        #         master_directory = '/home/ubuntu/Documents/ThaiJMP/'
        # this is inside docker container.
        master_directory = '/data/'
    else:

        if bl_awslocal:
            # Get results from AWS local directories
            # Post estimation and local sync, locally synced folder to s3
            master_directory = os.path.join(s3_local_sync_folder(), s3_bucket_name())

        else:
            if os.path.exists('D:/Dropbox (UH-ECON)'):
                # Precision
                # spn_dropbox = 'G:/Dropbox (UH-ECON)'
                # D:/repos/ThaiJMP on precision, local D drive folder, not synced
                master_directory = 'D:/repos/ThaiJMP'
            else:
                # XPS
                # os.path.exists('C:/Users/fan/Documents/Dropbox (UH-ECON)'):
                spn_dropbox = 'C:/Users/fan/Documents/Dropbox (UH-ECON)'
                master_directory = os.path.join(spn_dropbox, 'Project Dissertation')

    return master_directory


def get_paths_in_git(main_folder_name):
    """get the path to another file in git repository
    """
    gitrepo_directory = main_directory_gitrepo()
    if (main_folder_name == "_paper.preamble.group_d_data"):
        folder_name_to_return = os.path.join(gitrepo_directory, '_paper', 'preamble', 'group_d_data', '')
    elif (main_folder_name == "stata.estisimu_data"):
        folder_name_to_return = os.path.join(gitrepo_directory, 'stata', 'estisimu_data', '')
    elif (main_folder_name == "stata.graph.counter_3dims.do"):
        folder_name_to_return = os.path.join(gitrepo_directory, 'stata', 'graph', 'counter_3dims.do')
    elif (main_folder_name == "stata.graph.esti_fit_prob_j.do"):
        folder_name_to_return = os.path.join(gitrepo_directory, 'stata', 'graph', 'esti_fit_prob_j.do')
    elif (main_folder_name == "_paper.tables.data"):
        folder_name_to_return = os.path.join(gitrepo_directory, '_paper', 'tables', 'data', '')
    elif (main_folder_name == "parameters.json"):
        folder_name_to_return = os.path.join(gitrepo_directory, 'parameters', 'json', '')
    else:
        folder_name_to_return = gitrepo_directory

    return folder_name_to_return


def gen_path(combo_type, st_type='simuesti_subfolder'):
    """Name of simulation folders
    generate folder names like: e_20201025_esr_list_tKap

    Parameters
    ----------
    combo_type : list
        i.e. ['e', '20201025_esr_list_tKap']
    """

    sub_folder_name = combo_type[0] + '_' + combo_type[1]
    if st_type == 'simuesti_subfolder':
        return sub_folder_name


def get_paths(main_folder_name, sub_folder_name='', subsub_folder_name=''):
    """
    Examples
    --------
    import projectsupport.systemsupport as proj_sys_sup
    main_folder_name = ''
    sub_folder_name = ''
    subsub_folder_name = ''
    proj_sys_sup.get_paths(main_folder_name, sub_folder_name = '', subsub_folder_name = '')
    """

    master_directory = main_directory()
    master_directory = master_directory.replace(os.sep, '/')
    main_folder_name = main_folder_name.replace(os.sep, '/')

    if (main_folder_name == "model_test"):
        folder_name_to_return = os.path.join(master_directory, 'model_test', '')
    elif (main_folder_name == "logvig"):
        folder_name_to_return = os.path.join(master_directory, 'logvig', '')
    elif (main_folder_name == "simu"):
        # master_directory = os.path.join('D', 'repos', 'ThaiJMP')
        folder_name_to_return = os.path.join(master_directory, 'simu', '')
    elif (main_folder_name == "esti"):
        # master_directory = os.path.join('D', 'repos', 'ThaiJMP')
        folder_name_to_return = os.path.join(master_directory, 'esti', '')
    elif (main_folder_name == "esti_tst"):
        # master_directory = os.path.join('D', 'repos', 'ThaiJMP')
        folder_name_to_return = os.path.join(master_directory, 'esti_tst', '')
    elif (main_folder_name == "s3local_esti"):
        folder_name_to_return = s3_local_sync_folder() + s3_bucket_name() + '/esti/'
    elif (main_folder_name == "s3local_simu"):
        folder_name_to_return = s3_local_sync_folder() + s3_bucket_name() + '/simu/'
    elif (main_folder_name == "paper"):
        folder_name_to_return = os.path.join(master_directory, 'paper', '')
    elif (main_folder_name == "paper.imgtab"):
        folder_name_to_return = os.path.join(master_directory, 'paper', 'imgtab', '')
    else:
        '''
        If here, that means main_folder_name is already generated by get_paths()
        once, and respects master_directory.        
        just double check to geenerate the folder in case it does not exist yet. 
        '''

        if master_directory in main_folder_name:
            # master_directory already in main
            # i.e.: main_folder_name = 'D:/repos/ThaiJMP\\parameters\\json\\'
            Path(main_folder_name).mkdir(parents=True, exist_ok=True)
            folder_name_to_return = main_folder_name
        else:
            # a new folder name: i.e. test_tst2
            folder_name_to_return = os.path.join(master_directory, main_folder_name, '')
        # raise ValueError(f'the subfolder specified, {main_folder_name=}, is not allowed')

    if (sub_folder_name != ''):
        folder_name_to_return = IOSup.csvIO().createDirectory(folder_name_to_return, sub_folder_name)

    if (subsub_folder_name != ''):
        folder_name_to_return = IOSup.csvIO().createDirectory(folder_name_to_return, subsub_folder_name)

    folder_name_to_return = folder_name_to_return.replace(os.sep, '/')

    logger.debug('folder_name_to_return:%s\n', folder_name_to_return)
    return folder_name_to_return


def read_csv(csv_file_folder):
    """
    directory = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/test_solu/'
    param_combo = '20180701_basicJ7_basic'
    file_name = 'solu_'+param_combo+'.csv'
    csv_file_folder = directory + '/' + file_name
    solu_opti_pd = proj_sys_sup.read_csv(csv_file_folder)
    """
    return pd.read_csv(csv_file_folder)


def save_suffix_time(format=0, dash=False):
    if (format == 0):
        timestr = "{:%Y%m%d-%H%M%S-%f}".format(datetime.datetime.now())
    if (format == 1):
        timestr = "{:%Y%m%d}".format(datetime.datetime.now())
    if (format == 2):
        #         timestr = "{:%Y%m%d %H:%M:%S -%f}".format(datetime.datetime.now())
        timestr = "{:%Y%m%d%H%M%S%f}".format(datetime.datetime.now())
    if (format == 3):
        timestr = time.time()

    if (dash):
        return '_' + timestr
    else:
        return timestr


def log_vig_start(main_folder_name='logvig', sub_folder_name='parameters', subsub_folder_name='combo_type',
                  file_name='fs_gen_combo_type', it_time_format=1, log_level=logging.WARNING):
    spt_log = get_paths(main_folder_name, sub_folder_name, subsub_folder_name)
    snm_log = file_name + '_' + save_suffix_time(it_time_format)
    spn_log = get_path_file(spt_log, snm_log, st_file_type='log')
    logging.basicConfig(filename=spn_log, filemode='w', level=log_level, format=log_format())


def log_format(bl_set_print_opt=True, it_print_opt=1):
    if bl_set_print_opt:
        if it_print_opt == 1:
            np.set_printoptions(precision=2, linewidth=100, suppress=True, threshold=3000)

    return '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'


def jdump(dump_data, desc, logger=logger, print_here=False):
    support_json.jdump(dump_data, desc, logger=logger, print_here=print_here)


def decimals(type):
    """Printing to tex etc, decimal rules

    Examples
    --------
    import projectsupport.systemsupport as proj_sys_sup
    decimals = proj_sys_sup.decimals(type='prob')
    """

    if (type == 'prob'):
        format_str = '{0:.3g}'
    if (type == 'params'):
        format_str = '{0:.6g}'

    return format_str


def move_rename(cur_folder_file, next_folder_file):
    """
    Examples
    --------
    import projectsupport.systemsupport as proj_sys_sup
    cur_folder_file = ''
    next_folder_file = ''
    proj_sys_sup.move_rename(cur_folder_file, next_folder_file)
    """

    #     shutil.move("path/to/current/file.foo",
    #                 "path/to/new/destination/for/file.foo")

    shutil.move(cur_folder_file,
                next_folder_file)


def copy_rename(cur_folder_file, next_folder_file):
    """
    Examples
    --------
    import projectsupport.systemsupport as proj_sys_sup
    cur_folder_file = ''
    next_folder_file = ''
    proj_sys_sup.copy_rename(cur_folder_file, next_folder_file)
    """

    #     shutil.move("path/to/current/file.foo",
    #                 "path/to/new/destination/for/file.foo")

    shutil.copyfile(cur_folder_file, next_folder_file)
