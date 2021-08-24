'''
Created on Jul 28, 2018

@author: fan
'''

import logging
import pyfan.amto.json.json as support_json

import boto3aws.aws_ecr.ecr_docker as botodocker
import boto3aws.tools.manage_aws as boto3aws
import boto3aws.tools.support as aws_sup
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec

logger = logging.getLogger(__name__)


def gen_batch_job_dict(combo_type, speckey,
                       vcpus, memory, attempts=1,
                       graph_panda_list_name='',
                       save_directory_main='',
                       ge='', multiprocess='', estimate='',
                       dockerfilename='DockerfileConda'):
    """    
    Specify memory in binary
    
    Parameters
    ----------
    combo_type: list of strings
        =['a', '20180529_A', 'data_param.A']
    ge: string
        --ge or nothing (default no ge)
    multiproces: string
        --multiproces or nothing (default no multi)
    attempts: int
        initially set to 3, became 1 when esti_specs['esti_max_func_eval'] was added
        when estimation evaluations exceed max_func_eval, code exits, a 'fail'.
        If attemps = 3, would restart container and run identical estimation until fail again. 
        On local machine outside of docker would not matter, because computer on second 
        try would see that esti_max_func_eval number of entries in panda file already exists
        based on stored json files. But on docker, each retry starts new docker with new driver. 
    """

    compute_spec_key = estispec.compute_esti_spec_combine(spec_key=speckey, action='compute_spec_key')
    compute_specs = computespec.compute_set(compute_spec_key)
    speckey_strip = estispec.compute_esti_spec_combine(spec_key=speckey, action='strip')

    if (vcpus is None):
        vcpus = compute_specs['vcpus']
    if (memory is None):
        memory = compute_specs['memory']

    combo_type_dash = []
    for ctr, list_ele in enumerate(combo_type):
        if (list_ele is None):
            combo_type_dash.append('None')
        elif (isinstance(list_ele, int)):
            combo_type_dash.append(str(list_ele))
        elif (isinstance(list_ele, list)):
            combo_type_dash.append(''.join(list_ele).replace("_", "-"))
        else:
            combo_type_dash.append(list_ele.replace("_", "-"))

    combo_type_file = combo_type_dash[0]
    combo_type_date_param = combo_type_dash[1]
    combo_type_param = combo_type_dash[2]
    param_combo_select_ctr = combo_type_dash[3]

    if (combo_type_param == 'None'):
        if (estimate.strip() == '--esti'):
            container_name = 'esti-' + speckey_strip + '-' + combo_type_file + '-' + combo_type_date_param
        else:
            container_name = 'simu-' + speckey_strip + '-' + combo_type_file + '-' + combo_type_date_param
    else:
        container_name = combo_type_param.split('.')[0] + '-' + combo_type_param.split('.')[1]

    family = combo_type_file + '-' + combo_type_date_param
    if (param_combo_select_ctr != 'None'):
        family = family + '-' + param_combo_select_ctr
    family = family + estimate.strip()
    family = family + '--' + speckey_strip
    family = family + ge.strip()
    family = family + multiprocess.strip().replace("multiprocess", "mp")
    #     family = family + multiprocess.strip()
    family = family + '-c' + str(vcpus)
    family = family + 'm' + memory[0:2]
    family = family + 'a' + str(attempts)

    family = aws_sup.limit_batch_job_def_name(family)
    family = family.replace("--", "-")

    awslogs_opts = {"awslogs-group": container_name,
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": family}

    '''
    Parsing paramtype.paramname list
    '''
    if (combo_type[2] is None):
        combo_type_2 = 'None'
    elif (isinstance(combo_type[2], list)):
        # list like: ['data_param.A', 'esti_param.beta']
        # convert to string: data_param.A esti_param.beta
        # run.py parses this string with space as list and returns list line in line 1
        combo_type_2 = " ".join(combo_type[2])
    else:
        raise ('Bad combo_type[2] input, not list, not None')

    if (combo_type[3] is None):
        combo_type_3 = 'None'
    else:
        combo_type_3 = str(combo_type[3])
        # container definition is one of the keys, other apply to entire task

    job_def = {"jobDefinitionName": family,
               "type": "container",
               "containerProperties": {
                   "image": boto3aws.aws_keys()['main_aws_id'] + ".dkr.ecr." +
                            boto3aws.aws_keys()['region'] + ".amazonaws.com/" +
                            botodocker.get_docker_image_name(dockerfilename),
                   "vcpus": int(vcpus),
                   "memory": int(memory),
                   "command": ["python",
                               "/ThaiJMP/invoke/run.py",
                               "-A", speckey,
                               "-B", combo_type[0],
                               "-C", combo_type[1],
                               "-D", combo_type_2,
                               "-E", combo_type_3,
                               "-F", graph_panda_list_name,
                               "-G", save_directory_main,
                               ge.strip(),
                               multiprocess.strip(),
                               estimate.strip()],
                   "jobRoleArn": "arn:aws:iam::" + boto3aws.aws_keys()['main_aws_id'] + ":role/" +
                                 boto3aws.aws_keys()['batch_task_executionRoleArn']
               },
               "retryStrategy": {
                   "attempts": attempts
               }
               }

    support_json.jdump(job_def, 'job_def', logger=logger.warning)

    return job_def, awslogs_opts


def add_batch_job_def(batch, logs,
                      combo_type, speckey,
                      vcpus, memory, attempts,
                      graph_panda_list_name,
                      save_directory_main,
                      ge, multiprocess, estimate,
                      dockerfilename='DockerfileConda'):
    """
    First checks if job with the same command, cpu and memory requirements already exists. 
    If not, generate new job. If the jobDefinitionName already exists, a new revision
    will be created under the same jobDefinitionName. Otherwise, a new Job Definition would be
    created.  
        
    aws  register-task-definition --cli-input-json file://$HOME/docker/fancondajmp-task-def.json
    """

    """
    A. Generate Task fields
    """
    job_dict, awslogs_opts = gen_batch_job_dict(combo_type, speckey,
                                                vcpus, memory, attempts,
                                                graph_panda_list_name=graph_panda_list_name,
                                                save_directory_main=save_directory_main,
                                                ge=ge, multiprocess=multiprocess, estimate=estimate,
                                                dockerfilename=dockerfilename)

    job_def_name = job_dict['jobDefinitionName']
    command = job_dict['containerProperties']['command']
    if (vcpus is None):
        vcpus = job_dict['containerProperties']['vcpus']
    if (memory is None):
        memory = job_dict['containerProperties']['memory']

    """
    B. Add Log Group, required
    this was how fargate worked, but not here, all batch seem to go to the same log group, in some sense, d
    does not really work well. 
    """
    #     try:
    #         cloudwatchlog = logs.create_log_group(logGroupName=awslogs_opts['awslogs-group'])
    #         support_json.jdump(cloudwatchlog, 'cloudwatchlog, awslogs-group'
    #                                + awslogs_opts['awslogs-group']
    #                                + ':', logger=logger.info)
    #     except:
    #         logger.info('Log group %s already exists.', awslogs_opts['awslogs-group'])

    """
    C. Check if definition exists with identical fields
    """

    update_batch_job = True
    try:
        response = batch.describe_job_definitions(jobDefinitionName=job_dict['jobDefinitionName'])
        support_json.jdump(response, 'describe_job_definitions, job_def_name'
                           + job_def_name
                           + ':', logger=logger.info)
        jobDefinition = response['jobDefinitions']
        containerDefinitions = jobDefinition[0]['containerProperties']

        cur_command = containerDefinitions['command']
        cur_memory = containerDefinitions['memory']
        cur_vcpus = containerDefinitions['vcpus']
        cur_attempts = jobDefinition[0]['retryStrategy']['attempts']

        logger.info('cur_command:\n%s', cur_command)
        logger.info('command:\n%s', command)
        logger.info('cur_memory:\n%s', cur_memory)
        logger.info('memory:\n%s', memory)
        logger.info('cur_vcpus:\n%s', cur_vcpus)
        logger.info('vcpus:\n%s', vcpus)
        logger.info('cur_attempts:\n%s', cur_attempts)
        logger.info('attempts:\n%s', attempts)

        if (cur_command == command and
                cur_memory == memory and
                cur_vcpus == vcpus and
                cur_attempts == attempts):
            update_batch_job = False
            logger.info('Job with same memory and cpu and command exists already')

    except Exception:
        logger.info('Job definition jobDefinitionName does not exist yet: %s', job_dict['jobDefinitionName'])

    #     update_task = True

    """
    C. Add New Definition
    """
    #     update_batch_job = True
    if (update_batch_job):
        response = batch.register_job_definition(
            jobDefinitionName=job_dict['jobDefinitionName'],
            type=job_dict['type'],
            containerProperties=job_dict['containerProperties'],
            retryStrategy=job_dict['retryStrategy'])
        #                 timeout = job_dict['timeout']
        support_json.jdump(response, 'register_task_definition--response', logger=logger.info)

    return job_def_name
