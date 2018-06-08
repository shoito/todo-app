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

        res = table(TABLE_NAME).delete_item(
            Key={
                'id': id
            },
            ReturnValues='ALL_OLD'
        )

        if not res.get('Attributes'):
            return respond({'code': 404, 'message': 'Todo not found.'})
    except Exception as e:
        logging.error(e)
        return respond({'code': 400, 'message': 'Failed to delete the todo.'})

    return respond(None, res)


def respond(err, res=None):
    return {
        'statusCode': err['code'] if err else 204,
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }