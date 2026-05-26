"""Adapter for native Python strings used as prompts."""

import string
from typing import Any

from verger.core.prompts import PromptResolver, VergerPrompt
from verger.core.schema import MessageRole, VergerMessage


class NativeStringPrompt(VergerPrompt):
    """
    A prompt defined as a raw string.

    This adapter handles standard Python strings, supporting f-string style
    placeholders (e.g., '{name}'). It automatically wraps the string into
    a single USER message.
    """

    def __init__(self, text: str):
        """
        Initialize the native string prompt.

        Args:
            text: The raw prompt template string.
        """
        self.text = text

    def get_messages(self) -> list[VergerMessage]:
        """
        Get the prompt as a list of message templates.

        Returns:
            A list containing a single USER message template.
        """
        return [VergerMessage(role=MessageRole.USER, content=self.text)]

    def get_id(self) -> str:
        """
        Get a unique identifier for this prompt instance.

        Returns:
            A string ID.
        """
        return f"StringPrompt-{id(self)}"

    def format(self, **kwargs: Any) -> list[VergerMessage]:
        """
        Format the prompt string and return it as a list of messages.

        Args:
            **kwargs: Variables to inject into the placeholders.

        Returns:
            A list containing one fully formatted USER message.
        """
        formatted_content = self.text.format(**kwargs)
        return [VergerMessage(role=MessageRole.USER, content=formatted_content)]

    def get_variables(self) -> set[str]:
        """
        Identify all variable placeholders in the prompt text.

        Parses the prompt text using `string.Formatter` to identify all named fields
        found in the template (e.g., '{name}').

        Returns:
            A set of variable names.
        """
        formatter = string.Formatter()
        return {
            field_name
            for _, field_name, _, _ in formatter.parse(self.text)
            if field_name is not None
        }


class NativeStringResolver(PromptResolver):
    """
    Adapter that recognizes native Python strings and wraps them.
    """

    priority: int = 100

    def can_handle(self, obj: Any) -> bool:
        """
        Check if the object is a string.

        Args:
            obj: The object to inspect.

        Returns:
            True if the object is a string instance.
        """
        return isinstance(obj, str)

    def create_adapter(self, obj: Any) -> VergerPrompt:
        """
        Create a NativeStringPrompt for the given string.

        Args:
            obj: The string to wrap.

        Returns:
            A new NativeStringPrompt instance.
        """
        return NativeStringPrompt(obj)


def get_resolver() -> PromptResolver:
    """
    Entry point for the plugin system to get the Native string resolver.

    Returns:
        An instance of NativeStringResolver.
    """
    return NativeStringResolver()
