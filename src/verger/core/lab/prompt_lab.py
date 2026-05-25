"""Logic for managing prompt snapshots and collaboration."""

import logging

from .git_driver import GitService

logger = logging.getLogger(__name__)


class PromptLab:
    """
    Handles all business logic related to prompt versioning and collaboration.
    """

    def __init__(self, git: GitService):
        """
        Initialize the Prompt Lab.

        Args:
            git: The underlying Git storage driver.
        """
        self.git = git
