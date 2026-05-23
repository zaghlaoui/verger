"""Base interfaces for tool adapters and resolvers."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class VergerTool(Protocol):
    """
    The universal interface that every Tool Adapter must implement.

    This interface allows Verger to treat tools from different frameworks
    (e.g., LangChain, native Python functions) uniformly.
    """

    @property
    def name(self) -> str:
        """
        The unique name of the tool.

        Returns:
            The tool name used by models for identification.
        """
        ...

    @property
    def description(self) -> str:
        """
        A concise description of what the tool does.

        Returns:
            The description sent to the LLM to explain when to use the tool.
        """
        ...

    @property
    def args_schema(self) -> dict[str, Any]:
        """
        The JSON schema defining the tool's input arguments.

        Returns:
            A dictionary representing the JSON schema of the arguments.
        """
        ...

    async def run(self, **kwargs: Any) -> Any:
        """
        Execute the tool with the provided arguments.

        Args:
            **kwargs: The arguments for the tool execution.

        Returns:
            The result of the tool execution (usually a string or serializable object).
        """
        ...


@runtime_checkable
class ToolResolver(Protocol):
    """
    Interface for a Tool Plugin.

    Resolvers are responsible for identifying objects from specific frameworks
    (e.g., native functions) and wrapping them in a VergerTool adapter.
    """

    priority: int = 50
    """Priority of the resolver (lower numbers are checked first)."""

    def can_handle(self, obj: Any) -> bool:
        """
        Determine if this resolver can handle the given object.

        Args:
            obj: The tool object to inspect.

        Returns:
            True if the resolver recognizes the object's framework.
        """
        ...

    def create_adapter(self, obj: Any) -> VergerTool:
        """
        Wrap the user's object in a VergerTool adapter.

        Args:
            obj: The tool object to wrap.

        Returns:
            An instance of a VergerTool implementation.
        """
        ...
