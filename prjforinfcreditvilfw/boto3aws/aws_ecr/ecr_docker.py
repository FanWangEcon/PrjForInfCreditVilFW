'''
Created on Jun 4, 2018

@author: fan

Generate Docker Image, Update Using Amazon Send Message. 
'''

import base64
import logging
import os
import pyfan.amto.json.json as support_json
import time
from time import gmtime, strftime

import boto3aws.aws_ec2.ec2_manage as boto3ec2
import boto3aws.tools.commandline as commandline
import boto3aws.tools.manage_aws as boto3aws

logger = logging.getLogger(__name__)


def get_docker_image_name(dockerfilename):
    # fancondajmp is the default ECR Repository Name
    # https://us-east-1.console.aws.amazon.com/ecr/repositories?region=us-east-1
    docker_img_name = 'fancondajmp'
    if dockerfilename == 'DockerfileCondaPyFan':
        docker_img_name = 'fanconda'
    elif dockerfilename == 'DockerfileMiniconda':
        docker_img_name = 'fanminicondajmp'

    return docker_img_name


def install_docker(aim_type='amazon_linux'):
    """
    If EC2 does not have docker, install docker on remote machine
    """

    if (aim_type == "amazon_linux"):
        pass
    if (aim_type == "ubuntu"):
        #         sudo apt-get update
        #         sudo apt install docker.io
        #         sudo service docker start
        #         sudo usermod -a -G docker ubuntu
        #         sudo reboot
        #         docker info
        pass


def clean_docker_folder(ssm, instance_id):
    """
    If EC2 does not have docker, install docker on remote machine
    
    Make directory and remove existing contents    
    """
    commands = 'rm -r ~/docker/*'
    commands = 'rm /home/ec2-user/docker/Dockerfile'
    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=[commands],
                                              instance_ids=[instance_id])
    support_json.jdump(returns, 'ssm', logger=logger.warning)

    return returns


def docker_start(ssm, instance_id):
    commands = "sudo service docker start"
    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=[commands],
                                              instance_ids=[instance_id])


def build_docker(ssm, instance_id, dockerfilename):
    """
    """
    logger.warning('start build_docker:%s, id:%s', dockerfilename, instance_id)

    docker_start(ssm, instance_id)

    docker_img_name = get_docker_image_name(dockerfilename)

    CACHE_DATE_NEW = strftime("%Y-%m-%d-%H-%M-%S", gmtime())

    c_cd = 'cd /home/ec2-user/docker'
    c_docker_build = 'docker build -t ' + docker_img_name + ' --build-arg CACHE_DATE=' + CACHE_DATE_NEW + ' .'
    c_docker_prune = 'docker system prune --force'
    commands_list = [c_cd, c_docker_build, c_docker_prune]

    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=commands_list,
                                              instance_ids=[instance_id])

    logger.warning('finished build_docker:%s, id:%s', dockerfilename, instance_id)

    return returns


def update_docker_file_scp(ec2, instance_id,
                           dockerfilename='DockerfileConda'):
    """
    LOCALPEM="C:/Users/fan/Documents/Dropbox (UH-ECON)/Programming/AWS/fan_wang-key-pair-us_east_nv.pem"
    REMOTEIP=ec2-user@54.175.121.15    
    scp -i "$LOCALPEM"  $LOCALDOCKER/Dockerfile $REMOTEIP:~/docker/Dockerfile
    
    Parameters
    ----------
    container_name: string
        name follows docker files in container folder
    """
    logger.warning('start update_docker_file_scp:%s, id:%s', dockerfilename, instance_id)

    cur_directory = os.path.dirname(os.path.realpath(__file__))
    cur_directory = cur_directory.replace('\\', '/')

    local_source_docker = cur_directory + '/container/' + dockerfilename
    remote_dest_docker = '~/docker/Dockerfile'

    scp_command = boto3ec2.scp_link(ec2=ec2,
                                    instance_id=instance_id,
                                    local_source_folder=local_source_docker,
                                    remote_dest_folder=remote_dest_docker)

    # Execute Local SCP Command 
    commandline.commandline_local(scp_command)

    logger.warning('end update_docker_file_scp:%s, id:%s', dockerfilename, instance_id)

    return scp_command


