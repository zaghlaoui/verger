import os
from verger.core.config.loader import load_config, get_config
from verger.core.config.env import load_env


def test_load_config_from_pyproject(mock_user_project):
    """Test that Verger correctly finds and parses [tool.verger] in CWD."""
    config = load_config()

    assert config.env_file == ".env.test"
    assert "system" in config.prompts
    assert config.prompts["system"] == "prompts:SYSTEM_PROMPT"
    assert "simple" in config.models


def test_load_env_logic(mock_user_project):
    """Test that environment variables are loaded from the specified file."""
    load_config()
    load_env()

    assert os.getenv("OPENAI_API_KEY") == "sk-test-key"


def test_config_singleton(mock_user_project):
    """Test that get_config returns the same object after load_config."""
    config1 = load_config()
    config2 = get_config()

    assert config1 is config2
