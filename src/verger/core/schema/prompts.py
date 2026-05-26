"""The prompt snapshot schemas for the Prompt Lab."""

from pydantic import BaseModel, Field

from .messages import VergerMessage
from .metadata import CollaborationMetadata


class PromptSnapshot(BaseModel):
    """
    A complete snapshot of a prompt at a specific point in time.

    Contains the full conversation structure and collaboration metadata.
    """

    messages: list[VergerMessage] = Field(
        description="The list of message templates in the prompt."
    )
    metadata: CollaborationMetadata = Field(description="Collaboration and versioning info.")
