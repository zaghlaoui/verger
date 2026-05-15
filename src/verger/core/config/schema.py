from typing import Dict, Optional, Union
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for an AI model."""

    ref: str
    # Future fields: provider, temperature, etc. can be added here.


class VergerConfig(BaseModel):
    """The main [tool.verger] configuration schema."""

    env_file: Optional[str] = ".env"

    # Prompts are currently just a name mapped to a reference string
    prompts: Dict[str, str] = Field(default_factory=dict)

    # Models can be a simple reference string or a detailed ModelConfig object
    models: Dict[str, Union[str, ModelConfig]] = Field(default_factory=dict)

    def get_model_ref(self, model_name: str) -> str:
        """Helper to get the string reference for a model regardless of its config style."""
        config = self.models.get(model_name)
        if isinstance(config, ModelConfig):
            return config.ref
        return config
