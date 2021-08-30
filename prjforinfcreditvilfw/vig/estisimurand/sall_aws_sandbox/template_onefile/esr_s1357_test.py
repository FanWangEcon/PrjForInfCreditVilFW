"""
Assume that:

1. Container on ECR has been updated to contain latest pyfan and thaijmp code
2. A task with the task name below has been submitted.

Note that for different invokations, can adjust the default command and compute
size of registered tasks.

Submit two separate tasks, representing two different regions.
"""

import logging
import pyfan.amto.json.json as support_json

import boto3aws.tools.manage_aws as boto3aws
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

"""
OPTINAL PARAMETER SPECIFICATIONS
"""
esr_run = 5
it_esti_top_which_max = 5
# A1. Main folder name
save_directory_main = 'esti_tst_onefile'
# A2. subfolder name
esrbstfilesuffix = "_esr_tstN5_aws"
# C1. ITG or x, normal, or detailed
esrbxrditg = "x"
# esrbxrditg = "x_ITG"
# C2. compute spec key
esrscomputespeckey = "ng_s_t"
# esrscomputespeckey = "b_ng_p_d"
# C3. test scale (esti spec key)
esrssttestscale = "_tinytst_"

# Both regions
ar_regions = ['ce', 'ne']
# ar_regions = ['ne']

# Region-specific combo_type information
# st_cta, st_ctb = 'e', '20201025x_esr_medtst'
st_cta, st_ctb = 'e', '20201025' + esrbxrditg + esrbstfilesuffix
dc_combo_type = {'ce': {'cta': st_cta, 'ctb': st_ctb,
                        'ctc': 'list_tKap_mlt_ce1a2'},
                 'ne': {'cta': st_cta, 'ctb': st_ctb,
                        'ctc': 'list_tKap_mlt_ne1a2'}}

# Region specific speckey
dc_moment_key = {'ce': '3', 'ne': '4'}
momset_key = '3'
dc_compute_spec_key = {1: esrscomputespeckey, 3: 'mpoly_1',
                       5: esrscomputespeckey, 7: esrscomputespeckey}
dc_esti_spec_key = {1: 'esti' + esrssttestscale + 'thin_1', 3: 'esti' + esrssttestscale + 'mpoly_13',
                    5: 'esti_mplypostsimu_1', 7: 'esti_mplypostesti_12'}

"""
OPTINAL PARAMETER SPECIFICATIONS
"""
# Start Batch
aws_batch = boto3aws.start_boto3_client('batch')

# This is a already registered task: see esr_s0_register_task.py
jobDefinitionName = 'a-1-thaijmp-runesr-x'

# task info
job_queue = 'Spot'

# common code esr_run specific
# 1. Sepckey
compute_spec_key, esti_spec_key = dc_compute_spec_key[esr_run], dc_esti_spec_key[esr_run]
dc_speckey = {'ce': '='.join([compute_spec_key, esti_spec_key, dc_moment_key['ce'], momset_key]),
              'ne': '='.join([compute_spec_key, esti_spec_key, dc_moment_key['ne'], momset_key])}

# 1b. speckey ERS3
compute_spec_key_mpoly, esti_spec_key_mpoly = dc_compute_spec_key[3], dc_esti_spec_key[3]
dc_speckey_mpoly = {'ce': '='.join([compute_spec_key_mpoly, esti_spec_key_mpoly, dc_moment_key['ce'], momset_key]),
                    'ne': '='.join([compute_spec_key_mpoly, esti_spec_key_mpoly, dc_moment_key['ne'], momset_key])}

# 2. Container options
array_size = estispec.estimate_set(esti_spec_key)['esti_param_vec_count']
it_memory = computespec.compute_set(compute_spec_key)['memory']
it_vcpus = computespec.compute_set(compute_spec_key)['vcpus']

response = aws_batch.list_jobs(arrayJobId="c8206b03-033c-44fe-8cf7-506357281fa0")
support_json.jdump(response, 'submit_job--response', logger=logger.info)
response = aws_batch.describe_jobs(jobs=["c8206b03-033c-44fe-8cf7-506357281fa0"])
support_json.jdump(response, 'submit_job--response', logger=logger.info)

f'{it_wait_seconds=}, ArrayN={it_array_size},' \
f'SUCCEEDED={dc_status_summary["SUCCEEDED"]}, FAILED={dc_status_summary["FAILED"]}, ' \
f'RUNNING={dc_status_summary["RUNNING"]}, PENDING={dc_status_summary["PENDING"]}, ' \
f'RUNNABLE={dc_status_summary["RUNNABLE"]}'
