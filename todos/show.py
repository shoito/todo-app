import json
import logging
import os

from todos.utils import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    try:
        id = event['pathParameters']['id']
        res = table(TABLE_NAME).get_item(Key={'id': id})
        todo = res['Item']
    except Exception as e:
        logging.error(e)
        return respond({'code': 404, 'message': 'Todo not found.'})

    return respond(None, todo)


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 200,
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }