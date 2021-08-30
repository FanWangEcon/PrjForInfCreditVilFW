'''
@author: fan
'''

import logging

import pyfan.amto.json.json as support_json

logger = logging.getLogger(__name__)


def get_speckey_dict(gn_invoke_set=None):
    """speckey_dict uses integers to refer to string speckey names

    This is something that ends up adding confusion potentially, but when understood, is something
    useful. Rather than calling with a longer harder perhaps to remember string name. Use an integer
    index to specify which speckey to call.

    This is used by :func:`invoke.combo_type_list_wth_specs.gen_combo_type_list` for example

    Parameters
    ----------
    gn_invoke_set : str or int, optional
        Default is None, if string, then is a string that i  the string value corresponding to the integer keys
        below. If this is specified, it_speckey should be None. If Int, then find speckey from int

    Returns
    ------
    dict
        Returns the full speckey_dict dictionary if both st_speckey and it_speckey are None. Otherwise returns
        just one element of of the dictionary, that corresponds either to the st_speckey or it_speckey.
    """

    speckey_dict = {0: 'mpoly_1',
                    1: 'ng_s_t',
                    2: 'ng_s_d',
                    3: 'ng_p_t',
                    4: 'ng_p_d',

                    5: 'ge_p_t_mul',
                    6: 'ge_p_m_mul',
                    7: 'ge_p_d_mul',

                    8: 'ge_s_t_bis',
                    9: 'ge_p_t_bis',
                    10: 'ge_p_m_bis',
                    11: 'ge_p_d_bis',

                    12: 'b_ng_s_t',  # 12
                    13: 'b_ng_s_d',  # 13
                    14: 'b_ng_p_t',  # 14
                    15: 'b_ng_p_d',  # 15

                    16: 'b_ge_p_m_mul',  # 16
                    17: 'b_ge_p_d_mul',  # 17

                    18: 'b_ge_s_t_bis',  # 18
                    19: 'b_ge_p_m_bis',  # 19
                    20: 'b_ge_p_d_bis',  # 20
                    21: 'local_ng_par_d_cev'  # 21
                    }

    if gn_invoke_set is not None:

        if isinstance(gn_invoke_set, str):
            # select by key
            ls_it_keys = [gn_invoke_set]
            dc_speckey_dict_select_by_key = {it_key: speckey_dict[it_key] for it_key in ls_it_keys}
            return dc_speckey_dict_select_by_key

        elif isinstance(gn_invoke_set, int):
            # select by value
            ls_st_keys = [gn_invoke_set]
            dc_speckey_dict_select_by_val = {it_key: st_val for it_key, st_val in speckey_dict.items()
                                             if st_val in ls_st_keys}
            return dc_speckey_dict_select_by_val

        else:
            raise TypeError(f'{gn_invoke_set=} was not None and was not a string or an integer')

    else:

        # return full list
        return speckey_dict


def get_all_compute_specs(fargate):
    fargate_specifications = compute_set_gen(fargate=fargate)
    batch_specifications = compute_set_gen_morecpu(fargate=fargate)
    compute_specifications = {}
    for d in [fargate_specifications, batch_specifications]:
        for k, v in d.items():
            compute_specifications[k] = v

    return compute_specifications


def compute_set(compute_spec_key, fargate=False):
    compute_specifications = get_all_compute_specs(fargate)

    for compute_key, compute_spec in compute_specifications.items():
        compute_specifications[compute_key]['vcpus'] = \
            int(int(compute_specifications[compute_key]['cpu']) / 1024)

    cur_specification = compute_specifications[compute_spec_key]

    return cur_specification


def spec_key_counter(compute_spec_key, fargate=False):
    """Save Space Store Ctr
    What is the sequence position for spec_key
    """
    compute_specifications = get_all_compute_specs(fargate)

    index = {k: (i + 1) for i, k in enumerate(compute_specifications.keys())}
    support_json.jdump(index, 'compute spec index:', logger=logger.warning)
    cur_spec_key_index = index[compute_spec_key]

    return cur_spec_key_index


