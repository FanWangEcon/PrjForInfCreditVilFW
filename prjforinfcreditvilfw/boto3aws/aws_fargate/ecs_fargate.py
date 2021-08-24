'''
Created on Jun 5, 2018

@author: fan

Start Fargate services


If a subnet's traffic is routed to an internet gateway, the subnet is known as a public subnet
'''
import logging
import pyfan.amto.json.json as support_json

import boto3aws.aws_ecr.ecr_docker as botodocker
import boto3aws.tools.manage_aws as boto3aws
import boto3aws.tools.support as aws_sup
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec

logger = logging.getLogger(__name__)


def gen_task_dict(combo_type, speckey,
                  cpu, memory,
                  graph_panda_list_name='',
                  save_directory_main='',
                  ge='', multiprocess='', estimate='',
                  dockerfilename='DockerfileConda'):
    """
    Specify memory in binary

    Parameters
    ----------
    combo_type: list of strings
        =['a', '20180529_A', 'data_param.A']
    ge: string
        --ge or nothing (default no ge)
    multiproces: string
        --multiproces or nothing (default no multi)
    """

    compute_spec_key = estispec.compute_esti_spec_combine(spec_key=speckey, action='compute_spec_key')
    compute_specs = computespec.compute_set(compute_spec_key)
    speckey_strip = estispec.compute_esti_spec_combine(spec_key=speckey, action='strip')

    if (cpu is None):
        cpu = compute_specs['cpu']
    if (memory is None):
        memory = compute_specs['memory']

    combo_type_dash = []
    for ctr, list_ele in enumerate(combo_type):
        if (list_ele is None):
            combo_type_dash.append('None')
        elif (isinstance(list_ele, int)):
            combo_type_dash.append(str(list_ele))
        elif (isinstance(list_ele, list)):
            combo_type_dash.append(''.join(list_ele).replace("_", "-"))
        else:
            combo_type_dash.append(list_ele.replace("_", "-"))

    combo_type_file = combo_type_dash[0]
    combo_type_date_param = combo_type_dash[1]
    combo_type_param = combo_type_dash[2]
    param_combo_select_ctr = combo_type_dash[3]

    if (combo_type_param == 'None'):
        if (estimate.strip() == '--esti'):
            container_name = 'esti-' + speckey_strip + '-' + combo_type_file + '-' + combo_type_date_param
        else:
            container_name = 'simu-' + speckey_strip + '-' + combo_type_file + '-' + combo_type_date_param
    else:
        container_name = combo_type_param.split('.')[0] + '-' + combo_type_param.split('.')[1]

    family = combo_type_file + '-' + combo_type_date_param
    if (param_combo_select_ctr != 'None'):
        family = family + '-' + param_combo_select_ctr
    family = family + estimate.strip()
    family = family + '--' + speckey_strip
    family = family + ge.strip()
    family = family + multiprocess.strip()
    #     family = family + multiprocess.strip()
    family = family + '-c' + cpu
    family = family + 'm' + memory

    family = aws_sup.limit_batch_job_def_name(family)

    awslogs_opts = {"awslogs-group": container_name,
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": family}

    '''
    Parsing paramtype.paramname list
    '''
    if (combo_type[2] is None):
        combo_type_2 = 'None'
    elif (isinstance(combo_type[2], list)):
        # list like: ['data_param.A', 'esti_param.beta']
        # convert to string: data_param.A esti_param.beta
        # run.py parses this string with space as list and returns list line in line 1
        combo_type_2 = " ".join(combo_type[2])
    else:
        raise ('Bad combo_type[2] input, not list, not None')

    if (combo_type[3] is None):
        combo_type_3 = 'None'
    else:
        combo_type_3 = str(combo_type[3])

    # container definition is one of the keys, other apply to entire task
    task_def = {"family": family,
                "networkMode": "awsvpc",
                "containerDefinitions": [
                    {
                        "name": container_name,
                        "image": boto3aws.aws_keys()['main_aws_id'] + ".dkr.ecr." +
                                 boto3aws.aws_keys()['region'] + ".amazonaws.com/" +
                                 botodocker.get_docker_image_name(dockerfilename),
                        "portMappings": [
                            {
                                "containerPort": 80,
                                "hostPort": 80,
                                "protocol": "tcp"
                            }
                        ],
                        "essential": True,
                        "entryPoint": [
                            "sh",
                            "-c"
                        ],
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": awslogs_opts
                        },
                        "command": ["python /ThaiJMP/invoke/run.py" +
                                    " -A " + speckey + \
                                    " -B " + combo_type[0] + \
                                    " -C " + combo_type[1] + \
                                    " -D " + combo_type_2 + \
                                    " -E " + combo_type_3 + \
                                    " -F " + graph_panda_list_name + \
                                    " -G " + save_directory_main + \
                                    " " + ge + multiprocess + estimate
                                    ]
                    }
                ],
                "requiresCompatibilities": [
                    "FARGATE"
                ],

                "cpu": cpu,  # x1024 as well
                "memory": memory,  # x1024
                "executionRoleArn": "arn:aws:iam::" + boto3aws.aws_keys()['main_aws_id'] + ":role/" +
                                    boto3aws.aws_keys()['fargate_task_executionRoleArn']
                }

    #     256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
    #     512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
    #     1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
    #     2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
    #     4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

    support_json.jdump(task_def, 'task_def', logger=logger.warning)

    return task_def, awslogs_opts


