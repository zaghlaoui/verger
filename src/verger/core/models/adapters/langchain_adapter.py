"""Adapter for LangChain models and runnables."""

from typing import Any

from verger.core.models import ModelResolver, VergerModel
from verger.core.schema import MessageRole, VergerMessage
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
        messages: list[VergerMessage],
        tools: list[VergerTool] | None = None,
        **kwargs: Any,
    ) -> VergerMessage:
        """
        Invoke the LangChain runnable and return a VergerMessage result.

        Args:
            messages: A list of formatted messages.
            tools: Optional list of tools to bind to the model.
            **kwargs: Additional parameters to pass to ainvoke.

        Returns:
            A VergerMessage containing the AI's response.
        """
        runnable = self.runnable

        # Convert VergerMessage objects to LangChain tuple format
        role_mapping = {
            "system": "system",
            "user": "human",
            "ai": "ai",
            "tool": "tool",
        }
        lc_messages = [(role_mapping.get(m.role, "human"), m.content) for m in messages]

        # If tools are provided, try to bind them
        if tools and hasattr(runnable, "bind_tools"):
            runnable = runnable.bind_tools(tools)

        result = await runnable.ainvoke(lc_messages, **kwargs)

        # Extract content and return as VergerMessage
        content = str(getattr(result, "content", result))
        return VergerMessage(role=MessageRole.AI, content=content)


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
