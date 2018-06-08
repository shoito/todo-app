import boto3
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


def create_todos_table(table_name):
    return dynamodb().create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'todo_status-index',
                'KeySchema': [
                    {
                        'AttributeName': 'todo_status',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'todo_status',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )