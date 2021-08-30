'''
@author: fan
'''

import logging
import pyfan.amto.json.json as support_json

import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.loop_combo_type_list.param_str_esti as paramstresti
import parameters.loop_combo_type_list.param_str_simu as paramstrsimu

logger = logging.getLogger(__name__)


def gen_combo_type_list(file='a',
                        date='20180607',
                        paramstr_key_list_str=['list_all']):
    """
    overloads param2str_groups_simu
    """
    support_json.jdump(locals(), 'default', logger=logger.info)

    if (isinstance(paramstr_key_list_str, str)):
        return gen_combo_type_list_liststr(file=file, date=date,
                                           paramstr_key_list=None,
                                           paramstr_key_str=paramstr_key_list_str)
    elif (isinstance(paramstr_key_list_str, (list))):
        return gen_combo_type_list_liststr(file=file, date=date,
                                           paramstr_key_list=paramstr_key_list_str,
                                           paramstr_key_str=None)


def gen_combo_type_list_liststr(file='a',
                                date='20180607',
                                paramstr_key_list=None,
                                paramstr_key_str='list_reg_memory'):
    """
    
    Parameters
    ----------
    paramstr_key_list: list 
        if paramstr_key_list is None, use paramstr_key_str
    paramstr_key_str: string
        
    
    Returns
    -------
    combo_type_list: list
        That looks like this: 
        > combo_type_list = \
        > [
        >     ['a', '20180607_alpk', ['esti_param.alpha_k',
                                    'data_param.A']]
        >     ['a', '20180517_A', ['data_param.A']]
        >     ['a', '20180403a', None]
        > ]
        
    Examples
    --------
    import parameters.loop_combo_type_list.param_combo_type_list as paramloopstr
    list_all = paramstrnames.param2str_groups_simu()
    """

    '''
    1. Get simu and esti dicts
    '''
    paramstr_dict = paramloopstr.param2str()
    param_list_simu_dict = paramstrsimu.param2str_groups_simu()
    param_list_esti_dict = paramstresti.param2str_groups_esti()

    '''
    2. Combine dicts
    '''
    param_list_dict = {}
    for dictcur in [param_list_simu_dict, param_list_esti_dict]:
        for key, val in dictcur.items():
            param_list_dict[key] = val

    '''
    3. Generate combo_type_list
    '''
    combo_type_list = []
    if (paramstr_key_str is not None):
        '''
        3a, a string was specified, want to generate this:
        this means within each combo_type, we are looping over only one parameter
        combo_type_list = \
        [
            ['a', '20180607_d[0]', [dict[paramstr_key_str][0]]]
            ['a', '20180517_d[1]', [dict[paramstr_key_str][1]]]
            ['a', '20180517_d[2]', [dict[paramstr_key_str][2]]]
        ]          
        '''
        param_list_use = param_list_dict[paramstr_key_str]

        for param_key in param_list_use:
            paramstr_val = paramstr_dict[param_key]
            combo_type = gen_combo_type(file_name=file,
                                        file_sub_type=date + paramstr_val[0],
                                        param_group_key_list=[paramstr_val[1]])
            combo_type_list.append(combo_type)

    elif (paramstr_key_list is not None):
        '''
        3b, a list of strings was specified, each for a different param_group_key or a paramstr_key_str
        this means within each combo_type, we are looping over only one or multiple parameters
        combo_type_list = \
        [
            ['a', '20180607_paramstr_key_str', [dict[paramstr_key_str][0],
                                    dict[paramstr_key_str][1],
                                    dict[paramstr_key_str][2]]]
            ['a', '20180517_paramkey', [paramkey]]
        ]    
        '''

        for param_key_or_list in paramstr_key_list:

            '''
            3c. combo_type if key or list
            '''
            if (isinstance(param_key_or_list, list)):
                # if ['K_DEPRECIATION', 'list_policy_Fxc', 'A', ['std_eps', 'A']], dealing with 4th element here                
                param_group_key_list = []
                file_sub_type = date
                for param_key in param_key_or_list:
                    paramstr_val = paramstr_dict[param_key]
                    file_sub_type += paramstr_val[0]
                    param_group_key_list.append(paramstr_val[1])

            elif (param_key_or_list in paramstr_dict.keys()):
                # if ['K_DEPRECIATION', 'list_policy_Fxc', 'A', ['std_eps', 'A']], dealing with 1st and 3rd element here                
                paramstr_val = paramstr_dict[param_key_or_list]
                file_sub_type = date + paramstr_val[0]
                param_group_key_list = [paramstr_val[1]]

            elif (param_key_or_list in param_list_dict.keys()):
                # if ['K_DEPRECIATION', 'list_policy_Fxc', 'A', ['std_eps', 'A']], dealing with 2nd element here
                param_list = param_list_dict[param_key_or_list]
                file_sub_type = date + '_' + param_key_or_list
                param_group_key_list = []
                for param_key in param_list:
                    paramstr_val = paramstr_dict[param_key]
                    param_group_key_list.append(paramstr_val[1])

            else:
                raise ('Not possible')

            '''
            3c. generate combo_type
            '''
            combo_type = gen_combo_type(file_name=file,
                                        file_sub_type=file_sub_type,
                                        param_group_key_list=param_group_key_list)
            combo_type_list.append(combo_type)

    else:
        raise ('something wrong, this is not possible')

    support_json.jdump(combo_type_list, 'default', logger=logger.info)

    return combo_type_list


