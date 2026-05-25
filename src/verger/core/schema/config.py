"""Pydantic schemas for Verger configuration."""

from typing import Any

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for an AI model."""

    ref: str
    params: dict[str, Any] = Field(default_factory=dict)


class RuntimeStatus(BaseModel):
    """Internal state tracking for the Verger execution environment."""

    config_source: str = "Unknown"
    env_keys: list[str] = Field(default_factory=list)


class VergerConfig(BaseModel):
    """The main [tool.verger] configuration schema."""

    env_file: str | None = ".env"

    # Runtime status (not loaded from TOML)
    status: RuntimeStatus = Field(default_factory=RuntimeStatus, exclude=True)

    # Prompts are currently just a name mapped to a reference string
    prompts: dict[str, str] = Field(default_factory=dict)

    # Models can be a simple reference string or a detailed ModelConfig object
    models: dict[str, str | ModelConfig] = Field(default_factory=dict)

    # Tools are currently just a name mapped to a reference string
    tools: dict[str, str] = Field(default_factory=dict)

    def get_model_ref(self, model_name: str) -> str:
        """Helper to get the string reference for a model regardless of its config style."""
        config = self.models.get(model_name)
        if config is None:
            raise KeyError(f"Model '{model_name}' not found in configuration.")
        if isinstance(config, ModelConfig):
            return config.ref
        return config
