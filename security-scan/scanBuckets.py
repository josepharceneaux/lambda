__author__ = "Joseph Arceneaux joe.arceneaux@gmail.com"


import json
import boto3
from botocore.exceptions import ClientError


def get_statement_from_policy(policy):
    """
    Extract the Statement component from a bucket policy
    """
    if policy and 'Statement' in policy and len(policy['Statement']) > 0:
        return policy['Statement'][0]
    return None


def get_sid_string_from_policy(policy):
    """
    Extract the Sid component from a bucket policy
    """
    statement = get_statement_from_policy(policy)
    if statement and 'Sid' in statement:
        return statement['Sid']
    return None


def get_resource_from_policy(policy):
    """
    Extract the resource component from a bucket policy
    """
    statement = get_statement_from_policy(policy)
    if statement and 'Resource' in statement:
        return statement['Resource']
    return None


def fix_resource_if_needed(policy):
    """
    If the resource part of the policy, enforcing TLS to S3, applies to only the bucket or only its contents,
    change it to apply to both
    """
    resource_value = get_resource_from_policy(policy)
    if resource_value and type(resource_value) is str:
        new_resource_value = [resource_value]

        if resource_value.endswith('*'):
            # Addresses only the bucket content, add the bucket itself
            value2 = resource_value[0:-2]
        else:
            # Addresses only the bucket itself, so add its contents
            value2 = resource_value + "/*"

        new_resource_value.append(value2)
        return new_resource_value
        
    else:
        return None

    return resource_value


def fix_policy_if_needed(policy):
    """
    If the S3 bucket policy, enforcing TLS to S3, applies to only the bucket or only its contents,
    change it to apply to both
    """

    if 'Statement' in policy:
        for element in policy['Statement']:
            element['Resource'] = fix_resource_if_needed(policy)

        return policy
    else:
        return None


def print_bucket_names(buckets):
    """
    List all of our S3 buckets
    """
    bucket_list = buckets['Buckets']
    print("{} buckets:".format(len(bucket_list)))
    for b in bucket_list:
        print("    " + b['Name'])


def print_bucket_logging(buckets):
    """
    List all of our S3 buckets' logging status
    """
    bucket_list = buckets['Buckets']
    for b in bucket_list:
        try:
            logging = bucket_client.get_bucket_logging(Bucket=b['Name'])
        except Exception as e:
            status = "Can't get logging status: {}".format(e)
        else:
            if 'LoggingEnabled' in logging:
                status = "Logging enabled."
            else:
                status = "Logging disabled."

        print("    " + b['Name'] + " " + status)


