import pytest

from verger.core.plugins import load_plugins
from verger.core.prompts import prompt_registry
from verger.core.prompts.adapters.string_adapter import NativeStringPrompt


@pytest.fixture(autouse=True)
def init_plugins():
    """Ensure plugins are loaded before each test."""
    load_plugins()


def test_string_prompt_adapter(mock_user_project):
    """Test that NativeStringResolver can wrap a raw string object."""
    raw_prompt_string = "You are a helpful assistant."

    # Resolve should directly handle the raw string object
    prompt = prompt_registry.resolve(raw_prompt_string)

    messages = prompt.get_messages()
    assert len(messages) == 1
    assert messages[0].content == "You are a helpful assistant."


def test_string_prompt_format_error():
    """Test error when formatting with missing variables."""
    prompt = NativeStringPrompt("Hello {name}")
    with pytest.raises(KeyError):
        prompt.format()  # Missing 'name'


def test_string_prompt_format_success():
    """Test that formatting returns a list of messages."""
    prompt = NativeStringPrompt("Hello {name}")
    messages = prompt.format(name="World")
    assert len(messages) == 1
    assert messages[0].content == "Hello World"


def test_string_prompt_id():
    """Test that the prompt generates a unique ID."""
    prompt = NativeStringPrompt("test")
    prompt_id = prompt.get_id()
    assert "StringPrompt-" in prompt_id
    assert str(id(prompt)) in prompt_id
