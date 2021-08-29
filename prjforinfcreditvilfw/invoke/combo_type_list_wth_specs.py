'''
Created on Jun 9, 2018

@author: fan
'''

import parameters.loop_combo_type_list.param_combo_type_list as paramcombotypelist
import parameters.runspecs.compute_specs as computespec


def gen_combo_type_list(gn_invoke_set=1, fargate=False, paramstr_key_list=None,
                        combo_type_list_ab='a', combo_type_list_date='20180607',
                        combo_list_subset=None):
    """
        
    Parameters
    ----------
    combo_list_subset: list of int
        [0,1,2], [0], [3], [5,6] etc
        
    """

    '''cpu and memory none for fargate means use what is specified in spedificiation for each speckey'''
    vcpus = None
    cpu = None
    memory = None

    """
    invoke_set the same for farget and local.
    """
    bl_is_str = isinstance(gn_invoke_set, str)
    bl_is_int = isinstance(gn_invoke_set, int)
    if bl_is_int:
        bl_it_between = (1 <= gn_invoke_set <= 11)
    else:
        bl_it_between = False

    if bl_it_between:
        speckey = computespec.get_speckey_dict(gn_invoke_set)
    elif bl_is_str:
        speckey = gn_invoke_set
    else:
        pass

    if bl_it_between or bl_is_str:

        if (paramstr_key_list is None):
            # None means do not loop over parameter
            paramstr_key_list = ['']

            # If specify anything, loop over parameter
            paramstr_key_list = ['K_DEPRECIATION']
        #             paramstr_key_list = ['BNI_BORR_P']
        else:
            #             use list specified externally
            pass

        if (paramstr_key_list == ['']):
            '''
            grid_param.len_k_start below because in panda_param_loop, need to 
            sort by combo_type[2], there is only one row, so sorting not needed.  
            '''
            combo_type_list = [[combo_type_list_ab,
                                combo_type_list_date,
                                None,
                                None]]
        else:
            combo_type_list = paramcombotypelist.gen_combo_type_list(combo_type_list_ab,
                                                                     combo_type_list_date,
                                                                     paramstr_key_list)
    else:
        pass

    return speckey, vcpus, cpu, memory, combo_type_list
