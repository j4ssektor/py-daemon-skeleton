#!/usr/bin/env python
import logging
import datetime
from daemon import (daemonize, create_optparser)
from core import (load_config, schedule, configure_logging,
                  wait_for_shutdown, install_signal_handlers)

LOG = logging.getLogger(__name__)


def run():
    argument_parser = create_optparser()
    args = argument_parser.parse_args()

    if args.daemonize:
        daemonize(args.pidfile, args.error_log)

    configure_logging()
    install_signal_handlers()
    config = load_config(args.config)

    LOG.info('Starting')

    schedule(lambda: perform_useless_task(config['server']['host']),
             period=config['period'], run_now=False)


    wait_for_shutdown()


def perform_useless_task(server_address):
    LOG.info('azaza %s %s' % (datetime.datetime.now(), server_address))
