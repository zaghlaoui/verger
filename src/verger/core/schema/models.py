"""The model snapshot schemas for the Prompt Lab."""

from typing import Any

from pydantic import BaseModel, Field

from .metadata import CollaborationMetadata


class ModelSnapshot(BaseModel):
    """
    A complete snapshot of a model configuration.

    Captures the model reference, parameters, and collaboration metadata.
    """

    ref: str = Field(description="The unique reference string for the model.")
    params: dict[str, Any] = Field(
        default_factory=dict, description="Model parameters like temperature."
    )
    metadata: CollaborationMetadata = Field(description="Collaboration and versioning info.")
