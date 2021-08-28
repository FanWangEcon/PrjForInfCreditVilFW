'''
Created on Aug 5, 2018

@author: fan
'''
import parameters.model.a_model as param_model_a
import projectsupport.hardcode.string_shared as hardstring


def momsets_all_moments():
    """
    ib_btp_fb_opti_grid_j_agg
    
    Examples
    --------
    import estimation.moments.momsets_a as momsetsa
    all_moments = momentsa.momsets_all_moments()
    """
    momsets_type = ['a', 'all_moments']
    moment_sets, subtitle = momsets_a(momsets_type)

    all_moments = []
    for key, moment_set in moment_sets.items():
        for moment in moment_set[0]:
            if (moment not in all_moments):
                all_moments.append(moment)

    more_moments = all_choice_moments()
    for moment_cur in more_moments:
        if (moment_cur not in all_moments):
            all_moments.append(moment_cur)

    return all_moments


def all_choice_moments():
    choice_names = param_model_a.choice_index_names()['choice_names']

    steady_var_suffixes_dict = hardstring.get_steady_var_suffixes()
    steady_agg_suffixes = hardstring.steady_aggregate_suffixes()

    '''
    All Choice Moments
    '''
    param_type = ['a', '20180701']
    model_option, subtitle = param_model_a.param(param_type)
    all_choice_moments = []
    choice_set_list = model_option['choice_set_list']
    for choiceJ_counter, choiceJ_index in enumerate(choice_set_list):

        '''Probability'''
        prob_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_dict['probJ_opti_grid'] + \
                        steady_agg_suffixes['_j_agg'][0]
        all_choice_moments.append(prob_col_name)
        '''Aggregate each J b asset'''
        # 0. loop over: 'btp_opti_grid':2, 'ktp_opti_grid':3, 'consumption_opti_grid':4
        for steady_var_suffixes_cur in [steady_var_suffixes_dict['btp_opti_grid'],
                                        steady_var_suffixes_dict['ktp_opti_grid'],
                                        steady_var_suffixes_dict['consumption_opti_grid'],
                                        steady_var_suffixes_dict['btp_fb_opti_grid'],
                                        steady_var_suffixes_dict['btp_ib_opti_grid'],
                                        steady_var_suffixes_dict['btp_fs_opti_grid'],
                                        steady_var_suffixes_dict['btp_il_opti_grid']]:
            '''Kn, Bn, and cc'''
            cur_j_opti_col_name = choice_names[choiceJ_index] + '_' + steady_var_suffixes_cur
            col_name_j_agg = cur_j_opti_col_name + steady_agg_suffixes['_j_agg'][0]
            col_name_j_agg_ifj = cur_j_opti_col_name + steady_agg_suffixes['_j_agg_ifj'][0]

            all_choice_moments.append(col_name_j_agg)
            all_choice_moments.append(col_name_j_agg_ifj)

    return all_choice_moments


