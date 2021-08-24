'''
Created on Jun 5, 2018

@author: fan
'''
import boto3

def start_boto3_client(client_string):
    
    client_out = boto3.client(client_string,
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key,
                              region_name=region)
    
    return client_out 