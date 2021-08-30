"""
Same as esr_s1357_submit_job, but inputs provided by run_esr_parser
"""

import logging

import pyfan.amto.json.json as support_json
import boto3aws.tools.manage_aws as boto3aws
import projectsupport.systemsupport as proj_sys_sup
import parameters.runspecs.compute_specs as computespec
import invoke.run_sg_parser as run_sg_parser
import time

logger = logging.getLogger(__name__)
FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# This is a already registered task: see esr_s0_register_task.py
jobDefinitionName, job_queue = 'a-1-thaijmp-runesr-x', 'Spot'
sg_run = 1

# CEV main surface run, 101 cev levels, pe_itg
dc_it_execute_type = {'model_assumption': 1,
                      'compute_size': 1,
                      'simu_param': 0,
                      'call_type': 2,
                      'param_date': 16}

st_sg_args_compose, aws_local_sync_cmd, \
combo_type, combo_type_component, \
sgf, \
compute_spec_key = run_sg_parser.run_sg_arg_generator(
    sg_run, dc_it_execute_type=dc_it_execute_type, verbose=True)

if combo_type_component["ctc"] is None:
    combo_type_component["ctc"] = 'None'

# print outputs
print(f'{st_sg_args_compose=}')
print(f'{aws_local_sync_cmd=}')
print(f'{combo_type=}')
print(f'{combo_type_component=}')
print(f'{sgf=}')
print(f'{compute_spec_key=}')

# 2. Container options
compute_param_vec_count = computespec.compute_set(compute_spec_key)['compute_param_vec_count']
if len(combo_type) <= 2:
    array_size = 1
else:
    array_size = compute_param_vec_count ** len(combo_type[2])
it_memory = computespec.compute_set(compute_spec_key)['memory']
it_vcpus = computespec.compute_set(compute_spec_key)['vcpus']

# Start Batch
aws_batch = boto3aws.start_boto3_client('batch')

# run by region
for verbose_sync in [False, True]:
    if verbose_sync is False:
        if array_size == 1:
            response = aws_batch.submit_job(
                jobName=jobDefinitionName + '-' + proj_sys_sup.save_suffix_time(2),
                jobQueue=job_queue,
                jobDefinition=jobDefinitionName,
                containerOverrides={"vcpus": int(it_vcpus),
                                    "memory": int(it_memory),
                                    "command": ["python",
                                                "/ThaiJMP/invoke/run_sg.py",
                                                str(sg_run),
                                                "-s", compute_spec_key,
                                                "-cta", combo_type_component["cta"],
                                                "-ctb", combo_type_component["ctb"],
                                                "-ctc", combo_type_component["ctc"],
                                                "-f", sgf]})
        else:
            response = aws_batch.submit_job(
                jobName=jobDefinitionName + '-' + proj_sys_sup.save_suffix_time(2),
                jobQueue=job_queue,
                arrayProperties={'size': array_size},
                jobDefinition=jobDefinitionName,
                containerOverrides={"vcpus": int(it_vcpus),
                                    "memory": int(it_memory),
                                    "command": ["python",
                                                "/ThaiJMP/invoke/run_sg.py",
                                                str(sg_run),
                                                "-s", compute_spec_key,
                                                "-cta", combo_type_component["cta"],
                                                "-ctb", combo_type_component["ctb"],
                                                "-ctc", combo_type_component["ctc"],
                                                "-f", sgf]})

        support_json.jdump(response, 'submit_job--response', logger=logger.info)

        # Display status
        fl_start = time.time()
        bl_job_in_progress = True
        it_wait_seconds = 0
        while bl_job_in_progress and array_size > 1:

            # Get Job ID
            st_batch_jobID = response['jobId']
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
                    bl_job_in_progress = True
                    # sleep three seconds
                    time.sleep(it_wait_time)
                    it_wait_seconds = round(time.time() - fl_start)
                else:
                    bl_job_in_progress = False
                print(f'({it_wait_seconds} sec): '
                      f'ArrayN={it_array_size},'
                      f'SUBMITTED={dc_status_summary["SUBMITTED"]}, PENDING={dc_status_summary["PENDING"]}, '
                      f'RUNNABLE={dc_status_summary["RUNNABLE"]}, STARTING={dc_status_summary["STARTING"]}, '
                      f'RUNNING={dc_status_summary["RUNNING"]}, '
                      f'SUCCEEDED={dc_status_summary["SUCCEEDED"]}, FAILED={dc_status_summary["FAILED"]}')
            else:
                bl_job_in_progress = True
                # empty statussummary
                time.sleep(it_wait_time)
                it_wait_seconds = round(time.time() - fl_start)
                print(f'({it_wait_seconds} sec): ArrayN={it_array_size}')

    if verbose_sync is True:
        run_sg_parser.run_sg_arg_generator(
            sg_run, dc_it_execute_type=dc_it_execute_type, verbose=True, verbose_sync=True)
