'''
Created on Sep 22, 2018

@author: fan
'''


def estisimu_draw_counter_str(param_combo_ctr, gen_ctr_str=True, gen_ctr_from_str=False):
    """
    Examples
    --------
    import projectsupport.hardcode.str_estimation as hardcode_estimation    
    ctr_ctr = hardcode_estimation.estisimu_draw_counter_str(param_combo_ctr)
    """

    if (gen_ctr_str):
        str_out = '_c' + str(param_combo_ctr)
    elif (gen_ctr_from_str):
        pass
    else:
        pass

    return str_out


def string_estimation():
    """    
    Examples
    --------
    import projectsupport.hardcode.str_estimation as hardcode_estimation    
    hardcode_estimation.string_estimation()
    """

    string_dict = {'esti_obj': {'str': 'esti_obj',
                                'desc': 'prefix, top nested key'},
                   'main_obj': {'str': 'main_obj',
                                'str_full': 'esti_obj.main_obj',
                                'desc': 'each time period overall match objective'},
                   'main_allperiods_obj': {'str': 'main_allperiods_obj',
                                           'str_full': 'esti_obj.main_allperiods_obj',
                                           'desc': 'each time period overall match objective'},
                   'subsets_main': {'str': 'subsets_main',
                                    'desc': 'main estimation sub-moments'},
                   'subsets_other': {'str': 'subsets_other',
                                     'desc': 'other estimation moments to keep'},
                   'param_combo_list_ctr_str': {'str': 'param_combo_list_ctr_str',
                                                'str_full': 'support_arg.param_combo_list_ctr_str',
                                                'desc': '_c2362 which random draw'},
                   'moments_type': {'str': 'moments_type',
                                    'str_full': 'support_arg.moments_type',
                                    'desc': 'asdfasdf asdflkj sdflkj dsf'},
                   'momsets_type': {'str': 'moments_type',
                                    'str_full': 'support_arg.moments_type',
                                    'desc': 'asdfasdf asdflkj sdflkj dsf'},
                   'moments_type_regen': {'str': 'moments_type_regen',
                                          'str_full': 'support_arg.moments_type_regen',
                                          'desc': 'asdfasdf asdflkj sdflkj dsf'},
                   'momsets_type_regen': {'str': 'moments_type_regen',
                                          'str_full': 'support_arg.moments_type_regen',
                                          'desc': 'asdfasdf asdflkj sdflkj dsf'}}

    return string_dict


def connct_nested_dict_dot(momsetkey=None, momsetgroupkey='subset_main'):
    """
    
    Examples
    --------
    import projectsupport.hardcode.str_estimation as hardcode_estimation    
    hardcode_estimation.connct_nested_dict_dot(momsetkey, momsetgroupkey='subset_main')
    """

    if (momsetkey is None):
        full_key = string_estimation()['esti_obj']['str'] + \
                   '.' + \
                   string_estimation()[momsetgroupkey]['str']
    else:
        full_key = string_estimation()['esti_obj']['str'] + \
                   '.' + \
                   string_estimation()[momsetgroupkey]['str'] + \
                   '.' + \
                   momsetkey

    return full_key


def esti_predict_moment_csv():
    """
    For csv with: 
        multivariate polynomial moment regresses on simulated random parameter sets

    Examples
    --------
    import projectsupport.hardcode.str_estimation as hardcode_estimation    
    string_dict = hardcode_estimation.esti_predict_moment_csv()                
    """

    string_dict = {'moment_lhs': {'str': 'moment_lhs',
                                  'desc': 'current objective that the multivariate polynomial is predicting'},
                   'period_dictkey': {'str': 'period_dictkey',
                                      'desc': 'categories for region and time'}
                   }

    return string_dict
