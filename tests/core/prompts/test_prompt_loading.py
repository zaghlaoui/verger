import pytest

from verger.core.plugins import load_plugins
from verger.core.prompts import prompt_registry
from verger.utils.imports import import_reference


@pytest.fixture(autouse=True)
def init_plugins():
    """Ensure plugins are loaded before each test."""
    load_plugins()


def test_string_prompt_adapter(mock_user_project):
    """Test that NativeStringResolver can wrap a raw string object."""
    raw_prompt_string = "You are a helpful assistant."

    # Resolve should directly handle the raw string object
    prompt = prompt_registry.resolve(raw_prompt_string)

    assert prompt.get_text() == "You are a helpful assistant."


def test_import_reference_success(mock_user_project):
    """Test that our universal loader correctly loads a string from a user module."""
    # Add the mock project directory to sys.path so import_reference can find it
    import sys

    sys.path.append(str(mock_user_project))

    try:
        ref = "prompts:SYSTEM_PROMPT"
        loaded_obj = import_reference(ref)
        assert loaded_obj == "You are a helpful assistant."
    finally:
        sys.path.remove(str(mock_user_project))


def test_import_reference_attribute_missing(mock_user_project):
    """Test error handling when a variable is missing in the file."""
    import sys

    sys.path.append(str(mock_user_project))
    try:
        ref = "prompts:MISSING_VARIABLE"
        with pytest.raises(AttributeError, match="has no attribute 'MISSING_VARIABLE'"):
            import_reference(ref)
    finally:
        sys.path.remove(str(mock_user_project))


def test_import_reference_module_missing(mock_user_project):
    """Test error handling when the module itself is missing."""
    import sys

    sys.path.append(str(mock_user_project))
    try:
        ref = "non_existent_file:SOME_VAR"
        with pytest.raises(ImportError):
            import_reference(ref)
    finally:
        sys.path.remove(str(mock_user_project))