def update_ecr(ssm, instance_id, dockerfilename):
    """
    Struggled with this a lot, 
    Learned about 64 bit encoding commonly used to transfer password username
    data 
    """
    logger.warning('start update_ecr:%s, id:%s', dockerfilename, instance_id)

    """
    Docker start
    """
    docker_start(ssm, instance_id)

    """
    Create Registry if does not exist
    """

    docker_img_name = get_docker_image_name(dockerfilename)
    try:
        client = boto3aws.start_boto3_client('ecr')
        response = client.create_repository(repositoryName=docker_img_name)
        support_json.jdump(response, 'ecr-create_repository', logger=logger.warning)
    except:
        logger.warning('repository %s already exists', docker_img_name)

    """
    Tag
    """

    c_cd = 'cd /home/ec2-user/docker'
    docker_tag = 'docker tag ' + docker_img_name + ' ' + boto3aws.aws_keys()[
        'main_aws_id'] + '.dkr.ecr.us-east-1.amazonaws.com/' + docker_img_name
    commands_list = [c_cd, docker_tag]

    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=commands_list,
                                              instance_ids=[instance_id])

    """
    ECR Docker Log in
    """
    # Get Token
    response = client.get_authorization_token(registryIds=[boto3aws.aws_keys()['main_aws_id']])
    support_json.jdump(response, 'get_authorization_token', logger=logger.warning)
    # Transfered over with 64 bit encoding    
    authorizationToken64encoded = response['authorizationData'][0]['authorizationToken']
    decoded_byte = base64.b64decode(authorizationToken64encoded)
    decoded_string = decoded_byte.decode("utf-8")

    decoded_name_pass = decoded_string.split(":")
    login_full = 'docker login -u ' + decoded_name_pass[0] + ' -p ' + decoded_name_pass[1] + \
                 ' https://' + boto3aws.aws_keys()['main_aws_id'] + '.dkr.ecr.us-east-1.amazonaws.com'

    #     get_authorization_token = 'aws ecr get-login --no-include-email --region us-east-1'
    #     login_full = commandline.commandline_aws_ec2(client=ssm,
    #                                               commands=[get_authorization_token],
    #                                               instance_ids=[instance_id])

    # log in
    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=[login_full],
                                              instance_ids=[instance_id])

    """
    Docker Push
    """
    docker_push = 'docker push ' + boto3aws.aws_keys()[
        'main_aws_id'] + '.dkr.ecr.us-east-1.amazonaws.com/' + docker_img_name
    commands_list = [docker_push]
    returns = commandline.commandline_aws_ec2(client=ssm,
                                              commands=commands_list,
                                              instance_ids=[instance_id])

    logger.warning('finished update_ecr:%s, id:%s', dockerfilename, instance_id)


def docker_start_to_push(ec2=None, ssm=None, dockerfilename='DockerfileConda'):
    """Update Docker File To Have Latest Code
    1. ssm request: rm /home/ec2-user/docker/Dockerfile, faile if does not exist
    2.
    scp -o StrictHostKeyChecking=accept-new
        -i C:/Users/fan/Documents/Dropbox (UH-ECON)/repos/ThaiJMP/boto3aws/aws_ec2/pem/fan_wang-key-pair-us_east_nv.pem
        C:/Users/fan/Documents/Dropbox (UH-ECON)/repos/ThaiJMP/boto3aws/aws_ecr/container/DockerfileConda
        ec2-user@18.209.162.71:~/docker/Dockerfile

    """
    instance_id = boto3ec2.main_work_ec2_instance_id

    if (ec2 is None):
        ec2 = boto3aws.start_boto3_client('ec2')
    if (ssm is None):
        ssm = boto3aws.start_boto3_client('ssm')

    # """
    # Step 1 and 2 usually not needed, but can invoke anyway
    # """

    # 1. Clean Folder of Existing Dockerfile
    # sucessfully delets the Dockerfile inside the docker folder under EC2 root
    res = clean_docker_folder(ssm=ssm, instance_id=instance_id)
    # 2. Update via SCP local to remote docker file (usually no changes)
    update_docker_file_scp(ec2=ec2, instance_id=instance_id,
                           dockerfilename=dockerfilename)
    # 3. Essential: Build docker, this will update via git the git files, essential step
    build_docker(ssm=ssm, instance_id=instance_id,
                 dockerfilename=dockerfilename)
    # 4. Essential: Send remote EC2 built docker file to ECR so Fargate can access
    update_ecr(ssm=ssm, instance_id=instance_id,
               dockerfilename=dockerfilename)


if __name__ == "__main__":
    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    startTime = time.time()

    ec2_cur = boto3aws.start_boto3_client('ec2')
    ssm_cur = boto3aws.start_boto3_client('ssm')

    # re-start EC2 instance
    # boto3ec2.start_EC2_main(ec2=ec2_cur)
    # Sleep for five seconds
    # time.sleep(3)
    # ECR update
    dockerfilename = 'DockerfileConda'
    # dockerfilename = 'DockerfileCondaPyFan'
    docker_start_to_push(ec2=ec2_cur, ssm=ssm_cur, dockerfilename=dockerfilename)
    boto3ec2.stop_EC2_main(ec2=ec2_cur)

    t = time.time() - startTime
    logger.warning('Time Used: %s', t)
    print('Time Used:', str(t))
