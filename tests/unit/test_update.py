import json
import os
import pytest
import todos.update as update

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
def event_todo_valid():
    return {
        'body': json.dumps({
            'title': 'test title',
            'description': 'test description',
            'due_date': '2018-07-30T10:00:00Z',
            'todo_status': 'DOING'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_valid(event_todo_valid):
    res = update.lambda_handler(event_todo_valid, '')
    assert res['statusCode'] == 204

    res = table(TABLE_NAME).get_item(Key={'id': '1'})
    todo = res['Item']
    assert todo['title'] == 'test title'
    assert todo['description'] == 'test description'
    assert todo['due_date'] == '2018-07-30T10:00:00Z'
    assert todo['todo_status'] == 'DOING'


@pytest.fixture()
def event_todo_title_missing():
    return {
        'body': json.dumps({
            # 'title': 'test title', # missing title
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
            'todo_status': 'DOING'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_title_missing(event_todo_title_missing):
    res = update.lambda_handler(event_todo_title_missing, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_title_empty():
    return {
        'body': json.dumps({
            'title': '',
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
            'todo_status': 'DOING'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_title_empty(event_todo_title_empty):
    res = update.lambda_handler(event_todo_title_empty, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_description_missing():
    return {
        'body': json.dumps({
            'title': 'test title',
            # 'description': 'test description', # missing description
            'due_date': '2018-06-30T10:00:00Z',
            'todo_status': 'DOING'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_description_missing(event_todo_description_missing):
    res = update.lambda_handler(event_todo_description_missing, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_due_date_missing():
    return {
        'body': json.dumps({
            'title': 'test title',
            'description': 'test description',
            'due_date': '2018-06-30-10T00:00Z', # invalid format
            'todo_status': 'DOING'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_due_date_missing(event_todo_due_date_missing):
    res = update.lambda_handler(event_todo_due_date_missing, '')
    assert res['statusCode'] == 400


@pytest.fixture()
def event_todo_status_invalid():
    return {
        'body': json.dumps({
            'title': 'test title',
            'description': 'test description',
            'due_date': '2018-06-30T10:00:00Z',
            'todo_status': 'INVALID'
        }),
        'pathParameters': {
            'id': '1'
        },
        'httpMethod': 'POST',
    }


def test_todo_status_invalid(event_todo_status_invalid):
    res = update.lambda_handler(event_todo_status_invalid, '')
    assert res['statusCode'] == 400
