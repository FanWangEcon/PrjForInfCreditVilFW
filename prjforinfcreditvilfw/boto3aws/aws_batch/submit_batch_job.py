'''
Created on Jul 28, 2018

@author: fan
'''

import logging

logger = logging.getLogger(__name__)

import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup
import pyfan.amto.json.json as support_json


def submit_job_batch(batch, job_def_name, job_queue,
                     array_size=1,
                     clusterName='fanFargateMain'):
    """
    aws ecs run-task \
    --cluster fanFargateMain \
    --task-definition b-20180521-LENDFC:1 \
    --count 1 \
    --launch-type "FARGATE" \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-d9abbe82],securityGroups=[sg-e6642399]}"
    """

    networkConfiguration = {'awsvpcConfiguration':
                                {'subnets': [boto3aws.aws_keys()['fargate_public_subnet']],
                                 'securityGroups': [boto3aws.aws_keys()['fargate_security_group']],
                                 'assignPublicIp': 'ENABLED'
                                 }
                            }

    timesufx = '_' + proj_sys_sup.save_suffix_time(2)

    if (array_size == 1):
        response = batch.submit_job(
            jobName=job_def_name + timesufx,
            jobQueue=job_queue,
            jobDefinition=job_def_name)
    else:
        response = batch.submit_job(
            jobName=job_def_name + timesufx,
            jobQueue=job_queue,
            arrayProperties={'size': array_size},
            jobDefinition=job_def_name)

    support_json.jdump(response, 'register_task_definition--response', logger=logger.info)
