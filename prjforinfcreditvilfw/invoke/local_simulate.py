'''
Created on Jun 7, 2018

@author: fan

import invoke.local_simulate as invoke_simu
'''

import logging

import boto3aws.run_aws as runfargate
import invoke.combo_type_list_wth_specs as paramcombospecs
import invoke.run_simulate as runsimu
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.graph.graph_sets as sup_graphset

logger = logging.getLogger(__name__)


def manage_local_farge_kwargs(**kwargs):
    invoke = kwargs.get('invoke', 'local')
    sync_ecs = kwargs.get('sync_ecs', False)
    combo_type_list_ab = kwargs.get('combo_type_list_ab', 'b')
    combo_type_list_date = kwargs.get('combo_type_list_date', '20180814x')
    invoke_set = kwargs.get('invoke_set', 2)
    esti_spec_key_for_simu = kwargs.get('esti_spec_key_for_simu', 'kap_m0_nld_m_simu')
    save_directory_main = kwargs.get('save_directory_main', 'simu')
    moment_key = kwargs.get('moment_key', 2)
    momset_key = kwargs.get('momset_key', 3)
    graph_panda_list_name = kwargs.get('graph_panda_list_name', None)
    paramstr_key_list = kwargs.get('paramstr_key_list', ['beta'])

    manage_local_farge(invoke=invoke,
                       sync_ecs=sync_ecs,
                       combo_type_list_ab=combo_type_list_ab,
                       combo_type_list_date=combo_type_list_date,
                       invoke_set=invoke_set,
                       esti_spec_key_for_simu=esti_spec_key_for_simu,
                       save_directory_main=save_directory_main,
                       moment_key=moment_key,
                       momset_key=momset_key,
                       graph_panda_list_name=graph_panda_list_name,
                       paramstr_key_list=paramstr_key_list)


def manage_local_farge(invoke='local',
                       sync_ecs=False,
                       combo_type_list_ab='b',
                       combo_type_list_date='20180814x',
                       invoke_set=2,
                       esti_spec_key_for_simu='kap_m0_nld_m_simu',
                       save_directory_main='simu',
                       moment_key=2,
                       momset_key=3,
                       graph_panda_list_name=None,
                       paramstr_key_list=['beta']):
    if (invoke == 'local'):
        '''
        B. Local
        '''
        run_here(invoke_set,
                 esti_spec_key_for_simu=esti_spec_key_for_simu,
                 combo_type_list_ab=combo_type_list_ab,
                 combo_type_list_date=combo_type_list_date,
                 paramstr_key_list=paramstr_key_list,
                 moment_key=moment_key, momset_key=momset_key,
                 graph_panda_list_name=graph_panda_list_name,
                 save_directory_main=save_directory_main)

    else:
        '''
        B. Fargate
        '''
        if (invoke == 'fargate'):
            aws_type = 'fargate'
            job_queue = None
        elif (invoke == 'Spot'):
            aws_type = 'batch'
            job_queue = 'Spot'
        elif (invoke == 'OnDemand'):
            aws_type = 'batch'
            job_queue = 'OnDemand'
        else:
            raise ('error')

        '''
        A. Fargate
        '''
        invoke_list_fargate = [invoke_set]
        run_here_manage_fargate(invoke_list_fargate, sync_ecs,
                                esti_spec_key_for_simu=esti_spec_key_for_simu,
                                combo_type_list_ab=combo_type_list_ab,
                                combo_type_list_date=combo_type_list_date,
                                paramstr_key_list=paramstr_key_list,
                                moment_key=moment_key, momset_key=momset_key,
                                save_directory_main=save_directory_main,
                                aws_type=aws_type, job_queue=job_queue)


def run_here_manage_fargate(invoke_set_loop=[101, 102], sync_ecs=True,
                            esti_spec_key_for_simu=None,
                            combo_type_list_ab='a', combo_type_list_date='20180607',
                            paramstr_key_list=None,
                            moment_key=0, momset_key=1,
                            graph_panda_list_name=None,
                            save_directory_main='simu',
                            aws_type='fargate', job_queue=None):
    """
    This is relevant only for Fargate basically
    """
    fargate = True
    for ctr, run_cur in enumerate(invoke_set_loop):

        if (sync_ecs):
            ec2_start = True
            run_docker = True
        else:
            ec2_start = False
            run_docker = False

        #         ec2_start=False
        #         run_docker=False

        run_here(run_cur,
                 esti_spec_key_for_simu,
                 combo_type_list_ab, combo_type_list_date,
                 paramstr_key_list,
                 moment_key, momset_key,
                 graph_panda_list_name=graph_panda_list_name,
                 save_directory_main=save_directory_main,
                 aws_type=aws_type, job_queue=job_queue,
                 fargate=fargate,
                 ec2_start=ec2_start,
                 run_docker=run_docker)


