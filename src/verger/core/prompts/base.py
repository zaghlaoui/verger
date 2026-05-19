from typing import Any, Protocol, runtime_checkable


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
        """A unique identifier for this prompt (e.g., its class or memory address)."""
        ...

    def format(self, **kwargs) -> str:
        """Fill the prompt with variables and return the resulting string."""
        ...

    def get_variables(self) -> set[str]:
        """
        Extract and return the set of variable names required by this prompt.
        This allows for inspection and validation before formatting.
        """
        ...


@runtime_checkable
class PromptResolver(Protocol):
    """
    Interface for a prompt plugin.
    It knows how to wrap a specific type of prompt object (e.g., String, LangChain Template, etc.)
    """

    def can_handle(self, obj: Any) -> bool:
        """Return True if this resolver recognizes the object format."""
        ...

    def create_adapter(self, obj: Any) -> VergerPrompt:
        """Wrap the prompt object and return a VergerPrompt adapter."""
        ...
