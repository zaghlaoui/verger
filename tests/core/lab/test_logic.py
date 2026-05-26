from unittest.mock import MagicMock

from verger.core.lab.model_lab import ModelLab
from verger.core.lab.prompt_lab import PromptLab
from verger.core.schema import CollaborationMetadata, ModelSnapshot, PromptSnapshot


def test_prompt_lab_capture_and_load():
    """Test capturing and loading a prompt snapshot."""
    mock_git = MagicMock()
    lab = PromptLab(mock_git)

    messages = [{"role": "user", "content": "hi"}]
    mock_git.save_prompt_snapshot.return_value = "hash123"

    h = lab.capture_snapshot("p1", messages, author="alice", description="v1")
    assert h == "hash123"

    # Verify snapshot construction
    mock_git.save_prompt_snapshot.assert_called_once()
    snapshot = mock_git.save_prompt_snapshot.call_args[0][1]
    assert isinstance(snapshot, PromptSnapshot)
    assert snapshot.messages[0].content == "hi"
    assert snapshot.metadata.description == "v1"


def test_prompt_lab_history():
    """Test history retrieval for a prompt."""
    mock_git = MagicMock()
    lab = PromptLab(mock_git)

    mock_git.get_history.return_value = [{"hash": "h1", "parents": [], "message": "msg"}]
    mock_snapshot = PromptSnapshot(
        messages=[], metadata=CollaborationMetadata(author="alice", description="desc")
    )
    mock_git.load_prompt_snapshot.return_value = mock_snapshot

    history = lab.get_history("p1")
    assert len(history) == 1
    assert history[0]["hash"] == "h1"
    assert history[0]["author"] == "alice"

    # Test failure path
    mock_git.load_prompt_snapshot.side_effect = Exception("not found")
    assert lab.get_history("p1") == []


def test_model_lab_capture():
    """Test capturing a model snapshot."""
    mock_git = MagicMock()
    lab = ModelLab(mock_git)

    mock_git._run_git.side_effect = ["blob_hash", "tree_hash", "commit_hash", "ref_update"]
    mock_git.get_latest_commit.return_value = None

    h = lab.capture_snapshot("m1", "openai:gpt-4", {"temp": 0.7}, author="alice")
    assert h == "commit_hash"
    assert mock_git._run_git.call_count == 4


def test_model_lab_capture_with_parent():
    """Test capturing a model snapshot with an existing parent tree."""
    mock_git = MagicMock()
    lab = ModelLab(mock_git)

    mock_git.get_latest_commit.return_value = "parent_hash"
    mock_git._run_git.side_effect = [
        "blob_hash",
        "existing_tree_data\tother.model.json",
        "new_tree_hash",
        "new_commit_hash",
        "ref_update",
    ]

    h = lab.capture_snapshot("m1", "openai", {}, author="a")
    assert h == "new_commit_hash"
    # Verify ls-tree was called for parent
    mock_git._run_git.assert_any_call("ls-tree", "parent_hash", "--")


def test_model_lab_history():
    """Test history retrieval for a model."""
    mock_git = MagicMock()
    lab = ModelLab(mock_git)

    mock_git.get_history.return_value = [{"hash": "h1", "parents": [], "message": "msg"}]
    snapshot = ModelSnapshot(
        ref="openai", params={}, metadata=CollaborationMetadata(author="alice")
    )
    mock_git._run_git.return_value = snapshot.model_dump_json()

    history = lab.get_history("m1")
    assert len(history) == 1
    assert history[0]["hash"] == "h1"

    # Test failure path
    mock_git._run_git.side_effect = Exception("not found")
    assert lab.get_history("m1") == []


def test_model_lab_load():
    """Test loading a specific model snapshot."""
    mock_git = MagicMock()
    lab = ModelLab(mock_git)

    snapshot = ModelSnapshot(
        ref="openai", params={}, metadata=CollaborationMetadata(author="alice")
    )
    mock_git._run_git.return_value = snapshot.model_dump_json()

    loaded = lab.load_snapshot("m1", "h1")
    assert loaded.ref == "openai"


def test_prompt_lab_load():
    """Test loading a specific prompt snapshot."""
    mock_git = MagicMock()
    lab = PromptLab(mock_git)
    lab.load_snapshot("p1", "h1")
    mock_git.load_prompt_snapshot.assert_called_once_with("h1", "p1")
