"""Prompt registration and adapter interfaces."""

from .base import PromptResolver, VergerPrompt
from .prompt_registry import prompt_registry

__all__ = ["prompt_registry", "VergerPrompt", "PromptResolver"]
