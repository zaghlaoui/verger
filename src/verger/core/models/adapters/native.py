from typing import Any

from verger.core.models import ModelResolver, VergerModel


class NativeFunctionAdapter(VergerModel):
    """Adapter for a standard Python function that takes a string and returns a string."""

    def __init__(self, func):
        self.func = func

    async def invoke(self, prompt: str, **kwargs) -> str:
        # Note: A robust implementation would check if the func is async or sync
        # and handle it appropriately. This is a simplified version.
        import asyncio

        if asyncio.iscoroutinefunction(self.func):
            return await self.func(prompt)
        return self.func(prompt)


class NativeFunctionResolver(ModelResolver):
    """Resolver that detects if the object is a standard callable."""

    def can_handle(self, obj: Any) -> bool:
        # We handle anything that is callable as a native function
        # This should usually be the LAST resolver checked in the registry
        return callable(obj)

    def create_adapter(self, obj: Any) -> VergerModel:
        return NativeFunctionAdapter(obj)


def get_resolver() -> ModelResolver:
    return NativeFunctionResolver()
