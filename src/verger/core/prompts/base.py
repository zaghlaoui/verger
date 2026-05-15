from typing import Protocol, runtime_checkable


@runtime_checkable
class VergerPrompt(Protocol):
    """
    The interface for a loaded prompt.
    It provides the raw text and metadata about where it came from.
    """

    def get_text(self) -> str:
        """Return the current text of the prompt."""
        ...

    def get_id(self) -> str:
        """A unique identifier for this prompt (e.g., 'module.name:VARIABLE')."""
        ...


@runtime_checkable
class PromptResolver(Protocol):
    """
    Interface for a prompt plugin.
    It knows how to load a specific type of prompt (e.g., String in Python, Jinja file, etc.)
    """

    def can_handle(self, ref: str) -> bool:
        """Return True if this resolver recognizes the reference format."""
        ...

    def load(self, ref: str) -> VergerPrompt:
        """Load the prompt and return a VergerPrompt object."""
        ...
