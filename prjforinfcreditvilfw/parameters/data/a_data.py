'''

@author: fan
'''


def param(param_type=['a', 1]):
    """   
    Parameters
    ----------
    type: list
        = ['a', 1]
        could be longer, more and more          
    """

    if (len(param_type) == 1):
        data_param, subtitle = param_old(data_type=param_type)

    else:

        module = param_type[0]
        sub_type = str(param_type[1])
        #     grid_type = grid[2]
        #     grid_type = grid[3]

        if (sub_type == '20180512'):
            """log utility + 0.96 beta"""
            '''people not saving enough, see if they save more now'''
            '''Copy as many parameters as possible from Angeletos'''
            subtitle = 'Angeletos'
            data_param = {
                'mean_A': 0,
                'std_A': 0,
                'len_A': 1,
                'A': 0,
                'Region': 0,
                'Year': 0,
            }

        if (sub_type == '20180513'):
            A = 0.25
            std = 0.75
            subtitle = 'Angeletos'
            data_param = {
                'mean_A': A - ((std ** 2) / 2),
                'std_A': 0,
                'len_A': 1,
                'A': A - ((std ** 2) / 2),
                'Region': 0,
                'Year': 0,
            }

        if (sub_type == '20181024'):
            subtitle = 'Angeletos'
            data_param = {
                'mean_A': 0,
                'std_A': 0,
                'len_A': 1,
                'A': 0,
                'Region': 0,
                'Year': 0,
            }

        main_type_str_list = ['20180607', '20201025']
        if (any([main_type_str in sub_type
                 for main_type_str in main_type_str_list])):
            A = 0.25
            std = 0.75
            subtitle = 'Angeletos'
            data_param = {
                'mean_A': A - ((std ** 2) / 2),
                'std_A': 0,
                'len_A': 1,
                'A': A - ((std ** 2) / 2),
                'Region': 0,
                'Year': 0,
            }

    return data_param, subtitle


def param_A_dist():
    """   
    Parameters
    ----------
    type: list
        = ['a', 1]
        could be longer, more and more        
    """

    mean_A = 0.75
    std_A = 0
    len_A = 1

    return mean_A, std_A, len_A


def param_old(data_type=['a', {'A': 1, 'Region': 0, 'Year': 0}]):
    """   
    Parameters
    ----------
    type: list
        = ['a', 1]
        could be longer, more and more        
    """

    data_type_len = len(data_type)

    module = data_type[0]
    mean_A, std_A, len_A = param_A_dist()

    if (data_type_len == 1):
        subtitle = 'mesnstdlen'
        esti_param = {
            'mean_A': mean_A,
            'std_A': std_A,
            'len_A': len_A,
            'A': mean_A,
            'Region': 0,
            'Year': 0,
        }
    else:
        sub_details = data_type[1]
        subtitle = str(sub_details)
        esti_param = {
            'mean_A': mean_A,
            'std_A': std_A,
            'len_A': len_A,

            'A': sub_details['A'],
            'Region': sub_details['Region'],
            'Year': sub_details['Year'],
        }

    return esti_param, subtitle
