'''
Created on Sep 20, 2018

@author: fan

Model simulated and initially matched up withs ome parameters. 
Here change which parametesr are matched, and perhaps weights on moments
'''

import logging
import pyfan.amto.json.json as support_json

import estimation.moments.momcomp as momcomp
import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.hardcode.str_estimation as hardcode_estimation
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def moments_regen(moments_type=None, momsets_type=None, df_use=None,
                  save_directory='',
                  save_main_name=''):
    """
    Examples
    --------
    import estimation.postprocess.jsoncsv.gen_update_objectiv as esti_update_obj
    moments_type=None
    momsets_type=None
    df_use=None
    df_use = esti_update_obj.moments_regen(moments_type=moments_type, momsets_type=momsets_type, df_use=df_use)
    """

    region_time_suffix = hardstring.region_time_suffix()

    if (moments_type is None):
        moments_type = ''
        moments_type = ['a', '20180816a' + region_time_suffix['_ce1a2'][0]]

    if (momsets_type is None):
        momsets_type = ''
        momsets_type = ['a', '20180901a']
        momsets_type = ['a', '20180923a']

    '''
    A. Get Moments and Moment-Sets
    '''
    moments_data, momsets, momsets_graphing = momcomp.get_moments_momsets(moments_type, momsets_type)

    support_json.jdump(moments_data, 'moments_data', logger=logger.warning)
    support_json.jdump(momsets, 'momsets', logger=logger.warning)
    support_json.jdump(momsets_graphing, 'momsets_graphing', logger=logger.warning)

    '''
    B. Get Data
        csv for which we want to update moment.
    '''
    if (df_use is None):
        folder = 'C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation EC2/thaijmp201809j8vara/esti/c_20180918_ITG_list_tall_mlt_ce1a2/'
        file_base = 'c_20180918_ITG_list_tall_mlt_ce1a2_top_datamodel'
        file = file_base + '.csv'

        file_path = folder + file
        df_use = proj_sys_sup.read_csv(csv_file_folder=file_path)
        df_use_columns = df_use.columns.tolist()
        support_json.jdump((df_use.columns).tolist(), 'df_use.columns', logger=logger.warning)

    '''
    C. Update Moment objectives for each time period
    '''
    moments_type_eleone = moments_type[1]
    multi_periods, period_keys_esti_set = hardstring.momentstype_suffix_regiontype(moments_type_eleone)
    for period in period_keys_esti_set:

        dictkey = paramloopstr.peristr(period=period, action='dictkey')
        moments_data_cur_period = moments_data[dictkey]

        support_json.jdump(moments_data_cur_period, 'moments_data_cur_period', logger=logger.warning)

        period_dictkey = hardstring.moment_csv_strs()['period_dictkey'][1]
        df_use_cur_period = df_use[df_use[period_dictkey] == dictkey]

        moments_pdseries_dict = momcomp.compare_moments_direct(model_moments=df_use_cur_period,
                                                               moments_data=moments_data_cur_period,
                                                               momsets=momsets,
                                                               momsets_graphing=momsets_graphing)

        '''
        Update File
        '''
        for key, val_series in moments_pdseries_dict.items():
            df_use.loc[(df_use[period_dictkey] == dictkey), key] = val_series

    '''
    E. Update overall objective
    '''
    group_by_column = hardcode_estimation.string_estimation()['param_combo_list_ctr_str']['str_full']
    to_sum_column = hardcode_estimation.string_estimation()['main_obj']['str_full']
    summed_column = hardcode_estimation.string_estimation()['main_allperiods_obj']['str_full']
    df_use[summed_column] = df_use[to_sum_column].groupby(df_use[group_by_column]).transform('sum')

    '''
    F. Save New Results
    '''
    save_here = False
    if (save_here):
        save_file_name_remoment = save_main_name
        if (save_file_name_remoment.endswith('.csv')):
            file_name = save_file_name_remoment
        else:
            file_name = save_file_name_remoment + '.csv'

        df_use.to_csv(save_directory + file_name, header=True, index=False)

    return df_use
