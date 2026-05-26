import os

import pytest

from verger.core.config.loader import (
    _load_from_file,
    _parse_pyproject,
    get_config,
    load_config,
)
from verger.core.exceptions import VergerConfigurationError
from verger.core.schema.config import VergerConfig


def test_load_config_from_verger_toml(mock_user_project):
    """Test that Verger correctly finds and parses verger.toml in CWD."""
    config = load_config()

    assert config.env_file == ".env.test"
    assert "system" in config.prompts
    assert config.prompts["system"] == "prompts:SYSTEM_PROMPT"
    assert "simple" in config.models


def test_config_singleton(mock_user_project):
    """Test that get_config returns the same object after load_config."""
    config1 = load_config()
    config2 = get_config()

    assert config1 is config2


def test_get_config_not_loaded():
    """Test that get_config raises RuntimeError if config is not yet loaded."""
    # We need to reset the global _config for this test
    import verger.core.config.loader as loader

    original_config = loader._config
    loader._config = None
    try:
        with pytest.raises(RuntimeError, match="has not been loaded"):
            get_config()
    finally:
        loader._config = original_config


def test_priority_env_var(tmp_path):
    """Test that VERGER_CONFIG environment variable has highest priority."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    verger_toml = project_dir / "verger.toml"
    verger_toml.write_text('env_file = "verger.env"')

    env_config = project_dir / "env_config.toml"
    env_config.write_text('env_file = "env_var.env"')

    os.environ["VERGER_CONFIG"] = str(env_config)
    try:
        config = load_config(root_dir=project_dir)
        assert config.env_file == "env_var.env"
    finally:
        del os.environ["VERGER_CONFIG"]


def test_priority_env_var_missing_file():
    """Test that VergerConfigurationError is raised if VERGER_CONFIG points to a missing file."""
    os.environ["VERGER_CONFIG"] = "/non/existent/path.toml"
    try:
        with pytest.raises(VergerConfigurationError, match="points to non-existent file"):
            load_config()
    finally:
        del os.environ["VERGER_CONFIG"]


def test_priority_verger_toml(tmp_path):
    """Test that verger.toml has priority over pyproject.toml."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    verger_toml = project_dir / "verger.toml"
    verger_toml.write_text('env_file = "verger.env"')

    pyproject_toml = project_dir / "pyproject.toml"
    pyproject_toml.write_text('[tool.verger]\nenv_file = "pyproject.env"')

    config = load_config(root_dir=project_dir)
    assert config.env_file == "verger.env"


def test_priority_pyproject_toml(tmp_path):
    """Test that pyproject.toml is used if verger.toml is missing."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    pyproject_toml = project_dir / "pyproject.toml"
    pyproject_toml.write_text('[tool.verger]\nenv_file = "pyproject.env"')

    config = load_config(root_dir=project_dir)
    assert config.env_file == "pyproject.env"


def test_load_config_default_when_no_files(tmp_path):
    """Test that Verger returns a default config if no files exist."""
    empty_dir = tmp_path / "empty_project"
    empty_dir.mkdir()

    config = load_config(root_dir=empty_dir)

    assert isinstance(config, VergerConfig)
    # Check default values from schema
    assert config.env_file == ".env"
    assert config.prompts == {}
    assert config.models == {}


def test_internal_load_from_file(tmp_path):
    """Test the internal _load_from_file helper."""
    config_path = tmp_path / "custom.toml"
    config_path.write_text('env_file = "custom.env"\n[prompts]\ntest = "ref"')

    config = _load_from_file(config_path)

    assert config.env_file == "custom.env"
    assert config.prompts["test"] == "ref"


def test_internal_parse_pyproject(tmp_path):
    """Test the internal _parse_pyproject helper correctly extracts the [tool.verger] section."""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("""
[project]
name = "my-app"

[tool.other]
key = "value"

[tool.prompts]
other = "should_be_ignored"

[tool.verger]
env_file = "verger.env"

[tool.verger.prompts]
test = "should_be_extracted"
""")

    data = _parse_pyproject(pyproject_path)

    # Should contain exactly what is inside [tool.verger]
    assert data is not None
    assert data == {
        "env_file": "verger.env",
        "prompts": {"test": "should_be_extracted"},
    }
    # Ensure sibling [tool.prompts] was NOT leaked into the result
    assert "other" not in data


def test_internal_parse_pyproject_missing_section(tmp_path):
    """Test that _parse_pyproject returns None if the section is missing."""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[project]\nname = 'test'")

    data = _parse_pyproject(pyproject_path)

    assert data is None
