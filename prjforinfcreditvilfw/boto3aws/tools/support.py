
def limit_batch_job_def_name(job_def_name):
    """
        When generating batch job, aws throws errow if job name too long:
            botocore.errorfactory.ClientException: An error occurred (ClientException) 
            when calling the SubmitJob operation: Error executing request, Exception : 
                Job name should match valid pattern,
             RequestId: 2b840943-b750-11e8-827b-15f8ec75bcad
        specifically, according to this: https://github.com/nextflow-io/nextflow/issues/822
            needs to be less than 128 characters.
            
        Examples
        --------
        import boto3aws.tools.support as aws_sup
        job_def_name = aws_sup.limit_batch_job_def_name(job_def_name)
    """
    job_def_name_max_len = 120
    if (len(job_def_name) <= job_def_name_max_len):
        '''
        also see IOSupport:63
        '''            
        pass
    else:
        job_def_name_short = ''.join([l for l in job_def_name if l not in ['0',
                                                                    'a','e','i','o','u',
                                                                    'A','E','I','O','U']])
        job_def_name = job_def_name_short[:job_def_name_max_len]
        
    return job_def_name