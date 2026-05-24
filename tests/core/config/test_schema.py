import pytest

from verger.core.config.schema import ModelConfig, VergerConfig


def test_verger_config_defaults():
    """Test that VergerConfig has correct default values."""
    config = VergerConfig()
    assert config.env_file == ".env"
    assert config.prompts == {}
    assert config.models == {}


def test_verger_config_custom():
    """Test that VergerConfig accepts custom values."""
    config = VergerConfig(env_file="custom.env", prompts={"p": "ref"})
    assert config.env_file == "custom.env"
    assert config.prompts["p"] == "ref"


def test_model_config_object():
    """Test using ModelConfig object in VergerConfig."""
    model_cfg = ModelConfig(ref="my_model_ref", params={"temp": 0.7})
    config = VergerConfig(models={"m1": model_cfg})
    assert config.get_model_ref("m1") == "my_model_ref"


def test_get_model_ref_missing():
    """Test that get_model_ref raises KeyError for missing models."""
    config = VergerConfig()
    with pytest.raises(KeyError, match="Model 'nonexistent' not found"):
        config.get_model_ref("nonexistent")


def test_get_model_ref_string():
    """Test that get_model_ref works with simple string references."""
    config = VergerConfig(models={"m1": "ref_string"})
    assert config.get_model_ref("m1") == "ref_string"
