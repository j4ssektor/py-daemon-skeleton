#!/usr/bin/env python
import sys
import os
import subprocess
import atexit
import gc
import logging
import logging.config
import signal
import yaml
from threading import Event

# Timer was a factory function before python 3.3
try:
    from threading import _Timer as Timer  #pylint: disable=E0611
except ImportError:
    from threading import Timer  #pylint: disable=E0611

SHUTDOWN = Event()

LOG = logging.getLogger(__name__)


def daemonize(pidfile, error_log):
    if os.path.exists(pidfile):
        raise RuntimeError("Pid file {0} already exists".format(pidfile))

    def redirect_stream(system_stream, target_stream):
        os.dup2(target_stream.fileno(), system_stream.fileno())

    def fork_exit_parent():
        pid = os.fork()
        if pid > 0:
            os._exit(0)

    def close_all_open_files():
        '''Close all file descriptors except for stdin, stdout, stderr'''
        os.closerange(3, subprocess.MAXFD)

    fork_exit_parent()
    os.chdir('/')
    os.setsid()
    os.umask(0)
    fork_exit_parent()
    close_all_open_files()
 
    # redirect standard file descriptors
    with open(os.devnull) as devnull:
        redirect_stream(sys.stdin, devnull)

    with open(error_log, 'a') as error_log_file:
        redirect_stream(sys.stdout, error_log_file)
        redirect_stream(sys.stderr, error_log_file)
       
    with open(pidfile, 'w') as f:
        f.write(str(os.getpid()))

    atexit.register(lambda: os.remove(pidfile))

def configure_logging():
    log_config_path = os.getenv('LOG_CONFIG_PATH')
    if log_config_path:
        logging.config.fileConfig(log_config_path,
                                  disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.DEBUG)


def schedule(func, *, period, run_now=False):
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


def load_config():
    if len(sys.argv) != 2:
        sys.exit('You must provide config file')

    config_file_path = sys.argv[1]

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