def print_bucket_encryption(buckets):
    """
    List all of our S3 buckets' logging status
    """
    bucket_list = buckets['Buckets']
    for b in bucket_list:
        try:
            encryption = bucket_client.get_bucket_encryption(Bucket=b['Name'])
        except Exception as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                status = "No encryption"
            else:
                status = "Can't get encryption status: {}".format(e)
        else:
            if 'ServerSideEncryptionConfiguration' in encryption and 'Rules' in encryption['ServerSideEncryptionConfiguration']:
                rules = encryption['ServerSideEncryptionConfiguration']['Rules']
                status = ""
                for r in rules:
                    if 'ApplyServerSideEncryptionByDefault' in r:
                        status = status + " " + r['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
                if len(status) == 0:
                    status = " No encryption"
            else:
                status = " No encryption"

        print("    "+ b['Name'] + " " + status)


def bucket_policy_tls(bucket, bucket_name, action):
    """
    Examine this bucket's policy and report or change its TLS component
    """
    # Ensure that TLS for both the bucket and its contents is set on the bucket policy
    policy = None
    try:
        policy_string = bucket_client.get_bucket_policy(Bucket=bucket_name)
    except Exception as e:
        print("    Can't get policy: {}".format(e.response['Error']['Code']))
    else:
        policy = json.loads(policy_string['Policy'])
        if policy:
            sid = get_sid_string_from_policy(policy)
            if sid and sid == 'ForceSSLOnlyAccess':
                resource = get_resource_from_policy(policy)
                if resource:
                    replacement = fix_policy_if_needed(policy)
                    if action == 'modify':
                        if replacement:
                            print("    Replacing:\n    {}\n    With:\n    {}\n".format(resource, get_resource_from_policy(replacement)))
                        else:
                            print("    Replacement not required")
                    else:
                        if replacement:
                            print("    Would replace:\n    {}\n    With:\n    {}\n".format(resource, get_resource_from_policy(replacement)))
                        else:
                            print("    Replacement not required")
                else:
                    print("    No resource for policy")
            else:
                print("    Sid not ForceSSLOnlyAccess (it is {})".format(sid))
        else:
            print("    No policy for {}".format(bucket_name))

    return None


def bucket_encryption(bucket, bucket_name, action):
    """
    Examine this bucket's encryption status and either report it or force it on
    """
    encryption = None
    try:
        encryption = bucket_client.get_bucket_encryption(Bucket=bucket_name)
    except Exception as e:
        print("    Can't get encryption: {}".format(e))
    else:
        if encryption and 'ServerSideEncryptionConfiguration' in encryption and 'Rules' in encryption['ServerSideEncryptionConfiguration']:
            rules = encryption['ServerSideEncryptionConfiguration']['Rules']
            for r in rules:
                if 'ApplyServerSideEncryptionByDefault' in r:
                    print("    Encryption is: {}".format(r['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']))
        else:
            if action == 'modify':
                print("Enabled encryption for {}".format(bucket_name))
            else:
                print("No encryption for {}".format(bucket_name))

    return None


def bucket_logging(bucket, bucket_name, action):
    """
    Examine this bucket's logging status and either report it or force it on
    """
    logging = None
    try:
        logging = bucket_client.get_bucket_logging(Bucket=bucket_name)
    except Exception as e:
        print("    Can't get logging: {}".format(e))
    else:
        if logging and 'LoggingEnabled' in logging:
            print("    Logging ENABLED")
        else:
            print("    No logging")
            if action == 'modify':
                logging_status = { 'LoggingEnabled': { 'TargetBucket' : bucket_name, 'TargetPrefix' : 's3-log-'}}
                try:
                    bucket_client.put_bucket_logging(Bucket=bucket_name, BucketLoggingStatus=logging_status)
                except Exception as e:
                    print("Can't set logging on {}".format(bucket_name))
                else:
                    print("Turned logging on for {}".format(bucket_name))

    return None


def scan_bucket_security(buckets, action):
    """
    Go through all of our S3 buckets and examine their policies
    """
    # Consider returning True if we changed anything
    if buckets:
        bucket_list = buckets['Buckets']
        print("SCAN_BUCKET_SECURITY: {} buckets".format(len(bucket_list)))
    
        for b in bucket_list:
            bucket_name = b['Name']
            print("Bucket name: {}".format(bucket_name))

            # Buckets whose names start with aa belong to security and should not be touched
            if bucket_name.startswith('aa'):
                print("    Skipping {} - security bucket".format(bucket_name))
                continue

            # Exmine the bucket policy for TLS
            # bucket_policy_tls(b, bucket_name, 'scan');

            # Verify that there is encryption, if not turn it on
            bucket_encryption(b, bucket_name, 'scan');

            # Verify that there is logging, if not turn it on
            # bucket_logging(b, bucket_name, 'scan')
    else:
        print("    scan_bucket_security passed None buckets")


bucket_client = boto3.client('s3')

STATUS_CODE_NOT_FOUND = { "statusCode" : "404", "body" : json.dumps("Fail") }
STATUS_CODE_OK = { "statusCode" : "200", "body" : json.dumps("That seemed to succeed") }
STATUS_CODE_ERROR = { "statusCode" : "500", "body" : json.dumps("Server Error") }

ALLOWABLE_ACTIONS = ["scan", "modify", "list", "logging", "encryption"]


def lambda_handler(event, context):
    # print("Lambda Handler, Action: {}".format(event['action']))
    if 'action' in event and event['action'] in ALLOWABLE_ACTIONS:
        buckets = None
        try:
            buckets = bucket_client.list_buckets()
        except Exception as e:
            print("Can't get buckets: {}".format(e))
            return STATUS_CODE_NOT_FOUND

        if buckets:
            action = event['action']
            if action == "list":
                print_bucket_names(buckets)
                return STATUS_CODE_OK

            if action == "logging":
                print_bucket_logging(buckets)
                return STATUS_CODE_OK

            if action == "encryption":
                print_bucket_encryption(buckets)
                return STATUS_CODE_OK

            scan_bucket_security(buckets, action)
            return STATUS_CODE_OK

        else:
            print("Can't get buckets")
            return STATUS_CODE_NOT_FOUND

    print("Can't find allowable action in event parameter")
    return STATUS_CODE_ERROR


# If we're not in Lambda, presume we're running locally
if __name__ == "__main__":
    import argparse

    ACTION = 'action'

    parser = argparse.ArgumentParser(description="Examine S3 buckets.")
    parser.add_argument(ACTION, choices=ALLOWABLE_ACTIONS)
    args = parser.parse_args()
    action = vars(args)[ACTION]

    event = { 'action' : action }
    lambda_handler(event, None)
