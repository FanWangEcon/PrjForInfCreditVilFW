'''
Created on Jun 4, 2018

@author: fan
'''

import logging
import subprocess as sp
import time
import pyfan.amto.json.json as support_json
import shutil
from pathlib import Path
import os

logger = logging.getLogger(__name__)


def commandlinelocal_call(commands):
    command_list = commands.split()
    print(command_list)
    return sp.call(command_list, shell=True)


def commandline_local(commands):
    """
    command line opens up bash from within windows command,
    and add command line arguments

    commands is for example: C:/pem/fan_wang-key-pair-us_east_nv.pem C:/container/DockerfileConda ec2-user@54.221.154.196:~/docker/Dockerfile
    """

    # Finds where git is installed at, and hence where git-bash is installed at
    # https://fanwangecon.github.io/Py4Econ/support/inout/htmlpdfr/fp_files.html
    st_cmd = 'git'
    spn_path_to_git = shutil.which(st_cmd)
    # find path to git-bash.exe
    spn_path_to_gitbash = ''
    for it_up_iter in [0, 1]:
        # up-tier folder
        srt_path_git_up_folder = Path(spn_path_to_git).parents[it_up_iter]
        # search
        # get file names in folders (not recursively)
        ls_spn_found_git_bash = [spn_file for spt_srh in [srt_path_git_up_folder]
                                 for spn_file in Path(spt_srh).glob('git-bash.exe')]
        # if found, length of ls of founds files must be 1
        if len(ls_spn_found_git_bash) == 1:
            spn_path_to_gitbash = ls_spn_found_git_bash[0]
            break

    if spn_path_to_gitbash == '':
        raise NameError(f'failed to find git-bash, {spn_path_to_git=}')
    else:
        print(f'Found git-bash: {spn_path_to_gitbash} by searching around {spn_path_to_git=}')

    command_str = '"' + str(spn_path_to_gitbash).replace(os.sep, '/') +'" -c "' + commands + '"'
    logger.critical(f'GIT BASH: {command_str=}')

    process = sp.Popen(command_str, shell=True)
    process.wait()


def commandline_aws_ec2(client, commands, instance_ids):
    """Runs commands on remote linux instances
    http://boto3.readthedocs.io/en/latest/reference/services/ssm.html#SSM.Client.send_command

        param client: a boto/boto3 ssm client
        param commands: a list of strings, each one a command to execute on the instances
        param instance_ids: a list of instance_id strings, of the instances on which to execute the command
        return: the response from the send_command function (check the boto3 docs for ssm client.send_command() )

    Set up:
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial_run_command.html#rc-tutorial-ui
    1. add to my user, Fan_Wang, permission WRONG:
        go to aim, and add this to user: AmazonEC2RoleforSSM
        - actually not about adding to user, but about creating role!
        - Attach an IAM role with the AmazonEC2RoleforSSM managed policy to an Amazon EC2 instance.
        - not IAM USER, but IAM ROLE!!
            + https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-configuring-access-role.html
                - create iam ROLE for EC2 to attach to EC2 with manager permissions.
    2. start instance, add aim for Fan_Wang to instance
        + https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#attach-iam-role
        + aws ec2 describe-instances
        + aws ec2 associate-iam-instance-profile --instance-id i-06977cf6d5691a2da --iam-instance-profile Name=aws_ec2_ssm_role
    3. restart
    """

    logger.info('instance_ids:%s', instance_ids)

    resp = client.send_command(
        DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
        Parameters={'commands': commands},
        InstanceIds=instance_ids
    )
    support_json.jdump(resp, 'send_command', logger=logger.info)

    command_id = resp['Command']['CommandId']

    logger.info('commands:%s', commands)
    logger.info('command_id:%s', command_id)

    sleep_list_seconds = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5]
    cur_status = 'Pending'
    FAN_NULL = 'FanNull'
    status_check_ctr = 0
    #         Valid Values: Pending | InProgress | Success | TimedOut | Cancelled | Failed
    loop_status = ['Pending', 'InProgress', FAN_NULL]
    while (cur_status in loop_status):
        #         current_results = client.list_commands(
        #                             CommandId=command_id,
        #                             InstanceId=instance_ids[0])
        #
        #         cur_status = current_results['Commands'][0]['Status']

        current_results = client.list_command_invocations(
            CommandId=command_id,
            InstanceId=instance_ids[0],
            Details=True)

        CommandInvocations = current_results['CommandInvocations']
        if (len(CommandInvocations) == 0):
            # Just starting? No outputs here yet?
            support_json.jdump(current_results, 'failed:list_command_invocation', logger=logger.info)
            cur_status = FAN_NULL
        else:
            # Show status here now
            cur_status = CommandInvocations[0]['Status']

        if (status_check_ctr >= len(sleep_list_seconds)):
            delay = 10
        else:
            delay = sleep_list_seconds[status_check_ctr]

        time.sleep(delay)
        status_check_ctr = status_check_ctr + 1
        logger.info('status_check_ctr, delay, cur_status:%s,%s,%s', status_check_ctr, delay, cur_status)

    if (cur_status == 'Failed'):
        support_json.jdump(current_results, 'failed:list_command_invocation', logger=logger.info)
    else:
        pass

    cur_output = current_results['CommandInvocations'][0]['CommandPlugins'][0]['Output']
    support_json.jdump(cur_output.split('\n'), 'list_command_invocation-cur_output', logger=logger.info)

    #          the following command to get IP information for an instance.
    #
    #     aws ssm send-command --instance-ids "i-06977cf6d5691a2da" --document-name "AWS-RunShellScript" --comment "IP config" --parameters commands=ifconfig --output text
    #     aws ssm list-command-invocations --command-id 6fbf0938-1966-4928-ae74-105acda5b802 --details
    #
    #     aws ssm send-command --instance-ids "i-06977cf6d5691a2da" --document-name "AWS-RunShellScript" --comment "IP config" --parameters commands=ifconfig --output text
    #     aws ssm list-command-invocations --command-id 593d04d6-7e7b-4901-8945-4c0f11b22e87 --details
    #
    #     aws ssm send-command --instance-ids "i-06977cf6d5691a2da" --document-name "AWS-RunShellScript" --comment "IP config" --parameters commands="cd ~;pwd" --output text
    #     aws ssm list-command-invocations --command-id d76adc20-7e3c-432c-8518-0f0146bfbce6 --details
    #
    #     aws ssm send-command --instance-ids "i-06977cf6d5691a2da" --document-name "AWS-RunShellScript" --comment "IP config" --parameters commands="cd /home/ec2-user/docker;pwd" --output text
    #     aws ssm list-command-invocations --command-id 3383cb87-0f4e-49d6-9cee-c6826156ef76 --details

    return cur_output
