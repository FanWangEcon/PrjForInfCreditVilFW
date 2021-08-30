'''
@author: fan

Benchmark Simulation Invokations
'''

import logging
import pyfan.amto.json.json as support_json

import parameters.loop_param_combo_list.loop_values as paramspecs
import parameters.minmax.a_minmax as param_minmax_a

logger = logging.getLogger(__name__)


def get_combo_list(combo_type=['d', 'aB181021_T1_LXAX_IBXSX', None, None], compesti_specs=None):
    """
    
    Examples
    --------
    import parameters.paramset.combo_list_d_bench as combo_d_bench
    
    """
    combo_type[0]
    sub_type = combo_type[1]
    minmax_f = combo_type[1][0]
    minmax_t = combo_type[1][1:].split('_')[0]

    Ttype = combo_type[1][1:].split('_')[1]
    LX = combo_type[1][1:].split('_')[2].split('A')[0][1:]
    AX = combo_type[1][1:].split('_')[2].split('A')[1]
    IBX = combo_type[1][1:].split('_')[3].split('S')[0][2:]
    ISX = combo_type[1][1:].split('_')[3].split('S')[1]
    list_ctr = [int(LX), int(AX), int(IBX), int(ISX)]

    param_vec_count = combo_type[3]

    list_out = get_lists(minmax_type=[minmax_f, minmax_t], param_vec_count=param_vec_count)
    support_json.jdump(list_out, 'list_out', logger=logger.warning)

    logit_sd_scale = list_out['esti_type_logit_sd_scale'][list_ctr[0]]['use']
    # data__A_params_sd = list_out['dist_type_data__A.params.sd'][list_ctr[1]]['use']
    # data__A_params_sd['data__A']['integrate']['params']['points'] = 10
    data__A_params_sd = list_out['dist_type_epsA_frac_A'][list_ctr[1]]['use']

    BNI_BORR_P = list_out['esti_type_BNI_BORR_P'][list_ctr[2]]['use']
    BNI_LEND_P = list_out['esti_type_BNI_LEND_P'][list_ctr[3]]['use']

    if ("x_" in sub_type):
        grid_type = ['a', '20181024x']
        interpolant_type = ['a', '20180607x']
    elif ("d_" in sub_type):
        grid_type = ['a', '20181024d']
        interpolant_type = ['a', '20180607d']
    else:
        grid_type = ['a', '20181024']
        interpolant_type = ['a', '20180607']

    if ("_ITG_" in sub_type):
        dist_t = '20181025'
    else:
        dist_t = 'NONE'

    esti_type_dict = {}
    if ('T1' in Ttype):
        '''aB181021_T1_LXAX_IBXSX'''
        model_t = '20181013j016'

        esti_type_dict.update(logit_sd_scale)
        esti_type_dict.update(BNI_BORR_P)
        esti_type_dict.update(BNI_LEND_P)

    if ('T2' in Ttype):
        '''aB181021_T1_LXAX_IBXSX_FBXSXRXRXCX'''

        model_t = '20180701'

        FBX = combo_type[1][1:].split('_')[4].split('S')[0][2:]
        FSX = combo_type[1][1:].split('_')[4].split('S')[1].split('R')[0]
        BRX = combo_type[1][1:].split('_')[4].split('S')[1].split('R')[1]
        SRX = combo_type[1][1:].split('_')[4].split('S')[1].split('R')[2].split('C')[0]
        CX = combo_type[1][1:].split('_')[4].split('S')[1].split('R')[2].split('C')[1]
        list_ctr = list_ctr + [int(FBX), int(FSX), int(BRX), int(SRX), int(CX)]

        BNF_BORR_P = list_out['esti_type_BNF_BORR_P'][list_ctr[4]]['use']
        BNF_SAVE_P = list_out['esti_type_BNF_SAVE_P'][list_ctr[5]]['use']
        R_FORMAL_BORR = list_out['esti_type_R_FORMAL_BORR'][list_ctr[6]]['use']
        R_FORMAL_SAVE = list_out['esti_type_R_FORMAL_SAVE'][list_ctr[7]]['use']
        kappa = list_out['esti_type_kappa'][list_ctr[8]]['use']

        esti_type_dict.update(logit_sd_scale)
        esti_type_dict.update(BNI_BORR_P)
        esti_type_dict.update(BNI_LEND_P)
        esti_type_dict.update(BNF_BORR_P)
        esti_type_dict.update(BNF_SAVE_P)
        esti_type_dict.update(kappa)
        esti_type_dict.update(R_FORMAL_BORR)
        esti_type_dict.update(R_FORMAL_SAVE)

    if ('aB181028' in sub_type):
        '''In Yanji paper, they used 0.88 for discount, also try lower discount here. 
        0.926 in Townsend Kaboski
        '''
        discount = {'beta': 0.92}
        esti_type_dict.update(discount)

    combo_list = \
        [{'param_update_dict': {'grid_type': [grid_type[0], grid_type[1]],
                                'esti_type': ['a', '20181021bench', esti_type_dict],
                                'data_type': ['a', '20181024'],
                                'model_type': ['a', model_t],
                                'interpolant_type': [interpolant_type[0], interpolant_type[1]],
                                'dist_type': ['a', dist_t, data__A_params_sd],
                                'minmax_type': [minmax_f, minmax_t]}  # B181021 already called
             , 'title': 'Benchmark' + Ttype
             , 'combo_desc': 'Benchmark' + Ttype
             , 'file_save_suffix': '_' + Ttype}]

    return combo_list


