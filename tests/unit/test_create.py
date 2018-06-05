import json
import os
import pytest
import todos.create as create

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
    except ClientError:
        pass


def teardown():
    try:
        table(TABLE_NAME).delete()
    except ClientError:
        pass


@pytest.fixture()
def event_todo_valid():
    return {
        'body': json.dumps({
            'title': 'test title',
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
        }),
        'httpMethod': 'POST',
    }


def test_todo_valid(event_todo_valid):
    res = create.lambda_handler(event_todo_valid, '')
    assert res['statusCode'] == 200

    res = table(TABLE_NAME).get_item(Key={'id': '1'})
    assert res['Item']['id'] == '1'


@pytest.fixture()
def event_todo_title_missing():
    return {
        'body': json.dumps({
            # 'title': 'test title', # missing title
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
        }),
        'httpMethod': 'POST',
    }


def test_todo_title_missing(event_todo_title_missing):
    res = create.lambda_handler(event_todo_title_missing, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_title_empty():
    return {
        'body': json.dumps({
            'title': '',
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
        }),
        'httpMethod': 'POST',
    }


def test_todo_title_empty(event_todo_title_empty):
    res = create.lambda_handler(event_todo_title_empty, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_description_missing():
    return {
        'body': json.dumps({
            'title': 'test title',
            # 'description': 'test description', # missing description
            'due_date': '2018-06-30T10:00:00Z',
        }),
        'httpMethod': 'POST',
    }


def test_todo_description_missing(event_todo_description_missing):
    res = create.lambda_handler(event_todo_description_missing, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_due_date_missing():
    return {
        'body': json.dumps({
            'title': 'test title',
            'description': 'test description',
            'due_date': '2018-06-30-10T00:00Z', # invalid format
        }),
        'httpMethod': 'POST',
    }


def test_todo_due_date_missing(event_todo_due_date_missing):
    res = create.lambda_handler(event_todo_due_date_missing, '')
    assert res['statusCode'] == 400
