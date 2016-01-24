#!/usr/bin/env python
import sys
import os
import gc
import logging
import logging.config
import yaml
import signal
from threading import Event

# Timer was a factory function before python 3.3
try:
    from threading import _Timer as Timer
except ImportError:
    from threading import Timer

SHUTDOWN = Event()

LOG = logging.getLogger(__name__)

def configure_logging():
    log_config_path = os.getenv('LOG_CONFIG_PATH')
    if log_config_path:
        logging.config.fileConfig(log_config_path,
                                  disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.DEBUG)


def schedule(func, period, run_now=False):
    def wrapper():
        try:
            func()
        except Exception as e:  #pylint: disable=W0703
            LOG.error(e)
        finally:
            if not SHUTDOWN.is_set():
                schedule(func, period=period)

    t = Timer(0 if run_now else period, wrapper)

    t.start()


def load_config(config_file_path):
    config = None
    with open(config_file_path) as f:
        config = yaml.load(f)

    return config


def cancel_timers():
    """
    This is not suitable for large daemons as it scans through all objects.
    """
    for obj in gc.get_objects():
        if isinstance(obj, Timer):
            LOG.debug("Canceling {}".format(obj))
            obj.cancel()


def shutdown_handler(signum, frame):  #pylint: disable=W0613
    LOG.info('Shutting down')
    SHUTDOWN.set()

    cancel_timers()


def install_signal_handlers():
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)


def wait_for_shutdown():
    signal.pause()
