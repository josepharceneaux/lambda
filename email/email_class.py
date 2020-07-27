"""
"""


from botocore.exceptions import ClientError
import boto3

DEFAULT_ENCODING = "UTF-8"

DEFAULT_AWS_REGION = "us-east-1"

class Email(object):
    """
    """

    def __init__(self, message_content, sender_email, recipient_email, subject, aws_region=DEFAULT_AWS_REGION):
        """
        """

        self.message_content = message_content
        self.subject = subject
        self.recipient_email = recipient_email
        self.sender_email = sender_email
        self.aws_region = aws_region
        self.client = boto3.client('ses', region_name=aws_region)

    def send(self):
        """
        """
        print("Content; {}\n".format(self.message_content))
        print("Subject; {}\n".format(self.subject))

        # self.client.send()

        # send
        # print("Sender; {}".format(self.sender_email))
        # print("Recipient; {}".format(self.recipient_email))
        # print("Sender; {}".format(self.sender_email))
        # print("Body; {}".format(self.ses_body))
        # print("SES BODY: {}\n".format(self.ses_body))
        
