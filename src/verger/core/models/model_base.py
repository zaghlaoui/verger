"""Base interfaces for model adapters and resolvers."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class VergerModel(Protocol):
    """
    The universal interface that every Model Adapter must implement.

    The core execution logic of Verger only interacts with this interface,
    ensuring framework independence.
    """

    async def invoke(self, prompt: str, **kwargs: Any) -> str:
        """
        Run the prompt through the model and return the string result.

        Args:
            prompt: The formatted prompt string to send to the model.
            **kwargs: Additional model-specific parameters (e.g., temperature).

        Returns:
            The string response from the model.
        """
        ...


@runtime_checkable
class ModelResolver(Protocol):
    """
    Interface for a Model Plugin.

    Resolvers are responsible for identifying objects from specific frameworks
    (e.g., LangChain) and wrapping them in a VergerModel adapter.
    """

    priority: int = 50
    """Priority of the resolver (lower numbers are checked first)."""

    def can_handle(self, obj: Any) -> bool:
        """
        Determine if this resolver can handle the given object.

        Args:
            obj: The model object to inspect.

        Returns:
            True if the resolver recognizes the object's framework.
        """
        ...

    def create_adapter(self, obj: Any) -> VergerModel:
        """
        Wrap the user's object in a VergerModel adapter.

        Args:
            obj: The model object to wrap.

        Returns:
            An instance of a VergerModel implementation.
        """
        ...
