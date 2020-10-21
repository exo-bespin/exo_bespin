#!/usr/bin/env python
"""Tests for the ``logging_tools`` module.

Authors
-------

    - Matthew Bourque

Use
---

    These tests can be run via the command line (omit the -s to
    suppress verbose output to stdout):

    ::

        pytest -s test_logging_tools.py

Dependencies
------------

    - ``pytest``
"""

import os
import shutil

from exo_bespin.logging import logging_tools

def test_configure_logging():
    """Assert that the ``configure_logging`` function successfully
    creates a log file"""

    log_file = logging_tools.configure_logging('test_logging_tools')
    assert os.path.exists(log_file)

    # Remove the log file
    os.remove(log_file)