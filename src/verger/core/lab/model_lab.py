"""Logic for managing model snapshots and configuration tracking."""

import json
import logging
from typing import Any

from verger.core.schema import CollaborationMetadata, ModelSnapshot

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

    def capture_snapshot(
        self,
        anchor: str,
        ref: str,
        params: dict[str, Any],
        author: str,
        description: str | None = None,
        tags: list[str] | None = None,
        parent_hash: str | None = None,
    ) -> str:
        """
        Create and save a new snapshot of a model configuration.

        Args:
            anchor: The name/id of the model configuration.
            ref: The model reference string (e.g. 'openai:gpt-4').
            params: Model parameters (temperature, etc.).
            author: The person creating the snapshot.
            description: Optional summary of changes.
            tags: Optional list of organizational tags.
            parent_hash: Optional parent commit hash for branching.

        Returns:
            The hash of the newly created snapshot commit.
        """
        snapshot = ModelSnapshot(
            ref=ref,
            params=params,
            metadata=CollaborationMetadata(author=author, description=description, tags=tags or []),
        )

        # We reuse the Git storage logic.
        blob_hash = self.git._run_git(
            "hash-object", "-w", "--stdin", input_data=snapshot.model_dump_json()
        )

        tree_input = f"100644 blob {blob_hash}\t{anchor}.model.json\n"

        base_parent = parent_hash or self.git.get_latest_commit()
        if base_parent:
            existing_entries = self.git._run_git("ls-tree", base_parent, "--")
            for line in existing_entries.splitlines():
                if not line.endswith(f"\t{anchor}.model.json"):
                    tree_input += line + "\n"

        tree_hash = self.git._run_git("mktree", input_data=tree_input)
        commit_args = ["commit-tree", tree_hash, "-m", f"verger: model snapshot for {anchor}"]
        if base_parent:
            commit_args.extend(["-p", base_parent])

        commit_hash = self.git._run_git(*commit_args)
        self.git._run_git("update-ref", self.git.REF_NAME, commit_hash)

        return commit_hash

    def get_history(self, anchor: str) -> list[dict[str, Any]]:
        """
        Retrieve the version history for a specific model.

        Args:
            anchor: The name of the model configuration.

        Returns:
            A list of snapshot summaries.
        """
        all_commits = self.git.get_history()
        model_versions = []

        for entry in all_commits:
            try:
                content = self.git._run_git("show", f"{entry['hash']}:{anchor}.model.json", "--")
                snapshot = ModelSnapshot(**json.loads(content))
                model_versions.append(
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
                # If this commit doesn't contain the specific model, skip it
                logger.debug(f"Model {anchor} not found in commit {entry['hash']}")
                continue

        return model_versions

    def load_snapshot(self, anchor: str, commit_hash: str) -> ModelSnapshot:
        """
        Load a specific version of a model configuration.
        """
        content = self.git._run_git("show", f"{commit_hash}:{anchor}.model.json", "--")
        return ModelSnapshot(**json.loads(content))
