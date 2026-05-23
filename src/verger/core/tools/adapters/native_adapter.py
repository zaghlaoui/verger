"""Adapter for native Python functions to be used as Verger tools."""

import inspect
from collections.abc import Callable
from typing import Any

from verger.core.tools.tool_base import ToolResolver, VergerTool


class NativeToolAdapter:
    """
    Wraps a native Python function into the VergerTool interface.
    """

    def __init__(self, func: Callable[..., Any]):
        """
        Initialize the adapter.

        Args:
            func: The Python function to wrap.
        """
        self._func = func
        self._name = getattr(func, "__name__", str(func))
        self._description = getattr(func, "__doc__", None) or "No description provided."

    @property
    def name(self) -> str:
        """Get the name of the function."""
        return self._name

    @property
    def description(self) -> str:
        """Get the docstring of the function."""
        return self._description

    @property
    def args_schema(self) -> dict[str, Any]:
        """
        Extract a basic JSON schema from the function signature.
        Note: This is a simplified implementation for demonstration.
        """
        signature = inspect.signature(self._func)
        parameters = {}
        required = []

        for name, param in signature.parameters.items():
            param_info = {"type": "string"}  # Defaulting to string for simplicity
            if param.default is inspect.Parameter.empty:
                required.append(name)
            parameters[name] = param_info

        return {
            "type": "object",
            "properties": parameters,
            "required": required,
        }

    async def run(self, **kwargs: Any) -> Any:
        """
        Execute the function. Handles both sync and async functions.
        """
        if inspect.iscoroutinefunction(self._func):
            return await self._func(**kwargs)
        return self._func(**kwargs)


class NativeToolResolver:
    """
    Resolver for native Python functions.
    """

    priority: int = 100  # Lower priority than specific framework adapters

    def can_handle(self, obj: Any) -> bool:
        """Check if the object is a callable."""
        return callable(obj) and not isinstance(obj, type)

    def create_adapter(self, obj: Any) -> VergerTool:
        """Create a NativeToolAdapter for the callable."""
        return NativeToolAdapter(obj)


def get_resolver() -> ToolResolver:
    """Return the native tool resolver instance."""
    return NativeToolResolver()
