#! /usr/bin/env python3


import sys
from botocore.exceptions import ClientError
import boto3

import pprint


# This requires verification on AWS
SENDER = "jla.lists@gmail.com"

# Apparently this does too
RECIPIENT = "joe.arceneaux@gmail.com"

AWS_REGION = "us-east-1"

SUBJECT = "Test Email"

TEXT = "This is a simple text message sent from AWS."

ENCODING = "UTF-8"

BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with the AWS SDK for Python (Boto3)</a>.</p>
</body>
</html>
"""


# Make a client
client = boto3.client('ses', region_name=AWS_REGION)

# print("Got the client")
# print("Type: {}".format(client.send_email))

def print_exception(e):
    """
    """
    

# Now send an email
try:
    response = client.send_email(
                Destination={
            'ToAddresses': [
                RECIPIENT,
                ],
            },
                Message={
            'Body': {
                'Html': {
                    'Charset': ENCODING,
                    'Data': BODY_HTML,
                    },
                'Text': {
                    'Charset': ENCODING,
                    'Data': BODY_HTML,
                    },
                },
            'Subject': {
                'Charset': ENCODING,
                'Data': SUBJECT,
                },
            },
                Source=SENDER,
                )
except ClientError as e:
    # print("Exception: {} {}".format(e.response['Error']['Code']))
    # print("EXCEPTION:".format(e))
    print("EXCEPTION: {}".format(e))
    print("EXCEPTION: {}".format(type(e)))
    # for name,value in e.items():
    #     # print("{}: {}".format(name, value))
    # pprint.pprint(e, width=1)
else:
    print("Mail seems to have been sent.")


sys.exit(0)

