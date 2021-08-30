'''

@author: fan

'''


def choice_index_names():
    """    
    Sample
    ------
        import parameters.model.a_model as param_model_a
        choice_names = param_model_a.choice_index_names()['choice_names']        
    """

    '''For steady state, names for storing results, append choice_names to each'''
    choice_names = {0: 'ib', 1: 'is',
                    2: 'fb', 102: 'fb2',
                    3: 'fs',
                    4: 'ibfb', 104: 'ibfb2',
                    5: 'fbis', 105: 'fbis2',
                    6: 'none',
                    7: 'ibfb_f_imin', 8: 'fbis_f_imin'}

    choice_names_full = {0: 'Informal Borrow', 1: 'Informal Lend',
                         2: 'Formal Borrow', 102: 'Formal Borrow 2',
                         3: 'Formal Save',
                         4: 'Informal and Formal Borrow', 104: 'Informal and Formal Borrow 2',
                         5: 'Formal Borrow Informal Lend', 105: 'Formal Borrow Informal Lend 2',
                         6: 'Risky Asset Only',
                         7: 'IBFB f min', 8: 'FBIS f min'}

    choice_names_borrow = {0: 'Informal Borrow',
                           2: 'Formal Borrow', 102: 'Formal Borrow 2',
                           4: 'Informal and Formal Borrow', 104: 'Informal and Formal Borrow 2',
                           5: 'Formal Borrow Informal Lend', 105: 'Formal Borrow Informal Lend 2'}

    choice_names_graph_labels = {0: 'Informal Borrow', 1: 'Informal Lend',
                                 2: 'Formal Borrow', 102: 'Formal Borrow',
                                 3: 'Formal Save',
                                 4: 'Informal and Formal Borrow', 104: 'For+Inf Borr 2',
                                 5: 'Formal Borrow Informal Lend', 105: 'FB+IL 2',
                                 6: 'Risky Asset Only',
                                 7: 'IBFB f min', 8: 'FBIS f min',
                                 '04': 'All Informal Borrow',
                                 '15': 'All Informal Lend',
                                 '245': 'All Formal Borrow',
                                 '3': 'All Formal Save',
                                 '0245': 'All Borrow',
                                 '135': 'All Save/Lend'}

    bktp_geom_dict = {0: None,
                      1: None,
                      2: None,
                      102: None,
                      3: None,
                      4: None,
                      104: None,
                      5: None,
                      105: None,
                      6: None,
                      7: None,
                      8: None,
                      9: None}

    translate1t9 = {0: 0,
                    1: 1,
                    2: 2, 102: 2,
                    3: 3,
                    4: 4, 104: 4,
                    5: 5, 105: 5,
                    6: 6,
                    7: 7,
                    8: 8,
                    9: 9}

    '''
    For latex table output:
        this is stored in csv: model_option.choice_set_list: [0, 1, 102, 3, 104, 105, 6]
        translate to jinja var key components:['FB', 'FS', 'IB', 'IS', 'FBIB', 'FBIS', 'NONE']
    '''
    translate_jinja_name = {0: 'IB',
                            1: 'IS',
                            2: 'FB', 102: 'FB',
                            3: 'FS',
                            4: 'FBIB', 104: 'FBIB',
                            5: 'FBIS', 105: 'FBIS',
                            6: 'NONE'}

    jinja_key_list_credit = ['FB', 'FS', 'IB', 'IS', 'FBIB', 'FBIS', 'NONE']

    choices_index_names = {'choice_names': choice_names,
                           'choice_names_full': choice_names_full,
                           'choice_names_graph_labels': choice_names_graph_labels,
                           'bktp_geom_dict': bktp_geom_dict,
                           'translate1t9': translate1t9,
                           'translate_jinja_name': translate_jinja_name,
                           'choice_names_borrow': choice_names_borrow}

    return choices_index_names


def param(param_type=['a', 1]):
    """
    Examples
    --------
    import parameters.model.a_model as param_model_a
    param_type = ['20180701',1]
    model_option, subtitle = param_model_a.param(param_type)
    model_option['choice_set_list']
    """

    module = param_type[0]
    sub_type = str(param_type[1])

    if (sub_type == '1'):
        subtitle = '01'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1],
            'simu_iter_periods': 20,
            'simu_indi_count': 100,
        }
    if (sub_type == '2'):
        subtitle = '0123'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1, 2, 3],
            'simu_iter_periods': 20,
            'simu_indi_count': 100,
        }

    if (sub_type == '20180513'):
        subtitle = '013'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1, 3],
            'simu_iter_periods': 20,
            'simu_indi_count': 100,
        }

    if (sub_type == '20180607'):
        subtitle = '01'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1],
            'simu_iter_periods': 20,
            'simu_indi_count': 100,
        }

    if (sub_type == '20180613'):
        subtitle = '0,1,102,3,6'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1, 102, 3, 6],
        }

    if (sub_type == '20181011'):
        subtitle = '6'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [6],
        }

    if (sub_type == '20181013j16'):
        '''
        6 + save (give save high fixed cost or 0 interest rate so never chosen
        want to see no credit market internal save only choice. 
        '''
        subtitle = '6'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [1, 6],
        }

    if (sub_type == '20181013j016'):
        '''
        Informal market still as before, but now add additional cheap external borrowing option.  
        '''
        subtitle = '0,1,6'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1, 6],
        }

    main_type_str_list = ['20180701', '20201025']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):
        subtitle = '0,1,102,3,104,105,6'
        model_option = {
            'VFI_type': 'infinite',
            'choice_set_list': [0, 1, 102, 3, 104, 105, 6],
        }

    choice_names = choice_index_names()['choice_names']
    choice_names_full = choice_index_names()['choice_names_full']

    choice_names_use = []
    choice_names_full_use = []
    for ctr, choice_idx in enumerate(model_option['choice_set_list']):
        choice_names_use.append(choice_names[choice_idx])
        choice_names_full_use.append(choice_names_full[choice_idx])

    model_option['choice_names_use'] = choice_names_use
    model_option['choice_names_full_use'] = choice_names_full_use

    return model_option, subtitle


if __name__ == "__main__":
    print(get_steady_var_suffixes())
    print(get_steady_var_suffixes(prob_column_only=True))
