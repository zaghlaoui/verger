from typing import Any

from .base import PromptResolver, VergerPrompt


class PromptRegistry:
    """
    Registry for Prompt Resolvers.
    It takes an unknown prompt object, finds the right resolver, and returns an adapter.
    """

    def __init__(self):
        self._resolvers: list[PromptResolver] = []

    def register(self, resolver: PromptResolver) -> None:
        self._resolvers.append(resolver)

    def resolve(self, obj: Any) -> VergerPrompt:
        """Find the right resolver for the given prompt object."""
        for resolver in self._resolvers:
            if resolver.can_handle(obj):
                return resolver.create_adapter(obj)

        raise ValueError(
            f"No prompt adapter found for object of type: {type(obj)}. "
            "Please ensure the correct Verger prompt plugin is installed."
        )


# Singleton instance
registry = PromptRegistry()
