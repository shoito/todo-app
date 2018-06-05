import json
import os
import pytest
import todos.show as show

from botocore.exceptions import ClientError
from todos.utils import dynamodb, table

TABLE_NAME = os.getenv('TABLE_NAME')


def setup():
    try:
        dynamodb().create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        table(TABLE_NAME).put_item(
            Item={
                'id': '1',
                'title': 'test',
                'descr': 'test',
                'deadline': '2018-06-30T10:00:00Z',
                'status': 'TODO'
            }
        )
    except ClientError:
        pass


def teardown():
    try:
        table(TABLE_NAME).delete()
    except ClientError:
        pass


@pytest.fixture()
def event_todo_exists():
    return {
        'body': '{}',
        'queryStringParameters': {
        },
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_exists(event_todo_exists):
    ret = show.lambda_handler(event_todo_exists, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert data['id'] == '1'


@pytest.fixture()
def event_todo_not_found():
    return {
        'body': '{}',
        'queryStringParameters': {
        },
        'pathParameters': {
            'id': '999'
        },
        'httpMethod': 'POST',
    }


def test_todo_not_found(event_todo_not_found):
    ret = show.lambda_handler(event_todo_not_found, '')
    assert ret['statusCode'] == 404