def gen_combo_type(file_name, file_sub_type, param_group_key_list, combo_list_select_ctr=None):
    """
    Parameters
    ----------
    file_name: string
        like a, b or c, corresponding to: 
        a = combo_list_a.py
        b = combo_list_b_FC.py
        c = combo_list_c_esti.py
    file_sub_type: string
        sub_type conditioning in each of the a,b,c files
        20180512, 20180717debug_beta, 20180702x, 20180702d, 20180702, etc
    param_group_key_list: list
        paramgroup.paramname:
            [esti_param.alpha_k]
            [grid_param.BNI_BORR_P_startVal]
            etc...
            or multiple keys in one list
            [esti_param.alpha_k, grid_param.BNI_BORR_P_startVal]            
    """
    return [file_name, file_sub_type, param_group_key_list, combo_list_select_ctr]


def test_cases():
    results = gen_combo_type_list_liststr()
    support_json.jdump(results, 'default', logger=logger.warning)

    results = gen_combo_type_list_liststr(paramstr_key_list=None, paramstr_key_str='list_policy_Fxc')
    support_json.jdump(results, 'T1', logger=logger.warning)

    results = gen_combo_type_list(paramstr_key_list_str=['list_policy_Fxc'])
    support_json.jdump(results, 'T2', logger=logger.warning)

    results = gen_combo_type_list(paramstr_key_list_str=['K_DEPRECIATION', 'std_eps', 'A', 'list_policy_Fxc'])
    support_json.jdump(results, 'T3', logger=logger.warning)

    results = gen_combo_type_list(paramstr_key_list_str=[['std_eps', 'A']])
    support_json.jdump(results, 'T4', logger=logger.warning)

    results = gen_combo_type_list(paramstr_key_list_str=['K_DEPRECIATION', 'std_eps', 'A', ['std_eps', 'A']])
    support_json.jdump(results, 'T5', logger=logger.warning)
    print(results[3][2])
    print(" ".join(results[3][2]))

    results = gen_combo_type_list(paramstr_key_list_str='list_all_params_1and2')
    support_json.jdump(results, 'T6', logger=logger.warning)

    results = gen_combo_type_list(paramstr_key_list_str=['list_all_params_1and2'])
    support_json.jdump(results, 'T7', logger=logger.warning)


if __name__ == "__main__":
    test_cases()
