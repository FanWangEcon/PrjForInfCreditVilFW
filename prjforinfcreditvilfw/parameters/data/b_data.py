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

    module = param_type[0]
    sub_type = str(param_type[1])

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

    if (sub_type == '20180607'):
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
