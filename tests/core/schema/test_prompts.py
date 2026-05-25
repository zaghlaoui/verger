from verger.core.schema import CollaborationMetadata, MessageRole, PromptSnapshot, VergerMessage


def test_prompt_snapshot_creation():
    """Test creating a basic PromptSnapshot."""
    meta = CollaborationMetadata(author="alice")
    msg = VergerMessage(role=MessageRole.USER, content="Hello")
    snapshot = PromptSnapshot(messages=[msg], metadata=meta)
    assert len(snapshot.messages) == 1
    assert snapshot.messages[0].content == "Hello"
    assert snapshot.metadata.author == "alice"
