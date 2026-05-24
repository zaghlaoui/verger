import logging
import os

from verger.core.config.env import load_env
from verger.core.config.loader import load_config
from verger.core.config.schema import VergerConfig


def test_load_env_logic(mock_user_project):
    """Test that environment variables are loaded from the specified file."""
    load_config()
    load_env()

    assert os.getenv("OPENAI_API_KEY") == "sk-test-key"


def test_load_env_missing_specified_file(tmp_path, caplog):
    """Test warning when an explicitly specified env_file is missing."""
    import verger.core.config.loader as loader

    original_config = loader._config
    # Manually set config to simulate an explicit env_file setting
    loader._config = VergerConfig(env_file="missing.env")

    try:
        with caplog.at_level(logging.WARNING):
            load_env(root_dir=tmp_path)
        assert "Specified env_file not found" in caplog.text
    finally:
        loader._config = original_config


def test_load_env_exception(caplog):
    """Test error logging when an exception occurs during env loading."""
    import verger.core.config.loader as loader

    original_config = loader._config
    # This will cause load_env to fail when it calls get_config()
    loader._config = None

    try:
        with caplog.at_level(logging.ERROR):
            load_env()
        assert "Failed to load environment variables" in caplog.text
    finally:
        loader._config = original_config
