'''
@author: fan
'''

import logging
import numpy as np
import pyfan.amto.json.json as support_json

import projectsupport.hardcode.string_shared as hardstring

logger = logging.getLogger(__name__)


def compute_esti_spec_combine(compute_spec_key='',
                              esti_spec_key='',
                              moment_key='',
                              momset_key='',
                              spec_key='', action='combine'):
    """Combined string of the two for command line invoke
    
    import parameters.runspecs.estimate_specs as estispec
    spec_key_dict = estispec.compute_esti_spec_combine(spec_key=speckey, action='split')
    compute_spec_key = spec_key_dict['compute_spec_key']
    esti_spec_key = spec_key_dict['esti_spec_key']
    """

    connector = '='
    moment_key = str(moment_key)
    momset_key = str(momset_key)

    if (action == 'combine'):
        spec_key = compute_spec_key \
                   + connector + esti_spec_key \
                   + connector + moment_key \
                   + connector + momset_key

        return spec_key

    if (action == 'strip'):
        spec_key = spec_key.replace("=", "-")
        spec_key = spec_key.replace("_", "-")
        return spec_key

    elif (action == 'split'):
        if (connector in spec_key):
            # Split if both spec and esti keys are in spec_key
            compute_spec_key = spec_key.split(connector)[0]
            esti_spec_key = spec_key.split(connector)[1]
            moment_key = spec_key.split(connector)[2]
            momset_key = spec_key.split(connector)[3]
            spec_key_dict = {'compute_spec_key': compute_spec_key,
                             'esti_spec_key': esti_spec_key,
                             'moment_key': moment_key,
                             'momset_key': momset_key}
            return spec_key_dict

        else:
            # do nothing otherwise
            return spec_key

    elif (action == 'compute_spec_key'):
        if (connector in spec_key):
            compute_spec_key = spec_key.split(connector)[0]
        else:
            compute_spec_key = spec_key
        return compute_spec_key

    else:
        raise ('bad compute_esti_spec_combine:\n%s' + spec_key)


def estimate_set(esti_spec_key, moment_key=0, momset_key=1, fargate=False):
    """    
    Examples
    --------
    import parameters.runspecs.estimate_specs as estimatespecs
    estimate_specs = computespec.estimate_set(estispeckey)
    """
    moment_key = int(moment_key)
    momset_key = int(momset_key)

    estimate_specifications = estimate_set_gen(moment_key=moment_key,
                                               momset_key=momset_key)
    cur_specification = estimate_specifications[esti_spec_key]

    return cur_specification


def esti_key_counter(esti_spec_key, moment_key=0, momset_key=1):
    """Save Space Store Ctr    
    What is the sequence position for spec_key 
    """
    estimate_specifications = estimate_set_gen(moment_key=moment_key,
                                               momset_key=momset_key)

    index = {k: (i + 1) for i, k in enumerate(estimate_specifications.keys())}
    support_json.jdump(index, 'estimate spec index:', logger=logger.warning)
    cur_esti_key_index = index[esti_spec_key]

    return cur_esti_key_index


def moments_and_momsets():
    """
    These form a part of estimation subfolder name
    """

    region_time_suffix = hardstring.region_time_suffix()

    moments_type_list = {0: ['a', '20180805a'],
                         1: ['a', '20180813a_ce2'],
                         2: ['a', '20180816a' + region_time_suffix['_all_ne1a1ce1a1'][0]],
                         3: ['a', '20180816a' + region_time_suffix['_ce1a2'][0]],
                         4: ['a', '20180816a' + region_time_suffix['_ne1a2'][0]],
                         31: ['a', '20180816a' + region_time_suffix['_ce1'][0]],
                         32: ['a', '20180816a' + region_time_suffix['_ce2'][0]],
                         41: ['a', '20180816a' + region_time_suffix['_ne1'][0]],
                         42: ['a', '20180816a' + region_time_suffix['_ne2'][0]]}

    momsets_type_list = {0: ['a', '20180805a'],
                         1: ['a', '20180805b'],
                         2: ['a', '20180805d'],
                         3: ['a', '20180817a'],
                         4: ['a', '20180901a'],
                         5: ['a', '20180923a'],
                         6: ['a', '20180924a']}

    return moments_type_list, momsets_type_list


