import dateutil.parser
import json
import logging
import os

from todos.utils import respond, table

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    try:
        req = json.loads(event['body'])

        if not validate(req):
            return respond({'code': 400, 'message': 'Failed to create the todo.'})

        res = table(TABLE_NAME).put_item(
            Item={
                'id': '1',
                'title': req.get('title'),
                'description': req.get('description', ''),
                'due_date': req.get('due_date', ''),
                'todo_status': 'TODO'
            }
        )
    except:
        import traceback
        traceback.print_exc()
        return respond({'code': 400, 'message': 'Failed to create the todo.'})

    return respond(None, res)


def validate(req):
    if not req.get('title'):
        return False
    if req.get('due_date'):
        try:
            dateutil.parser.parse(req.get('due_date'))
        except ValueError:
            return False

    return True
