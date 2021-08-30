import logging
import pyfan.amto.json.json as support_json

import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# This is a already registered task: see esr_s0_register_task.py
jobDefinitionName = 'a-1-thaijmp-runesr-x'

# Start Batch
aws_batch = boto3aws.start_boto3_client('batch')

# Container command
array_size = 100
job_queue = 'Spot'

response = aws_batch.submit_job(
    jobName=jobDefinitionName + '-' + proj_sys_sup.save_suffix_time(2),
    jobQueue=job_queue,
    arrayProperties={'size': array_size},
    jobDefinition=jobDefinitionName,
    containerOverrides={"vcpus": int(1), "memory": int(1024),
                        "command": ["python",
                                    "/ThaiJMP/invoke/run_esr.py",
                                    "1",
                                    "-s", "ng_s_t=esti_medtst_thin_1=3=3",
                                    "-cta", "e",
                                    "-ctb", "20201025x_esr",
                                    "-ctc", "list_tKap_mlt_ce1a2",
                                    "-f", "esti"]})

support_json.jdump(response, 'submit_job--response', logger=logger.info)
