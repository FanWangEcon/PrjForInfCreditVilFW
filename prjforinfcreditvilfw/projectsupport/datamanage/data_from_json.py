'''
Created on May 18, 2018

@author: fan

Model Invokation Generates Json results single files. Gather Their results
Into panda files
'''

import glob as glob

import logging
from pandas.io.json import json_normalize

import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def get_all_files(directory='', file_str=''):
    file_list = glob.glob(directory + file_str)
    return file_list


def json_to_panda(directory='', file_str='',
                  agg_df_name_and_directory=None,
                  count_file_only=False):
    """Pretty Amazing normalize function
    
    I store key solution results as nested json dicts, one file for each model
    steady state solution invokation. 
    
    This file:
        1. pulls all json files from a directory with certain regexp search string
        2. creates a list of the json dicts
        3. uses json_normalize to convert list of nested json dicts to panda. 
        
    The nice thing here is that the nested json dicts have look like this:
      {
        "model_option": {
          "VFI_type": "infinite",
          "choice_set_list": [
            0,
            1
          ],
          "simu_iter_periods": 20,
          "simu_indi_count": 100,
          "choice_names_use": [
            "ib",
            "is"
          ],
          "choice_names_full_use": [
            "Informal Borrow",
            "Informal Lend"
          ]
        },
        "title": "A0:(INF BORR+SAVE)+(0MIN,0FC)+(LOG,Angeletos)+i3+(R=1.08)) (g:quick, e:zeroFE, e:Angeletos, e:01, i:griddata)",
        "combo_desc": "Angeletos quick",
        "file_save_suffix": "_20180517_quick_quick",
        "aggregate_borrow": -1.5647267188388065,
      }    
    Some variables in first tier, some variables nested. normalize creates panda
    where column names are combo_desc, file_save_suffix and:
        model_option.model_option
        model_option.simu_indi_count
        etc.
    
    Parameters
    ----------
    file_str: regexp
        do not include .json in string.
    count_file_only: boolean
        count file only, use if in estimation, do not generate aggregate json csv 
        file yet still want to count how many estimations have been done to stop estimation
        when it exceeds max.
        
    Examples
    --------
    import projectsupport.datamanage.data_from_json as datajson    
    """

    file_list = get_all_files(directory=directory, file_str=file_str + '.json')
    json_data_list = []
    if (count_file_only):

        return len(file_list)
    else:
        for file_path in file_list:
            json_data = proj_sys_sup.load_json(file_name_and_directory=file_path)
            json_data_list.append(json_data)

        #     proj_sys_sup.jdump(json_data_list, 'json_data_list', logger=logger.info)

        return json_to_panda_nofile(json_data_list, agg_df_name_and_directory)


def json_to_panda_nofile(json_data_list, agg_df_name_and_directory=None, s3=proj_sys_sup.s3_status):
    """
    Examples
    --------
    import projectsupport.datamanage.data_from_json as datajson
    panda_df = datajson.json_to_panda_nofile(json_data_list, agg_df_name_and_directory = None)
    """
    panda_df = json_normalize(json_data_list)
    logger.info('panda_df\n:%s', panda_df)

    if (agg_df_name_and_directory is not None):
        proj_sys_sup.save_panda(agg_df_name_and_directory, panda_df, s3=s3)

    return panda_df


if __name__ == "__main__":
    cur_directory_main = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/'
    cur_directory_subb = 'model_test/test_simuanalytical/'
    cur_directory_full = cur_directory_main + cur_directory_subb
    json_to_panda(cur_directory_full, '*')
