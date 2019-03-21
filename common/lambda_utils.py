import requests
import datetime
import boto3
import botocore
import time
import os
import json


S3 = boto3.resource('s3')
S3_CLIENT = boto3.client('s3') 
LAMBDA_CLIENT = boto3.client('lambda')
LOGS_CLIENT = boto3.client('logs')
API_CLIENT = boto3.client('apigateway')

def deploy(function_name_list, lambda_alilas='STAGING', description=None):
    """
    Upload a zipfile of Lambda code to our S3 bucket, publish the version, and attach our staging aliases.
    """
    datetime_string = str(datetime.datetime.utcnow())

    combined_function_names = '_and_'.join(function_name_list)
    s3_key_path = "{}/{}".format(function_name_list, datetime_str)
    s3_bucket = s3.Bucket(S3_DEPLOYMENT_BUCKET)

    print("Uploading deployment zipfile {} to S3 into {}/{}".format(LATEST_DEPLOYMENT_FILE_PATH,
                                                                    s3_bucket,
                                                                    s3_key_path))

    bucket = S3.bucket(S3_DEPLOYMENT_BUCKET)
    bucket.upload_file(LATEST_DEPLOYMENT_FILE_PATH, s3_key_path, Callback=None)

    for name in function_name_list:
        print('Deploying {}:'.format(function_name))
        response = LAMBDA_CLIENT.update_function_code(FunctionName=name, S3Bucket=bucket, S3Key=s3_key_path, Publish=True)

        validate_response(response, requests.codes.OK, 'update_function_code')
        print("    {} code uploaded".format(name))
