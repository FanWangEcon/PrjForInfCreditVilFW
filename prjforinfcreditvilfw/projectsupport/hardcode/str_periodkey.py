'''
Created on Sep 25, 2018

@author: fan
'''


def region_time_dict(return_periods_keys=False):
    """
    Examples
    --------
    import projectsupport.hardcode.str_periodkey as hardcode_periodkey
    periods_keys = hardcode_periodkey.region_time_dict()
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


def period_key_list():
    """
    Examples
    --------
    import projectsupport.hardcode.str_periodkey as hardcode_periodkey
    all_feasible_key_list = hardcode_periodkey.period_key_list()
    """
    all_feasible_key_list = []

    for key, val in region_time_dict().items():
        all_feasible_key_list.append(val[0])

    return all_feasible_key_list


def peristr(period=None, action='str'):
    """Combined string of the two for command line invoke

    period string control

    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')
    compute_spec_key = spec_key_dict['compute_spec_key']
    esti_spec_key = spec_key_dict['esti_spec_key']

    Examples
    --------
    import projectsupport.hardcode.str_periodkey as hardcode_periodkey
    period_str = hardcode_periodkey.peristr(period=0, action='period_name')
    periods = hardcode_periodkey.peristr(action='list')
    """

    suffix_start = '_'
    periods_keys = region_time_dict(return_periods_keys=True)
    periods = list(periods_keys.keys())

    if (action == 'list'):
        """
        This is the list of all periods available
        """
        return list(periods)
    elif (action == 'str'):
        """
        This is the string representation of period
        """
        if (period in periods):
            period_str = suffix_start + periods_keys[period]
            return period_str
        else:
            raise Exception("Period supplied not in periods list:" + str(period) + ',' + str(periods))
    elif (action == 'dictkey'):
        """
        This is the string representation of period
        """
        if (period in periods):
            period_dictkey = periods_keys[period]
            return period_dictkey
        else:
            raise Exception("Period supplied not in periods list:" + str(period) + ',' + str(periods))
    else:
        raise ('bad action:' + action)


if __name__ == '__main__':
    print(period_key_list())
