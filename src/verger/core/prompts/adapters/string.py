"""Adapter for native Python strings used as prompts."""

import string
from typing import Any

from verger.core.prompts import PromptResolver, VergerPrompt


class NativeStringPrompt(VergerPrompt):
    """
    A prompt defined as a raw string.

    This adapter handles standard Python strings and supports f-string style
    placeholders (e.g., '{name}') for variable injection.
    """

    def __init__(self, text: str):
        """
        Initialize the native string prompt.

        Args:
            text: The raw prompt template string.
        """
        self.text = text

    def get_text(self) -> str:
        """
        Get the raw template text.

        Returns:
            The template string.
        """
        return self.text

    def get_id(self) -> str:
        """
        Get a unique identifier for this prompt instance.

        Returns:
            A string ID.
        """
        return f"StringPrompt-{id(self)}"

    def format(self, **kwargs: Any) -> str:
        """
        Format the prompt string with the provided variables.

        Args:
            **kwargs: Variables to inject into the placeholders.

        Returns:
            The formatted prompt string.
        """
        return self.text.format(**kwargs)

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
