import logging
import os

from todos.utils import respond, table

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    res = table(TABLE_NAME).scan()

    return respond(None, res['Items'])
