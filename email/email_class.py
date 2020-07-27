"""
"""


from botocore.exceptions import ClientError
import boto3

DEFAULT_ENCODING = "UTF-8"

DEFAULT_AWS_REGION = "us-east-1"

class Email(object):
    """
    """

    def __init__(self, message_content, sender_email, recipient_list, subject, aws_region=DEFAULT_AWS_REGION):
        """
        """

        self.message_content = message_content
        self.subject = subject
        self.recipient_list = recipient_list
        self.sender_email = sender_email
        self.aws_region = aws_region
        self.ses_client = boto3.client('ses', region_name=aws_region)

    def send(self):
        """
        """
        print("Content; {}\n".format(self.message_content))
        print("Subject; {}\n".format(self.subject))

        response = None
        # response = self.ses_client.send_email(
        # try:
        #     content = "Go fuck yourselves"
        #     response = client.send_email(
        #         Destination={
        #             'ToAddresses': [
        #                 RECIPIENT,
        #                 ],
        #             },
        #         Message={
        #             'Body': {
        #                 'Html': {
        #                     'Charset': ENCODING,
        #                     'Data': BODY_HTML,
        #                     },
        #                 'Text': {
        #                     'Charset': ENCODING,
        #                     'Data': BODY_HTML,
        #                     },
        #                 },
        #             'Subject': {
        #                 'Charset': ENCODING,
        #                 'Data': SUBJECT,
        #                 },
        #             },
        #         Source=SENDER,
        #         )
        # )
        
