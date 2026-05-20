"""Base interfaces for model adapters and resolvers."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class VergerModel(Protocol):
    """
    The universal interface that every Model Adapter must implement.
    The core runner logic will only interact with this interface.
    """

    async def invoke(self, prompt: str, **kwargs) -> str:
        """Run the prompt through the model and return the string result."""
        ...


@runtime_checkable
class ModelResolver(Protocol):
    """
    The interface for a Plugin. It tells Verger if it can handle a specific
    user object, and how to create the adapter for it.
    """

    def can_handle(self, obj: Any) -> bool:
        """Return True if this resolver recognizes the object's framework."""
        ...

    def create_adapter(self, obj: Any) -> VergerModel:
        """Wrap the user's object in a class that implements VergerModel."""
        ...
