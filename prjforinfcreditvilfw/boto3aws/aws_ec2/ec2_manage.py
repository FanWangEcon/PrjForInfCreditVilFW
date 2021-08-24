'''
Created on Jun 4, 2018

@author: fan
'''

import boto3
import logging
import os
import pyfan.amto.json.json as support_json
import time
from botocore.exceptions import ClientError

import boto3aws.tools.manage_aws as botoaws

logger = logging.getLogger(__name__)

aws_keys_dict = botoaws.aws_keys()
main_work_ec2_instance_id = aws_keys_dict['main_ec2_instance_id']


def stop_EC2_main(ec2=None,
                  instance_id=main_work_ec2_instance_id):
    if (ec2 is None):
        ec2 = boto3.client('ec2')

    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        support_json.jdump(response, 'stop_instances', logger=logger.warning)

    except ClientError as e:
        logger.warning('Error:\n%s', e)

    # Check Status
    EC2_status(80, ec2)


def start_EC2_main(ec2=None,
                   instance_id=main_work_ec2_instance_id):
    if (ec2 is None):
        ec2 = boto3.client('ec2')

    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        support_json.jdump(response, 'start_instances', logger=logger.warning)
    except ClientError as e:
        logger.warning('Error:\n%s', e)

    # Wait Until Instance has finished Starting
    EC2_status(16, ec2)


def EC2_status(desired_status, ec2=None,
               instance_id=main_work_ec2_instance_id):
    if (ec2 is None):
        ec2 = boto3.client('ec2')

    #     0 : pending
    #     16 : running
    #     32 : shutting-down
    #     48 : terminated
    #     64 : stopping
    #     80 : stopped

    #     instance_info = ec2.describe_instances(InstanceIds=[instance_id])
    #     support_json.jdump(instance_info, 'instance_info', logger=logger.warning)

    cur_status = 0
    status_check_ctr = 0
    while (cur_status != desired_status):
        instance_info = ec2.describe_instances(InstanceIds=[instance_id])
        #         support_json.jdump(instance_info, 'instance_info', logger=logger.warning)

        cur_status = instance_info['Reservations'][0]['Instances'][0]['State']['Code']

        delay = 1
        time.sleep(delay)
        status_check_ctr = status_check_ctr + 1
        logger.warning('status_check_ctr, delay, cur_status:%s,%s,%s', status_check_ctr, delay, cur_status)

    time.sleep(5)


def reboot_EC2_main(ec2=None,
                    instance_id=main_work_ec2_instance_id):
    if (ec2 is None):
        ec2 = boto3.client('ec2')

    try:
        ec2.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            logger.warning("You don't have permission to reboot instances.")
            raise

    try:
        response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        support_json.jdump(response, 'reboot_instances', logger=logger.warning)
    except ClientError as e:
        logger.warning('Error:\n%s', e)


def stop_start_reboot_stop():
    """
    Testing Across feasible states
    note first reboot gives error because can not reboot when machined is stopped
    """
    ec2_cur = boto3.client('ec2')
    stop_EC2_main(ec2=ec2_cur)
    reboot_EC2_main(ec2=ec2_cur)
    start_EC2_main(ec2=ec2_cur)
    reboot_EC2_main(ec2=ec2_cur)
    stop_EC2_main(ec2=ec2_cur)


def get_public_dns(ec2=None,
                   instance_id=main_work_ec2_instance_id):
    ec2_descs = ec2.describe_instances(InstanceIds=[instance_id])
    support_json.jdump(ec2_descs, 'ec2_descs', logger=logger.warning)
    PublicDnsName = ec2_descs['Reservations'][0]['Instances'][0]['PublicDnsName']
    PublicIpAddress = ec2_descs['Reservations'][0]['Instances'][0]['PublicIpAddress']
    KeyName = ec2_descs['Reservations'][0]['Instances'][0]['KeyName']

    instance_info = {'PublicDnsName': PublicDnsName,
                     'PublicIpAddress': PublicIpAddress,
                     'KeyName': KeyName}

    support_json.jdump(instance_info, 'instance_info', logger=logger.warning)

    return instance_info


def get_pem_key(KeyName, ec2=None, instance_id=main_work_ec2_instance_id):
    cur_directory = os.path.dirname(os.path.realpath(__file__))
    cur_directory = cur_directory.replace('\\', '/')
    pem_key = cur_directory + '/pem/' + KeyName + '.pem'
    logger.warning(pem_key)

    return pem_key


