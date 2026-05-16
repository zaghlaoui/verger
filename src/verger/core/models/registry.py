from typing import Any

from .base import ModelResolver, VergerModel


class ModelRegistry:
    """
    A central hub that holds all registered Model Resolvers.
    It takes an unknown object, finds the right resolver, and returns an adapter.
    """

    def __init__(self):
        self._resolvers: list[ModelResolver] = []

    def register(self, resolver: ModelResolver) -> None:
        """Add a new plugin/resolver to the registry."""
        self._resolvers.append(resolver)

    def resolve(self, obj: Any) -> VergerModel:
        """
        Iterate through registered plugins to find one that can handle the object.
        Returns the unified VergerModel adapter.
        """
        for resolver in self._resolvers:
            if resolver.can_handle(obj):
                return resolver.create_adapter(obj)

        # If no plugin recognizes the object, we raise a helpful error.
        raise ValueError(
            f"No adapter found for object of type: {type(obj)}. "
            "Please ensure the correct Verger plugin is installed and registered."
        )


# Singleton instance to be imported across the application
registry = ModelRegistry()
