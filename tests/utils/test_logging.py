import logging
import os
from unittest.mock import patch

from verger.utils.logging import setup_logging


def test_setup_logging_default():
    """Test that logging is set up with default WARNING level."""
    with patch("logging.basicConfig") as mock_basic_config:
        with patch.dict(os.environ, {}, clear=True):
            setup_logging()
            # We check the 'level' argument in the first call
            kwargs = mock_basic_config.call_args.kwargs
            assert kwargs["level"] == logging.WARNING


def test_setup_logging_debug():
    """Test that logging level can be set via environment variable."""
    with patch("logging.basicConfig") as mock_basic_config:
        with patch.dict(os.environ, {"VERGER_LOG": "DEBUG"}):
            setup_logging()
            kwargs = mock_basic_config.call_args.kwargs
            assert kwargs["level"] == logging.DEBUG
            assert "%(name)s" in kwargs["format"]
