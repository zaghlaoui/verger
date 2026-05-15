from typing import List
from .base import PromptResolver, VergerPrompt


class PromptRegistry:
    """
    Registry for Prompt Resolvers.
    Unlike models (which are objects), prompts are often identified by a
    reference string (e.g., a path or a module:var).
    """

    def __init__(self):
        self._resolvers: List[PromptResolver] = []

    def register(self, resolver: PromptResolver) -> None:
        self._resolvers.append(resolver)

    def resolve(self, ref: str) -> VergerPrompt:
        """Find the right resolver for the given prompt reference."""
        for resolver in self._resolvers:
            if resolver.can_handle(ref):
                return resolver.load(ref)

        raise ValueError(f"No prompt resolver found for reference: {ref}")


# Singleton instance
registry = PromptRegistry()
