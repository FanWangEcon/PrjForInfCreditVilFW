'''
Created on Dec 18, 2017

@author: fan
'''

import logging
import numpy as np
import pandas as pd

import estimation.moments.moments_a as momentsa
import estimation.moments.momsets_a as momsetsa
import projectsupport.hardcode.str_estimation as hardcode_estimation


def get_moments_momsets(moments_type, momsets_type):
    """    
    Examples
    --------
    import estimation.moments.momcomp as momcomp    
    """

    if (moments_type[0] == 'a'):
        moments_data, subtitle = momentsa.moments_a(moments_type)

    if (momsets_type[0] == 'a'):
        momsets, subtitle = momsetsa.momsets_a(momsets_type)
        momsets_graphing, subtitle_graphing = momsetsa.momsets_a(momsets_type=['a', 'graphing'])

    return moments_data, momsets, momsets_graphing


def show_moments(moments_type, momsets_type, opti_esti_data_frame):
    """
    After estimation, at optimal estimates, where are the data moments, and model moments?
    out = {'data':data, 'model':model}
    data = {'mom1':1, ... , 'momN':Z}
    model = {'mom1':3, ... , 'momN':W}
    
    Need to include momsets_graphing, want to keep all data and model moments
    Perhaps moment not used for estimation, but still grab it out. 
    """
    moments_data, momsets, momsets_graphing = get_moments_momsets(moments_type, momsets_type)

    data_actual_dict = {}
    model_simu_dict = {}
    model_data_simu_dict = {}

    ctr = 0
    momsetkey_added = []
    for momsets_ctr in [1, 2]:

        if (momsets_ctr == 1):
            momsets_cur = momsets
        if (momsets_ctr == 2):
            momsets_cur = momsets_graphing

        for momsetkey, momsetwgt in momsets_cur.items():
            # This statement means only add momsets_graphing keys if hey are not already in momsets
            if (momsetkey not in momsetkey_added):
                momsetkey_added.append(momsetkey)
                moment_set = momsetwgt[0]
                for momkey in moment_set:

                    found_match = False
                    if ('+' in momkey or '-' in momkey):
                        '''
                            if have more advanced needs
                            >>> import re
                            >>> def mysplit(mystr):
                            ...     return re.split("([+-/*])", mystr.replace(" ", ""))
                            ...
                            >>> mysplit("A7*4")
                            ['A7', '*', '4']
                            >>> mysplit("Z3+8")
                            ['Z3', '+', '8']
                            >>> mysplit("B6 / 11")
                            ['B6', '/', '11']
                            >>>                        
                        '''

                        if ('+' in momkey):
                            momkey_set = momkey.split('+')
                        if ('-' in momkey):
                            momkey_set = momkey.split('-')

                        if_contains = []
                        for k in momkey_set:
                            if (k in list(opti_esti_data_frame.columns)):
                                if_contains.append(True)
                            else:
                                if_contains.append(False)

                        if ((momkey in moments_data) and all(if_contains)):
                            found_match = True
                            # Data Actual, Data Simulated
                            moments_actual = moments_data[momkey]
                            moments_simu_1 = np.array(list(opti_esti_data_frame[momkey_set[0]].to_dict().values()))
                            moments_simu_2 = np.array(list(opti_esti_data_frame[momkey_set[1]].to_dict().values()))
                            if ('+' in momkey):
                                moments_simu = moments_simu_1 + moments_simu_2
                            if ('-' in momkey):
                                moments_simu = moments_simu_1 - moments_simu_2

                            # Save to dicts
                            results = {'data': moments_actual, 'simu': moments_simu}
                            data_actual_dict[momkey] = results['data']
                            model_simu_dict[momkey] = results['simu']
                            model_data_simu_dict[momkey] = results

                    else:
                        '''
                        Regular momkey, each variable = momkey
                        '''
                        if ((momkey in moments_data) and (momkey in list(opti_esti_data_frame.columns))):
                            found_match = True
                            # Data Actual, Data Simulated
                            moments_actual = moments_data[momkey]
                            moments_simu = np.array(list(opti_esti_data_frame[momkey].to_dict().values()))

                    if (found_match):
                        # Save to dicts
                        results = {'data': moments_actual, 'simu': moments_simu}
                        data_actual_dict[momkey] = results['data']
                        model_simu_dict[momkey] = results['simu']
                        model_data_simu_dict[momkey] = results

    return data_actual_dict, model_simu_dict, model_data_simu_dict


def compare_moments(model_moments, moments_type=None, momsets_type=None,
                    logger=logging.getLogger(__name__)):
    '''
    A. Obtain Data, and Obtain Moments
    '''
    moments_data, momsets, momsets_graphing = get_moments_momsets(moments_type, momsets_type)
    return compare_moments_direct(model_moments, moments_data, momsets, momsets_graphing,
                                  logger=logger)


