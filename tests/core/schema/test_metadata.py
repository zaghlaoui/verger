from datetime import datetime

from verger.core.schema import CollaborationMetadata, Comment


def test_comment_creation():
    """Test creating a comment."""
    comment = Comment(author="alice", text="Great prompt")
    assert comment.author == "alice"
    assert isinstance(comment.timestamp, datetime)


def test_collaboration_metadata_defaults():
    """Test default values for CollaborationMetadata."""
    meta = CollaborationMetadata(author="bob")
    assert meta.author == "bob"
    assert meta.tags == []
    assert meta.comments == []
    assert meta.archived is False
    assert isinstance(meta.created_at, datetime)


def test_collaboration_metadata_with_data():
    """Test CollaborationMetadata with tags and comments."""
    comment = Comment(author="alice", text="Looks good")
    meta = CollaborationMetadata(
        author="bob", description="Version 2", tags=["stable", "v2"], comments=[comment]
    )
    assert len(meta.tags) == 2
    assert meta.tags[0] == "stable"
    assert len(meta.comments) == 1
    assert meta.comments[0].author == "alice"
