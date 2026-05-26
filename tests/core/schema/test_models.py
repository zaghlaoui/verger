from verger.core.schema import CollaborationMetadata, ModelSnapshot


def test_model_snapshot_creation():
    """Test creating a basic ModelSnapshot."""
    meta = CollaborationMetadata(author="alice")
    snapshot = ModelSnapshot(ref="openai:gpt-4", params={"temperature": 0.7}, metadata=meta)
    assert snapshot.ref == "openai:gpt-4"
    assert snapshot.params["temperature"] == 0.7
    assert snapshot.metadata.author == "alice"
