import json
import logging
import os

from boto3.dynamodb.conditions import Key
from todos.todo_status import TodoStatus
from todos.utils import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    if not validate(event):
        return respond({'code': 400, 'message': 'Bad request parameter.'})

    todo_status = event.get('todo_status')

    if todo_status:
        res = table(TABLE_NAME).query(
            IndexName='todo_status-index',
            KeyConditionExpression=Key('todo_status').eq(todo_status)
        )
    else:
        res = table(TABLE_NAME).scan()

    return respond(None, res['Items'])


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 200,
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {},
        'isBase64Encoded': 'false'
    }


def validate(event):
    todo_status = event.get('todo_status')

    if (todo_status and not todo_status
            in [TodoStatus.TODO.name, TodoStatus.DOING.name, TodoStatus.DONE.name]):
        return False

    return True