def show_all_ask_def(ecs):
    """
    All Task Definitions
    """
    #     response = client.list_task_definition_families(familyPrefix='a-',status='ALL')
    response = ecs.list_task_definition_families(status='ALL')
    support_json.jdump(response, 'describe_task_definition', logger=logger.info)
    task_definition_list = response['families']

    for task_definition in task_definition_list:
        response = ecs.describe_task_definition(taskDefinition=task_definition)
        support_json.jdump(response, 'describe_task_definition, '
                           + task_definition
                           + ':', logger=logger.info)


def start_cluster(ecs, clusterName):
    """
    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/get-started-ipv6.html

    0. Tutorial: Creating a VPC with Public and Private Subnets for Your Clusters
        https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-public-private-vpc.html
    1. Scenario 1: VPC with a Single Public Subnet
        https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario1.html
    2. Scenario 2: VPC with Public and Private Subnets (NAT):
        https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario2.html

    1. Delete your security group:
        aws ec2 delete-security-group --group-id sg-e1fb8c9a
    2. Delete your subnets:
        aws ec2 delete-subnet --subnet-id subnet-b46032ec
        aws ec2 delete-subnet --subnet-id subnet-a46032fc
    3. Delete your custom route table:
        aws ec2 delete-route-table --route-table-id rtb-c1c8faa6
        Detach your Internet gateway from your VPC:
    4. aws ec2 detach-internet-gateway --internet-gateway-id igw-1ff7a07b --vpc-id vpc-2f09a348
        Delete your Internet gateway:
    5. aws ec2 delete-internet-gateway --internet-gateway-id igw-1ff7a07b
        Delete your VPC:
        aws ec2 delete-vpc --vpc-id vpc-2f09a348

    After starting cluster
    Can launch fargate into cluster.
    That requires a subnet id and a security group
    Subnet id is key, the subnet could be a public subnet or priviate.
    Ahead of time, create VPC group either with just public ID.
    or VPC group with both public and private ID which allows us to put cluster in private subnet
        so that cluster operations and data are hidden from internet.
        but cluster in private subnet communicates with public subnet using NAT gateway
        then public subnet communicates with outside world
        that has added NAT cost, could be expensive.
    If launch cluster in public subnet, can directly communicate with internet,
        meaning can download coontainer from ECR or docker etc and no NAT cost.
        can still restrict traffic through security group settings for who can
        enter the public subnet cluster.
        - Note in subnet section under VPC gui page, need to chose SUBNET ACTION
            and auto-assign public IP (i think this is assinging public IP to
            container for cluster, so the container in the -public subnet
            can communicate with the outside.
    See: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-public-private-vpc.html
    """

    response = ecs.create_cluster(clusterName=clusterName)
    support_json.jdump(response, 'create_cluster', logger=logger.info)

    clusterArn = response['cluster']['clusterArn']

    """
    Multiple approaches:
    to generate a cluster with vpc security group and subnet directly, can use:
        ecs-cli up, this means I do not have to figure out which existing vpc, security group,
        subnet to use. Are the subnets generated public or private?

            ecs-cli up \
                --cluster-config fanFargate \
                --force
            output:
                cluster=fanCluster region=us-east-1
                    VPC created: vpc-6c8b8217
                    Subnet created: subnet-55ed2509
                    Subnet created: subnet-0af82f6d
                    Cluster creation succeeded.
    """

    return clusterArn


