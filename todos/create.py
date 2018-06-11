import dateutil.parser
import json
import logging
import os
import uuid

from todos.todo_status import TodoStatus
from todos.utils import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    try:
        req = json.loads(event['body'])

        if not validate(req):
            return respond({'code': 400, 'message': 'Bad request. Failed to create the todo.'})

        todo = {
            'id': str(uuid.uuid4().hex[:8]),
            'title': req.get('title'),
            'description': req.get('description', ''),
            'due_date': req.get('due_date', ''),
            'todo_status': TodoStatus.TODO.name
        }

        table(TABLE_NAME).put_item(
            Item=todo,
            Expected={
                'primary_key': {
                    'Exists': False
                }
            }
        )
    except Exception as e:
        logging.error(e)
        return respond({'code': 400, 'message': 'Failed to create the todo.'})

    return respond(None, todo)


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 201,
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {},
        'isBase64Encoded': 'false'
    }


def validate(req):
    if not req.get('title'):
        return False
    if req.get('due_date'):
        try:
            dateutil.parser.parse(req.get('due_date'))
        except ValueError:
            return False

    return True