def compute_bisection():
    """
    bis for bisections
    mul for multisection

    t for test
    m for medium
    d for detail
    """

    bis_t = {'int_rate_counts': 3,
             'bisection_iter': 3}
    bis_m = {'int_rate_counts': 3,
             'bisection_iter': 6}
    bis_d = {'int_rate_counts': 3,
             'bisection_iter': 10}

    mul_t = {'int_rate_counts': 4,
             'bisection_iter': 2}
    mul_m = {'int_rate_counts': 4,
             'bisection_iter': 3}
    mul_d = {'int_rate_counts': 4,
             'bisection_iter': 4}

    mul_t = {'int_rate_counts': 4,
             'bisection_iter': 2}
    mul_m = {'int_rate_counts': 4,
             'bisection_iter': 3}
    mul_d = {'int_rate_counts': 4,
             'bisection_iter': 4}

    inf_m = {'int_rate_counts': 8,
             'bisection_iter': 2}
    inf_d = {'int_rate_counts': 16,
             'bisection_iter': 2}

    return bis_t, bis_m, bis_d, mul_t, mul_m, mul_d, inf_m, inf_d


def compute_set_gen(fargate=True):
    """
    compute_detail
    - (0.0506*4 + 0.0127*10) = 0.329, machine per hour cost.
    - (0.0506*1 + 0.0127*3) = 0.0887, machine per hour cost.
    - (0.0506*2 + 0.0127*8)*18, 36 cores, 144 gb, more expensive than: m5.12xlarge 48 173 192 GiB EBS Only $2.304 per Hour
    - no-ge: solve model 10 times
    - ge: Compute_detail=4*4=16 interest rate for each of 10 parameter grid, solve model 160 times
        + sequentially:
            - If each solution takes 30 seconds, (160*30)/60 = 80 minutes time cost
        + in parallel:
            - 4*10=40 40 sets of parallel sessions, so if each session 1 minute, about 40 minutes.
        + cost = (0.0506*4 + 0.0127*10)*(1+20/60)
    - Actual Speed:
        Time:
            + A = 2062s = 34 min
                + (0.0506*4 + 0.0127*8)*(2062/(60*60)) = 0.174
            + max_inter = 1059s = 17 min
                + (0.0506*4 + 0.0127*8)*(1059/(60*60)) = 0.089
            + beta = 2327s = 40m
                + (0.0506*4 + 0.0127*8)*(2327/(60*60)) = 0.1965
            + markov_points = 1752s = 30m
            + alpha_k = 2442s = 40m
        len_choices (4 cpu, 16 gb ram) =
    """

    """
    Group A, Parallize over interest rate vector:
    Bisection and Multisection specficiations
    """
    bis_t, bis_m, bis_d, mul_t, mul_m, mul_d, inf_m, inf_d = compute_bisection()

    """
    A. GE, not integrated, parallel
    """
    # fargate_ge_mul_d_par: 4 x 10 = 40 sets of (par 4) evaluations if not integrated
    # 40 x 4 = 160 model evaluations
    fargate_ge_mul_d_par = {'cpu': str(1024 * 4), 'memory': str(1024 * 25),
                            'workers': 4,
                            'compute_param_vec_count': 10,
                            'int_rate_counts': mul_d['int_rate_counts'],
                            'bisection_iter': mul_d['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    # fargate_ge_mul_m_par: 3 x 8 = 24 sets of (par 4) evaluations if not integrated
    # 24 x 4 = 96 model evaluations
    fargate_ge_mul_m_par = {'cpu': str(1024 * 4), 'memory': str(1024 * 25),
                            'workers': 4,
                            'compute_param_vec_count': 10,
                            'int_rate_counts': mul_m['int_rate_counts'],
                            'bisection_iter': mul_m['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    # fargate_ge_mul_m_par: 2 x 3 = 6 sets of (par 4) evaluations if not integrated
    # 6 x 4 = 24 model evaluations
    # local takes 573 seconds (not integrated)
    fargate_ge_mul_t_par = {'cpu': str(1024 * 4), 'memory': str(1024 * 25),
                            'workers': 4,
                            'compute_param_vec_count': 3,
                            'int_rate_counts': mul_t['int_rate_counts'],
                            'bisection_iter': mul_t['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    """
    B. GE, integrated, parallel
    """
    # fargate_ge_mul_d_par: 10 x 8 = 80 sets of (integrated) evaluations if not integrated
    # with 8 integration points: 8 x 80 = 640 model evaluations or maybe slightly more? if 10 x 12 x 8 = 120 x 8 = 960
    # but 80 evaluations concurrently, or perhaps 120, if each takes 2 minutes, 4 hours. If each on average 4 minutes, 120 evaluates =
    # avg 4 min each 8 eval = 120 * 4 = 480 minutes, 8 hours potentially.
    # total file generated, could be as many as 120 x 10 = 1200, 1200 x 2 = 2400
    fargate_ge_bis_d_par = {'cpu': str(1024 * 10), 'memory': str(1024 * 55),
                            'workers': 10,
                            'compute_param_vec_count': 10,
                            'int_rate_counts': bis_d['int_rate_counts'],
                            'bisection_iter': bis_d['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    # fargate_ge_mul_m_par: 8 x 5 = 40 sets of (integrated) evaluations if not integrated
    # with 4 integration points: 4 x 40 = 160 model evaluations
    # local takes 1790 seconds (not integrated)
    fargate_ge_bis_m_par = {'cpu': str(1024 * 8), 'memory': str(1024 * 40),
                            'workers': 8,
                            'compute_param_vec_count': 10,
                            'int_rate_counts': bis_m['int_rate_counts'],
                            'bisection_iter': bis_m['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    # fargate_ge_mul_m_par: 5 x 3 = 15 sets of (integrated) evaluations if not integrated
    # with 3 integration points: 3 x 15 = 45 model evaluations
    fargate_ge_bis_t_par = {'cpu': str(1024 * 8), 'memory': str(1024 * 40),
                            'workers': 8,
                            'compute_param_vec_count': 3,
                            'int_rate_counts': bis_t['int_rate_counts'],
                            'bisection_iter': bis_t['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': True,
                            'graph': True}

    # fargate_ge_mul_m_par: 5 x 3 = 15 sets of (integrated) evaluations if not integrated
    # with 3 integration points: 3 x 15 = 45 model evaluations
    fargate_ge_bis_t_seq = {'cpu': str(1024 * 1), 'memory': str(1024 * 7),
                            'workers': 4,
                            'compute_param_vec_count': 3,
                            'int_rate_counts': bis_t['int_rate_counts'],
                            'bisection_iter': bis_t['bisection_iter'],
                            'aws_fargate': fargate,
                            'ge': True,
                            'multiprocess': False,
                            'graph': True}
    """
    C. Not GE
    """
    fargate_ng_seq_d = {'cpu': str(1024 * 1),
                        'memory': str(1024 * 6),
                        'workers': 1,
                        'compute_param_vec_count': 56,
                        'aws_fargate': fargate,
                        'ge': False,
                        'multiprocess': False,
                        'graph': True}
    fargate_ng_seq_t = {'cpu': str(1024 * 1),
                        'memory': str(1024 * 6),
                        'workers': 1,
                        'compute_param_vec_count': 3,
                        'aws_fargate': fargate,
                        'ge': False,
                        'multiprocess': False,
                        'graph': True}

    # structure for local CEV surface calculations
    # for local run, cpu and memory requirements are not relevant,
    # will keep these here nevertheless
    # actually not used locally, but remotely
    local_ng_par_d_cev = {'cpu': str(1024 * 10),
                          'memory': str(1024 * 55),
                          'workers': 8,  # 24 threads available
                          'compute_param_vec_count': 201,
                          'aws_fargate': fargate,
                          'ge': False,
                          'multiprocess': True,
                          'graph': True}

    fargate_ng_par_d = {'cpu': str(1024 * 10),
                        'memory': str(1024 * 55),
                        'workers': 10,
                        'compute_param_vec_count': 6,
                        'aws_fargate': fargate,
                        'ge': False,
                        'multiprocess': True,
                        'graph': True}

    # for integrated runs
    fargate_ng_par_t = {'cpu': str(1024 * 8),
                        'memory': str(1024 * 45),
                        'workers': 8,
                        'compute_param_vec_count': 14,
                        'aws_fargate': fargate,
                        'ge': False,
                        'multiprocess': True,
                        'graph': True}

    # for mpoly
    fargate_mpoly_1vcpu = {'cpu': str(1024 * 1),
                           'memory': str(517),  # only need about 160 mb in reality
                           'workers': 1,
                           'compute_param_vec_count': 14,
                           'aws_fargate': fargate,
                           'ge': False,
                           'multiprocess': False,
                           'graph': True}

    compute_specifications = {'mpoly_1': fargate_mpoly_1vcpu,  # 0
                              'ng_s_t': fargate_ng_seq_t,  # 1
                              'ng_s_d': fargate_ng_seq_d,  # 2
                              'ng_p_t': fargate_ng_par_t,  # 3
                              'ng_p_d': fargate_ng_par_d,  # 4

                              'ge_p_t_mul': fargate_ge_mul_t_par,  # 5
                              'ge_p_m_mul': fargate_ge_mul_m_par,  # 6
                              'ge_p_d_mul': fargate_ge_mul_d_par,
                              # 7

                              'ge_s_t_bis': fargate_ge_bis_t_seq,  # 8
                              'ge_p_t_bis': fargate_ge_bis_t_par,  # 9
                              'ge_p_m_bis': fargate_ge_bis_m_par,  # 10
                              'ge_p_d_bis': fargate_ge_bis_d_par,  # 11
                              'local_ng_par_d_cev': local_ng_par_d_cev}  # 12

    return compute_specifications


def compute_set_gen_morecpu(fargate=True):
    """
    With Batch Mode, Have access it seems, to a very large number of vcpus per task/job.
    Here, specify compute_specificaitons when there are no vcpu limits.
    """
    bis_t, bis_m, bis_d, mul_t, mul_m, mul_d, inf_m, inf_d = compute_bisection()

    """
    A. GE, not integrated, parallel
    """
    # batch_ge_inf_d_par: 2 x 20 = 40 sets of (par 4) evaluations if not integrated
    # 40 x 16 = 640 model evaluations
    # Likely use: r4.4xlarge most likely: 16 vcpu, 122 GiB, spot $0.1489 per Hour
    batch_ge_inf_d_par = {'cpu': str(1024 * inf_d['int_rate_counts']),
                          'memory': str(1024 * inf_d['int_rate_counts'] * 6),
                          'workers': inf_m['int_rate_counts'],
                          'compute_param_vec_count': 20,
                          'int_rate_counts': inf_d['int_rate_counts'],
                          'bisection_iter': inf_d['bisection_iter'],
                          'aws_fargate': fargate,
                          'ge': True,
                          'multiprocess': True,
                          'graph': True}

    # batch_ge_inf_m_par: 20 x 10 = 20 sets of (par 4) evaluations if not integrated
    # 20 x 9 = 180 model evaluations
    # likely use: instance with 16 vcpu and 64 GB ram.
    batch_ge_inf_m_par = {'cpu': str(1024 * inf_m['int_rate_counts']),
                          'memory': str(1024 * inf_m['int_rate_counts'] * 6),
                          'workers': inf_m['int_rate_counts'],
                          'compute_param_vec_count': 10,
                          'int_rate_counts': inf_m['int_rate_counts'],
                          'bisection_iter': inf_m['bisection_iter'],
                          'aws_fargate': fargate,
                          'ge': True,
                          'multiprocess': True,
                          'graph': True}

    """
    B. GE, integrated, parallel
    """
    # batch_ge_bis_d_par: 10 x 10 = 100 sets of (integrated) evaluations if not integrated
    # with 8 integration points: 8 x 100 = 800 model evaluations
    batch_ge_bis_d_par = {'cpu': str(1024 * 8),
                          'memory': str(1024 * 8 * 6),
                          'workers': 8,
                          'compute_param_vec_count': 10,
                          'int_rate_counts': bis_d['int_rate_counts'],
                          'bisection_iter': bis_d['bisection_iter'],
                          'aws_fargate': fargate,
                          'ge': True,
                          'multiprocess': True,
                          'graph': True}

    # batch_ge_bis_m_par: 8 x 8 = 64 sets of (integrated) evaluations if not integrated
    # with 4 integration points: 8 x 64 = 512 model evaluations
    # local takes 1790 seconds (not integrated)
    batch_ge_bis_m_par = {'cpu': str(1024 * 4), 'memory': str(1024 * 8 * 6),
                          'workers': 8,
                          'compute_param_vec_count': 8,
                          'int_rate_counts': bis_m['int_rate_counts'],
                          'bisection_iter': bis_m['bisection_iter'],
                          'aws_fargate': fargate,
                          'ge': True,
                          'multiprocess': True,
                          'graph': True}

    # batch_ge_bis_t_seq: 5 x 3 = 15 sets of (integrated) evaluations if not integrated
    # with 3 integration points: 3 x 15 = 45 model evaluations
    batch_ge_bis_t_seq = {'cpu': str(1024 * 2), 'memory': str(1024 * 1 * 7),
                          'workers': 1,
                          'compute_param_vec_count': 3,
                          'int_rate_counts': bis_t['int_rate_counts'],
                          'bisection_iter': bis_t['bisection_iter'],
                          'aws_fargate': fargate,
                          'ge': True,
                          'multiprocess': False,
                          'graph': True}
    """
    C. Not GE
    """
    batch_ng_seq_d = {'cpu': str(1024 * 2),
                      'memory': str(1024 * 7),
                      'workers': 1,
                      'compute_param_vec_count': 56,
                      'aws_fargate': fargate,
                      'ge': False,
                      'multiprocess': False,
                      'graph': True}
    batch_ng_seq_t = {'cpu': str(1024 * 2),
                      'memory': str(1024 * 7),
                      'workers': 1,
                      'compute_param_vec_count': 3,
                      'aws_fargate': fargate,
                      'ge': False,
                      'multiprocess': False,
                      'graph': True}
    batch_ng_par_d = {'cpu': str(1024 * 8),
                      'memory': str(1024 * 8 * 6),
                      'workers': 8,
                      'compute_param_vec_count': 56,
                      'aws_fargate': fargate,
                      'ge': False,
                      'multiprocess': True,
                      'graph': True}

    batch_ng_par_t = {'cpu': str(1024 * 4),
                      'memory': str(1024 * 25),
                      'workers': 4,
                      'compute_param_vec_count': 4,
                      'aws_fargate': fargate,
                      'ge': False,
                      'multiprocess': True,
                      'graph': True}

    batch_compute_specifications = {'b_ng_s_t': batch_ng_seq_t,  # 12
                                    'b_ng_s_d': batch_ng_seq_d,  # 13
                                    'b_ng_p_t': batch_ng_par_t,  # 14
                                    'b_ng_p_d': batch_ng_par_d,  # 15

                                    'b_ge_p_m_mul': batch_ge_inf_m_par,  # 16
                                    'b_ge_p_d_mul': batch_ge_inf_d_par,
                                    # 17

                                    'b_ge_s_t_bis': batch_ge_bis_t_seq,  # 18
                                    'b_ge_p_m_bis': batch_ge_bis_m_par,  # 19
                                    'b_ge_p_d_bis': batch_ge_bis_d_par  # 20
                                    }

    return batch_compute_specifications
