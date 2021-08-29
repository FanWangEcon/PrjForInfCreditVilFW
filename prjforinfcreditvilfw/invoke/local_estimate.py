'''
Created on Jul 24, 2018

@author: fan
'''
import logging

import boto3aws.run_aws as runfargate
import invoke.combo_type_list_wth_specs as paramcombospecs
import invoke.run_estimate as runesti
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.graph.graph_sets as sup_graphset
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

timesufx = '_' + proj_sys_sup.save_suffix_time(1)
saveDirectory = proj_sys_sup.get_paths('esti', '')


def estimate(invoke, invoke_set, sync_ecs=True,
             esti_spec_key='kap_m0_nld_m',
             combo_type_list_ab='a', combo_type_list_date='20180607',
             paramstr_key_list=None,
             moment_key=0, momset_key=1):
    if (invoke == 'local'):
        '''
        B. Local
        '''
        estimate_local(invoke_set,
                       esti_spec_key=esti_spec_key,
                       combo_type_list_ab=combo_type_list_ab,
                       combo_type_list_date=combo_type_list_date,
                       paramstr_key_list=paramstr_key_list,
                       moment_key=moment_key, momset_key=momset_key)

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

        estimate_fargate(invoke_set,
                         sync_ecs=sync_ecs,
                         esti_spec_key=esti_spec_key,
                         combo_type_list_ab=combo_type_list_ab,
                         combo_type_list_date=combo_type_list_date,
                         paramstr_key_list=paramstr_key_list,
                         moment_key=moment_key, momset_key=momset_key,
                         aws_type=aws_type, job_queue=job_queue)


def estimate_fargate(invoke_set, sync_ecs=True,
                     esti_spec_key='kap_m0_nld_m',
                     combo_type_list_ab='a', combo_type_list_date='20180607',
                     paramstr_key_list=None,
                     moment_key=0, momset_key=1,
                     graph_panda_list_name=None,
                     save_directory_main='esti',
                     aws_type='fargate', job_queue=None):
    """
    This is relevant only for Fargate basically
    """
    fargate = True
    if (sync_ecs):
        ec2_start = True
        run_docker = True
    else:
        ec2_start = False
        run_docker = False

    estimate_local(invoke_set, esti_spec_key,
                   combo_type_list_ab=combo_type_list_ab, combo_type_list_date=combo_type_list_date,
                   paramstr_key_list=paramstr_key_list,
                   moment_key=moment_key, momset_key=momset_key,
                   graph_panda_list_name=graph_panda_list_name,
                   save_directory_main=save_directory_main,
                   aws_type=aws_type, job_queue=job_queue,
                   fargate=fargate, ec2_start=ec2_start, run_docker=run_docker)