def estimate_set_gen(moment_key=0, momset_key=0):
    """Estimation Specifications
    
    Different pre-defined structures for estimation. 
    
    Why specify values in combo_list_c_esti as well if specify same here?
        - combo_list_c_esti is to provide default specifications.
        - more importantly, it is about what set of esti, model, ... parameters to use.

    esti_method : str
        'MomentsSimuStates'
    moments_type : str
        str for moments
    momsets_type : str
        str for momset to use
    esti_option_type : int
        scipy optimizer options like tol
    esti_func_type : str
        scipy otpimizer algorithm structure
    param_grid_or_rand : str
        'rand' or 'grid'
    esti_param_vec_count : int
        the
    graph_frequncy : int
        the
    bl_mpoly_approx : bool
        if true, look for mpoly approximation coefficients to evaluate model rather than
        to resolve model fully
    """

    moments_type_list, momsets_type_list = moments_and_momsets()
    moments_type = moments_type_list[moment_key]
    momsets_type = momsets_type_list[momset_key]

    esti_func_types = ['bfgs', 'Nelder-Mead', 'Powell',
                       'L-BFGS-B',
                       'TNC',
                       'SLSQP']

    nonespec = {'esti_method': None,
                'moments_type': None,
                'momsets_type': None,
                'esti_option_type': None,
                'esti_func_type': None,
                'param_grid_or_rand': None,
                'esti_param_vec_count': None,
                'graph_frequncy': None,
                'bl_mpoly_approx': False}

    kap_m0_nld_m = {'esti_method': 'MomentsSimuStates',
                    'moments_type': moments_type,
                    'momsets_type': momsets_type,
                    'esti_option_type': 1,
                    'esti_func_type': esti_func_types[3],
                    'param_grid_or_rand': 'rand',
                    'esti_param_vec_count': 1,
                    'esti_max_func_eval': 10,
                    'graph_frequncy': 20,
                    'bl_mpoly_approx': False}

    estimate_specifications = {'nonespec': nonespec,
                               'kap_m0_nld_m': kap_m0_nld_m}

    '''
    Generate Estimate Test
    '''
    spec_key_bases = ['esti_tinytst_thin', 'esti_tinytst_mpoly',
                      'esti_medtst_thin', 'esti_medtst_mpoly',
                      'esti_bigtst_thin', 'esti_bigtst_mpoly',
                      'esti_mplypostsimu', 'esti_mplypostesti',
                      'esti_test', 'esti_testfull', 'esti_main', 'esti_long', 'esti_mpoly',
                      'esti_thin', 'esti_tstthin']
    for spec_key_base in spec_key_bases:
        for it_esti_optsalgo in [0, 1, 2, 3, 4,
                                 10, 11, 12, 13, 14,
                                 20, 21, 22, 23, 24,
                                 30, 31, 32, 33, 34]:
            '''
            esti_param_vec_count: number of random draws between parameter mins and maxs
                if 10, and 3 estimation methods, that is 30 containers.
            esti_max_func_eval: number of solution iteration allowed for each estimation (per initial parameter value)
                see: soluequi/param_loop.py:166, esti_max_func_eval is not a parameter for the estimator, but
                set outside as a control parameter. Setting this below the estimation tolerance and iteration 
                requirements leads to error, which is caught. This is a way to force evaluation to stop after 1 
                iteration.
            '''
            esti_spec = {'esti_method': 'MomentsSimuStates',
                         'moments_type': moments_type,
                         'momsets_type': momsets_type,
                         'esti_option_type': 1,
                         'esti_func_type': esti_func_types[3],
                         'param_grid_or_rand': 'rand',
                         'esti_param_vec_count': 3,
                         'esti_max_func_eval': 18000,
                         'graph_frequncy': 90,
                         'bl_mpoly_approx': False}

            if (spec_key_base == 'esti_test'):
                pass

            if ('tinytst' in spec_key_base) or \
                    ('medtst' in spec_key_base) or \
                    ('bigtst' in spec_key_base):

                esti_spec['bl_mpoly_approx'] = False

                # estimation test with only 5 random starting points.
                if 'tinytst' in spec_key_base:
                    esti_spec['esti_param_vec_count'] = 5
                elif 'medtst' in spec_key_base:
                    esti_spec['esti_param_vec_count'] = 100
                elif 'bigtst' in spec_key_base:
                    esti_spec['esti_param_vec_count'] = 500

                if 'thin' in spec_key_base:
                    # esti_tinytst_thin
                    # esr first step, solve at random seeds once (all region/time periods)
                    esti_spec['esti_max_func_eval'] = 1
                elif 'mpoly' in spec_key_base:
                    # esti_tinytst_mpoly
                    # esr third setp, solve with polynomial surface
                    esti_spec['esti_max_func_eval'] = 18000
                    esti_spec['bl_mpoly_approx'] = True
                else:
                    raise NameError(f'tinytst esti with {spec_key_base=}, does not contain thin, mpoly or post')

            if 'mplypostsimu' in spec_key_base:
                esti_spec['bl_mpoly_approx'] = False
                esti_spec['esti_param_vec_count'] = 1
                esti_spec['esti_max_func_eval'] = 1

            if 'mplypostesti' in spec_key_base:
                esti_spec['bl_mpoly_approx'] = False
                esti_spec['esti_param_vec_count'] = 1
                esti_spec['esti_max_func_eval'] = 18000

            if (spec_key_base == 'esti_main'):
                esti_spec['esti_param_vec_count'] = 640
                esti_spec['esti_max_func_eval'] = 1000

            if (spec_key_base == 'esti_long'):
                # max of 10,000 evaluations, will be less than 10k due to some stopping earlier
                esti_spec['esti_param_vec_count'] = 50
                esti_spec['esti_max_func_eval'] = 200

            if (spec_key_base == 'esti_mpoly'):
                # 50,000 evaluations
                esti_spec['esti_param_vec_count'] = 6400
                esti_spec['esti_max_func_eval'] = 18000

            if (spec_key_base == 'esti_thin'):
                esti_spec['esti_param_vec_count'] = 6400
                #
                esti_spec['esti_max_func_eval'] = 18000

            if spec_key_base == 'esti_tstthin':
                esti_spec['esti_param_vec_count'] = 100
                esti_spec['esti_max_func_eval'] = 1

            it_esti_optsalgo_tens = int(np.floor(it_esti_optsalgo / 10))
            it_esti_optsalgo_digits = it_esti_optsalgo % 10

            if it_esti_optsalgo_tens == 0:
                # Nelder-Mead does not have bounds
                esti_spec['esti_func_type'] = esti_func_types[1]
            elif it_esti_optsalgo_tens == 1:
                esti_spec['esti_func_type'] = esti_func_types[3]
            elif it_esti_optsalgo_tens == 2:
                esti_spec['esti_func_type'] = esti_func_types[4]
            elif it_esti_optsalgo_tens == 3:
                esti_spec['esti_func_type'] = esti_func_types[5]
            else:
                raise ValueError(f'{it_esti_optsalgo_tens=} of {it_esti_optsalgo=} is not allowed')

            # see: estimation/estimate.py: 177, what esti_option_type correspond to
            if it_esti_optsalgo_digits == 0:
                esti_spec['esti_option_type'] = 0
            elif it_esti_optsalgo_digits == 1:
                esti_spec['esti_option_type'] = 1
            elif it_esti_optsalgo_digits == 2:
                esti_spec['esti_option_type'] = 2
            elif it_esti_optsalgo_digits == 3:
                esti_spec['esti_option_type'] = 3
            elif it_esti_optsalgo_digits == 4:
                esti_spec['esti_option_type'] = 4
            else:
                raise ValueError(f'{it_esti_optsalgo_tens=} of {it_esti_optsalgo=}  is not allowed')

            spec_key = spec_key_base + '_' + str(it_esti_optsalgo)
            estimate_specifications[spec_key] = esti_spec

    '''
    Generate key with same key name, _simu appended at the end,
    with only moments_type and momsets_type for simluation. So that
    simulaiton can use the same esti key as estimation to generate moment graphs.
    Can not include other keys, specifically, param_grid_or_rand, which would 
    change how grid values are drawn.
    
    For example, will generate kap_m0_nld_m_simu from kap_m0_nld_m, and the 
    kap_m0_nld_m_simu will only have *moments_type* and *momsets_type* two keys.
    '''
    esti_specs_for_simu = {}
    for key, esti_specs in estimate_specifications.items():
        new_dict = {}
        for k in ('moments_type', 'momsets_type'):
            if (k == 'moments_type'):
                moments_type = esti_specs[k]
                if (moments_type == None):
                    pass
                else:
                    # see: estimation/moments/moments_a.py: 120
                    # add _simu to moments_type to average over two periods moment outcome
                    # during simu exercise, does not distinguish between time periods.
                    new_dict[k] = [moments_type[0], moments_type[1] + '_simu']
            if (k == 'momsets_type'):
                new_dict[k] = esti_specs[k]

        esti_specs_for_simu[key + '_simu'] = new_dict

    estimate_specifications.update(esti_specs_for_simu)

    return estimate_specifications


def test_cases():
    estimate_specifications = estimate_set_gen()
    support_json.jdump(estimate_specifications, 'estimate_specifications', logger=logger.warning)


if __name__ == "__main__":
    test_cases()
