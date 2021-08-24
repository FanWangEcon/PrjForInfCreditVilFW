import logging
import pyfan.amto.json.json as support_json

import boto3aws.aws_ecr.ecr_docker as botodocker
import boto3aws.tools.manage_aws as boto3aws

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
                            "-s", "ng_s_t=esti_tinytst_thin_1=3=3",
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

response = aws_batch.register_job_definition(
    jobDefinitionName=job_dict['jobDefinitionName'],
    type=job_dict['type'],
    containerProperties=job_dict['containerProperties'],
    retryStrategy=job_dict['retryStrategy'])
#                 timeout = job_dict['timeout']
support_json.jdump(response, 'register_task_definition--response', logger=logger.info)
