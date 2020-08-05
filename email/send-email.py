#! /usr/bin/env python3

__author__ = "Joseph Arceneaux joe.arceneaux@gmail.com"


from botocore.exceptions import ClientError
from email_class import Email


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
    email = Email("I am another message", SENDER, [ RECIPIENT ], SUBJECT, AWS_REGION)

    try:
        email.send()
        print("Fake mail seems to have been sent.")
    except ClientError as e:
        print("EXCEPTION: {}".format(e))


