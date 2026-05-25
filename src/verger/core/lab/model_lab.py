"""Logic for managing model snapshots and configuration tracking."""

import logging

from .git_driver import GitService

logger = logging.getLogger(__name__)


class ModelLab:
    """
    Handles all business logic related to model versioning and collaboration.
    """

    def __init__(self, git: GitService):
        """
        Initialize the Model Lab.

        Args:
            git: The underlying Git storage driver.
        """
        self.git = git
