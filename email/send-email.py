#! /usr/bin/env python3

__author__ = "Joseph Arceneaux joe.arceneaux@gmail.com"


import json
from botocore.exceptions import ClientError
# import boto3
from email import Email



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


# If we're not in Lambda, presume we're running locally
if __name__ == "__main__":
    content = "Go fuck yourselves"
    email = Email(content, SENDER, RECIPIENT, SUBJECT, "us-east-1")
    email.send()
    print("Sending this template:")
    email.send()