def compare_moments_direct(model_moments, moments_data, momsets, momsets_graphing,
                           logger=logging.getLogger(__name__)):
    json_df_name_prefix = 'main_obj'
    json_df_name_prefix = 'subsets_main'

    '''
    B. Match up momsets with moments, create dataframe
    consider only parameters that are both specified in momsets and that have
    data in moments.  
    '''
    # For collecting when doing row by row json
    moment_df = pd.DataFrame(columns=['moment', 'weight', 'data', 'model', 'gap', 'counter'])
    # collecting re generating aggregate moments
    moments_pdseries_dict = {}

    '''
    C. Loop over estimation moment set and general all info
    '''
    ctr = 0
    momsetkey_added = []
    for momsets_ctr in [1, 2]:

        if (momsets_ctr == 1):
            momsets_cur = momsets
            store_key_type = 'subsets_main'
            overall_obj = 0
        if (momsets_ctr == 2):
            momsets_cur = momsets_graphing
            store_key_type = 'subsets_other'
            overall_obj = None

        '''
        Looping over sub-groups of main
        '''
        model_moments_cur = None
        for momsetkey, momsetwgt in momsets_cur.items():

            # This statement means only add momsets_graphing keys if hey are not already in momsets
            if (momsetkey not in momsetkey_added):
                momsetkey_added.append(momsetkey)
                moment_set = momsetwgt[0]
                moment_weight = momsetwgt[1]
                moment_power = momsetwgt[2]

                subset_obj = 0
                for momkey in moment_set:

                    found_match = False
                    if ('+' in momkey or '-' in momkey):
                        if ('+' in momkey):
                            momkey_set = momkey.split('+')
                        if ('-' in momkey):
                            momkey_set = momkey.split('-')
                        if_contains = [k in model_moments for k in momkey_set]

                        if ((momkey in moments_data) and all(if_contains)):
                            found_match = True
                            # Data Actual, Data Simulated
                            moments_data_cur = moments_data[momkey]
                            moments_simu_1 = model_moments[momkey_set[0]]
                            moments_simu_2 = model_moments[momkey_set[1]]
                            if ('+' in momkey):
                                model_moments_cur = moments_simu_1 + moments_simu_2
                            if ('-' in momkey):
                                model_moments_cur = moments_simu_1 - moments_simu_2

                    elif ((momkey in moments_data) and (momkey in model_moments)):
                        found_match = True
                        moments_data_cur = moments_data[momkey]
                        model_moments_cur = model_moments[momkey]

                    else:
                        pass

                    if (found_match):
                        if (isinstance(model_moments_cur, pd.Series)):
                            '''
                            This means invoked after simulation, swicihng which moments to match up to
                            '''
                            current_obj = ((abs(
                                model_moments_cur - moments_data_cur) * moment_weight) ** moment_power)
                            #                             current_obj = moment_weight*((abs(model_moments_cur - moments_data_cur))**moment_power)
                            '''
                            subset_obj summing over individual moments belong to subset of overall
                            '''
                            subset_obj = subset_obj + current_obj
                            '''
                            summing over all moments used for matching moments
                            '''
                            if (momsets_ctr == 1):
                                overall_obj = overall_obj + current_obj
                        else:
                            '''
                            This is invoked when each simulation generates own JSON file. 
                            '''
                            ctr = ctr + 0
                            row = pd.Series({'moment': momkey,
                                             'momsetkey': momsetkey,
                                             'weight': moment_weight,
                                             'power': moment_power,
                                             'data': moments_data_cur,
                                             'model': model_moments_cur,
                                             'gap': abs(model_moments_cur - moments_data_cur),
                                             'counter': ctr,
                                             'momsets_ctr': momsets_ctr},
                                            name=ctr + 0)
                            moment_df = moment_df.append(row)

                if (isinstance(model_moments_cur, pd.Series)):
                    df_key = hardcode_estimation.connct_nested_dict_dot(momsetkey, momsetgroupkey=store_key_type)
                    moments_pdseries_dict[df_key] = subset_obj

        if (isinstance(model_moments_cur, pd.Series) and (momsets_ctr == 1)):
            df_key = hardcode_estimation.connct_nested_dict_dot(
                momsetgroupkey=hardcode_estimation.string_estimation()['main_obj']['str'])
            moments_pdseries_dict[df_key] = overall_obj

    if moment_df.empty:
        '''
        Happens in multi-period estimation intentionally.
        Data moments have added time specific suffix, simulated meoments do not, 
        can not be matched up. This is intential, matching to be done within
        estimate_objective_multiperiods.py
        '''
        moments_dict = moments_pdseries_dict
    else:
        '''
        C. Print Results to Log
        '''
        moment_gap_wp = moment_df['weight'] * ((moment_df['gap']) ** moment_df['power'])
        moment_df = moment_df.assign(moment_gap_wp=moment_gap_wp.values)
        logger.warning('moment_df:\n%s', moment_df)

        '''
        D. Conditional Sum
        '''
        estimation_main = (moment_df['momsets_ctr'] == 1)
        moment_gap = np.sum(moment_df[estimation_main]['moment_gap_wp'])

        '''
        E. Moment Dict
        '''
        moments_dict = {'main_obj': moment_gap}

        '''
        F. Overall Moment
        '''
        subsets_obj = {}
        for momsets_ctr in [1, 2]:
            if (momsets_ctr == 1):
                # estimation_main
                cur_subset = (moment_df['momsets_ctr'] == 1)
                store_key = hardcode_estimation.string_estimation()['subsets_main']['str']
            if (momsets_ctr == 2):
                # other_moment_gaps
                cur_subset = (moment_df['momsets_ctr'] == 2)
                store_key = hardcode_estimation.string_estimation()['subsets_other']['str']
            moment_gap_groups = moment_df[cur_subset].groupby(['momsetkey'])['moment_gap_wp'].sum()
            subsets_obj[store_key] = moment_gap_groups.to_dict()

        '''
        G. Combine to Dict
        '''
        moments_dict = {hardcode_estimation.string_estimation()['main_obj']['str']: moment_gap}
        moments_dict.update(subsets_obj)

    return moments_dict
