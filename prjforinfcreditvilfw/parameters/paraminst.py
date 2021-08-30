'''

@author: fan
'''

import logging
import pyfan.devel.obj.classobjsupport as Clsobj_Sup

import dataandgrid.choices.fixed.tics as tics
import parameters.default as default
import parameters.dist.a_dist as param_dist_a
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def get_param_inst(
        title='default',
        combo_desc='default',
        file_save_suffix='',
        grid_param_update={},
        data_param_update={},
        esti_param_update={},
        model_option_update={},
        interpolant_update={},
        dist_param_update={},
        support_arg_update={},
        return_object=True):
    """Generate parameters needed to invoke function
    
    Function uses defaults unless things are otherwise specified
    The parameters allow for changing any particular parameter one by one    
    """

    grid_param, data_param, esti_param, \
    model_option, interpolant, dist_param, support_arg = \
        default.get_all_param_default()

    '''
    Update Parameters
    '''
    grid_param.update(grid_param_update)
    data_param.update(data_param_update)
    esti_param.update(esti_param_update)
    model_option.update(model_option_update)
    interpolant.update(interpolant_update)
    dist_param.update(dist_param_update)
    support_arg.update(support_arg_update)

    '''
    Some parameters that have to be internally consistent
    '''
    K_choice_discretePoints, B_choice_discretePoints = tics.gentics_KB_count(grid_param['len_choices'])
    grid_param['len_choices_k'] = K_choice_discretePoints
    grid_param['len_choices_b'] = B_choice_discretePoints

    '''
    Distribution Checking
    '''
    if (dist_param != {}):
        if ('epsA_frac_A' in dist_param):
            # see: https://www.evernote.com/shard/s10/nl/1203171/ce0cbc17-1f49-4046-a865-63429f2cc691
            return_dict = param_dist_a.gen_mu_sigma(sigma=dist_param['epsA_std'],
                                                    F=dist_param['epsA_frac_A'])

            grid_param['std_eps'] = return_dict['sigma_epsilon']
            grid_param['mean_eps'] = return_dict['mu_epsilon']

            grid_param['std_eps_E'] = return_dict['sigma_epsilon']
            grid_param['mean_eps_E'] = return_dict['mu_epsilon']

            dist_param['data__A']['params']['sd'] = return_dict['sigma_A']
            dist_param['data__A']['params']['mu'] = return_dict['mu_A']

        dist_param_integrate_points = param_dist_a.gen_dist_param_integrate_points(dist_param)
        dist_param['dist_param_integrate_points'] = dist_param_integrate_points

    '''
    Combine
    '''
    param_dict = {'grid_param': grid_param,
                  'data_param': data_param,
                  'esti_param': esti_param,
                  'model_option': model_option,
                  'interpolant': interpolant,
                  'dist_param': dist_param,
                  'support_arg': support_arg,
                  'title': title,
                  'combo_desc': combo_desc,
                  'file_save_suffix': file_save_suffix}

    proj_sys_sup.jdump(param_dict, 'param_dict', logger=logger.info)

    if (return_object):
        attribute_array = []
        attribute_values_array = []
        for param_key, param_value in param_dict.items():
            attribute_array.append(param_key)
            attribute_values_array.append(param_value)
            param_inst = Clsobj_Sup.dynamic_obj_attr(attribute_array, attribute_values_array)
        return param_inst
    else:
        return param_dict
