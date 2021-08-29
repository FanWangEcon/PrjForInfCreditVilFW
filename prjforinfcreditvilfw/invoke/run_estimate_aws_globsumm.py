'''
Created on Aug 30, 2018

@author: fan
'''

import logging

import boto3aws.aws_s3.sync_s3 as sync_s3
import estimation.postprocess.process_main as esticomp
import invoke.run_estimate_aws_multi as svesti_sigle
import parameters.loop_combo_type_list.param_str as paramloopstr
import projectsupport.graph.graph_sets as sup_graphset
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def esti_glob_summ(paramstr_key_list=None,
                   run_size='x',
                   esti_spec_key_root='esti_test',
                   run_type='sync',
                   sync_ecs_init=True,
                   **kwargs):
    """
    1. go to moments_a:
        update moments data
        - '20180816a_cs_1and2'
    2. got o momsets_a:
        update which moments are to be matched
        acutually, I am currently already matching based on prob each of seven.
        Just that for display, showing 4 charts to save space I suppose.
        - '20180817a'

    Parameters
    ----------
    run_type: string
        if run_type == 'glob': aggregate files together, save all df, replace
        if run_type == 'summ': use existing aggregate file, generate top, summarize, latex, jinja update
        if run_type == 'graph': use existing aggregate file, generate graphs, could take a while here
    
    Examples
    --------
    import invoke.run_aws_esti_sync.aws_estimate_manager as estimanage
    estimanage.esti_glob_summ(paramstr_key_list = paramstr_key_list,
                               run_size = 'x',
                               esti_spec_key_root = 'esti_test',
                               run_type='sync',
                               sync_ecs_init = True, 
                               **kwargs)
    """

    logger.critical('Starting esti_glob_summ, run_type:%s', run_type)

    moment_key = kwargs.get('moment_key', 2)
    momset_key = kwargs.get('momset_key', 3)
    esti_save_directory_main = kwargs.get('esti_save_directory_main', None)  # 'esti'
    simu_save_directory_main = kwargs.get('simu_save_directory_main', None)  # 'simu'
    simu_combo_type_list_ab = kwargs.get('simu_combo_type_list_ab', 'b')
    esti_combo_type_list_ab = kwargs.get('esti_combo_type_list_ab', 'c')
    simu_combo_type_list_date = kwargs.get('simu_combo_type_list_date', '20180814')
    esti_combo_type_list_date = kwargs.get('esti_combo_type_list_date', '20180815')
    integrated = kwargs.get('integrated', False)
    esti_invoke_set = kwargs.get('esti_invoke_set', 1)
    simu_invoke_set = kwargs.get('simu_invoke_set', 2)

    exo_or_endo_graph_row_select = kwargs.get('exo_or_endo_graph_row_select', '_exo_wgtJ')

    #     paramstr_key_list = 'list_all_params_1and2'
    if (paramstr_key_list is None):
        paramstr_key_list = ['beta']

    simulate_grid = True
    combine_results = False

    '''
    B. Integrated or not
    '''
    if (integrated):
        '''possible that integrated is false, but this is becuase
        do not want to have _ITG_ITG. because already added _ITG
        '''
        ITG = '_ITG'
    else:
        ITG = ''

    #     aws_type = 'fargate'
    #     job_queue = None

    aws_type = 'batch'
    job_queue = 'Spot'

    paramstr_dict = paramloopstr.param2str()
    if ('list_' in str(paramstr_key_list)):
        folder_param_name = '_' + paramstr_key_list[0]
    else:
        folder_param_name = paramstr_dict[paramstr_key_list[0]][0]

    '''
    Main Directories
    '''
    d_root = proj_sys_sup.s3_local_sync_folder()
    bucket_name = proj_sys_sup.s3_bucket_name()
    s3_directory_main = 's3://' + bucket_name
    local_sync_directory_main = '' + d_root + bucket_name

    if (run_type == 'esti'):
        svesti_sigle.multistart_esti(
            paramstr_key_list=paramstr_key_list,
            run_size=run_size,
            esti_spec_key_root=esti_spec_key_root,
            moment_key=moment_key,
            momset_key=momset_key,
            esti_invoke_set=esti_invoke_set,
            simu_invoke_set=simu_invoke_set,
            simu_combo_type_list_ab=simu_combo_type_list_ab,
            esti_combo_type_list_ab=esti_combo_type_list_ab,
            simu_combo_type_list_date=simu_combo_type_list_date,
            esti_combo_type_list_date=esti_combo_type_list_date,
            integrated=integrated,
            sync_ecs_init=sync_ecs_init,
            simulate_grid=simulate_grid,
            combine_results=combine_results,
            aws_type=aws_type,
            job_queue=job_queue,
            simu_save_directory_main=simu_save_directory_main,
            esti_save_directory_main=esti_save_directory_main)

    elif (run_type == 'sync'):

        aws_sync_command = 'aws s3 sync'

        '''
        Directories specific to the current estimation run. p
            - either esti or simu
        '''

        if (simu_save_directory_main is not None):
            ITG = ''
            sync_s3.sync_s3(simu_save_directory_main,
                            simu_combo_type_list_ab, simu_combo_type_list_date,
                            run_size, ITG, folder_param_name,
                            s3_directory_main, local_sync_directory_main,
                            esti_or_simu='simu')

        if (esti_save_directory_main is not None):
            sync_s3.sync_s3(esti_save_directory_main,
                            esti_combo_type_list_ab, esti_combo_type_list_date,
                            run_size, ITG, folder_param_name,
                            s3_directory_main, local_sync_directory_main,
                            esti_or_simu='esti')

    elif (run_type == 'glob' or
          run_type == 'gentopsumm' or
          run_type == 'summ' or
          run_type == 'graph'):

        combo_type_list_ab = esti_combo_type_list_ab
        combo_type_list_date = esti_combo_type_list_date + run_size + ITG
        esti_spec_key = esti_spec_key_root + '_11'
        search_directory_main = local_sync_directory_main + '/' + esti_save_directory_main + '/'
        search_directory = search_directory_main + combo_type_list_ab + \
                           '_' + combo_type_list_date \
                           + folder_param_name + '/'

        logger.critical('summ, combo_type_list_ab:\n%s', combo_type_list_ab)
        logger.critical('summ, combo_type_list_date:\n%s', combo_type_list_date)
        logger.critical('summ, esti_spec_key:\n%s', esti_spec_key)
        logger.critical('summ, search_directory_main:\n%s', search_directory_main)
        logger.critical('summ, search_directory:\n%s', search_directory)

        if (run_type == 'glob'):
            '''
            Save new panda_all and panda_top
            '''
            save_panda_all = True
            return_current_panda_all = False
            save_panda_top = True
            return_panda_top = False
            graph_list = None

        if (run_type == 'gentopsumm'):
            '''
            Generates new panda top based on existing panda_all, does not graph
            '''
            save_panda_all = False
            return_current_panda_all = True  # Assume file already generated, return it
            save_panda_top = True
            return_panda_top = False  # if this is true, if file found will return existing
            graph_list = None
        #             graph_list = sup_graphset.graph_panda_sets_names(graph_panda_list_name='min_graphs')

        if (run_type == 'summ'):
            '''
            Use existing panda top generate summ results
            '''
            save_panda_all = False
            return_current_panda_all = False
            save_panda_top = False
            return_panda_top = True
            graph_list = None

        if (run_type == 'graph'):
            '''
            Graph using existing panda all: even if panda_all does not exist, still works, will create one
            but will not save it.
            '''
            save_panda_all = False
            return_current_panda_all = True
            save_panda_top = False
            return_panda_top = True
            graph_list = sup_graphset.graph_panda_sets_names(graph_panda_list_name='min_graphs')

        esticomp.search_combine_indi_esti(
            paramstr_key_list,
            combo_type_list_ab,
            combo_type_list_date, esti_spec_key,
            image_save_name_prefix='AGG_ALLESTI_',
            search_directory=search_directory,
            fils_search_str=None,
            save_file_name=None,
            save_panda_all=save_panda_all,
            return_current_panda_all=return_current_panda_all,
            save_panda_top=save_panda_top,
            return_panda_top=return_panda_top,
            graph_list=graph_list,
            **kwargs)


if __name__ == "__main__":
    region_time_suffix = hardstring.region_time_suffix()
    esti_setting_dict = {}
    esti_setting_dict['esti_combo_type_list_ab'] = 'c'
    esti_setting_dict['esti_combo_type_list_date'] = '20180901'
    esti_setting_dict['integrated'] = False

    esti_setting_dict['momset_key'] = 4
    esti_setting_dict['moment_key'] = 3
    paramstr_key_list = ['list_tKap' + region_time_suffix['_ce1a2'][0]]

    esti_glob_summ(paramstr_key_list=paramstr_key_list,
                   run_size='',
                   esti_spec_key_root='esti_testfull',
                   run_type='summ',
                   sync_ecs_init=False,
                   **esti_setting_dict)
