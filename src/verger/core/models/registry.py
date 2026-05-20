from typing import Any

from verger.core.exceptions import VergerResolutionError

from .base import ModelResolver, VergerModel


class ModelRegistry:
    """
    Registry for Model Resolvers.

    This class serves as a central hub for all registered model adapters. It takes an
    unknown model object (e.g., from LangChain or a native function), identifies the
    appropriate resolver, and returns a unified VergerModel adapter.
    """

    def __init__(self):
        self._resolvers: list[ModelResolver] = []

    def register(self, resolver: ModelResolver) -> None:
        """
        Register a new model resolver.

        Args:
            resolver: The ModelResolver instance to add to the registry.
        """
        self._resolvers.append(resolver)

    def resolve(self, obj: Any) -> VergerModel:
        """
        Resolve an object into a unified VergerModel adapter.

        This method iterates through all registered resolvers and returns the adapter
        provided by the first resolver that can handle the given object.

        Args:
            obj: The object to be resolved (e.g., a model instance).

        Returns:
            The corresponding VergerModel adapter.

        Raises:
            VergerResolutionError: If no registered resolver can handle the provided object.
        """
        for resolver in self._resolvers:
            if resolver.can_handle(obj):
                return resolver.create_adapter(obj)

        raise VergerResolutionError(
            f"No model adapter found for object of type: {type(obj)}. "
            "Please ensure the correct Verger model plugin is installed and registered."
        )


# Singleton instance to be used across the application
registry = ModelRegistry()
