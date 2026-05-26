"""The conversation message schemas for AI interactions."""

from enum import StrEnum

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    """The role of the sender of a message."""

    SYSTEM = "system"
    USER = "user"
    AI = "ai"
    TOOL = "tool"


class VergerMessage(BaseModel):
    """
    A single message in an AI conversation.

    This format is designed to be compatible with most AI providers
    (OpenAI, Anthropic) and frameworks (LangChain).
    """

    role: MessageRole = Field(description="The role of the message sender.")
    content: str = Field(description="The text content of the message.")
    name: str | None = Field(
        default=None, description="Optional name for the sender (e.g. for multiple tools)."
    )
    tool_call_id: str | None = Field(
        default=None, description="The ID of the tool call this message responds to."
    )
