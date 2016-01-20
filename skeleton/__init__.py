import logging
import datetime

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)


def perform_useless_task(server_address):
    LOG.info('azaza %s %s' % (datetime.datetime.now(), server_address))