def estimate_local(invoke_set,
                   esti_spec_key='m0_nld_m',
                   combo_type_list_ab='a', combo_type_list_date='20180607',
                   paramstr_key_list=None,
                   moment_key=0, momset_key=1,
                   graph_panda_list_name=None,
                   save_directory_main='esti',
                   aws_type='fargate', job_queue=None,
                   fargate=False, ec2_start=False, run_docker=False):
    """
    Examples
    --------
    """

    '''
    0. Specify some basic things:
        - parameters
    '''
    if (graph_panda_list_name is None):
        graph_panda_list_name = 'min_graphs'
    graph_list = sup_graphset.graph_panda_sets_names(graph_panda_list_name)
    logger.info('graph_list:\n%s', graph_list)

    '''
    1. Generate combo_type_list and comput and esti specs:
        + combo_type_list should have one element
        + compute_spec and esti_spec merge together into one specs dictionary
    '''
    compute_spec_key, vcpus, cpu, memory, combo_type_list = \
        paramcombospecs.gen_combo_type_list(invoke_set, fargate, paramstr_key_list,
                                            combo_type_list_ab, combo_type_list_date)
    logger.info('compute_spec_key:\n%s', compute_spec_key)

    cur_spec = computespec.compute_set(compute_spec_key, fargate=fargate)
    aws_fargate = cur_spec['aws_fargate']
    ge = cur_spec['ge']
    multiprocess = cur_spec['multiprocess']

    '''
    2. Obtain Param_combo_list (combo_list) associated with the combo_type
        + each element of list represents a different initial value for estimation
        + or could be perhaps same initial parameters, different estimation method
            - if this is the case, then need to specify esti_specs inside combo_list_c_est.py
                using compute_specs that are exogenously feeded in as we do here means that
                (unless they are specified as null), we force each element of combo_list
                to share the same compute_esti_specs.
    '''

    run_ctr = 0
    for combo_type in combo_type_list:

        '''
        Estimate looping over independent random draws of initial parameter values
        '''
        cur_esti_spec = estispec.estimate_set(esti_spec_key,
                                              moment_key=moment_key,
                                              momset_key=momset_key)
        esti_param_vec_count = cur_esti_spec['esti_param_vec_count']
        for rand_ctr in range(esti_param_vec_count):
            #             if (rand_ctr < 315):
            param_combo_select_ctr = rand_ctr
            combo_type[3] = param_combo_select_ctr

            if (aws_fargate):

                #         aws_type = 'fargate'
                #         job_queue = None

                #         aws_type = 'batch'
                #         job_queue = 'Spot'
                #         job_queue = 'OnDemand'

                spec_key = estispec.compute_esti_spec_combine(
                    compute_spec_key=compute_spec_key,
                    esti_spec_key=esti_spec_key,
                    moment_key=moment_key, momset_key=momset_key,
                    action='combine')

                if (run_ctr != 0):
                    run_docker = False
                    ec2_start = False
                run_ctr = run_ctr + 1

                runfargate.invoke_aws_ecs(combo_type,
                                          aws_type=aws_type,
                                          job_queue=job_queue,
                                          speckey=spec_key,
                                          vcpus=vcpus, cpu=cpu, memory=memory,
                                          ge=ge,
                                          multiprocess=multiprocess,
                                          estimate=True,
                                          graph_panda_list_name=graph_panda_list_name,
                                          save_directory_main=save_directory_main,
                                          ec2_start=ec2_start, run_docker=run_docker)

            else:
                logging_level = logging.WARNING
                log_file = False
                log_file_suffix = ''
                runesti.invoke_estimate(combo_type,
                                        compute_spec_key, esti_spec_key,
                                        moment_key, momset_key,
                                        ge, multiprocess,
                                        graph_list, save_directory_main,
                                        logging_level,
                                        log_file,
                                        log_file_suffix)


if __name__ == "__main__":
    """
    import invoke.local_estimate as invoke_esti
    import invoke.local_simulate as invoke_simu
    """
    invoke = 'local'

    #     invoke = 'fargate'
    invoke = 'Spot'
    #     invoke = 'OnDemand'
    sync_ecs = True
    #     sync_ecs = False

    combo_type_list_ab = 'c'
    combo_type_list_date = '20180901'
    invoke_set = 1
    #     esti_spec_key = 'kap_m0_nld_m'
    esti_spec_key = 'esti_testfull_11'
    save_directory_main = 'esti'

    region_time_suffix = hardstring.region_time_suffix()

    momset_key = 4
    paramstr_key_list = ['list_tall' + region_time_suffix['_ne1a2'][0]]
    moment_key = 4
    #     paramstr_key_list = ['list_tall' + region_time_suffix['_ce1a2'][0]]
    #     moment_key = 3

    estimate(invoke, invoke_set, sync_ecs=sync_ecs,
             esti_spec_key=esti_spec_key,
             combo_type_list_ab=combo_type_list_ab, combo_type_list_date=combo_type_list_date,
             paramstr_key_list=paramstr_key_list,
             moment_key=moment_key, momset_key=momset_key)
