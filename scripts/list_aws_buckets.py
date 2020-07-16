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



S3_RESOURCE = boto3.resource('s3')


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


def list_buckets():
    """
    """
    buckets = None
    try:
        buckets = bucket_client.list_buckets()
    except Exception as e:
        print("Can't get buckets: {}".format(e))
        return None

    return buckets


if __name__ == "__main__":
    print("All Lambda functions")
    list_functions()
else:
    fatal("Error: intended to run locally")