def scp_link(user_name='ec2-user', ec2=None,
             instance_id=main_work_ec2_instance_id,
             local_source_folder='',
             remote_dest_folder=''):
    """
    Local SCP, send from current local computer to remote EC2 machine
    
    LOCALPEM="C:/Users/fan/Documents/Dropbox (UH-ECON)/Programming/AWS/fan_wang-key-pair-us_east_nv.pem"
    REMOTEIP=ec2-user@52.201.242.139
    LOCALDOCKER=C:/Users/fan/docker
    LOCALAWS=C:/Users/fan/.aws
    
    scp -i "$LOCALPEM"  $LOCALAWS/credentials $REMOTEIP:~/.aws/credentials
    scp -i "$LOCALPEM"  $LOCALAWS/config $REMOTEIP:~/.aws/config
    
    scp -i "$LOCALPEM"  $LOCALDOCKER/Dockerfile $REMOTEIP:~/docker/Dockerfile
    scp -i "$LOCALPEM"  $LOCALDOCKER/execution-assume-role.json $REMOTEIP:~/docker/execution-assume-role.json
    scp -i "$LOCALPEM"  $LOCALDOCKER/fancondajmp-task-def.json $REMOTEIP:~/docker/fancondajmp-task-def.json
    scp -i "$LOCALPEM"  $LOCALDOCKER/docker-compose.yml $REMOTEIP:~/docker/docker-compose.yml
    scp -i "$LOCALPEM"  $LOCALDOCKER/ecs-params.yml $REMOTEIP:~/docker/ecs-params.yml    
    """

    local_source_folder = local_source_folder.replace('\\', '/')

    instance_info = get_public_dns(ec2, instance_id)
    pem_key = get_pem_key(instance_info['KeyName'], ec2=ec2, instance_id=instance_id)

    '''ec2-user@54.175.121.15'''
    remoteip = user_name + '@' + instance_info['PublicIpAddress']

    scp_dict = {'prefix': "scp -o StrictHostKeyChecking=accept-new -i",
                'pem_key': pem_key,
                'remoteip': remoteip}

    local_scp_command = scp_dict['prefix'] + ' ' \
                        + scp_dict['pem_key'] + ' ' \
                        + local_source_folder + ' ' \
                        + scp_dict['remoteip'] + ':' + remote_dest_folder

    support_json.jdump(scp_dict, 'scp_dict', logger=logger.warning)
    support_json.jdump(local_scp_command, 'local_scp_command', logger=logger.warning)

    return local_scp_command


def ssh_link(user_name='ec2-user', ec2=None,
             instance_id=main_work_ec2_instance_id):
    """    
    LOCALPEM="C:/Users/fan/Documents/Dropbox (UH-ECON)/Programming/AWS/fan_wang-key-pair-us_east_nv.pem"
    IPADD=18.212.120.176
    REMOTEIP=ec2-user@$IPADD
    ssh-keygen -R $IPADD
    ssh -i "$LOCALPEM" $REMOTEIP
    sudo yum install htop
    """

    instance_info = get_public_dns(ec2, instance_id)
    pem_key = get_pem_key(instance_info['KeyName'], ec2=ec2, instance_id=instance_id)

    '''ec2-user@54.175.121.15'''
    remoteip = user_name + '@' + instance_info['PublicIpAddress']

    ssh_dict = {'prefix': "ssh -i",
                'pem_key': pem_key,
                'remoteip': remoteip}

    local_ssh_command_1 = 'ssh-keygen -R ' + instance_info['PublicIpAddress']
    local_ssh_command_2 = ssh_dict['prefix'] + ' "' + ssh_dict['pem_key'] + '" ' + ssh_dict['remoteip']

    local_ssh_command = [local_ssh_command_1, local_ssh_command_2]

    support_json.jdump(local_ssh_command, 'local_ssh_command', logger=logger.warning)

    return local_ssh_command


if __name__ == "__main__":
    ec2_cur = boto3.client('ec2')
    # stop_EC2_main(ec2=ec2_cur)
    # reboot_EC2_main(ec2=ec2_cur)
    start_EC2_main(ec2=ec2_cur)
    # get_public_dns(ec2=ec2_cur)
    # ssh_link(ec2=ec2_cur)
    # scp_link(ec2=ec2_cur)
