import pytest

from verger.core.schema import MessageRole, VergerMessage


def test_verger_message_creation():
    """Test creating a basic VergerMessage."""
    msg = VergerMessage(role=MessageRole.USER, content="Hello")
    assert msg.role == MessageRole.USER
    assert msg.content == "Hello"
    assert msg.name is None


def test_verger_message_with_optional_fields():
    """Test VergerMessage with optional fields like name and tool_call_id."""
    msg = VergerMessage(
        role=MessageRole.TOOL, content="Success", name="calculator", tool_call_id="call_123"
    )
    assert msg.name == "calculator"
    assert msg.tool_call_id == "call_123"


def test_invalid_role():
    """Test that pydantic validates the role enum."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        VergerMessage(role="invalid_role", content="test")  # type: ignore
