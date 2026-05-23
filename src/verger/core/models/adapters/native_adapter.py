"""Adapter for native Python functions used as models."""

import asyncio
from collections.abc import Callable
from typing import Any

from verger.core.models import ModelResolver, VergerModel
from verger.core.tools.tool_base import VergerTool


class NativeFunctionAdapter(VergerModel):
    """
    Adapter for a standard Python function that takes a string and returns a string.

    This allows any simple Python function (sync or async) to be treated as an
    AI model within Verger.
    """

    def __init__(self, func: Callable[[str], str] | Callable[[str], Any]):
        """
        Initialize the native function adapter.

        Args:
            func: A callable that takes a string and returns a string or coroutine.
        """
        self.func = func

    async def invoke(
        self,
        prompt: str,
        tools: list[VergerTool] | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Invoke the native function with the given prompt.

        Args:
            prompt: The formatted prompt string.
            tools: Optional list of tools (passed if the function signature allows it).
            **kwargs: Additional parameters (ignored by default for native functions).

        Returns:
            The string result returned by the function.
        """
        # If the function accepts a 'tools' argument, we pass it.
        # Otherwise, we just pass the prompt.
        import inspect
        from typing import cast

        sig = inspect.signature(self.func)
        if "tools" in sig.parameters:
            if asyncio.iscoroutinefunction(self.func):
                func = cast(Callable[..., Any], self.func)
                return await func(prompt, tools=tools)
            func = cast(Callable[..., Any], self.func)
            return str(func(prompt, tools=tools))

        if asyncio.iscoroutinefunction(self.func):
            return await self.func(prompt)
        return str(self.func(prompt))


class NativeFunctionResolver(ModelResolver):
    """
    Resolver that detects if the object is a standard callable.

    This resolver is highly generic and should typically be registered as a
    fallback (last in the list).
    """

    priority: int = 100

    def can_handle(self, obj: Any) -> bool:
        """
        Check if the object is callable.

        Args:
            obj: The object to inspect.

        Returns:
            True if the object is a callable function or method.
        """
        return callable(obj)

    def create_adapter(self, obj: Any) -> VergerModel:
        """
        Create a NativeFunctionAdapter for the given callable.

        Args:
            obj: The callable to wrap.

        Returns:
            A new NativeFunctionAdapter instance.
        """
        return NativeFunctionAdapter(obj)


def get_resolver() -> ModelResolver:
    """
    Entry point for the plugin system to get the Native function resolver.

    Returns:
        An instance of NativeFunctionResolver.
    """
    return NativeFunctionResolver()
