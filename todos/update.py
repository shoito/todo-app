import dateutil.parser
import json
import logging
import os

from todos.utils import respond, table
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
            UpdateExpression='set title=:title, description=:description, deadline=:deadline, todo_status=:todo_status',
            ExpressionAttributeValues={
                ':title': req.get('title'),
                ':description': req.get('description'),
                ':deadline': req.get('deadline'),
                ':todo_status': req.get('todo_status')
            }
        )
    except:
        import traceback
        traceback.print_exc()
        return respond({'code': 400, 'message': 'Failed to update the todo.'})

    return respond(None, res)


def validate(req):
    if (not req.get('title')
            or not req.get('description')
            or not req.get('deadline')
            or not req.get('todo_status')):
        return False

    if req.get('deadline'):
        try:
            dateutil.parser.parse(req.get('deadline'))
        except ValueError:
            return False
    if (not req.get('todo_status')
           in [TodoStatus.TODO.name, TodoStatus.DOING.name, TodoStatus.DONE.name]):
        return False

    return True
