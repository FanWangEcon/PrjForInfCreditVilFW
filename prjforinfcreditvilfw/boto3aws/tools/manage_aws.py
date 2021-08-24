'''
Created on Jun 5, 2018

@author: fan

Real ID and Keys have been deleted from the file below
'''

import boto3

def aws_keys():
    """

    Initiate VPC with public subnet and security group:
        - make sure user has proper access

    fargate_vpc_id: the vpc in which fargate task container resides
    fargate_public_subnet: the subnet into which I deploy the fargate task.
    fargate_security_group: security rules of fargate task deployed subnet
    """
    aws_general = {'main_aws_id':'XXXXXXXXXXXXX',
                   'aws_access_key_id':'XXXXXXXXXXXXXXXXXX',
                   'aws_secret_access_key':'XXXXXXXXXXXXXXXXXXXXXX',
                   'region':'us-east-1'}


    # ec2_main = {'main_ec2_instance_id':'i-06977cf6d5691a2da',
    #             'main_ec2_linux_ami':'ami-afd15ed0',
    #             'main_ec2_public_subnet':'subnet-d9abbe82'}

    # From AWS instance started using 2020-09
    ec2_main = {'main_ec2_instance_id':'XXXXXXXXXXXXXXXXXXXXX',
                'main_ec2_linux_ami':'XXXXXXXXXXXXXXXXXXXXX',
                'main_ec2_public_subnet':'subnet-XXXXXXXX'}

    """
    Fargate networking is same as normal VPC, it is just regular VPC.
        could configure so that we launch task in private or public subnet.
    if can not get container image, see:
        https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html
    """
    fargate_networking = {'fargate_vpc_name': 'FanCluster',
                          'fargate_vpc_id': 'vpc-fbf5e280',
                          'fargate_public_subnet':'subnet-XXXXXX',
                          'fargate_security_group':'sg-XXXXXXX',
                          'fargate_task_executionRoleArn':'ecsTaskExecutionRole',
                          'batch_task_executionRoleArn':'ecsExecutionRole',
                          'fargate_route_table':'rtb-XXXXXXXX'}

#     'fargate_task_executionRoleArn':'ecsExecutionRole'

    aws_keys = {}
    aws_keys.update(aws_general)
    aws_keys.update(ec2_main)
    aws_keys.update(fargate_networking)

    return aws_keys

def start_boto3_client(client_string):
    aws_keys_dict = aws_keys()

    client_out = boto3.client(client_string,
                              aws_access_key_id=aws_keys_dict['aws_access_key_id'],
                              aws_secret_access_key=aws_keys_dict['aws_secret_access_key'],
                              region_name=aws_keys_dict['region'])

    return client_out
