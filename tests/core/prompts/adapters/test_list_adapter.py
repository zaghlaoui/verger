import pytest

from verger.core.prompts.adapters.list_adapter import NativeListPrompt, NativeListResolver
from verger.core.schema import MessageRole


def test_list_prompt_initialization():
    """Test creating a NativeListPrompt from a list of dicts."""
    messages = [
        {"role": "system", "content": "System prompt"},
        {"role": "user", "content": "User prompt {name}"},
    ]
    prompt = NativeListPrompt(messages)

    msg_templates = prompt.get_messages()
    assert len(msg_templates) == 2
    assert msg_templates[0].role == MessageRole.SYSTEM
    assert msg_templates[1].content == "User prompt {name}"


def test_list_prompt_format():
    """Test formatting a list-based prompt."""
    messages = [
        {"role": "system", "content": "Expert in {domain}"},
        {"role": "user", "content": "Query: {query}"},
    ]
    prompt = NativeListPrompt(messages)

    formatted = prompt.format(domain="AI", query="How are you?")
    assert len(formatted) == 2
    assert formatted[0].content == "Expert in AI"
    assert formatted[1].content == "Query: How are you?"


def test_list_prompt_variables():
    """Test variable discovery across multiple messages."""
    messages = [
        {"role": "system", "content": "{a} and {b}"},
        {"role": "user", "content": "{b} and {c}"},
    ]
    prompt = NativeListPrompt(messages)
    assert prompt.get_variables() == {"a", "b", "c"}


def test_list_resolver():
    """Test that the resolver correctly identifies lists of messages."""
    resolver = NativeListResolver()

    valid_list = [{"role": "user", "content": "hi"}]
    empty_list = []
    invalid_list = ["just a string"]
    not_a_list = "hi"

    assert resolver.can_handle(valid_list) is True
    assert resolver.can_handle(empty_list) is False
    assert resolver.can_handle(invalid_list) is False
    assert resolver.can_handle(not_a_list) is False

    adapter = resolver.create_adapter(valid_list)
    assert isinstance(adapter, NativeListPrompt)


def test_list_prompt_invalid_role():
    """Test that NativeListPrompt raises ValueError for unknown roles."""
    invalid_messages = [{"role": "invalid", "content": "hi"}]
    with pytest.raises(ValueError):
        NativeListPrompt(invalid_messages)


def test_list_prompt_missing_key():
    """Test that NativeListPrompt raises KeyError for missing keys in dict."""
    invalid_messages = [{"role": "user"}]  # Missing 'content'
    with pytest.raises(KeyError):
        NativeListPrompt(invalid_messages)  # type: ignore


def test_list_prompt_id():
    """Test that NativeListPrompt generates a unique ID."""
    prompt = NativeListPrompt([{"role": "user", "content": "hi"}])
    assert "ListPrompt-" in prompt.get_id()
