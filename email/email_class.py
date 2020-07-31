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
        try:
            print("In Try")
            response = ses_client.send_email(
                Source=self.sender_email,
                Destination = {
                    'ToAddresses': [
                        self.recipient_list,
                        ],
                    'CcAddresses': [],
                    'BccAddresses': []
                    },
                Message={
                    'Subject': {
                        'Charset': DEFAULT_ENCODING,
                        'Data': self.subject,
                        },
                    'Body': {
                        'Html': {
                            'Charset': DEFAULT_ENCODING,
                            'Data': BODY_HTML,
                            },
                        'Text': {
                            'Charset': DEFAULT_ENCODING,
                            'Data': BODY_HTML,
                            },
                        },
                    },
                ReplyToAddresses = [],
                ReturnPath = '',
                SourceArn = '',
                ReturnPathARN = '',
                Tags = [],
                ConfigurationSetName = ''
                )                

        except ClientError as e:
            print("EXCEPTION: {}".format(e))
        else:
            print("Email appears to have been sent: {}".format(response['MessageId']))
