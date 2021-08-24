'''
Created on Jun 7, 2018

@author: fan
'''

import logging
import time

import boto3aws.aws_batch.gen_batch_job as genbatch
import boto3aws.aws_batch.submit_batch_job as submitbatch
import boto3aws.aws_ec2.ec2_manage as boto3ec2
import boto3aws.aws_ecr.ecr_docker as botodocker
import boto3aws.aws_fargate.ecs_fargate as ecsfargate
import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def update_docker():
    """
    import boto3aws.run_aws as runfargate
    runfargate.update_docker()             
    """
    proj_sys_sup.log_start(logging_level=logging.INFO, log_file=False)
    ec2 = boto3aws.start_boto3_client('ec2')
    ssm = boto3aws.start_boto3_client('ssm')

    boto3ec2.start_EC2_main(ec2=ec2)
    time.sleep(5)
    botodocker.docker_start_to_push(ec2=ec2, ssm=ssm)
    boto3ec2.stop_EC2_main(ec2=ec2)


def invoke_aws_ecs(combo_type, speckey='l-ng-s-x',
                   aws_type='fargate',
                   job_queue='Spot',
                   vcpus=None, cpu=None, memory=None, attempts=1,
                   ge=False, multiprocess=False, estimate=False,
                   graph_panda_list_name='main_graphs',
                   save_directory_main='simu',
                   ec2_start=True, run_docker=True):
    """
    
    Parameters
    ----------
    cpu: string
        if cpu is None, use what is specified in speckey under specs
    memory: string
        if memory is None, use what is specified in speckey under specs
    attempts: int
        initially set to 3, became 1 when esti_specs['esti_max_func_eval'] was added
        when estimation evaluations exceed max_func_eval, code exits, a 'fail'.
        If attemps = 3, would restart container and run identical estimation until fail again. 
        On local machine outside of docker would not matter, because computer on second 
        try would see that esti_max_func_eval number of entries in panda file already exists
        based on stored json files. But on docker, each retry starts new docker with new driver.         
    """
    proj_sys_sup.log_start(logging_level=logging.INFO, log_file=False)

    ec2 = boto3aws.start_boto3_client('ec2')
    logs = boto3aws.start_boto3_client('logs')
    ssm = boto3aws.start_boto3_client('ssm')

    clusterName = 'fanFargateMain'
    dockerfilename = 'DockerfileConda'

    if (ec2_start):
        boto3ec2.start_EC2_main(ec2=ec2)
        time.sleep(5)

    if (run_docker):
        botodocker.docker_start_to_push(ec2=ec2, ssm=ssm)

    if (ge):
        ge = ' --ge'
    else:
        ge = ' --no-ge'

    if (multiprocess):
        multiprocess = ' --multiprocess'
    else:
        multiprocess = ' --no-multiprocess'

    if (estimate):
        estimate = ' --esti'
    else:
        estimate = ' --no-esti'

    if (aws_type.lower() == 'fargate'):
        ecs = boto3aws.start_boto3_client('ecs')
        ecsfargate.start_cluster(ecs, clusterName=clusterName)
        family = ecsfargate.add_task_def(ecs, logs,
                                         combo_type, speckey,
                                         cpu, memory,
                                         graph_panda_list_name,
                                         save_directory_main,
                                         ge, multiprocess, estimate,
                                         dockerfilename=dockerfilename)
        ecsfargate.run_task_on_fargate(ecs, task_family=family, clusterName=clusterName)

    if (aws_type.lower() == 'batch'):
        batch = boto3aws.start_boto3_client('batch')
        #         job_queue = 'OnDemand'
        #         job_queue = 'Spot'
        array_size = 1
        job_def_name = genbatch.add_batch_job_def(batch, logs, combo_type, speckey,
                                                  vcpus, memory, attempts,
                                                  graph_panda_list_name,
                                                  save_directory_main,
                                                  ge, multiprocess, estimate,
                                                  dockerfilename)
        submitbatch.submit_job_batch(batch, job_def_name, job_queue, array_size, clusterName)

    if (ec2_start):
        boto3ec2.stop_EC2_main(ec2=ec2)


if __name__ == "__main__":
    update_docker()
