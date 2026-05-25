import shutil
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from verger.core.git_service import GitService
from verger.core.schema import (
    CollaborationMetadata,
    MessageRole,
    PromptSnapshot,
    VergerMessage,
)


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository for testing."""
    git_path = shutil.which("git")
    if not git_path:
        pytest.skip("git not found")

    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    subprocess.run([git_path, "init"], cwd=repo_dir, check=True)  # noqa: S603, S607
    # Git requires a name/email to commit
    subprocess.run(  # noqa: S603
        [git_path, "config", "user.name", "Test User"], cwd=repo_dir, check=True
    )  # noqa: S607
    subprocess.run(  # noqa: S603
        [git_path, "config", "user.email", "test@example.com"], cwd=repo_dir, check=True
    )  # noqa: S607
    # Create an initial commit so logs work
    (repo_dir / "README").write_text("initial")
    subprocess.run(  # noqa: S603
        [git_path, "add", "README"], cwd=repo_dir, check=True
    )  # noqa: S607
    subprocess.run(  # noqa: S603
        [git_path, "commit", "-m", "initial commit"], cwd=repo_dir, check=True
    )  # noqa: S607
    return repo_dir


def test_git_service_availability(temp_repo):
    """Test that the service correctly identifies a git repo."""
    service = GitService(repo_path=temp_repo)
    assert service.is_available() is True

    non_repo = temp_repo.parent / "not_a_repo"
    non_repo.mkdir()
    service_fail = GitService(repo_path=non_repo)
    assert service_fail.is_available() is False


def test_git_service_no_git_installed():
    """Test that GitService raises RuntimeError when git is missing."""
    with patch("shutil.which", return_value=None):
        service = GitService()
        assert service.is_available() is False

        with pytest.raises(RuntimeError, match="Git executable not found"):
            service._run_git("status")


def test_git_service_is_available_exception():
    """Test that is_available returns False when git command fails."""
    service = GitService()
    with patch.object(service, "_run_git", side_effect=Exception("error")):
        assert service.is_available() is False


def test_save_and_load_snapshot(temp_repo):
    """Test saving a snapshot and reading it back."""
    service = GitService(repo_path=temp_repo)

    snapshot = PromptSnapshot(
        messages=[VergerMessage(role=MessageRole.USER, content="Hello {name}")],
        metadata=CollaborationMetadata(author="alice"),
    )

    commit_hash = service.save_prompt_snapshot("my_prompt", snapshot)
    assert commit_hash is not None

    # Load it back
    loaded = service.load_prompt_snapshot(commit_hash, "my_prompt")
    assert loaded.messages[0].content == "Hello {name}"
    assert loaded.metadata.author == "alice"


def test_git_history_and_branching(temp_repo):
    """Test that history tracks snapshots correctly across multiple commits."""
    service = GitService(repo_path=temp_repo)

    # Snapshot 1
    s1 = PromptSnapshot(
        messages=[VergerMessage(role=MessageRole.USER, content="V1")],
        metadata=CollaborationMetadata(author="alice"),
    )
    h1 = service.save_prompt_snapshot("p1", s1)

    # Snapshot 2 (child of h1)
    s2 = PromptSnapshot(
        messages=[VergerMessage(role=MessageRole.USER, content="V2")],
        metadata=CollaborationMetadata(author="bob"),
    )
    h2 = service.save_prompt_snapshot("p1", s2, parent_hash=h1)

    history = service.get_history()
    assert len(history) == 2
    assert history[0]["hash"] == h2
    assert history[0]["parents"] == [h1]
    assert history[1]["hash"] == h1
    assert history[1]["parents"] == []  # It's the first in the custom ref


def test_git_service_get_history_empty():
    """Test that get_history returns empty list when no commits exist."""
    service = GitService()
    with patch.object(service, "get_latest_commit", return_value=None):
        assert service.get_history() == []


def test_ls_tree_integration(temp_repo):
    """Test that multiple prompts can coexist in the same hidden ref tree."""
    service = GitService(repo_path=temp_repo)

    # Save prompt A
    service.save_prompt_snapshot(
        "prompt_a",
        PromptSnapshot(
            messages=[VergerMessage(role=MessageRole.USER, content="A")],
            metadata=CollaborationMetadata(author="a"),
        ),
    )

    # Save prompt B (should preserve A in the tree)
    h_b = service.save_prompt_snapshot(
        "prompt_b",
        PromptSnapshot(
            messages=[VergerMessage(role=MessageRole.USER, content="B")],
            metadata=CollaborationMetadata(author="b"),
        ),
    )

    # Verify both exist in the latest commit
    assert service.load_prompt_snapshot(h_b, "prompt_a").messages[0].content == "A"
    assert service.load_prompt_snapshot(h_b, "prompt_b").messages[0].content == "B"


def test_git_service_anchor_validation():
    """Test that invalid anchor names are rejected."""
    service = GitService()
    invalid_names = ["../root", "with space", "semi;colon", "back\\slash"]

    for name in invalid_names:
        with pytest.raises(ValueError, match="Invalid or unsafe anchor name"):
            service.save_prompt_snapshot(name, MagicMock())


def test_git_service_non_string_args():
    """Test that _run_git rejects non-string arguments for security."""
    service = GitService()
    with pytest.raises(ValueError, match="All git arguments must be strings"):
        service._run_git("status", 123)  # type: ignore


def test_git_service_malformed_log_line():
    """Test that get_history handles malformed log lines gracefully."""
    service = GitService()
    # Mock log output with a bad line
    with patch.object(service, "get_latest_commit", return_value="some_hash"):
        with patch.object(service, "_run_git", return_value="hash|parent|msg\nbad_line"):
            history = service.get_history()
            # Should have skipped the bad line
            assert len(history) == 1
            assert history[0]["hash"] == "hash"
