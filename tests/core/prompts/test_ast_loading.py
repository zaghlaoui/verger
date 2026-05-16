import pytest

from verger.core.plugins import load_plugins
from verger.core.prompts.registry import registry as prompt_registry


@pytest.fixture(autouse=True)
def init_plugins():
    """Ensure plugins are loaded before each test."""
    load_plugins()


def test_ast_prompt_loading(mock_user_project):
    """Test that NativeStringResolver can read a string via AST from user code."""
    # The mock_user_project fixture already switched CWD to the project root
    # where prompts.py exists.

    ref = "prompts:SYSTEM_PROMPT"
    prompt = prompt_registry.resolve(ref)

    assert prompt.get_id() == ref
    assert prompt.get_text() == "You are a helpful assistant."


def test_ast_prompt_variable_missing(mock_user_project):
    """Test error handling when a variable is missing in the file."""
    ref = "prompts:MISSING_VARIABLE"

    with pytest.raises(ValueError, match="Variable 'MISSING_VARIABLE' not found"):
        prompt_registry.resolve(ref)


def test_ast_prompt_file_missing(mock_user_project):
    """Test error handling when the file itself is missing."""
    ref = "non_existent_file:SOME_VAR"

    with pytest.raises(FileNotFoundError):
        prompt_registry.resolve(ref)
