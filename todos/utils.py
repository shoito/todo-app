import boto3
import json
import os
import sys

DEFAULT_REGION = os.getenv('DEFAULT_REGION', None) # ap-northeast-1
DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT', None) # https://dynamodb.ap-northeast-1.amazonaws.com/

if DEFAULT_REGION is None:
    print('Could not find DEFAULT_REGION env.')
    sys.exit(1)
if DYNAMODB_ENDPOINT is None:
    print('Could not find DYNAMODB_ENDPOINT env.')
    sys.exit(1)


def dynamodb():
    return boto3.resource('dynamodb', region_name=DEFAULT_REGION, endpoint_url=DYNAMODB_ENDPOINT)


def table(table_name):
    return dynamodb().Table(table_name)


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 200,
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
