import dateutil.parser
import json
import logging
import os

from todos.utils import table
from todos.todo_status import TodoStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    try:
        req = json.loads(event['body'])

        if not validate(req):
            return respond({'code': 400, 'message': 'Failed to update the todo.'})

        res = table(TABLE_NAME).update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            UpdateExpression='set title=:title, description=:description, due_date=:due_date, todo_status=:todo_status',
            ExpressionAttributeValues={
                ':title': req.get('title'),
                ':description': req.get('description'),
                ':due_date': req.get('due_date'),
                ':todo_status': req.get('todo_status')
            }
        )
    except Exception as e:
        logging.error(e)
        return respond({'code': 400, 'message': 'Failed to update the todo.'})

    return respond(None, res)


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 204,
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def validate(req):
    if (not req.get('title')
            or not req.get('description')
            or not req.get('due_date')
            or not req.get('todo_status')):
        return False

    if req.get('due_date'):
        try:
            dateutil.parser.parse(req.get('due_date'))
        except ValueError:
            return False
    if (not req.get('todo_status')
           in [TodoStatus.TODO.name, TodoStatus.DOING.name, TodoStatus.DONE.name]):
        return False

    return True
