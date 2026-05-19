import string
from typing import Any

from verger.core.prompts.base import PromptResolver, VergerPrompt


class NativeStringPrompt(VergerPrompt):
    """A prompt defined as a raw string."""

    def __init__(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> str:
        return f"StringPrompt-{id(self)}"

    def format(self, **kwargs) -> str:
        return self.text.format(**kwargs)

    def get_variables(self) -> set[str]:
        """
        Parses the prompt text using string.Formatter to identify all named fields.
        Returns a set of variable names found in the template (e.g., '{name}').
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
        return isinstance(obj, str)

    def create_adapter(self, obj: Any) -> VergerPrompt:
        return NativeStringPrompt(obj)


def get_resolver() -> PromptResolver:
    return NativeStringResolver()
