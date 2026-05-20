"""Logging configuration for the Verger application."""

import logging
import os
import sys


def setup_logging():
    """
    Configures the logging for Verger.
    By default, it shows WARNING and above.
    Users can set VERGER_LOG=DEBUG to see all logs including plugin discovery.
    """
    # Get level from environment variable, default to WARNING
    log_level_str = os.getenv("VERGER_LOG", "WARNING").upper()

    # Map string to logging constants
    level = getattr(logging, log_level_str, logging.WARNING)

    # Create a clean format for CLI usage
    log_format = "%(levelname)s: %(message)s"
    if level == logging.DEBUG:
        # Show more details (like the module name) in debug mode
        log_format = "%(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=level, format=log_format, stream=sys.stderr)
