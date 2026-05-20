from unittest.mock import MagicMock

import pytest

from verger.core.exceptions import VergerResolutionError
from verger.core.prompts import PromptResolver, VergerPrompt, prompt_registry


def test_prompt_registry_resolution_success():
    """Test that the registry can resolve an object using a registered resolver."""
    from verger.core.prompts.registry import PromptRegistry

    test_registry = PromptRegistry()

    mock_resolver = MagicMock(spec=PromptResolver)
    mock_resolver.can_handle.return_value = True
    mock_adapter = MagicMock(spec=VergerPrompt)
    mock_resolver.create_adapter.return_value = mock_adapter

    test_registry.register(mock_resolver)

    obj = "some_prompt_obj"
    resolved = test_registry.resolve(obj)

    assert resolved == mock_adapter
    mock_resolver.can_handle.assert_called_once_with(obj)
    mock_resolver.create_adapter.assert_called_once_with(obj)


def test_prompt_registry_resolution_failure():
    """Test that the registry raises VergerResolutionError when no resolver matches."""
    from verger.core.prompts.registry import PromptRegistry

    test_registry = PromptRegistry()

    mock_resolver = MagicMock(spec=PromptResolver)
    mock_resolver.can_handle.return_value = False

    test_registry.register(mock_resolver)

    with pytest.raises(VergerResolutionError, match="No prompt adapter found for object of type"):
        test_registry.resolve("unknown_obj")


def test_singleton_registry_instance():
    """Ensure that the exported prompt_registry is a singleton instance of PromptRegistry."""
    from verger.core.prompts.registry import PromptRegistry

    assert isinstance(prompt_registry, PromptRegistry)
