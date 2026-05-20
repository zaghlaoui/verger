from typing import Any

from verger.core.exceptions import VergerResolutionError

from .base import PromptResolver, VergerPrompt


class PromptRegistry:
    """
    Registry for Prompt Resolvers.

    This class serves as a central hub for all registered prompt adapters. It takes an
    unknown prompt object (e.g., a string or a complex template), identifies the
    appropriate resolver, and returns a unified VergerPrompt adapter.
    """

    def __init__(self):
        self._resolvers: list[PromptResolver] = []

    def register(self, resolver: PromptResolver) -> None:
        """
        Register a new prompt resolver.

        Args:
            resolver: The PromptResolver instance to add to the registry.
        """
        self._resolvers.append(resolver)

    def resolve(self, obj: Any) -> VergerPrompt:
        """
        Resolve an object into a unified VergerPrompt adapter.

        This method iterates through all registered resolvers and returns the adapter
        provided by the first resolver that can handle the given object.

        Args:
            obj: The object to be resolved (e.g., a prompt instance).

        Returns:
            The corresponding VergerPrompt adapter.

        Raises:
            VergerResolutionError: If no registered resolver can handle the provided object.
        """
        for resolver in self._resolvers:
            if resolver.can_handle(obj):
                return resolver.create_adapter(obj)

        raise VergerResolutionError(
            f"No prompt adapter found for object of type: {type(obj)}. "
            "Please ensure the correct Verger prompt plugin is installed and registered."
        )


# Singleton instance to be used across the application
registry = PromptRegistry()
