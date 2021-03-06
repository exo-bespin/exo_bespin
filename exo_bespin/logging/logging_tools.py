"""This module contains various functions for logging the execution of
``exo_bespin`` software

Authors
-------

    - Matthew Bourque

Use
---

    This script is inteneded to be imported and used by other modules,
    for example:

        from exo_bespin.logging.logging_tools import configure_logging
        configure_logging('my_log')

    This will create a log file at the location
    ``$HOME/exo_bespin_logs/my_log.log``

    Users may also supply a ``log_dir`` parameter to change the parent
    directory in which the log file is saved, for example:

        configure_logging('my_log', '/user/myself/log_files/')

    This will create a log file at the location
    ``/user/myself/log_files/my_log.log``
"""

import datetime
import getpass
import logging
import os
import socket
import subprocess
import sys
import time


def _log_environment_info():
    """Logs information about the user's environment and system"""

    # Log environment information
    logging.info('User: ' + getpass.getuser())
    logging.info('System: ' + socket.gethostname())
    logging.info('Python Version: ' + sys.version.replace('\n', ''))
    logging.info('Python Executable Path: ' + sys.executable)

    # Log the software environment
    environment = subprocess.check_output(['conda', 'env', 'export'], universal_newlines=True)
    logging.info('Environment:')
    for line in environment.split('\n'):
        logging.info(line)


def configure_logging(log_filename, log_dir=os.path.join(os.path.expanduser("~"), 'exo_bespin_logs/')):
    """Configure the log file with a standard logging format.

    By default, the log file will be written to a ``exo_bespin_logs/``
    subdirectory in the user's ``$HOME`` directory.  However, the user
    may supply a ``log_dir`` parameter to write this file somewhere
    else.

    Parameters
    ----------
    log_filename : str
        The name that will be used to create the log file (e.g.
        ``my_log_<timestamp>.log``)

    Returns
    -------
    full_filename : str
        The full path to the created log file
    """

    # Make sure log_dir exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Build complete log filename
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    full_filename = os.path.join(log_dir, '{0}_{1}.log'.format(log_filename, timestamp))

    # Make sure no other root lhandlers exist before configuring the logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create the log file and set the permissions
    logging.basicConfig(filename=full_filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S %p',
                        level=logging.INFO)

    print('Log file initialized to {}'.format(full_filename))

    # Log system information
    _log_environment_info()

    return full_filename


def log_timing(func):
    """Decorator to time a module or function within a code.

    Parameters
    ----------
    func : func
        The function to time.

    Returns
    -------
    wrapped : func
        The wrapped function. Will log the time."""

    def wrapped(*args, **kwargs):

        # Call the function and time it
        start = time.time()
        func(*args, **kwargs)
        end = time.time()

        # Log execution time
        hours, remainder = divmod(end - start, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        logging.info('')
        logging.info('Elapsed Time of {}: {}:{}:{}'.format(func.__name__, int(hours), int(minutes), int(seconds)))

    return wrapped
