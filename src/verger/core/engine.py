from typing import Any

from verger.core.models import model_registry
from verger.core.prompts import prompt_registry


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
        **kwargs: Any,
    ) -> str:
        """
        Loads the prompt, fills it with variables, and runs it on the model.

        Args:
            model_obj: The model instance (or object to be resolved)
            prompt_obj: The prompt instance (or object to be resolved)
            variables: A dictionary of variables to inject into the prompt
            **kwargs: Additional parameters to pass to the model's invoke method

        Returns:
            The string response from the model.
        """
        # 1. Resolve the model adapter
        model = model_registry.resolve(model_obj)

        # 2. Resolve and load the prompt adapter
        prompt = prompt_registry.resolve(prompt_obj)

        # 3. Format the prompt with variables
        formatted_text = prompt.format(**(variables or {}))

        # 4. Invoke the model and return the result
        return await model.invoke(formatted_text, **kwargs)
