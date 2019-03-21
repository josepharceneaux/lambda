import sys
import requests

def validate_response(response, code=requests.codes.OK, operation=None):
    """
    If the request didn't return CODE, bail
    :param dict response: Response from AWS client call.
    :param code HTTP status code expected
    :param operation Descriptive name of what we were trying to do
    """
    if response and u'ResponseMetadata' in response and u'HTTPStatusCode' in response[u'ResponseMetadata']:
        if response[u'ResponseMetadata'][u'HTTPStatusCode'] != code:
            print "Operation {} not OK: Status: {} Full Response: {}".format(operation, response[u'ResponseMetadata'][u'HTTPStatusCode'], response)
            sys.exit(1)

    else:
        print "API call: {} Malformatted AWS response: {}".format(operation, response)
        sys.exit(1)

