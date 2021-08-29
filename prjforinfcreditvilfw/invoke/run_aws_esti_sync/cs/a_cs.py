'''
Created on Aug 17, 2018

@author: fan

Central Estimation, focused on fitting Choice Probabilities
'''

import logging
from subprocess import call

import estimation.postprocess.process_main as esticomp
import invoke.run_estimate_aws_multi as svesti_sigle
import parameters.loop_combo_type_list.param_str as paramloopstr
import parameters.loop_combo_type_list.param_str_esti as paramstrnames
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def estimate_loop(run_type='sync',
                  run_size='',
                  list_all_key_2loop='list_all_params_1and2',
                  esti_spec_key_root='esti_test'):
    """Testing simulating, try over the vector of parameters
    
    when testing period specific parameters, only moments in the period
    associated with the period specific parameter will change. not the other period
    In another word, half of the graphs should stay flat in moments.
    """
    list_all = paramstrnames.param2str_groups_esti()
    for ctr, cur_param in enumerate(list_all[list_all_key_2loop]):
        if (ctr == 0):
            sync_ecs_init = True
        else:
            sync_ecs_init = False

        esti_glob_summ(paramstr_key_list=[cur_param],
                       run_size=run_size,
                       esti_spec_key_root=esti_spec_key_root,
                       run_type=run_type,
                       sync_ecs_init=sync_ecs_init)


def esti_glob_summ(paramstr_key_list=None,
                   run_size='x',
                   esti_spec_key_root='esti_test',
                   run_type='sync',
                   sync_ecs_init=True):
    """  
    1. go to moments_a:
        update moments data
        - '20180816a_cs_1and2'
    2. got o momsets_a:
        update which moments are to be matched
        acutually, I am currently already matching based on prob each of seven. 
        Just that for display, showing 4 charts to save space I suppose.
        - '20180817a'
    """

    logger.critical('Starting esti_glob_summ, run_type:%s', run_type)

    esti_save_directory_main = 'esti'
    simu_save_directory_main = 'simu'

    simu_combo_type_list_ab = 'b'
    esti_combo_type_list_ab = 'c'
    simu_combo_type_list_date = '20180814'
    esti_combo_type_list_date = '20180815'

    integrated = False

    #     paramstr_key_list = 'list_all_params_1and2'
    if (paramstr_key_list is None):
        paramstr_key_list = ['beta']

    moment_key = 2
    momset_key = 3
    esti_invoke_set = 1  # low memory 1 cpu
    simu_invoke_set = 2  # high memory
    simulate_grid = True
    combine_results = False

    '''
    B. Integrated or not
    '''
    if (integrated):
        ITG = '_ITG'
    else:
        ITG = ''

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

    if run_type == 'esti':
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

    elif run_type == 'sync':

        aws_sync_command = 'aws s3 sync'

        '''
        Directories specific to the current estimation run. 
        '''
        esti_sub_direct = esti_save_directory_main + '/' + esti_combo_type_list_ab + '_' \
                          + esti_combo_type_list_date + run_size + ITG + folder_param_name
        s3_subdirect_esti = '\"' + s3_directory_main + '/' + esti_sub_direct + '\"'
        local_sync_subdirect_esti = '\"' + local_sync_directory_main + '/' + esti_sub_direct + '\"'

        simu_sub_direct = simu_save_directory_main + '/' + simu_combo_type_list_ab + '_' \
                          + simu_combo_type_list_date + run_size + ITG + folder_param_name
        s3_subdirect_simu = '\"' + s3_directory_main + '/' + simu_sub_direct + '\"'
        local_sync_subdirect_simu = '\"' + local_sync_directory_main + '/' + simu_sub_direct + '\"'

        '''
        File Sync Type
        '''
        sync_csv = '--exclude \"*\" --include \"*.csv\"'
        sync_png = '--exclude \"*\" --include \"*.png\"'

        '''
        Join Sync Commands
        '''
        esti_command_line_list = [aws_sync_command, s3_subdirect_esti, local_sync_subdirect_esti, sync_csv]
        simu_command_line_list = [aws_sync_command, s3_subdirect_simu, local_sync_subdirect_simu, sync_png]

        s3_sync_esti = " ".join(esti_command_line_list)
        s3_sync_simu = " ".join(simu_command_line_list)

        logger.critical('sync, s3_sync_esti:\n%s', s3_sync_esti)
        call(s3_sync_esti)

        logger.critical('sync, s3_sync_simu:\n%s', s3_sync_simu)
        call(s3_sync_simu)

        esti_glob_summ(paramstr_key_list=paramstr_key_list,
                       run_size=run_size,
                       esti_spec_key_root=esti_spec_key_root,
                       run_type='summ',
                       sync_ecs_init=sync_ecs_init)

    elif (run_type == 'summ'):

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

        esticomp.search_combine_indi_esti(
            paramstr_key_list,
            combo_type_list_ab,
            combo_type_list_date, esti_spec_key,
            moment_key=moment_key, momset_key=momset_key,
            exo_or_endo_graph_row_select='_exo_wgtJ',
            image_save_name_prefix='AGG_ALLESTI_',
            search_directory=search_directory,
            fils_search_str=None,
            save_file_name=None,
            save_panda_all=False,
            graph_list=None,
            top_estimates_keep_count=4)


def test_cases():
    '''
    1. Quick Test Run, individual Parameters
        simulate each dimentions of list_all_params_1and2
        estimate one parameter one by one
    '''

    '''
    Main Run
    '''
    esti_glob_summ(
        paramstr_key_list=['list_all_params_1and2'],
        run_size='',
        esti_spec_key_root='esti_main',
        run_type='sync',
        sync_ecs_init=True)


if __name__ == "__main__":
    test_cases()
