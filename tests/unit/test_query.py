import json
import os
import pytest
import todos.query as query

from botocore.exceptions import ClientError
from todos.utils import table, create_todos_table

TABLE_NAME = os.getenv('TABLE_NAME')


def setup():
    try:
        create_todos_table(TABLE_NAME)

        table(TABLE_NAME).put_item(
            Item={
                'id': '1',
                'title': 'test1',
                'description': 'test1',
                'due_date': '2018-06-01T10:00:00Z',
                'todo_status': 'TODO'
            }
        )

        table(TABLE_NAME).put_item(
            Item={
                'id': '2',
                'title': 'test2',
                'description': 'test2',
                'due_date': '2018-07-01T10:00:00Z',
                'todo_status': 'DOING'
            }
        )

        table(TABLE_NAME).put_item(
            Item={
                'id': '3',
                'title': 'test3',
                'description': 'test3',
                'due_date': '2018-08-01T10:00:00Z',
                'todo_status': 'DOING'
            }
        )

        table(TABLE_NAME).put_item(
            Item={
                'id': '4',
                'title': 'test4',
                'description': 'test4',
                'due_date': '2018-09-01T10:00:00Z',
                'todo_status': 'DONE'
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
def event_todo_TODO():
    return {
        'queryStringParameters': {
            'todo_status': 'TODO'
        },
        'httpMethod': 'POST'
    }


def test_todo_TODO(event_todo_TODO):
    ret = query.lambda_handler(event_todo_TODO, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert len(data) == 1


@pytest.fixture()
def event_todo_DOING():
    return {
        'queryStringParameters': {
            'todo_status': 'DOING'
        },
        'httpMethod': 'POST'
    }


def test_todo_DOING(event_todo_DOING):
    ret = query.lambda_handler(event_todo_DOING, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert len(data) == 2


@pytest.fixture()
def event_todo_DONE():
    return {
        'queryStringParameters': {
            'todo_status': 'DONE'
        },
        'httpMethod': 'POST'
    }


def test_todo_DONE(event_todo_DONE):
    ret = query.lambda_handler(event_todo_DONE, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert len(data) == 1


@pytest.fixture()
def event_todo_invalid_status():
    return {
        'queryStringParameters': {
            'todo_status': 'HOGE'
        },
        'httpMethod': 'POST'
    }


def test_todo_invalid_status(event_todo_invalid_status):
    ret = query.lambda_handler(event_todo_invalid_status, '')
    assert ret['statusCode'] == 400


@pytest.fixture()
def event_todo_list():
    return {
        'httpMethod': 'POST'
    }


def test_todo_list(event_todo_list):
    ret = query.lambda_handler(event_todo_list, '')
    assert ret['statusCode'] == 200

    data = json.loads(ret['body'])
    assert len(data) == 4