def run_here(invoke_set,
             esti_spec_key_for_simu=None,
             combo_type_list_ab='a', combo_type_list_date='20180607',
             paramstr_key_list=None,
             moment_key=0, momset_key=1,
             graph_panda_list_name=None,
             save_directory_main='simu',
             aws_type='fargate', job_queue=None,
             fargate=False, ec2_start=False, run_docker=False,
             logging_level=logging.DEBUG,
             log_file=False,
             log_file_suffix=''):
    """

    Examples
    --------
    import invoke.run_local as runlocal
    runlocal.run_here(invoke_set,
             combo_type_list_ab='a', combo_type_list_date = '20180607',
             paramstr_key_list=None,
             graph_list=None, fargate=False, ec2_start=False, run_docker=False)
    """
    speckey, vcpus, cpu, memory, combo_type_list = \
        paramcombospecs.gen_combo_type_list(invoke_set, fargate, paramstr_key_list,
                                            combo_type_list_ab, combo_type_list_date)

    if (graph_panda_list_name is None):
        graph_panda_list_name = 'main_aAcsv_graphs'
        # graph_panda_list_name = 'min_graphs'
    graph_list = sup_graphset.graph_panda_sets_names(graph_panda_list_name)

    define_here = False
    if (define_here):
        # Local non parrallel no ge simple run, similar to invoke_set == 1
        aws_fargate = False
        ge = False
        multiprocess = False
    else:
        cur_spec = computespec.compute_set(speckey, fargate=fargate)
        print('cur_spec:', cur_spec)
        aws_fargate = cur_spec['aws_fargate']
        ge = cur_spec['ge']
        multiprocess = cur_spec['multiprocess']

    for ctr, combo_type in enumerate(combo_type_list):

        print(combo_type)
        if (aws_fargate):

            if (ctr == 0):
                "Only first ctr==0 in invokek_setFals_loop should start ec2 and run docker"
                pass
            else:
                ec2_start = False
                run_docker = False

            if (esti_spec_key_for_simu is None):
                # speckey has key, compesti_spec is None, simulate
                pass
            else:
                speckey_use = estispec.compute_esti_spec_combine(
                    compute_spec_key=speckey,
                    esti_spec_key=esti_spec_key_for_simu,
                    moment_key=moment_key, momset_key=momset_key,
                    action='combine')

            runfargate.invoke_aws_ecs(combo_type,
                                      aws_type=aws_type,
                                      job_queue=job_queue,
                                      speckey=speckey_use,
                                      vcpus=vcpus, cpu=cpu, memory=memory,
                                      ge=ge,
                                      multiprocess=multiprocess,
                                      estimate=False,
                                      graph_panda_list_name=graph_panda_list_name,
                                      save_directory_main=save_directory_main,
                                      ec2_start=ec2_start, run_docker=run_docker)

        else:

            if (esti_spec_key_for_simu is None):
                # speckey has key, compesti_spec is None, simulate
                compesti_specs = None
            else:
                # this is simulate or estimate, both can specify comp+esti keys
                cur_compute_spec = computespec.compute_set(speckey)
                cur_esti_spec = estispec.estimate_set(esti_spec_key_for_simu,
                                                      moment_key=moment_key,
                                                      momset_key=momset_key)
                compesti_specs = cur_compute_spec.copy()
                compesti_specs.update(cur_esti_spec)

            runsimu.invoke_soluequi_partial(combo_type=combo_type,
                                            speckey=speckey,
                                            compesti_specs=compesti_specs,
                                            ge=ge, multiprocess=multiprocess,
                                            graph_list=graph_list,
                                            save_directory_main=save_directory_main,
                                            logging_level=logging_level,
                                            log_file=log_file,
                                            log_file_suffix=log_file_suffix)


if __name__ == "__main__":
    invoke = 'local'

    sync_ecs = False

    combo_type_list_ab = 'b'

    combo_type_list_date = '20180829x_ITG'
    combo_type_list_date = '20180814_beta'
    invoke_set = 1  # 56 invoke, parallel

    #     esti_spec_key_for_simu = None
    esti_spec_key_for_simu = 'kap_m0_nld_m_simu'
    #     esti_spec_key_for_simu = 'esti_test_11_simu'
    save_directory_main = 'simu'

    # moment_key = 3
    # momset_key = 4
    moment_key = 2
    momset_key = 3

    # estimate squentially each parameter in list_policy_Kap
    #     paramstr_key_list = [['alpha_k','beta']]
    #     paramstr_key_list = ['alpha_k']
    #     paramstr_key_list = ['beta', ['alpha_k','K_DEPRECIATION'], 'list_policy_Fxc']
    #     paramstr_key_list = ['K_DEPRECIATION']
    #     paramstr_key_list = 'list_policy_Fxc'
    #     paramstr_key_list = 'list_reg_memory'
    paramstr_key_list = ['beta']
    paramstr_key_list = ['R_INFORM_SAVE']  # this updates both save and borrow
    paramstr_key_list = ['R_INFORM_SAVE']  # this updates both save and borrow
    paramstr_key_list = ['data__A_params_sd']  # data__A_params_sd data__A_params_mu
    #     paramstr_key_list = ['data__A_params_mu'] # data__A_params_sd data__A_params_mu
    paramstr_key_list = ['beta']

    graph_panda_list_name = 'min_graphs'

    manage_local_farge(invoke=invoke,
                       sync_ecs=sync_ecs,
                       combo_type_list_ab=combo_type_list_ab,
                       combo_type_list_date=combo_type_list_date,
                       invoke_set=invoke_set,
                       esti_spec_key_for_simu=esti_spec_key_for_simu,
                       save_directory_main=save_directory_main,
                       moment_key=moment_key,
                       momset_key=momset_key,
                       graph_panda_list_name=graph_panda_list_name,
                       paramstr_key_list=paramstr_key_list)
