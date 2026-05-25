"""Base interfaces for prompt adapters and resolvers."""

from typing import Any, Protocol, runtime_checkable

from verger.core.schema import VergerMessage


@runtime_checkable
class VergerPrompt(Protocol):
    """
    The interface for a loaded prompt.

    It provides the message templates and metadata about where it came from,
    regardless of the underlying prompt framework.
    """

    def get_messages(self) -> list[VergerMessage]:
        """
        Return the raw message templates of the prompt.

        Returns:
            A list of VergerMessage objects acting as templates.
        """
        ...

    def get_id(self) -> str:
        """
        Get a unique identifier for this prompt instance.

        Returns:
            A string identifier (e.g., class name or memory address).
        """
        ...

    def format(self, **kwargs: Any) -> list[VergerMessage]:
        """
        Fill the prompt templates with variables and return the resulting messages.

        Args:
            **kwargs: Variables to inject into the message templates.

        Returns:
            A list of fully formatted VergerMessage objects.
        """
        ...

    def get_variables(self) -> set[str]:
        """
        Extract the set of variable names required by this prompt.

        This allows for inspection and validation of placeholders
        before the prompt is formatted.

        Returns:
            A set of required variable names.
        """
        ...


@runtime_checkable
class PromptResolver(Protocol):
    """
    Interface for a Prompt Plugin.

    Resolvers are responsible for identifying objects from specific frameworks
    (e.g., standard strings) and wrapping them in a VergerPrompt adapter.
    """

    priority: int = 50
    """Priority of the resolver (lower numbers are checked first)."""

    def can_handle(self, obj: Any) -> bool:
        """
        Determine if this resolver can handle the given object.

        Args:
            obj: The prompt object to inspect.

        Returns:
            True if the resolver recognizes the object format.
        """
        ...

    def create_adapter(self, obj: Any) -> VergerPrompt:
        """
        Wrap the prompt object in a VergerPrompt adapter.

        Args:
            obj: The prompt object to wrap.

        Returns:
            An instance of a VergerPrompt implementation.
        """
        ...