def show_clusters(ecs):
    current_clusters = ecs.list_clusters()['clusterArns']
    support_json.jdump(current_clusters, 'current_clusters', logger=logger.info)


def add_task_def(ecs, logs,
                 combo_type, speckey,
                 cpu, memory,
                 graph_panda_list_name,
                 save_directory_main,
                 ge, multiprocess, estimate,
                 dockerfilename='DockerfileConda'):
    """
    aws ecs register-task-definition --cli-input-json file://$HOME/docker/fancondajmp-task-def.json
    """

    """
    A. Generate Task fields
    """
    task_dict, awslogs_opts = gen_task_dict(combo_type, speckey,
                                            cpu, memory,
                                            graph_panda_list_name=graph_panda_list_name,
                                            save_directory_main=save_directory_main,
                                            ge=ge, multiprocess=multiprocess, estimate=estimate,
                                            dockerfilename=dockerfilename)

    family = task_dict['family']
    command = task_dict['containerDefinitions'][0]['command'][0]
    if (cpu is None):
        cpu = task_dict['cpu']
    if (memory is None):
        memory = task_dict['memory']

    """
    B. Add Log Group, required
    """
    try:
        cloudwatchlog = logs.create_log_group(logGroupName=awslogs_opts['awslogs-group'])
        support_json.jdump(cloudwatchlog, 'cloudwatchlog, awslogs-group'
                           + awslogs_opts['awslogs-group']
                           + ':', logger=logger.info)
    except:
        logger.info('Log group %s already exists.', awslogs_opts['awslogs-group'])

    """
    C. Check if definition exists with identical fields
    """

    update_task = True
    try:
        response = ecs.describe_task_definition(taskDefinition=task_dict['family'])
        support_json.jdump(response, 'describe_task_definition, family'
                           + family
                           + ':', logger=logger.info)
        taskDefinition = response['taskDefinition']
        containerDefinitions = response['taskDefinition']['containerDefinitions'][0]

        cur_command = containerDefinitions['command'][0]
        cur_memory = taskDefinition['memory']
        cur_cpu = taskDefinition['cpu']

        logger.info('cur_command:\n%s', cur_command)
        logger.info('command:\n%s', command)
        logger.info('cur_memory:\n%s', cur_memory)
        logger.info('memory:\n%s', memory)
        logger.info('cur_cpu:\n%s', cur_cpu)
        logger.info('cpu:\n%s', cpu)

        if (cur_command == command and
                cur_memory == (memory) and
                cur_cpu == cpu):
            update_task = False
            logger.info('Task with same memory and cpu and command exists already')

    except Exception:
        logger.info('Task definition family does not exist yet: %s', task_dict['family'])

    #     update_task = True

    """
    C. Add New Definition
    """
    if (update_task):
        response = ecs.register_task_definition(
            family=family,
            executionRoleArn=task_dict['executionRoleArn'],
            networkMode=task_dict['networkMode'],
            memory=memory,
            cpu=cpu,
            requiresCompatibilities=task_dict['requiresCompatibilities'],
            containerDefinitions=task_dict['containerDefinitions']
        )
        support_json.jdump(response, 'register_task_definition--response', logger=logger.info)

    return family


#     response = client.delete_cluster(cluster='fanFargateMain')
#     support_json.jdump(response, 'delete_cluster', logger=logger.info)

def run_task_on_fargate(ecs, task_family,
                        clusterName='fanFargateMain'):
    """
    aws ecs run-task \
    --cluster fanFargateMain \
    --task-definition b-20180521-LENDFC:1 \
    --count 1 \
    --launch-type "FARGATE" \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-d9abbe82],securityGroups=[sg-e6642399]}"
    """

    '''
    public ip enable key!!!
    '''
    networkConfiguration = {'awsvpcConfiguration':
                                {'subnets': [boto3aws.aws_keys()['fargate_public_subnet']],
                                 'securityGroups': [boto3aws.aws_keys()['fargate_security_group']],
                                 'assignPublicIp': 'ENABLED'
                                 }
                            }

    response = ecs.run_task(
        cluster=clusterName,
        taskDefinition=task_family,
        count=1,
        launchType='FARGATE',
        networkConfiguration=networkConfiguration)
    support_json.jdump(response, 'register_task_definition--response', logger=logger.info)


def ec2_cluster():
    response = ec2_client.run_instances(
        # Use the official ECS image
        ImageId="ami-8f7687e2",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config"
    )


