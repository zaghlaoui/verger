"""The core execution engine for running prompts against models."""

from typing import Any

from verger.core.models import model_registry
from verger.core.prompts import prompt_registry
from verger.core.tools import tool_registry


class ExecutionEngine:
    """
    The orchestrator that brings together models, prompts, and variables.
    It resolves the requested resources and executes the logic.
    """

    async def run(
        self,
        model_obj: Any,
        prompt_obj: Any,
        variables: dict[str, Any] | None = None,
        tools: list[Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Loads the prompt, fills it with variables, and runs it on the model.

        Args:
            model_obj: The model instance (or object to be resolved)
            prompt_obj: The prompt instance (or object to be resolved)
            variables: A dictionary of variables to inject into the prompt
            tools: A list of tool objects to be resolved and passed to the model
            **kwargs: Additional parameters to pass to the model's invoke method

        Returns:
            The string response from the model.
        """
        # 1. Resolve the model adapter
        model = model_registry.resolve(model_obj)

        # 2. Resolve and load the prompt adapter
        prompt = prompt_registry.resolve(prompt_obj)

        # 3. Resolve tool adapters
        resolved_tools = [tool_registry.resolve(t) for t in (tools or [])]

        # 4. Format the prompt and invoke the model
        return await model.invoke(
            prompt.format(**(variables or {})),
            tools=resolved_tools or None,
            **kwargs,
        )