def list_of_eight():
    """"
    All nine key parameters all from esti_type
    """
    list_of_8 = ['logit_sd_scale',
                 'BNI_LEND_P', 'BNI_BORR_P',
                 'BNF_SAVE_P', 'BNF_BORR_P',
                 'kappa', 'R_FORMAL_SAVE', 'R_FORMAL_BORR']

    list_out = []
    for each in list_of_8:
        list_out.append(['esti_type', each])

    #     list_out.append(['dist_type','data__A.params.sd'])
    list_out.append(['dist_type', 'epsA_frac_A'])

    return list_out


def get_lists(minmax_type=['a', 'B181021'], param_vec_count=11):
    """
    Given current minmax, and param_vec-count, obtain list of parameters 
    for each of 9 key parameters. 
    """

    minmax_f = minmax_type[0]
    minmax_t = minmax_type[1]
    if (minmax_f == 'a'):
        minmax_param, minmax_subtitle = param_minmax_a.param(minmax_type)

    param_vec_count = 10  # 10 so that the index from 0 to 9, takes less space
    param_grid_or_rand = 'grid'

    list_out = list_of_eight()

    param_list_coll = {}
    for each in list_out:
        param_type = each[0]
        param_name = each[1]

        param_list = paramspecs.gen_param_grid(param_type=param_type,
                                               param_name=param_name,
                                               minmax_param=minmax_param,
                                               param_vec_count=param_vec_count,
                                               param_grid_or_rand=param_grid_or_rand)

        param_list_coll[param_type + "_" + param_name] = param_list

    return param_list_coll


if __name__ == '__main__':
    LX = 1
    AX = 2
    IBX = 3
    ISX = 4

    FBX = 1
    FSX = 2
    BRX = 3
    SRX = 4
    CX = 5

    combo_type = ['d', 'aB181021_T1_L0A0_IB0S0', None, None]
    combo_type = ['d', 'aB181021_T1_L10A10_IB10S10', None, None]
    combo_type = ['d', 'aB181021_T1_L9A10_IB2S10', None, None]

    combo_type = ['d', 'aB181021_T1' +
                  '_L' + str(LX) + 'A' + str(AX) +
                  '_IB' + str(IBX) + 'S' + str(ISX),
                  None, None]

    combo_type = ['d', 'aB181021_T2' +
                  '_L' + str(LX) + 'A' + str(AX) +
                  '_IB' + str(IBX) + 'S' + str(ISX) +
                  '_FB' + str(FBX) + 'S' + str(FSX)
                  + 'R' + str(BRX) + 'R' + str(SRX)
                  + 'C' + str(CX),
                  None, None]

    combo_list = get_combo_list(combo_type=combo_type, compesti_specs=None)
    support_json.jdump(combo_list, 'combo_list', logger=logger.warning)
