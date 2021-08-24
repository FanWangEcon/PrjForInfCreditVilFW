import logging
import pyfan.amto.json.json as support_json

import boto3aws.aws_ecr.ecr_docker as botodocker
import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)

FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

dockerfilename = 'DockerfileConda'
job_dict = {"jobDefinitionName": 'a-1-thaijmp-runesr-x',
            "type": "container",
            "containerProperties": {
                "image": boto3aws.aws_keys()['main_aws_id'] + ".dkr.ecr." +
                         boto3aws.aws_keys()['region'] + ".amazonaws.com/" +
                         botodocker.get_docker_image_name(dockerfilename),
                "vcpus": int(1),
                "memory": int(1024),
                "command": ["python",
                            "/ThaiJMP/invoke/run_esr.py",
                            "1",
                            "-s", "ng_s_t=esti_medtst_thin_1=3=3",
                            "-cta", "e",
                            "-ctb", "20201025x_esr",
                            "-ctc", "list_tKap_mlt_ce1a2",
                            "-f", "esti"],
                "jobRoleArn": "arn:aws:iam::" + boto3aws.aws_keys()['main_aws_id'] + ":role/" +
                              boto3aws.aws_keys()['batch_task_executionRoleArn']
            },
            "retryStrategy": {
                "attempts": 1
            }}

aws_batch = boto3aws.start_boto3_client('batch')

array_size = 100
timesufx = '_' + proj_sys_sup.save_suffix_time(2)
job_queue = 'Spot'
response = aws_batch.submit_job(
    jobName=job_dict['jobDefinitionName'] + '-' + timesufx,
    jobQueue=job_queue,
    arrayProperties={'size': array_size},
    jobDefinition=job_dict['jobDefinitionName'],
    containerOverrides={"command": job_dict['containerProperties']['command']})

support_json.jdump(response, 'submit_job--response', logger=logger.info)