def sample_task_defs():
    response = ecs_client.register_task_definition(
        containerDefinitions=[
            {
                "name": "wordpress",
                "links": [
                    "mysql"
                ],
                "image": "wordpress",
                "essential": True,
                "portMappings": [
                    {
                        "containerPort": 80,
                        "hostPort": 80
                    }
                ],
                "memory": 300,
                "cpu": 10
            },
            {
                "environment": [
                    {
                        "name": "MYSQL_ROOT_PASSWORD",
                        "value": "password"
                    }
                ],
                "name": "mysql",
                "image": "mysql",
                "cpu": 10,
                "memory": 300,
                "essential": True
            }
        ],
        family="hello_world"
    )


if __name__ == "__main__":

    FORMAT = '%(filename)s - %(funcName)s - %(lineno)d -  %(asctime)s - %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    ecs = boto3aws.start_boto3_client('ecs')
    logs = boto3aws.start_boto3_client('logs')

    clusterName = 'fanFargateMain'
    dockerfilename = 'DockerfileConda'
    start_cluster(ecs, clusterName=clusterName)

    combo_type_list = [['a', '20180529_A', 'data_param.A'],
                       ['b', '20180521_LENDFC', 'esti_param.BNI_LEND_P']]

    graph_panda_list_name = 'main_graphs'

    ge_list = ['', ' --ge']
    multiprocess = ' --multiprocess'
    cpu = str(1024 * 4)
    memory = str(1024 * 9)
    combo_type_A, combo_type_B_group = 'a', '20180607'
    combo_type_1 = [combo_type_A, combo_type_B_group + '_alphak', 'esti_param.alpha_k']
    combo_type_2 = [combo_type_A, combo_type_B_group + '_beta', 'esti_param.beta']
    combo_type_3 = [combo_type_A, combo_type_B_group + '_depre', 'esti_param.K_DEPRECIATION']
    combo_type_4 = [combo_type_A, combo_type_B_group + '_rho', 'esti_param.rho']
    combo_type_5 = [combo_type_A, combo_type_B_group + '_rinfor', 'esti_param.R_INFORM_SAVE']
    combo_type_6 = [combo_type_A, combo_type_B_group + '_logitsd', 'esti_param.logit_sd_scale']

    combo_type_7 = [combo_type_A, combo_type_B_group + '_A', 'data_param.A']
    combo_type_8 = [combo_type_A, combo_type_B_group + '_stdeps', 'grid_param.std_eps']

    combo_type_9 = [combo_type_A, combo_type_B_group + '_vfimax', 'interpolant.maxinter']

    combo_type_list = [combo_type_1, combo_type_2, combo_type_3,
                       combo_type_4, combo_type_5, combo_type_6,
                       combo_type_7, combo_type_8, combo_type_9]

    #     combo_type_list = [combo_type_4, combo_type_6, combo_type_9]

    """
    No Parallel needed, no equilibrium to solve for over parameter value...
    hmmming, actually there is.
    """
    ge_list = ['', ' --ge']
    multiprocess = ''
    cpu = str(1024 * 2)
    memory = str(1024 * 16)  # 2 cpu: Min. 4GB and Max. 16GB, in 1GB increments
    combo_type_A, combo_type_B_group = 'a', '20180607'
    combo_type_1 = [combo_type_A, combo_type_B_group + '_lenstates', 'grid_param.len_states']
    combo_type_2 = [combo_type_A, combo_type_B_group + '_lenchoice', 'grid_param.len_choices']
    combo_type_3 = [combo_type_A, combo_type_B_group + '_maxstdcoh', 'grid_param.max_steady_coh']
    combo_type_4 = [combo_type_A, combo_type_B_group + '_markovpts', 'grid_param.markov_points']
    combo_type_list = [combo_type_1, combo_type_2, combo_type_3, combo_type_4]
    combo_type_list = [combo_type_1, combo_type_2]

    #     combo_type_list = [['a', '20180529_A', 'data_param.A']]

    estimate = '--esti'
    for ge in ge_list:
        for cur_combo in combo_type_list:
            combo_type = cur_combo
            family = add_task_def(ecs, logs, combo_type,
                                  graph_panda_list_name,
                                  ge, multiprocess, estimate,
                                  dockerfilename=dockerfilename,
                                  cpu=cpu, memory=memory)
            run_task_on_fargate(ecs, task_family=family, clusterName=clusterName)
