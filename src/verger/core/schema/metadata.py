"""The collaboration and versioning metadata schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """A feedback comment from a team member."""

    author: str = Field(description="The name or email of the commenter.")
    text: str = Field(description="The comment content.")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the comment was made."
    )


class CollaborationMetadata(BaseModel):
    """
    Metadata used for collaboration and version tracking in the Prompt Lab.

    This data lives alongside the prompt/model content in the hidden Git branch.
    """

    author: str = Field(description="The creator of this snapshot.")
    description: str | None = Field(default=None, description="Why this version was created.")
    tags: list[str] = Field(default_factory=list, description="Labels for organizing snapshots.")
    comments: list[Comment] = Field(default_factory=list, description="Team feedback history.")
    created_at: datetime = Field(
        default_factory=datetime.now, description="When this snapshot was created."
    )
    archived: bool = Field(default=False, description="Whether this version is hidden/archived.")