def momsets_a(momsets_type):
    module = momsets_type[0]
    sub_type = str(momsets_type[1])

    # weight and power
    wp = {'agg_prob': [1, 1],
          'agg_prob_inf': [1, 1],
          'agg_prob_for': [1, 1],
          'agg_prob_jnt': [1, 1],
          'agg_prob_brr': [1, 1],
          'agg_prob_sav': [1, 1],
          'mean_KYC': [0.25, (1 / 2)],
          'mean_BKYC': [0.25, (1 / 2)],
          'mean_B': [0.25, (1 / 2)],
          'mean_K': [0.25, (1 / 2)],
          'mean_Y': [0.25, (1 / 2)],
          'mean_C': [0.25, (1 / 2)],
          'mean_ibil': [1.5, 2],
          'mean_fbfs': [1.5, 2]}

    agg_prob = ['ib_probJ_opti_grid_j_agg',
                'is_probJ_opti_grid_j_agg',
                'fb2_probJ_opti_grid_j_agg',
                'fs_probJ_opti_grid_j_agg',
                'ibfb2_probJ_opti_grid_j_agg',
                'fbis2_probJ_opti_grid_j_agg',
                'none_probJ_opti_grid_j_agg']

    agg_prob_inf = ['ib_probJ_opti_grid_j_agg',
                    'is_probJ_opti_grid_j_agg']
    agg_prob_for = ['fb2_probJ_opti_grid_j_agg',
                    'fs_probJ_opti_grid_j_agg', ]
    agg_prob_jnt = ['ibfb2_probJ_opti_grid_j_agg',
                    'fbis2_probJ_opti_grid_j_agg']
    agg_prob_brr = ['ib_probJ_opti_grid_j_agg',
                    'fb2_probJ_opti_grid_j_agg',
                    'ibfb2_probJ_opti_grid_j_agg']
    agg_prob_sav = ['is_probJ_opti_grid_j_agg',
                    'fs_probJ_opti_grid_j_agg',
                    'fbis2_probJ_opti_grid_j_agg']

    mean_BKYC = ['btp_opti_grid_allJ_agg',
                 'ktp_opti_grid_allJ_agg',
                 'y_opti_grid_allJ_agg',
                 'consumption_opti_grid_allJ_agg']

    mean_B = ['btp_opti_grid_allJ_agg']
    mean_K = ['ktp_opti_grid_allJ_agg']
    mean_Y = ['y_opti_grid_allJ_agg']
    mean_C = ['consumption_opti_grid_allJ_agg']

    mean_KYC = ['ktp_opti_grid_allJ_agg',
                'y_opti_grid_allJ_agg',
                'consumption_opti_grid_allJ_agg']

    mean_ibil = ["btp_ib_opti_grid_allJ_agg",
                 "btp_il_opti_grid_allJ_agg"]

    mean_fbfs = ["btp_fb_opti_grid_allJ_agg",
                 "btp_fs_opti_grid_allJ_agg"]

    equi_BI = ['btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg']

    if (sub_type == '20180805a'):
        subtitle = 'moment_sets test'
        moment_sets = {'agg_prob': [agg_prob, wp['agg_prob'][0], wp['agg_prob'][1]]}

    if (sub_type == '20180805b'):
        subtitle = 'moment_sets test'
        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_none': [['none_probJ_opti_grid_j_agg'], wp['agg_prob'][0], wp['agg_prob'][1]]}

    if (sub_type == '20180805c'):
        subtitle = 'moment_sets test'
        moment_sets = {'agg_prob': [agg_prob, wp['agg_prob'][0], wp['agg_prob'][0]],
                       'mean_KYC': [mean_KYC, wp['mean_KYC'][0], wp['mean_KYC'][1]],
                       'mean_ibil': [mean_ibil, wp['mean_ibil'][0], wp['mean_ibil'][1]],
                       'mean_fbfs': [mean_fbfs, wp['mean_fbfs'][0], wp['mean_fbfs'][1]]}

    if (sub_type == '20180805d'):
        subtitle = 'moment_sets test'
        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_none': [['none_probJ_opti_grid_j_agg'], wp['agg_prob'][0], wp['agg_prob'][1]],
                       'mean_B': [mean_B, wp['mean_B'][0], wp['mean_B'][1]],
                       'mean_K': [mean_K, wp['mean_K'][0], wp['mean_K'][1]],
                       'mean_Y': [mean_Y, wp['mean_Y'][0], wp['mean_Y'][1]],
                       'mean_C': [mean_C, wp['mean_C'][0], wp['mean_C'][1]]}

    if (sub_type == '20180817a'):
        subtitle = 'prob and k'
        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_none': [['none_probJ_opti_grid_j_agg'], wp['agg_prob'][0], wp['agg_prob'][1]],
                       'mean_K': [mean_K, wp['mean_K'][0], wp['mean_K'][1]]}

    if (sub_type == '20180901a'):
        subtitle = 'quad x10 prob equi_BI'
        wp = {'agg_prob': [10, 2],
              'agg_prob_inf': [10, 2],
              'agg_prob_for': [10, 2],
              'agg_prob_jnt': [10, 2],
              'agg_prob_brr': [10, 2],
              'agg_prob_sav': [10, 2],
              'mean_KYC': [1, 2],
              'mean_BKYC': [1, 2],
              'mean_B': [1, 2],
              'mean_K': [1, 2],
              'mean_Y': [1, 2],
              'mean_C': [1, 2],
              'mean_ibil': [1, 2],
              'mean_fbfs': [1, 2],
              'equi_BI': [1, 2]}

        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_none': [['none_probJ_opti_grid_j_agg'], wp['agg_prob'][0], wp['agg_prob'][1]],
                       'mean_K': [mean_K, wp['mean_K'][0], wp['mean_K'][1]],
                       'equi_BI': [equi_BI, wp['equi_BI'][0], wp['equi_BI'][1]]}

    if (sub_type == '20180923a'):
        subtitle = 'quad x10 prob equi_BI'
        wp = {'agg_prob': [10, 2],
              'agg_prob_inf': [10, 2],
              'agg_prob_for': [10, 2],
              'agg_prob_jnt': [10, 2],
              'agg_prob_brr': [10, 2],
              'agg_prob_sav': [10, 2],
              'mean_KYC': [1, 2],
              'mean_BKYC': [1, 2],
              'mean_B': [1, 2],
              'mean_K': [1, 2],
              'mean_Y': [1, 2],
              'mean_C': [1, 2],
              'mean_ibil': [1, 2],
              'mean_fbfs': [1, 2],
              'equi_BI': [1, 2]}

        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]], }

    if (sub_type == '20180924a'):
        subtitle = 'quad x10 prob equi_BI'
        wp = {'agg_prob': [10, 2],
              'agg_prob_inf': [10, 2],
              'agg_prob_for': [10, 2],
              'agg_prob_jnt': [10, 2],
              'agg_prob_brr': [10, 2],
              'agg_prob_sav': [10, 2],
              'mean_KYC': [1, 2],
              'mean_BKYC': [1, 2],
              'mean_B': [1, 2],
              'mean_K': [1, 2],
              'mean_Y': [1, 2],
              'mean_C': [1, 2],
              'mean_ibil': [1, 2],
              'mean_fbfs': [1, 2],
              'equi_BI': [1, 2]}

        moment_sets = {'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]]}

    if (sub_type == 'graphing'):
        '''
        Could include more/many repeats
        '''
        subtitle = 'graphing groups'
        moment_sets = {'agg_prob': [agg_prob, wp['agg_prob'][0], wp['agg_prob'][0]],
                       'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_brr': [agg_prob_brr, wp['agg_prob_brr'][0], wp['agg_prob_brr'][1]],
                       'agg_prob_sav': [agg_prob_sav, wp['agg_prob_sav'][0], wp['agg_prob_sav'][1]],
                       'mean_KYC': [mean_KYC, wp['mean_KYC'][0], wp['mean_KYC'][1]],
                       'mean_ibil': [mean_ibil, wp['mean_ibil'][0], wp['mean_ibil'][1]],
                       'mean_fbfs': [mean_fbfs, wp['mean_fbfs'][0], wp['mean_fbfs'][1]]}

    if (sub_type == 'all_moments'):
        '''
        Could include more/many repeats
        '''
        subtitle = 'graphing groups'
        moment_sets = {'agg_prob': [agg_prob, wp['agg_prob'][0], wp['agg_prob'][0]],
                       'agg_prob_inf': [agg_prob_inf, wp['agg_prob_inf'][0], wp['agg_prob_inf'][1]],
                       'agg_prob_for': [agg_prob_for, wp['agg_prob_for'][0], wp['agg_prob_for'][1]],
                       'agg_prob_jnt': [agg_prob_jnt, wp['agg_prob_jnt'][0], wp['agg_prob_jnt'][1]],
                       'agg_prob_brr': [agg_prob_brr, wp['agg_prob_brr'][0], wp['agg_prob_brr'][1]],
                       'agg_prob_sav': [agg_prob_sav, wp['agg_prob_sav'][0], wp['agg_prob_sav'][1]],
                       'mean_BKYC': [mean_BKYC, wp['mean_BKYC'][0], wp['mean_BKYC'][1]],
                       'mean_ibil': [mean_ibil, wp['mean_ibil'][0], wp['mean_ibil'][1]],
                       'mean_fbfs': [mean_fbfs, wp['mean_fbfs'][0], wp['mean_fbfs'][1]]}

    return moment_sets, subtitle


def all_possible_keys():
    moment_keys = {
        "probJ_opti_grid_allJ_agg": 0.9999999999999801,
        "btp_opti_grid_allJ_agg": -1.2337262282180355,
        "ktp_opti_grid_allJ_agg": 3.934625954455946,
        "consumption_opti_grid_allJ_agg": 1.2870913617174071,

        "btp_fb_opti_grid_allJ_agg": -0.2661729904001723,
        "btp_ib_opti_grid_allJ_agg": -1.026135044138899,
        "btp_fs_opti_grid_allJ_agg": 0.013072665981130382,
        "btp_il_opti_grid_allJ_agg": 0.04550914033990551,

        "ib_probJ_opti_grid_j_agg": 0.2841523384541719,
        "ib_btp_opti_grid_j_agg": -0.8080284188919505,
        "ib_btp_opti_grid_j_agg_ifj": -2.944030596000148,
        "ib_ktp_opti_grid_j_agg": 1.35261383910931,
        "ib_ktp_opti_grid_j_agg_ifj": 5.526600057064562,
        "ib_consumption_opti_grid_j_agg": 0.33325502203627,
        "ib_consumption_opti_grid_j_agg_ifj": 1.5008843967113614,
        "ib_btp_fb_opti_grid_j_agg": 0,
        "ib_btp_fb_opti_grid_j_agg_ifj": 0,
        "ib_btp_ib_opti_grid_j_agg": -0.8080284188919505,
        "ib_btp_ib_opti_grid_j_agg_ifj": -2.944030596000148,
        "ib_btp_fs_opti_grid_j_agg": 0,
        "ib_btp_fs_opti_grid_j_agg_ifj": 0,
        "ib_btp_il_opti_grid_j_agg": 0,
        "ib_btp_il_opti_grid_j_agg_ifj": 0,

        "is_probJ_opti_grid_j_agg": 0.026731522289728984,
        "is_btp_opti_grid_j_agg": 0.024251207090910443,
        "is_btp_opti_grid_j_agg_ifj": 0.3268659635922395,
        "is_ktp_opti_grid_j_agg": 0.07300725926540677,
        "is_ktp_opti_grid_j_agg_ifj": 1.5616347970991629,
        "is_consumption_opti_grid_j_agg": 0.04029557612426725,
        "is_consumption_opti_grid_j_agg_ifj": 0.6999255612590607,
        "is_btp_fb_opti_grid_j_agg": 0,
        "is_btp_fb_opti_grid_j_agg_ifj": 0,
        "is_btp_ib_opti_grid_j_agg": 0,
        "is_btp_ib_opti_grid_j_agg_ifj": 0,
        "is_btp_fs_opti_grid_j_agg": 0,
        "is_btp_fs_opti_grid_j_agg_ifj": 0,
        "is_btp_il_opti_grid_j_agg": 0.024251207090910443,
        "is_btp_il_opti_grid_j_agg_ifj": 0.3268659635922395,

        "fb2_probJ_opti_grid_j_agg": 0.13709104029628677,
        "fb2_btp_opti_grid_j_agg": -0.07980120007638962,
        "fb2_btp_opti_grid_j_agg_ifj": -0.5225346999595015,
        "fb2_ktp_opti_grid_j_agg": 0.5107674630140073,
        "fb2_ktp_opti_grid_j_agg_ifj": 3.262571854570359,
        "fb2_consumption_opti_grid_j_agg": 0.18025846652627836,
        "fb2_consumption_opti_grid_j_agg_ifj": 1.1368919285324555,
        "fb2_btp_fb_opti_grid_j_agg": -0.07980120007638962,
        "fb2_btp_fb_opti_grid_j_agg_ifj": -0.5225346999595015,
        "fb2_btp_ib_opti_grid_j_agg": 0,
        "fb2_btp_ib_opti_grid_j_agg_ifj": 0,
        "fb2_btp_fs_opti_grid_j_agg": 0,
        "fb2_btp_fs_opti_grid_j_agg_ifj": 0,
        "fb2_btp_il_opti_grid_j_agg": 0,
        "fb2_btp_il_opti_grid_j_agg_ifj": 0,

        "fs_probJ_opti_grid_j_agg": 0.15802010125186614,
        "fs_btp_opti_grid_j_agg": 0.013072665981130382,
        "fs_btp_opti_grid_j_agg_ifj": 0.07636836528926151,
        "fs_ktp_opti_grid_j_agg": 0.5044915067332771,
        "fs_ktp_opti_grid_j_agg_ifj": 2.8527836750958047,
        "fs_consumption_opti_grid_j_agg": 0.2091813192990893,
        "fs_consumption_opti_grid_j_agg_ifj": 1.1738755767624096,
        "fs_btp_fb_opti_grid_j_agg": 0,
        "fs_btp_fb_opti_grid_j_agg_ifj": 0,
        "fs_btp_ib_opti_grid_j_agg": 0,
        "fs_btp_ib_opti_grid_j_agg_ifj": 0,
        "fs_btp_fs_opti_grid_j_agg": 0.013072665981130382,
        "fs_btp_fs_opti_grid_j_agg_ifj": 0.07636836528926151,
        "fs_btp_il_opti_grid_j_agg": 0,
        "fs_btp_il_opti_grid_j_agg_ifj": 0,

        "ibfb2_probJ_opti_grid_j_agg": 0.15034019009106742,
        "ibfb2_btp_opti_grid_j_agg": -0.39062191284697356,
        "ibfb2_btp_opti_grid_j_agg_ifj": -2.427287258258688,
        "ibfb2_ktp_opti_grid_j_agg": 0.7186565650348887,
        "ibfb2_ktp_opti_grid_j_agg_ifj": 4.680307097655593,
        "ibfb2_consumption_opti_grid_j_agg": 0.21128137561750615,
        "ibfb2_consumption_opti_grid_j_agg_ifj": 1.405624726552921,
        "ibfb2_btp_fb_opti_grid_j_agg": -0.17251528760002505,
        "ibfb2_btp_fb_opti_grid_j_agg_ifj": -1.1217310412162305,
        "ibfb2_btp_ib_opti_grid_j_agg": -0.2181066252469485,
        "ibfb2_btp_ib_opti_grid_j_agg_ifj": -1.3055562170424575,
        "ibfb2_btp_fs_opti_grid_j_agg": 0,
        "ibfb2_btp_fs_opti_grid_j_agg_ifj": 0,
        "ibfb2_btp_il_opti_grid_j_agg": 0,
        "ibfb2_btp_il_opti_grid_j_agg_ifj": 0,

        "fbis2_probJ_opti_grid_j_agg": 0.017915253431241354,
        "fbis2_btp_opti_grid_j_agg": 0.007401430525237481,
        "fbis2_btp_opti_grid_j_agg_ifj": -0.06583564639013961,
        "fbis2_ktp_opti_grid_j_agg": 0.05542601089503035,
        "fbis2_ktp_opti_grid_j_agg_ifj": 1.6145257582127845,
        "fbis2_consumption_opti_grid_j_agg": 0.027536976456097494,
        "fbis2_consumption_opti_grid_j_agg_ifj": 0.612311511625282,
        "fbis2_btp_fb_opti_grid_j_agg": -0.013856502723757588,
        "fbis2_btp_fb_opti_grid_j_agg_ifj": -0.40363143955319614,
        "fbis2_btp_ib_opti_grid_j_agg": 0,
        "fbis2_btp_ib_opti_grid_j_agg_ifj": 0,
        "fbis2_btp_fs_opti_grid_j_agg": 0,
        "fbis2_btp_fs_opti_grid_j_agg_ifj": 0,
        "fbis2_btp_il_opti_grid_j_agg": 0.021257933248995067,
        "fbis2_btp_il_opti_grid_j_agg_ifj": 0.3377957931630565,

        "none_probJ_opti_grid_j_agg": 0.22574955418561737,
        "none_btp_opti_grid_j_agg": 0,
        "none_btp_opti_grid_j_agg_ifj": 0,
        "none_ktp_opti_grid_j_agg": 0.7196633104040248,
        "none_ktp_opti_grid_j_agg_ifj": 3.136977459857847,
        "none_consumption_opti_grid_j_agg": 0.28528262565789864,
        "none_consumption_opti_grid_j_agg_ifj": 1.2645527383623827,
        "none_btp_fb_opti_grid_j_agg": 0,
        "none_btp_fb_opti_grid_j_agg_ifj": 0,
        "none_btp_ib_opti_grid_j_agg": 0,
        "none_btp_ib_opti_grid_j_agg_ifj": 0,
        "none_btp_fs_opti_grid_j_agg": 0,
        "none_btp_fs_opti_grid_j_agg_ifj": 0,
        "none_btp_il_opti_grid_j_agg": 0,
        "none_btp_il_opti_grid_j_agg_ifj": 0
    }

    moment_group_1 = [1, 2, 3, 4, 5, 6]


if __name__ == '__main__':
    print(momsets_all_moments())
