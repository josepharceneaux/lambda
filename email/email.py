"""
"""
 
# SES_TEMPLATE = 'Destination={{            "ToAddresses": [],
#             }},
#                 Message={{            "Body": {{
#                 "Html": {{                    "Charset": ENCODING,
#                     "Data": BODY_HTML,
#                     }},                "Text": {{                    "Charset": ENCODING,
#                     "Data": BODY_HTML,
#                     }},                }},            "Subject": {{
#                 "Charset": ENCODING,
#                 "Data": SUBJECT,
#                 }},
#             }},
#                 Source=SENDER,'

SES_TEMPLATE = 'Destination={{"CONTENT: {}\n,
SENDER: {}\n,
RECIPIENT: {}\n
SUBJECT: {}\n,
REGION: {}"'

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
        # self.ses_body = "Foobar"
        self.aws_region = aws_region
        self.ses_body = SES_TEMPLATE.format(message_content, sender_email, recipient_email, subject, aws_region)
        # print("INIT Values: {} {} {} {} {}".format(message_content, sender_email, recipient_email, subject, aws_region))
        # self.ses_body = SES_TEMPLATE.format(message_content, sender_email, recipient_email, subject)
        # self.ses_body = "Foobar {}".format("Iam a string")

    def send(self):
        """
        """
        # print("Here's the SES body:")
        print("Content; {}\n".format(self.message_content))
        print("Subject; {}"\n.format(self.subject))
        print("And here's the template: {}}"\n.format()
        # print("Sender; {}".format(self.sender_email))
        # print("Recipient; {}".format(self.recipient_email))
        # print("Sender; {}".format(self.sender_email))
        # print("Body; {}".format(self.ses_body))
        print("SES BODY: {}\n".format(self.ses_body))
        
