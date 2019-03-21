import json

example_policy = '{ \
    "Version": "2008-10-17", \
    "Id": "PolicyForCloudFrontPrivateContent", \
    "Statement": [ \
        { \
            "Sid": "1", \
            "Effect": "Allow", \
            "Principal": { \
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E23PFR7PPYBMWR" \
            }, \
            "Action": "s3:GetObject", \
            "Resource": "arn:aws:s3:::doc-viewer-poc/*" \
        } \
    ] \
}'
o = json.loads(example_policy)

def add_ssl_sid(policy, bucket_name):
    """
    Given a policy object and a bucket name, add an SSL sid element to the policy
    """
    resource = [ "arn:aws:s3:::{}/*".format(bucket_name), "arn:aws:s3:::{}".format(bucket_name) ]
    ssl_sid = { "Sid": "ForceSSLOnlyAccess",
                "Effect": "Deny",
                "Principal": { "AWS": "*" },
                "Action": "s3:*",
                "Resource": resource,
                "Condition": { "Bool": { "aws:SecureTransport": "false" } }
                }
    policy['Statement'].append(ssl_sid)
    return policy
    
print(add_ssl_sid(o, "wmrk-dev-config-logs-s3"))

# o['Statement'].append(ssl_sid)

# print(o['Statement'])
# print(o)

