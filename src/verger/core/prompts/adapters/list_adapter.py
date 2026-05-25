"""Adapter for native Python lists used as prompts."""

import string
from typing import Any

from verger.core.prompts import PromptResolver, VergerPrompt
from verger.core.schema import MessageRole, VergerMessage


class NativeListPrompt(VergerPrompt):
    """
    A prompt defined as a list of message dictionaries.

    Supports formats like:
    [
        {"role": "system", "content": "You are a {role}"},
        {"role": "user", "content": "Hello {name}"}
    ]
    """

    def __init__(self, messages: list[dict[str, str]]):
        """
        Initialize the native list prompt.

        Args:
            messages: A list of dictionaries representing messages.
        """
        self.message_templates = [
            VergerMessage(role=MessageRole(m["role"]), content=m["content"]) for m in messages
        ]

    def get_messages(self) -> list[VergerMessage]:
        """
        Get the raw message templates.

        Returns:
            The list of VergerMessage templates.
        """
        return self.message_templates

    def get_id(self) -> str:
        """
        Get a unique identifier.

        Returns:
            A string ID.
        """
        return f"ListPrompt-{id(self)}"

    def format(self, **kwargs: Any) -> list[VergerMessage]:
        """
        Format all message templates with variables.

        Args:
            **kwargs: Variables for template injection.

        Returns:
            A list of formatted VergerMessage objects.
        """
        return [
            VergerMessage(role=m.role, content=m.content.format(**kwargs))
            for m in self.message_templates
        ]

    def get_variables(self) -> set[str]:
        """
        Identify all variables across all messages.

        Returns:
            A set of unique variable names.
        """
        formatter = string.Formatter()
        all_vars = set()
        for m in self.message_templates:
            vars_in_msg = {
                field_name
                for _, field_name, _, _ in formatter.parse(m.content)
                if field_name is not None
            }
            all_vars.update(vars_in_msg)
        return all_vars


class NativeListResolver(PromptResolver):
    """
    Adapter that recognizes lists of dictionaries as prompts.
    """

    priority: int = 80

    def can_handle(self, obj: Any) -> bool:
        """
        Check if the object is a list of dicts with role and content.
        """
        if not isinstance(obj, list) or not obj:
            return False

        first = obj[0]
        return isinstance(first, dict) and "role" in first and "content" in first

    def create_adapter(self, obj: Any) -> VergerPrompt:
        """
        Create a NativeListPrompt.
        """
        return NativeListPrompt(obj)


def get_resolver() -> PromptResolver:
    """
    Entry point for the plugin system.
    """
    return NativeListResolver()
