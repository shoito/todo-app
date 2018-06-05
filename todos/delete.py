import logging
import os

from botocore.exceptions import ClientError
from todos.utils import respond, table

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
    except ClientError as e:
        message = 'Todo cannot delete.'
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            message = e.response['Error']['Message']
        return respond({'code': 400, 'message': message})

    return respond(None, res)
