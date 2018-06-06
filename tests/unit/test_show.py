import json
import os
import pytest
import todos.show as show

from botocore.exceptions import ClientError
from todos.utils import create_todos_table, table

TABLE_NAME = os.getenv('TABLE_NAME')


def setup():
    try:
        create_todos_table(TABLE_NAME)

        table(TABLE_NAME).put_item(
            Item={
                'id': '1',
                'title': 'test',
                'description': 'test',
                'due_date': '2018-06-30T10:00:00Z',
                'todo_status': 'TODO'
            }
        )
    except ClientError:
        import traceback
        traceback.print_exc()


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
