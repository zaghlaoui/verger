"""Adapter for LangChain models and runnables."""

from typing import Any

from verger.core.models import ModelResolver, VergerModel
from verger.core.tools.tool_base import VergerTool


class LangChainAdapter(VergerModel):
    """
    Adapter for LangChain 'Runnable' objects.

    This adapter allows Verger to interact with any LangChain object that implements
    the Runnable interface (specifically the async `ainvoke` method).
    """

    def __init__(self, runnable: Any):
        """
        Initialize the LangChain adapter.

        Args:
            runnable: A LangChain object (e.g., ChatOpenAI, PromptTemplate, etc.).
        """
        self.runnable = runnable

    async def invoke(
        self,
        prompt: str,
        tools: list[VergerTool] | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Invoke the LangChain runnable with the given prompt.

        Args:
            prompt: The formatted prompt string to send to the model.
            tools: Optional list of tools to bind to the model.
            **kwargs: Additional parameters to pass to ainvoke.

        Returns:
            The string content of the model's response.
        """
        runnable = self.runnable

        # If tools are provided, try to bind them if the runnable supports it
        if tools and hasattr(runnable, "bind_tools"):
            # LangChain models usually take the tools directly or as a list
            # We pass the underlying tool objects if possible, but for now
            # we just pass the adapters if they are already LangChain-compatible
            # OR we might need a LangChainToolAdapter.
            # For this MVP, we just log a warning if we can't easily bind.
            runnable = runnable.bind_tools(tools)

        # Assuming the runnable returns an object with a .content attribute
        # like AIMessage, or just a string.
        result = await runnable.ainvoke(prompt, **kwargs)
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)


class LangChainResolver(ModelResolver):
    """
    Resolver that detects LangChain objects using duck-typing.

    This resolver identifies LangChain objects without requiring 'langchain'
    to be installed as a mandatory dependency of Verger.
    """

    priority: int = 20

    def can_handle(self, obj: Any) -> bool:
        """
        Check if the object is a LangChain runnable.

        Args:
            obj: The object to inspect.

        Returns:
            True if the object has an 'ainvoke' method and belongs to a langchain module.
        """
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
        """
        Create a LangChainAdapter for the given object.

        Args:
            obj: The LangChain runnable to wrap.

        Returns:
            A new LangChainAdapter instance.
        """
        return LangChainAdapter(obj)


def get_resolver() -> ModelResolver:
    """
    Entry point for the plugin system to get the LangChain resolver.

    Returns:
        An instance of LangChainResolver.
    """
    return LangChainResolver()
