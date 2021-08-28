'''
Created on Jul 24, 2018

@author: fan
'''
import logging
import pyfan.amto.json.json as support_json

import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def moments_a(moments_type):
    """
    This provides moments data, is not concerned which which subset of the values here
    will be relied upon for matching during estimation. 
    """

    module = moments_type[0]
    sub_type = str(moments_type[1])

    moments = {'ib_probJ_opti_grid_j_agg': 0.14,
               'is_probJ_opti_grid_j_agg': 0.14,
               'fb2_probJ_opti_grid_j_agg': 0.14,
               'fs_probJ_opti_grid_j_agg': 0.14,
               'ibfb2_probJ_opti_grid_j_agg': 0.14,
               'fbis2_probJ_opti_grid_j_agg': 0.15,
               'none_probJ_opti_grid_j_agg': 0.15,

               'ktp_opti_grid_allJ_agg': 3,
               'btp_opti_grid_allJ_agg': 1,

               'btp_ib_opti_grid_allJ_agg': -0.5,
               'btp_il_opti_grid_allJ_agg': 0.5,
               'btp_fb_opti_grid_allJ_agg': -0.5,
               'btp_fs_opti_grid_allJ_agg': 1}

    if ('20180805a' in sub_type):
        subtitle = 'moment_sets test'
        moments['btp_fs_opti_grid_allJ_agg'] = 1.5

    if ('20180813a_ce2' in sub_type):
        subtitle = 'moment_sets test_acutal'
        moments['ktp_opti_grid_allJ_agg'] = 1.298797965 * 3.3
        moments['btp_opti_grid_allJ_agg'] = 0.640706837 * 3.3
        prob_seven = {'ib_probJ_opti_grid_j_agg': 0.061,
                      'is_probJ_opti_grid_j_agg': 0.038,
                      'fb2_probJ_opti_grid_j_agg': 0.242,
                      'fs_probJ_opti_grid_j_agg': 0.341,
                      'ibfb2_probJ_opti_grid_j_agg': 0.143,
                      'fbis2_probJ_opti_grid_j_agg': 0.038,
                      'none_probJ_opti_grid_j_agg': 0.138}

    suff_mlt = hardstring.region_time_suffix(True)
    if ('20180816a' + suff_mlt in sub_type):
        """
        Tested below probabilities all sum up to 1
        """
        periods_keys_dict = hardstring.region_time_dict()

        '''
            checking if sub_type has these strings within:
                _mlt_ne1a2 _mlt_ce1a2 _mlt_all_ne1a2ce1a2
            depending on each: 
                decide to get [1,2], or [3,4] or all
        '''
        region_time_suffix = hardstring.region_time_suffix()
        for key_rt, val_rt in region_time_suffix.items():
            if (val_rt[0] in sub_type):
                periods_keys = val_rt[1]
                break

        k_multiplier = 3.3
        subtitle = 'central_four_periods_probk'
        paramloopstr.peristr(action='list')
        period_ce1_raw = {'ktp_opti_grid_allJ_agg': 0.981827855 * k_multiplier,
                          'ib_probJ_opti_grid_j_agg': 0.092,
                          'is_probJ_opti_grid_j_agg': 0.030,
                          'fb2_probJ_opti_grid_j_agg': 0.215,
                          'fs_probJ_opti_grid_j_agg': 0.300,
                          'ibfb2_probJ_opti_grid_j_agg': 0.05,
                          'fbis2_probJ_opti_grid_j_agg': 0.017,
                          'none_probJ_opti_grid_j_agg': 0.297,
                          'btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg': 0}

        period_ce2_raw = {'ktp_opti_grid_allJ_agg': 1.298797965 * k_multiplier,

                          'ib_probJ_opti_grid_j_agg': 0.061,
                          'is_probJ_opti_grid_j_agg': 0.038,
                          'fb2_probJ_opti_grid_j_agg': 0.242,
                          'fs_probJ_opti_grid_j_agg': 0.341,
                          'ibfb2_probJ_opti_grid_j_agg': 0.143,
                          'fbis2_probJ_opti_grid_j_agg': 0.038,
                          'none_probJ_opti_grid_j_agg': 0.138,
                          'btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg': 0}

        period_ne1_raw = {'ktp_opti_grid_allJ_agg': 0.47 * k_multiplier,

                          'ib_probJ_opti_grid_j_agg': 0.250,
                          'is_probJ_opti_grid_j_agg': 0.070,
                          'fb2_probJ_opti_grid_j_agg': 0.149,
                          'fs_probJ_opti_grid_j_agg': 0.062,
                          'ibfb2_probJ_opti_grid_j_agg': 0.241,
                          'fbis2_probJ_opti_grid_j_agg': 0.074,
                          'none_probJ_opti_grid_j_agg': 0.155,
                          'btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg': 0}

        period_ne2_raw = {'ktp_opti_grid_allJ_agg': 0.61 * k_multiplier,

                          'ib_probJ_opti_grid_j_agg': 0.062,
                          'is_probJ_opti_grid_j_agg': 0.049,
                          'fb2_probJ_opti_grid_j_agg': 0.290,
                          'fs_probJ_opti_grid_j_agg': 0.140,
                          'ibfb2_probJ_opti_grid_j_agg': 0.325,
                          'fbis2_probJ_opti_grid_j_agg': 0.078,
                          'none_probJ_opti_grid_j_agg': 0.056,
                          'btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg': 0}

        if ('_simu' in sub_type):
            '''
            this is for simulation (combine together)
                so that simulation which does not have 2 periods, just 1 simulation
                can be compared to the summed average objective of two periods
            '''
            moments = {}
            for key, val in period_ce1_raw.items():
                mom_value = 0
                for key_pkd in periods_keys:
                    if (key_pkd == 1):
                        mom_value = mom_value + period_ce1_raw[key]
                    elif (key_pkd == 2):
                        mom_value = mom_value + period_ce2_raw[key]
                    elif (key_pkd == 3):
                        mom_value = mom_value + period_ne1_raw[key]
                    elif (key_pkd == 4):
                        mom_value = mom_value + period_ne2_raw[key]
                    else:
                        raise ('bad')
                moments[key] = mom_value / len(periods_keys)

        else:
            '''
            this is for estimation
            '''
            moments = {}
            for key_pkd in periods_keys:
                dictkey = paramloopstr.peristr(period=key_pkd, action='dictkey')
                if (key_pkd == 1):
                    moments[dictkey] = period_ce1_raw
                elif (key_pkd == 2):
                    moments[dictkey] = period_ce2_raw
                elif (key_pkd == 3):
                    moments[dictkey] = period_ne1_raw
                elif (key_pkd == 4):
                    moments[dictkey] = period_ne2_raw
                else:
                    break

    return moments, subtitle


def possible_moments():
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


def test_cases():
    moments_type = ['a', '20180816a_mlt_ce1a2_simu']
    moments, subtitle = moments_a(moments_type)
    support_json.jdump(moments, 'moments', logger=logger.warning)


if __name__ == "__main__":
    test_cases()
