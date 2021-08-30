'''
@author: fan

grid invoke structure, copying largely from b_FC
'''

import parameters.loop_param_combo_list.loops_gen as paramloops


def get_combo_list(combo_type=['e', '20200901'], compesti_specs=None):
    """
    created 2018-10-24 16:20, copied over 2020-09-07 09:28
    """

    module = combo_type[0]
    sub_type = combo_type[1]

    main_type_str_list = ['20200901']
    if (any([main_type_str in sub_type
             for main_type_str in main_type_str_list])):

        '''
        sizing
        '''
        if (any([main_type_str + 'x' in sub_type
                 for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024x']
            interpolant_type = ['a', '20180607x']
        elif (any([main_type_str + 'd' in sub_type
                   for main_type_str in main_type_str_list])):
            grid_type = ['a', '20181024d']
            interpolant_type = ['a', '20180607']
        else:
            grid_type = ['a', '20181024']
            interpolant_type = ['a', '20180607']

        '''
        Integration: add the x, d, and regular options here too
        '''
        if ("_ITG_" in sub_type):
            dist_t = '20181025'
        else:
            dist_t = 'NONE'

        '''
        min max range adjustments
        '''
        if ('20200901' in sub_type):
            minmax_t = '20180901'
        else:
            raise ('bad')

        '''
        Which model
        '''
        if ("_1j7" in sub_type):
            model_t = '20181011'
            esti_t = '20180607'
        elif ("_1ja7" in sub_type):
            '''
            _1j7 does not work, 1ja7 approximates 1j7 by making fixed cost very high for saving option
            '''
            model_t = '20181013j16'
            esti_t = '20181013simuinfFC'
        elif ("_2j127" in sub_type):
            model_t = '20181013j016'
            esti_t = '20181021bench'
        elif ("_5j12347" in sub_type):
            model_t = '20180613'
            esti_t = '20181013simuFC5j12347'
        elif ("_7jAll" in sub_type):
            model_t = '20180701'
            esti_t = '20181013simuFC5j12347'
        else:
            raise ('bad _j12347 etc not in sub_type')

        combo_list = paramloops.combo_list_auto(
            combo_type=combo_type,
            compesti_specs=compesti_specs,
            grid_f=grid_type[0], grid_t=grid_type[1],
            esti_f='a', esti_t=esti_t,
            data_f='a', data_t='20181024',
            model_f='a', model_t=model_t,
            interpolant_f=interpolant_type[0], interpolant_t=interpolant_type[1],
            dist_f='a', dist_t=dist_t,
            minmax_f='a', minmax_t=minmax_t)

    return combo_list
