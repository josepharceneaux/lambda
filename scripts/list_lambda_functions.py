#! /usr/bin/env python3


import os
import sys
import shutil
import subprocess
import re
import zipfile
import datetime
import requests
import boto3
import argparse


LAMBDA_CLIENT = boto3.client('lambda')
S3_RESOURCE = boto3.resource('s3')

# The S3 bucket we'll install the zip file into
LAMBDA_BUCKET_NAME = "www.arceneaux.me"

# The AWS region. Need to parameterize this.
# AWS_REGION = "us-east-1"
# AWS_REGION = "us-west-2"
US_REGIONS = [ "us-west-1", "us-west-2", "us-east-1", "us-east-2" ]

def validate_response(response, operation=None, code=requests.codes.OK):
    """
    If the request didn't return CODE, bail
    :param dict response: Response from AWS client call.
    :param code HTTP status code expected
    :param operation Descriptive name of what we were trying to do
    """
    if response and u'ResponseMetadata' in response and u'HTTPStatusCode' in response[u'ResponseMetadata']:
        if response[u'ResponseMetadata'][u'HTTPStatusCode'] != code:
            print("Operation {} not OK: Status: {} Full Response: {}".format(operation, response[u'ResponseMetadata'][u'HTTPStatusCode'], response))
            sys.exit(1)

    else:
        print("API call: {} Malformatted AWS response: {}".format(operation, response))
        sys.exit(1)


def list_functions():
    """
    """

    # response = LAMBDA_CLIENT.list_functions(MasterRegion=AWS_REGION, FunctionVersion='ALL', Marker='NextPage', MaxItems=256)
    # response = LAMBDA_CLIENT.list_functions(MasterRegion=AWS_REGION, FunctionVersion='ALL', MaxItems=256)

    for region in US_REGIONS:
        print("Searching region {} ... ".format(region), end='')
        response = LAMBDA_CLIENT.list_functions(MasterRegion=region, FunctionVersion='ALL', MaxItems=256)
        validate_response(response, "list_lambda_functions")
        function_list = response['Functions']
        print("{} Functions".format(len(function_list)))

if __name__ == "__main__":
    print("All Lambda functions")
    list_functions()
else:
    fatal("Error: intended to run locally")
