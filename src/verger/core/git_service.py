"""Service for interacting with Git for hidden data storage."""

import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from verger.core.schema import PromptSnapshot

logger = logging.getLogger(__name__)


class GitService:
    """
    Service to manage prompt and model snapshots in a hidden Git reference.

    Uses Git plumbing commands to store data in the Git object database
    without affecting the user's working directory.
    """

    REF_NAME = "refs/verger/data"
    # Security: Strict regex for anchor names to prevent path traversal or injection
    ANCHOR_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\./]+$")

    def __init__(self, repo_path: Path | None = None):
        """
        Initialize the Git service.

        Args:
            repo_path: Path to the git repository. Defaults to CWD.
        """
        self.repo_path = repo_path or Path.cwd()
        self._git_path = shutil.which("git")

    def _validate_anchor(self, anchor: str) -> None:
        """Ensure the anchor name is safe."""
        if not self.ANCHOR_PATTERN.match(anchor) or ".." in anchor:
            raise ValueError(f"Invalid or unsafe anchor name: {anchor}")

    def _run_git(self, *args: str, input_data: str | None = None) -> str:
        """Run a git command and return stdout."""
        if not self._git_path:
            raise RuntimeError("Git executable not found in PATH.")

        # Security check: Ensure all arguments are strings
        if not all(isinstance(arg, str) for arg in args):
            raise ValueError("All git arguments must be strings.")

        try:
            result = subprocess.run(
                [self._git_path, *args],
                cwd=self.repo_path,
                input=input_data,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.cmd} -> {e.stderr}")
            raise RuntimeError(f"Git operation failed: {e.stderr}") from e

    def is_available(self) -> bool:
        """Check if git is installed and we are inside a repo."""
        if not self._git_path:
            return False
        try:
            self._run_git("rev-parse", "--is-inside-work-tree")
            return True
        except Exception:
            return False

    def get_latest_commit(self) -> str | None:
        """Get the hash of the latest commit in the hidden ref."""
        try:
            return self._run_git("rev-parse", self.REF_NAME)
        except Exception:
            return None

    def save_prompt_snapshot(
        self, anchor: str, snapshot: PromptSnapshot, parent_hash: str | None = None
    ) -> str:
        """
        Save a prompt snapshot to the hidden Git branch.

        Args:
            anchor: The name/id of the prompt being saved.
            snapshot: The PromptSnapshot object.
            parent_hash: Optional parent commit hash for branching.
                        If None, uses the current head of the hidden ref.

        Returns:
            The hash of the new commit.
        """
        self._validate_anchor(anchor)

        # 1. Write the JSON as a blob
        data_json = snapshot.model_dump_json()
        blob_hash = self._run_git("hash-object", "-w", "--stdin", input_data=data_json)

        # 2. Build a tree object containing this file
        # Format: <mode> <type> <hash>\t<filename>
        tree_input = f"100644 blob {blob_hash}\t{anchor}.json\n"

        # If we have a parent, we should ideally carry over other files from that parent's tree
        base_parent = parent_hash or self.get_latest_commit()
        if base_parent:
            # Get existing tree entries excluding the one we are updating
            # Use -- to separate flags from the ref
            existing_entries = self._run_git("ls-tree", base_parent, "--")
            for line in existing_entries.splitlines():
                if not line.endswith(f"\t{anchor}.json"):
                    tree_input += line + "\n"

        tree_hash = self._run_git("mktree", input_data=tree_input)

        # 3. Create a commit
        commit_args = ["commit-tree", tree_hash, "-m", f"verger: snapshot for {anchor}"]
        if base_parent:
            commit_args.extend(["-p", base_parent])

        commit_hash = self._run_git(*commit_args)

        # 4. Update the hidden ref
        self._run_git("update-ref", self.REF_NAME, commit_hash)

        return commit_hash

    def load_prompt_snapshot(self, commit_hash: str, anchor: str) -> PromptSnapshot:
        """
        Load a specific prompt snapshot from a commit hash.

        Args:
            commit_hash: The commit hash to read from.
            anchor: The name of the prompt file to extract.

        Returns:
            The PromptSnapshot object.
        """
        self._validate_anchor(anchor)
        # Use -- to ensure the filename is not interpreted as a flag
        content = self._run_git("show", f"{commit_hash}:{anchor}.json", "--")
        data = json.loads(content)
        return PromptSnapshot(**data)

    def get_history(self) -> list[dict[str, Any]]:
        """
        Get the full commit history of the hidden reference.

        Returns:
            A list of dicts with hash, parent, and message.
        """
        if not self.get_latest_commit():
            return []

        # Format: hash | parent | subject
        # Use -- to separate ref from flags
        log_out = self._run_git("log", self.REF_NAME, "--format=%H|%P|%s", "--")
        history = []
        for line in log_out.splitlines():
            parts = line.split("|")
            if len(parts) < 3:
                continue
            h, p, s = parts
            history.append({"hash": h, "parents": p.split() if p else [], "message": s})
        return history
