# Updating and Pushing New Container. 

- run boto3aws.aws_ec2.ec2_manage.start_EC2_main() to start EC2
- run boto3aws.aws_ecr.ecr_docker.docker_start_to_push() to push to ECR, decide which Container to push

When pushing to new ecr, specify: dockerfilename='DockerfileCondaPyFan' below, this determines which file in C:\Users\fan\ThaiJMP\boto3aws\aws_ecr\container to use 
- docker_start_to_push(ec2=ec2_cur, ssm=ssm_cur, dockerfilename='DockerfileCondaPyFan')
see: boto3aws.aws_ecr.ecr_docker.get_docker_image_name() function to determine what is the name that will appear in ECR.

check: https://us-east-1.console.aws.amazon.com/ecr/repositories?region=us-east-1#