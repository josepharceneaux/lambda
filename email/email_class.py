"""
"""


from botocore.exceptions import ClientError
import boto3

DEFAULT_ENCODING = "UTF-8"

DEFAULT_AWS_REGION = "us-east-1"

BODY_HTML = ""

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
        self.destination = {}
        self.message = {}
        self.reply_to_addresses = []
        self.return_path = sender_email
        self.source_arn = "Some ARN"
        self.return_path_arn = "Some ARN"
        self.tags = []
        self.configuration_set_name = "Some configuration"
        self.text = message_content
        self.html = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with the AWS SDK for Python (Boto3)</a>.</p>
</body>
</html>
"""
        self.ses_client = boto3.client('ses', region_name=aws_region)

    def send(self):
        """
        """
        print("Content; {}\n".format(self.message_content))
        print("Subject; {}\n".format(self.subject))

        response = None
        try:
            print("In Try")

            
        #     print("In Try")
        #     response = ses_client.send_email(
        #         Source=self.sender_email,
        #         Destination = {
        #             'ToAddresses': [
        #                 self.recipient_list,
        #                 ],
        #             'CcAddresses': [],
        #             'BccAddresses': []
        #             },
        #         Message={
        #             'Subject': {
        #                 'Charset': DEFAULT_ENCODING,
        #                 'Data': self.subject,
        #                 },
        #             'Body': {
        #                 'Html': {
        #                     'Charset': DEFAULT_ENCODING,
        #                     'Data': BODY_HTML,
        #                     },
        #                 'Text': {
        #                     'Charset': DEFAULT_ENCODING,
        #                     'Data': BODY_HTML,
        #                     },
        #                 },
        #             },
        #         ReplyToAddresses = [],
        #         ReturnPath = '',
        #         SourceArn = '',
        #         ReturnPathARN = '',
        #         Tags = [],
        #         ConfigurationSetName = ''
        #         )                

        except ClientError as e:
            print("EXCEPTION: {}".format(e))
        else:
            # print("Email appears to have been sent: {}".format(response['MessageId']))
            if response:
                print("Email appears to have been sent: {}".format(response))
            else:
                print("No response from email")
