'''
Created on Aug 30, 2018

@author: fan
'''

import subprocess as sp
from math import isnan

import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup


def csv_to_dict(df_row):
    """    
    Examples
    --------
    import estimation.postprocess.texdo_gen_distribute as esti_texdo_gendist
    esti_texdo_gendist.csv_to_dict(df_row)
    """
    row_dict = df_row.to_dict()
    row_dict_nonan = {}
    for key, val in row_dict.items():
        if (key == 'btp_il_opti_grid_allJ_agg+btp_ib_opti_grid_allJ_agg'):
            pass
        if (isinstance(val, str)):
            # Keep strings
            row_dict_nonan[key] = val
        else:
            if (isnan(val)):
                pass
            else:
                row_dict_nonan[key] = val

    return row_dict_nonan


def save_to_tex_do(save_directory, save_name, DATA_PARAM_DICT,
                   save_agg_tex=True, update_compile_folder=True,
                   format_str=proj_sys_sup.decimals(type='prob'), gen_graph_stata=True):
    """dictionary key and value generate do globals and tex newcommands with same key and values
    
    push file to various locations:
    - git _draft folder for compile
        + preamble for tex
        + stata folder for do
    - dropbox draft folder
    - EC2 estimation folder
        + region specific folders with region specific results
        + aggregate folder with aggregate results
        
    Key functionality below is that append if one region, create new file if 
    another, this way, puts two files on top of each other. 
    
    Examples
    --------
    import estimation.postprocess.texdo_gen_distribute as esti_texdo_gendist
    save_to_tex_do(save_directory, save_name, DATA_PARAM_DICT, save_agg_tex = True, update_compile_folder = True)
    """

    tex_do_list = ['tex', 'do']
    for tex_do in tex_do_list:

        if (tex_do == 'tex'):
            tex_do_suffix = '.tex'
            folder_aggregate_simu = '_paper.preamble.group_d_data'
        elif (tex_do == 'do'):
            tex_do_suffix = '.do'
            folder_aggregate_simu = 'stata.estisimu_data'
        else:
            pass

        '''
        A. Save to simulation folder, Probability files
        '''
        tex_save_directory_name_main = save_directory + save_name + tex_do_suffix
        textfile = open(tex_save_directory_name_main, 'w')
        comment_str = tex_do_comment(tex_do, save_directory)
        textfile.write(comment_str)
        for key, val in DATA_PARAM_DICT.items():
            cur_line = tex_do_line(tex_do, key, format_str, val)
            textfile.write(cur_line)
        textfile.flush()

        if (save_agg_tex):
            '''
            B1. Aggregate Folder+File Name
            '''
            non_region_specific_esti_directory, append_or_add, last_folder, \
            last_folder_non_region_specific \
                = hardstring.get_generic_folder(save_directory=save_directory, same_root=True)
            tex_save_directory_name_combine = non_region_specific_esti_directory + save_name + tex_do_suffix

            '''
            B2. combine north east and central result into one folder, one file
            Save to simulation folder (without region suffix) so both regions together
            '''
            textfile = open(tex_save_directory_name_combine, append_or_add)
            textfile.write(comment_str)
            for key, val in DATA_PARAM_DICT.items():
                cur_line = tex_do_line(tex_do, key, format_str, val)
                textfile.write(cur_line)
            textfile.flush()
            next_folder_file = tex_save_directory_name_combine

            '''
            C. Results D file moving to paper folder where tex/do files used for compilation can be stored with dates.
            '''
            sub_folder_name = last_folder_non_region_specific
            next_folder_file_imgtab = proj_sys_sup.get_paths('paper.imgtab',
                                                             sub_folder_name=sub_folder_name) + save_name + tex_do_suffix
            proj_sys_sup.copy_rename(tex_save_directory_name_combine, next_folder_file_imgtab)

            if (update_compile_folder):
                '''
                D. Results C file moving to _paper folder where tex can be compiled.
                '''
                next_folder_file = proj_sys_sup.get_paths_in_git(folder_aggregate_simu) + save_name + tex_do_suffix
                proj_sys_sup.copy_rename(tex_save_directory_name_combine, next_folder_file)

                if ((tex_do == 'do') and gen_graph_stata and (save_name == 'DATASIMUPROBJ') and (
                        append_or_add == 'a')):
                    stata_estifitprobj_data = proj_sys_sup.get_paths_in_git('stata.graph.esti_fit_prob_j.do')
                    stata_exe_directory = proj_sys_sup.local_stata_exe_directory()
                    command_str = '"' + stata_exe_directory + '" -e do "' + stata_estifitprobj_data + '" ' + save_name
                    process = sp.Popen(command_str, shell=True)
                    process.wait()

                    cur_img_pdf = save_name + '.pdf'
                    stata_estisimu_data = proj_sys_sup.get_paths_in_git('stata.estisimu_data')
                    cur_img_pdf_file_directory = stata_estisimu_data + cur_img_pdf

                    nxt_esti_file_directory = non_region_specific_esti_directory + cur_img_pdf
                    proj_sys_sup.copy_rename(cur_img_pdf_file_directory, nxt_esti_file_directory)

                    nxt_img_pdf_file_directory = next_folder_file_imgtab + cur_img_pdf
                    proj_sys_sup.copy_rename(cur_img_pdf_file_directory, nxt_img_pdf_file_directory)


def tex_do_comment(tex_do, commentline):
    if (tex_do == 'tex'):
        comment_str = '%' + commentline + '\n'
    if (tex_do == 'do'):
        comment_str = '//-- ' + commentline + '\n'
    return comment_str


def tex_do_line(tex_do, key, format_str, val):
    if (isinstance(val, str)):
        format_val = val
    else:
        format_val = format_str.format(val)

    if (tex_do == 'tex'):
        cur_line = '\\newcommand{\\' + key + '}{' + format_val + '}\n'
    if (tex_do == 'do'):
        cur_line = 'global ' + key + ' = \"' + format_val + '\"\n'
    return cur_line
