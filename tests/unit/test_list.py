import json
import os
import pytest
import todos.list as list

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
                'deadline': '2018-06-30',
                'status': 'TODO'
            }
        )
        table(TABLE_NAME).put_item(
            Item={
                'id': '2',
                'title': 'test',
                'descr': 'test',
                'deadline': '2018-07-30',
                'status': 'DOING'
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
def event_todo_list():
    return {
        'httpMethod': 'POST',
    }


def test_todo_list(event_todo_list):
    ret = list.lambda_handler(event_todo_list, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert len(data) == 2
