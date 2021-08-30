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
import time

import boto3aws.tools.manage_aws as boto3aws
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

"""
OPTINAL PARAMETER SPECIFICATIONS
"""
esr_run = 7
it_call_options = 2

if it_call_options == 1:

    it_esti_top_which_max = 5
    # A1. Main folder name
    save_directory_main = 'esti_tst_onefile_xN5'
    # A2. subfolder name
    esrbstfilesuffix = "_esr_tstN5_aws"
    # C1. ITG or x, normal, or detailed
    esrbxrditg = "x"
    # C2. compute spec key
    esrscomputespeckey = "ng_s_t"
    # C3. test scale (esti spec key)
    esrssttestscale = "_tinytst_"

elif it_call_options == 2:

    it_esti_top_which_max = 5
    save_directory_main = 'esti_tst_onefile_ITGN5'
    esrbstfilesuffix = "_esr_tstN5_aws"
    esrbxrditg = "_ITG"
    esrscomputespeckey = "b_ng_p_d"
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

# run by region
dc_responses = {}
for st_regions in ar_regions:
    if esr_run == 1 or esr_run == 3:
        response = aws_batch.submit_job(
            jobName=jobDefinitionName + '-' + st_regions + '-' + proj_sys_sup.save_suffix_time(2),
            jobQueue=job_queue,
            arrayProperties={'size': array_size},
            jobDefinition=jobDefinitionName,
            containerOverrides={"vcpus": int(it_vcpus),
                                "memory": int(it_memory),
                                "command": ["python",
                                            "/ThaiJMP/invoke/run_esr.py",
                                            str(esr_run),
                                            "-s", dc_speckey[st_regions],
                                            "-cta", dc_combo_type[st_regions]["cta"],
                                            "-ctb", dc_combo_type[st_regions]["ctb"],
                                            "-ctc", dc_combo_type[st_regions]["ctc"],
                                            "-f", save_directory_main]})

    elif esr_run == 5 or esr_run == 7:
        response = aws_batch.submit_job(
            jobName=jobDefinitionName + '-' + st_regions + '-' + proj_sys_sup.save_suffix_time(2),
            jobQueue=job_queue,
            arrayProperties={'size': it_esti_top_which_max},
            jobDefinition=jobDefinitionName,
            containerOverrides={"vcpus": int(it_vcpus),
                                "memory": int(it_memory),
                                "command": ["python",
                                            "/ThaiJMP/invoke/run_esr.py",
                                            str(esr_run),
                                            "-s", dc_speckey[st_regions],
                                            "-cta", dc_combo_type[st_regions]["cta"],
                                            "-ctb", dc_combo_type[st_regions]["ctb"],
                                            "-ctc", dc_combo_type[st_regions]["ctc"],
                                            "-cte1", dc_speckey_mpoly[st_regions],
                                            "-cte2", str(it_esti_top_which_max),
                                            "-f", save_directory_main]})

    else:
        raise ValueError(f'The specified esr_run, {esr_run=} is not allowed.')

    support_json.jdump(response, 'submit_job--response', logger=logger.info)
    dc_responses[st_regions] = response

# Display status
fl_start = time.time()
dc_bl_job_in_progress = {'ce': True, 'ne': True}
dc_it_wait_seconds = {'ce': 0, 'ne': 0}
while (dc_bl_job_in_progress['ce'] or dc_bl_job_in_progress['ne']):

    for st_regions in ar_regions:
        dc_json_batch_response = dc_responses[st_regions]
        # Get Job ID
        st_batch_jobID = dc_json_batch_response['jobId']
        # Print Job ID
        # print(f'{st_batch_jobID=}')
        # While loop to check status

        # describe job
        dc_json_batch_describe_job_response = aws_batch.describe_jobs(jobs=[st_batch_jobID])
        # pprint.pprint(dc_json_batch_describe_job_response, width=1)
        it_array_size = dc_json_batch_describe_job_response['jobs'][0]['arrayProperties']['size']
        if it_array_size >= 1000:
            it_wait_time = 300
        elif it_array_size >= 100:
            it_wait_time = 120
        elif it_array_size >= 10:
            it_wait_time = 60
        else:
            it_wait_time = 20
        dc_status_summary = dc_json_batch_describe_job_response['jobs'][0]['arrayProperties']['statusSummary']
        if dc_status_summary:
            # check status
            it_completed = dc_status_summary['SUCCEEDED'] + dc_status_summary['FAILED']
            if it_completed < it_array_size:
                dc_bl_job_in_progress[st_regions] = True
                # sleep three seconds
                time.sleep(it_wait_time)
                dc_it_wait_seconds[st_regions] = round(time.time() - fl_start)
            else:
                dc_bl_job_in_progress[st_regions] = False
            print(f'{st_regions.upper()} ({dc_it_wait_seconds[st_regions]} sec): '
                  f'ArrayN={it_array_size},'
                  f'SUCCEEDED={dc_status_summary["SUCCEEDED"]}, FAILED={dc_status_summary["FAILED"]}, '
                  f'RUNNING={dc_status_summary["RUNNING"]}, PENDING={dc_status_summary["PENDING"]}, '
                  f'RUNNABLE={dc_status_summary["RUNNABLE"]}')
        else:
            dc_bl_job_in_progress[st_regions] = True
            # empty statussummary
            time.sleep(it_wait_time)
            dc_it_wait_seconds[st_regions] = round(time.time() - fl_start)
            print(f'{st_regions.upper()} ({dc_it_wait_seconds[st_regions]} sec): ArrayN={it_array_size}')
