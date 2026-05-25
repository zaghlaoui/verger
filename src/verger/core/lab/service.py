"""Main facade for the Verger Prompt Lab."""

import logging
from pathlib import Path

from .git_driver import GitService
from .model_lab import ModelLab
from .prompt_lab import PromptLab

logger = logging.getLogger(__name__)


class LabService:
    """
    The orchestrator that brings together prompt and model management.

    This class provides a unified interface for the rest of the application
    to interact with the Prompt Lab features.
    """

    def __init__(self, repo_path: Path | None = None):
        """
        Initialize the Lab service.

        Args:
            repo_path: Path to the git repository.
        """
        self.git = GitService(repo_path=repo_path)
        self.prompts = PromptLab(self.git)
        self.models = ModelLab(self.git)
