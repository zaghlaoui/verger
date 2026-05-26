"""Adapter for native Python functions used as models."""

import asyncio
from collections.abc import Callable
from typing import Any

from verger.core.models import ModelResolver, VergerModel
from verger.core.schema import MessageRole, VergerMessage
from verger.core.tools.tool_base import VergerTool


class NativeFunctionAdapter(VergerModel):
    """
    Adapter for a standard Python function used as an AI model.

    This allows any simple Python function (sync or async) to be treated as an
    AI model. It intelligently handles both string-based and message-based
    function signatures.
    """

    def __init__(self, func: Callable[..., Any]):
        """
        Initialize the native function adapter.

        Args:
            func: A callable to wrap as a model.
        """
        self.func = func

    async def invoke(
        self,
        messages: list[VergerMessage],
        tools: list[VergerTool] | None = None,
        **kwargs: Any,
    ) -> VergerMessage:
        """
        Invoke the native function and return the result as a message.

        Args:
            messages: The list of formatted messages.
            tools: Optional list of tools.
            **kwargs: Additional parameters.

        Returns:
            A VergerMessage with role=AI containing the function's output.
        """
        import inspect

        sig = inspect.signature(self.func)
        params = sig.parameters

        # Prepare arguments based on what the function accepts
        args_to_pass: dict[str, Any] = {}

        if "messages" in params:
            args_to_pass["messages"] = messages
        elif params:
            # If it doesn't accept 'messages', join all content as a single 'prompt' string
            # This provides backward compatibility for string-based functions.
            full_prompt = "\n\n".join(m.content for m in messages)
            # Find the first parameter name to pass the prompt to
            first_param = list(params.keys())[0]
            args_to_pass[first_param] = full_prompt

        if "tools" in params:
            args_to_pass["tools"] = tools

        # Execute
        if asyncio.iscoroutinefunction(self.func):
            result = await self.func(**args_to_pass, **kwargs)
        else:
            result = self.func(**args_to_pass, **kwargs)

        return VergerMessage(role=MessageRole.AI, content=str(result))


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
