"""Central registry for discovering and resolving AI tool adapters."""

from typing import Any

from verger.core.exceptions import VergerResolutionError

from .tool_base import ToolResolver, VergerTool


class ToolRegistry:
    """
    Registry for Tool Resolvers.

    This class serves as a central hub for all registered tool adapters. It takes an
    unknown tool object (e.g., a native function), identifies the appropriate
    resolver, and returns a unified VergerTool adapter.
    """

    def __init__(self):
        self._resolvers: list[ToolResolver] = []

    def register(self, resolver: ToolResolver) -> None:
        """
        Register a new tool resolver.

        The registry automatically sorts resolvers by priority (lower numbers first).

        Args:
            resolver: The ToolResolver instance to add to the registry.
        """
        self._resolvers.append(resolver)
        self._resolvers.sort(key=lambda r: getattr(r, "priority", 50))

    def resolve(self, obj: Any) -> VergerTool:
        """
        Resolve an object into a unified VergerTool adapter.

        This method iterates through all registered resolvers and returns the adapter
        provided by the first resolver that can handle the given object.

        Args:
            obj: The object to be resolved (e.g., a tool instance or function).

        Returns:
            The corresponding VergerTool adapter.

        Raises:
            VergerResolutionError: If no registered resolver can handle the provided object.
        """
        for resolver in self._resolvers:
            if resolver.can_handle(obj):
                return resolver.create_adapter(obj)

        raise VergerResolutionError(
            f"No tool adapter found for object of type: {type(obj)}. "
            "Please ensure the correct Verger tool plugin is installed and registered."
        )


# Singleton instance to be used across the application
tool_registry = ToolRegistry()
