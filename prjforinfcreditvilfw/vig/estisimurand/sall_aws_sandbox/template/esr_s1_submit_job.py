"""
Assume that:

1. Container on ECR has been updated to contain latest pyfan and thaijmp code
2. A task with the task name below has been submitted.

Note that for different invokations, can adjust the default command and compute
size of registered tasks.

Submit two separate tasks, representing two different regions.
"""

import logging

import boto3aws.tools.manage_aws as boto3aws
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# This is a already registered task: see esr_s0_register_task.py
jobDefinitionName = 'a-1-thaijmp-runesr-x'

# Start Batch
aws_batch = boto3aws.start_boto3_client('batch')

# Both regions
ar_regions = ['ce', 'ne']
# ar_regions = ['ne']

# Region-specific combo_type information
st_cta, st_ctb = 'e', '20201025_esr_CTBCTBCTB'
dc_combo_type = {'ce': {'cta': st_cta, 'ctb': st_ctb,
                        'ctc': 'list_tKap_mlt_ce1a2'},
                 'ne': {'cta': st_cta, 'ctb': st_ctb,
                        'ctc': 'list_tKap_mlt_ne1a2'}}

# Region specific speckey
compute_spec_key, esti_spec_key = 'ng_s_t', 'esti_COMPSIZE_thin_1'
dc_moment_key = {'ce': '3', 'ne': '4'}
momset_key = '3'
dc_speckey = {'ce': '='.join([compute_spec_key, esti_spec_key, dc_moment_key['ce'], momset_key]),
              'ne': '='.join([compute_spec_key, esti_spec_key, dc_moment_key['ne'], momset_key])}

for st_regions in ar_regions:
    # Container command
    array_size = estispec.estimate_set(esti_spec_key)['esti_param_vec_count']
    it_memory = computespec.compute_set(compute_spec_key)['memory']
    # it_memory = 1024
    it_vcpus = computespec.compute_set(compute_spec_key)['vcpus']
    # it_vcpus = 1
    job_queue = 'Spot'
    # Print
    logger.info(array_size)

    # Responses
    response = aws_batch.submit_job(
        jobName=jobDefinitionName + '-' + st_regions + '-' + proj_sys_sup.save_suffix_time(2),
        jobQueue=job_queue,
        arrayProperties={'size': array_size},
        jobDefinition=jobDefinitionName,
        containerOverrides={"vcpus": int(it_vcpus),
                            "memory": int(it_memory),
                            "command": ["python",
                                        "/ThaiJMP/invoke/run_esr.py",
                                        "1",
                                        "-s", dc_speckey[st_regions],
                                        "-cta", dc_combo_type[st_regions]["cta"],
                                        "-ctb", dc_combo_type[st_regions]["ctb"],
                                        "-ctc", dc_combo_type[st_regions]["ctc"],
                                        "-f", "esti_tst"]})

    # support_json.jdump(response, 'submit_job--response', logger=logger.info)
