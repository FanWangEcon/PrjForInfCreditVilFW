"""
Same as esr_s1357_submit_job, but inputs provided by run_esr_parser
"""

import logging

import pyfan.amto.json.json as support_json
import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup
import parameters.runspecs.estimate_specs as estispec
import parameters.runspecs.compute_specs as computespec
import invoke.run_esr_parser as run_esr_parser
import time
import subprocess

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# This is a already registered task: see esr_s0_register_task.py
jobDefinitionName, job_queue = 'a-1-thaijmp-runesr-x', 'Spot'
ar_regions = ['ce', 'ne']
esr_run = 1
it_esti_top_which_max = 5
dc_it_execute_type = {'model_assumption': 0, 'compute_size': 0, 'esti_size': 0, 'esti_param': 0,
                      'call_type': 2, 'param_date': 0}

dc_st_esr_args_compose, dc_aws_local_sync_cmd, \
dc_combo_type, dc_combo_type_component, \
dc_st_speckey, dc_st_speckey_mpoly, esrf, it_esti_top_which_max, \
compute_spec_key, esti_spec_key = \
    run_esr_parser.run_esr_arg_generator(esr_run,
                                         ar_regions=ar_regions,
                                         dc_it_execute_type=dc_it_execute_type,
                                         it_esti_top_which_max=it_esti_top_which_max,
                                         awslocal=True,
                                         verbose=True)

# print outputs
print(f'{dc_aws_local_sync_cmd=}')
print(f'{dc_combo_type=}')
print(f'{dc_st_speckey=}')
print(f'{dc_st_speckey_mpoly=}')
print(f'{esrf=}')

# 2. Container options
array_size = estispec.estimate_set(esti_spec_key)['esti_param_vec_count']
it_memory = computespec.compute_set(compute_spec_key)['memory']
it_vcpus = computespec.compute_set(compute_spec_key)['vcpus']

# Start Batch
aws_batch = boto3aws.start_boto3_client('batch')

# run by region
dc_responses = {}
for st_regions in ar_regions:
    if esr_run in [1, 3, 5, 7]:
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
                                                "-s", dc_st_speckey[st_regions],
                                                "-cta", dc_combo_type_component[st_regions]["cta"],
                                                "-ctb", dc_combo_type_component[st_regions]["ctb"],
                                                "-ctc", dc_combo_type_component[st_regions]["ctc"],
                                                "-f", esrf]})

        if esr_run == 5 or esr_run == 7:
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
                                                "-s", dc_st_speckey[st_regions],
                                                "-cta", dc_combo_type_component[st_regions]["cta"],
                                                "-ctb", dc_combo_type_component[st_regions]["ctb"],
                                                "-ctc", dc_combo_type_component[st_regions]["ctc"],
                                                "-cte1", dc_st_speckey_mpoly[st_regions],
                                                "-cte2", str(it_esti_top_which_max),
                                                "-f", esrf]})

        support_json.jdump(response, 'submit_job--response', logger=logger.info)
        dc_responses[st_regions] = response

    elif esr_run in [2, 4, 6, 8]:
        # source "G:/ProgramData/Anaconda3/etc/profile.d/conda.sh"
        ls_st_cmd_sync_call = dc_aws_local_sync_cmd[st_regions]
        print(f'{ls_st_cmd_sync_call=}')
        # ls_st_cmd_sync_call = ['call', 'conda.bat'] + ls_st_cmd_sync_call
        # print(f'{ls_st_cmd_sync_call=}')
        # cmd_popen = subprocess.Popen(ls_st_cmd_sync_call,
        #                              stdin=subprocess.PIPE,
        #                              stdout=subprocess.PIPE,
        #                              stderr=subprocess.PIPE)
        # output, err = cmd_popen.communicate()
        # print(f'{output=}')
        # print(f'{err=}')

        # ls_st_cmd_sync_call = dc_aws_local_sync_cmd[st_regions]
        # print(ls_st_cmd_sync_call)
        # cmd_popen = subprocess.Popen(ls_st_cmd_sync_call,
        #                              stdin=subprocess.PIPE,
        #                              stdout=subprocess.PIPE,
        #                              stderr=subprocess.PIPE)
        # output, err = cmd_popen.communicate()

    else:
        raise ValueError(f'The specified esr_run, {esr_run=} is not allowed.')


# Display status
fl_start = time.time()
dc_bl_job_in_progress = {'ce': True, 'ne': True}
dc_it_wait_seconds = {'ce': 0, 'ne': 0}
if len(dc_responses) > 0:

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
                      f'SUBMITTED={dc_status_summary["SUBMITTED"]}, PENDING={dc_status_summary["PENDING"]}, '
                      f'RUNNABLE={dc_status_summary["RUNNABLE"]}, STARTING={dc_status_summary["STARTING"]}, '
                      f'RUNNING={dc_status_summary["RUNNING"]}, '
                      f'SUCCEEDED={dc_status_summary["SUCCEEDED"]}, FAILED={dc_status_summary["FAILED"]}')
            else:
                dc_bl_job_in_progress[st_regions] = True
                # empty statussummary
                time.sleep(it_wait_time)
                dc_it_wait_seconds[st_regions] = round(time.time() - fl_start)
                print(f'{st_regions.upper()} ({dc_it_wait_seconds[st_regions]} sec): ArrayN={it_array_size}')
