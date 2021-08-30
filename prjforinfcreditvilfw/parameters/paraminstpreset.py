'''
Created on Jan 1, 2018

@author: fan
'''

import logging

import parameters.data.a_data as param_data_a
import parameters.data.b_data as param_data_b
import parameters.dist.a_dist as param_dist_a
import parameters.esti.a_esti as param_esti_a
import parameters.grid.a_grid as param_grid_a
import parameters.interpolant.a_interpolant as interpolant_a
import parameters.model.a_model as param_model_a
import parameters.paraminst as paraminst
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def get_param_inst_preset_combo(param_combo=None):
    """
    
    Examples
    --------
    import parameters.paraminstpreset as param_inst_preset
    param_inst = param_inst_preset.get_param_inst_preset_combo(param_combo)
    
    """
    proj_sys_sup.jdump(param_combo, 'param_combo', logger=logger.info)

    if (param_combo is None):
        return get_param_inst_preset()
    else:

        if ('param_update_dict' in param_combo):
            param_update_dict = param_combo['param_update_dict']
        else:
            param_update_dict = None

        if ('title' in param_combo):
            title = param_combo['title']
        else:
            title = 'Default'

        if ('combo_desc' in param_combo):
            combo_desc = param_combo['combo_desc']
        else:
            combo_desc = 'Default'

        if ('file_save_suffix' in param_combo):
            file_save_suffix = param_combo['file_save_suffix']
        else:
            file_save_suffix = ''

        return get_param_inst_preset(
            param_update_dict=param_update_dict,
            title=title,
            combo_desc=combo_desc,
            file_save_suffix=file_save_suffix)


def get_param_inst_preset(param_update_dict=None,
                          title='Default',
                          combo_desc='Default',
                          file_save_suffix=''):
    """    
    same as get_param_inst, except the input parameters here
    are not dictionaries with parameters to update, but preset subtypes from 
    various modules
    
    Parameters
    ----------    
        grid_type: list
            ['a', 1]
        esti_type:
            ['a', 1]
        param_inst_name: string
            some description for the particular combination of parameters    
    """

    # Default Values
    dict_name = []

    grid_param_update = {}
    data_param_update = {}
    esti_param_update = {}
    model_option_update = {}
    interpolant_update = {}
    dist_param_update = {}
    support_arg_update = {}

    if (param_update_dict is not None):
        proj_sys_sup.jdump(param_update_dict, 'param_update_dict', logger=logger.info)

        if ('grid_type' in param_update_dict):
            grid_type = param_update_dict['grid_type']
            if (grid_type[0] == 'a'):
                grid_param_update, grid_subtitle = param_grid_a.param(grid_type)
            if (len(grid_type) >= 3):
                for param_key, key_val in grid_type[2].items():
                    grid_param_update[param_key] = key_val
            dict_name.append('g:' + grid_subtitle)

        if ('esti_type' in param_update_dict):
            esti_type = param_update_dict['esti_type']
            if (esti_type[0] == 'a'):
                esti_param_update, esti_subtitle = param_esti_a.param(esti_type)
            if (len(esti_type) >= 3):
                for param_key, key_val in esti_type[2].items():
                    esti_param_update[param_key] = key_val
            dict_name.append('e:' + esti_subtitle)

        if ('data_type' in param_update_dict):
            data_type = param_update_dict['data_type']
            if (data_type[0] == 'a'):
                data_param_update, data_subtitle = param_data_a.param(data_type)
            if (data_type[0] == 'b'):
                data_param_update, data_subtitle = param_data_b.param(data_type)
            if (len(data_type) >= 3):
                for param_key, key_val in data_type[2].items():
                    data_param_update[param_key] = key_val
            dict_name.append('e:' + data_subtitle)

        if ('model_type' in param_update_dict):
            model_type = param_update_dict['model_type']
            if (model_type[0] == 'a'):
                model_option_update, model_subtitle = param_model_a.param(model_type)
            if (len(model_type) >= 3):
                for param_key, key_val in model_type[2].items():
                    model_option_update[param_key] = key_val
            dict_name.append('e:' + model_subtitle)

        if ('interpolant_type' in param_update_dict):
            interpolant_type = param_update_dict['interpolant_type']
            if (interpolant_type[0] == 'a'):
                interpolant_update, interpolant_subtitle = interpolant_a.param(interpolant_type)
            if (len(interpolant_type) >= 3):
                for param_key, key_val in interpolant_type[2].items():
                    interpolant_update[param_key] = key_val
            dict_name.append('i:' + interpolant_subtitle)

        if ('dist_type' in param_update_dict):
            dist_type = param_update_dict['dist_type']
            if dist_type is not None:
                if (dist_type[0] == 'a'):
                    dist_param_update, dist_subtitle = param_dist_a.param(dist_type)
                if (len(dist_type) >= 3):
                    for param_key, key_val in dist_type[2].items():
                        param_key_list = param_key.split('.')
                        if (len(param_key_list) == 1):
                            dist_param_update[param_key] = key_val
                        elif (len(param_key_list) == 2):
                            dist_param_update[param_key_list[0]][param_key_list[1]] = key_val
                        elif (len(param_key_list) == 3):
                            dist_param_update[param_key_list[0]][param_key_list[1]][param_key_list[2]] = key_val
                        else:
                            raise ('len(param_key_list) too long')

        if ('support_arg' in param_update_dict):
            support_arg_update = param_update_dict['support_arg']
            support_arg_update['time_start'] = proj_sys_sup.save_suffix_time(3)

    if (dict_name == []):
        dict_name = 'default'
    else:
        dict_name = ", ".join(dict_name)

    param_inst = paraminst.get_param_inst(
        title=title + ' (' + dict_name + ')',
        combo_desc=combo_desc,
        file_save_suffix=file_save_suffix,
        grid_param_update=grid_param_update,
        data_param_update=data_param_update,
        esti_param_update=esti_param_update,
        model_option_update=model_option_update,
        interpolant_update=interpolant_update,
        dist_param_update=dist_param_update,
        support_arg_update=support_arg_update,
        return_object=True)

    return param_inst
