import json
import boto3
import os
from botocore.vendored import requests
# pull in test case files
import sb_issues as test1
import sb_has_mongo_lat_movement_and_sec_event_finding as test2
import saved_query_checks as test3
import sb_internet_exposure as test4

# Standard headers
HEADERS_AUTH = {"Content-Type": "application/x-www-form-urlencoded"}
HEADERS = {"Content-Type": "application/json"}

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

# Create an SNS client
sns = boto3.client('sns')
sns_arn = os.environ['sns_arn']

def post_to_sns(message):
    print(message)
    response = sns.publish(
        TopicArn=sns_arn,    
        Message=message,    
    )
    print(response)

def query_wiz_api(query, variables):
    """Query WIZ API for the given query data schema"""
    data = {"variables": variables, "query": query}

    try:
        result = requests.post(url="https://api.eu1.demo.wiz.io/graphql",
                                json=data, headers=HEADERS)

    except Exception as e:
        if ('502: Bad Gateway' not in str(e) and
                '503: Service Unavailable' not in str(e) and
                '504: Gateway Timeout' not in str(e)):
            print("<p>Wiz-API-Error: %s</p>" % str(e))
            return(e)
        else:
            print("Retry")

    return result.json()

def request_wiz_api_token(client_id, client_secret):
    print("Getting token.")
    """Retrieve an OAuth access token to be used against Wiz API"""
    auth_payload = {
        'grant_type': 'client_credentials',
        'audience': 'wiz-api',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(url="https://auth.demo.wiz.io/oauth/token",
                            headers=HEADERS_AUTH, data=auth_payload)

    if response.status_code != requests.codes.ok:
        raise Exception('Error authenticating to Wiz [%d] - %s' %
                        (response.status_code, response.text))

    try:
        response_json = response.json()
        TOKEN = response_json.get('access_token')
        if not TOKEN:
            message = 'Could not retrieve token from Wiz: {}'.format(
                    response_json.get("message"))
            raise Exception(message)
    except ValueError as exception:
        print(exception)
        raise Exception('Could not parse API response')
    HEADERS["Authorization"] = "Bearer " + TOKEN

    return TOKEN    

def lambda_handler(event, context):
    # Initial Setup
    request_wiz_api_token(client_id, client_secret)

    message = ""
    # Test Cases
    failure_message = test1.test(query_wiz_api) # sb_issues
    if failure_message:
        message = message + failure_message
    failure_message = test2.test(query_wiz_api) # sb_mongo_lat_etc....
    if failure_message:
        message = message + failure_message
    failure_message = test3.test(query_wiz_api) # saved queries
    if failure_message:
        message = message + failure_message
    failure_message = test4.test(query_wiz_api) # sb internet exposure
    if failure_message:
        message = message + failure_message
    

    if message:
        print(message)
        post_to_sns(message)

    return