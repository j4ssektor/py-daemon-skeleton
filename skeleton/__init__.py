import logging

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)


def send_useless_info_to_server(server_address):
    useles_data = SenderData()

    data.append_data('host', 'key', value=0)

    result = send(data, server_address)

    LOG.info(result)
