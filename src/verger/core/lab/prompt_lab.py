"""Logic for managing prompt snapshots and collaboration."""

import logging
from typing import Any

from verger.core.schema import CollaborationMetadata, MessageRole, PromptSnapshot, VergerMessage

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

    def capture_snapshot(
        self,
        anchor: str,
        messages: list[dict[str, str]],
        author: str,
        description: str | None = None,
        tags: list[str] | None = None,
        parent_hash: str | None = None,
    ) -> str:
        """
        Create and save a new snapshot of a prompt.

        Args:
            anchor: The name/id of the prompt being versioned.
            messages: List of message dictionaries (role, content).
            author: The person creating the snapshot.
            description: Optional summary of changes.
            tags: Optional list of organizational tags.
            parent_hash: Optional parent commit hash for branching.

        Returns:
            The hash of the newly created snapshot commit.
        """
        # 1. Convert dicts to VergerMessage objects
        verger_messages = [
            VergerMessage(role=MessageRole(m["role"]), content=m["content"]) for m in messages
        ]

        # 2. Build metadata
        metadata = CollaborationMetadata(author=author, description=description, tags=tags or [])

        # 3. Create full snapshot
        snapshot = PromptSnapshot(messages=verger_messages, metadata=metadata)

        # 4. Save via Git
        return self.git.save_prompt_snapshot(anchor, snapshot, parent_hash=parent_hash)

    def get_history(self, anchor: str) -> list[dict[str, Any]]:
        """
        Retrieve the version history for a specific prompt.

        Args:
            anchor: The name of the prompt.

        Returns:
            A list of snapshot summaries (hash, author, date, description).
        """
        all_commits = self.git.get_history()
        prompt_versions = []

        for entry in all_commits:
            try:
                snapshot = self.git.load_prompt_snapshot(entry["hash"], anchor)
                prompt_versions.append(
                    {
                        "hash": entry["hash"],
                        "parents": entry["parents"],
                        "author": snapshot.metadata.author,
                        "created_at": snapshot.metadata.created_at,
                        "description": snapshot.metadata.description,
                        "tags": snapshot.metadata.tags,
                    }
                )
            except Exception:
                # If this commit doesn't contain the specific anchor, skip it
                logger.debug(f"Prompt {anchor} not found in commit {entry['hash']}")
                continue

        return prompt_versions

    def load_snapshot(self, anchor: str, commit_hash: str) -> PromptSnapshot:
        """
        Load a specific version of a prompt.

        Args:
            anchor: The name of the prompt.
            commit_hash: The specific version to load.

        Returns:
            The PromptSnapshot object.
        """
        return self.git.load_prompt_snapshot(commit_hash, anchor)
