import boto3
import invoke.boto3aws.aws_ec2.ec2_manage as boto3ec2
import invoke.boto3aws.aws_ecr.ecr_docker as botodocker

import logging

logger = logging.getLogger(__name__)

FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

instance_id = boto3ec2.main_work_ec2_instance_id
print(instance_id)
ec2_cur = boto3.client('ec2')
ssm_cur = boto3.client('ssm')

# # Start EC2
boto3ec2.start_EC2_main(ec2=ec2_cur)
# boto3ec2.reboot_EC2_main(ec2=ec2_cur)
# """
# Step 1 and 2 usually not needed, but can invoke anyway
# """
dockerfilename = 'DockerfileConda'
# 1. Clean Folder of Existing Dockerfile
res = botodocker.clean_docker_folder(ssm=ssm_cur, instance_id=instance_id)
# 2. Update via SCP local to remote docker file (usually no changes)
botodocker.update_docker_file_scp(ec2=ec2_cur, instance_id=instance_id,
                                  dockerfilename=dockerfilename)
# 3. Essential: Build docker, this will update via git the git files, essential step
botodocker.build_docker(ssm=ssm_cur, instance_id=instance_id,
                        dockerfilename=dockerfilename)
# 4. Essential: Send remote EC2 built docker file to ECR so Fargate can access
botodocker.update_ecr(ssm=ssm_cur, instance_id=instance_id,
                      dockerfilename=dockerfilename)

# Stop EC2
boto3ec2.stop_EC2_main(ec2=ec2_cur)

# ssh_command = boto3ec2.ssh_link(ec2=ec2_cur, instance_id=instance_id)
# print(ssh_command)

# scp -i C:\\Users\\fan\\ThaiJMP\\invoke\\boto3aws/pem/fan_wang-key-pair-us_east_nv.pem C:\\Users\\fan\\ThaiJMP\\invoke\\boto3aws/container/DockerfileConda ec2-user@54.221.154.196:~/docker/Dockerfile
