from typing import Any

from verger.core.models import ModelResolver, VergerModel


class LangChainAdapter(VergerModel):
    """Adapter for LangChain 'Runnable' objects."""

    def __init__(self, runnable):
        self.runnable = runnable

    async def invoke(self, prompt: str, **kwargs) -> str:
        # Assuming the runnable returns an object with a .content attribute
        # like AIMessage, or just a string.
        result = await self.runnable.ainvoke(prompt)
        if hasattr(result, "content"):
            return result.content
        return str(result)


class LangChainResolver(ModelResolver):
    """Resolver that detects LangChain objects using duck-typing."""

    def can_handle(self, obj: Any) -> bool:
        # We don't import langchain here! We check structurally to avoid Dependency Errors.
        # 1. Check if it has the standard LangChain method 'ainvoke'
        # 2. Verify 'langchain' is somewhere in its module path.
        if hasattr(obj, "ainvoke"):
            # Check the class hierarchy (MRO) for langchain modules
            for base in obj.__class__.__mro__:
                if "langchain" in base.__module__:
                    return True
        return False

    def create_adapter(self, obj: Any) -> VergerModel:
        return LangChainAdapter(obj)


def get_resolver() -> ModelResolver:
    return LangChainResolver()
