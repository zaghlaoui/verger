from unittest.mock import MagicMock

import pytest

from verger.core.exceptions import VergerResolutionError
from verger.core.models import ModelResolver, VergerModel, model_registry


def test_model_registry_resolution_success():
    """Test that the registry can resolve an object using a registered resolver."""
    # Create a fresh registry for testing to avoid side effects
    from verger.core.models.model_registry import ModelRegistry

    test_registry = ModelRegistry()

    mock_resolver = MagicMock(spec=ModelResolver)
    mock_resolver.can_handle.return_value = True
    mock_adapter = MagicMock(spec=VergerModel)
    mock_resolver.create_adapter.return_value = mock_adapter

    test_registry.register(mock_resolver)

    obj = "some_model_obj"
    resolved = test_registry.resolve(obj)

    assert resolved == mock_adapter
    mock_resolver.can_handle.assert_called_once_with(obj)
    mock_resolver.create_adapter.assert_called_once_with(obj)


def test_model_registry_resolution_failure():
    """Test that the registry raises VergerResolutionError when no resolver matches."""
    from verger.core.models.model_registry import ModelRegistry

    test_registry = ModelRegistry()

    mock_resolver = MagicMock(spec=ModelResolver)
    mock_resolver.can_handle.return_value = False

    test_registry.register(mock_resolver)

    with pytest.raises(VergerResolutionError, match="No model adapter found for object of type"):
        test_registry.resolve("unknown_obj")


def test_model_registry_priority_sorting():
    """Test that the registry respects resolver priority."""
    from verger.core.models.model_registry import ModelRegistry

    test_registry = ModelRegistry()

    # Resolver 1: Generic (Low Priority)
    low_priority_resolver = MagicMock(spec=ModelResolver)
    low_priority_resolver.can_handle.return_value = True
    low_priority_resolver.priority = 100
    low_adapter = MagicMock(spec=VergerModel)
    low_priority_resolver.create_adapter.return_value = low_adapter

    # Resolver 2: Expert (High Priority)
    high_priority_resolver = MagicMock(spec=ModelResolver)
    high_priority_resolver.can_handle.return_value = True
    high_priority_resolver.priority = 10
    high_adapter = MagicMock(spec=VergerModel)
    high_priority_resolver.create_adapter.return_value = high_adapter

    # Register in reverse order
    test_registry.register(low_priority_resolver)
    test_registry.register(high_priority_resolver)

    resolved = test_registry.resolve("some_obj")

    # Should pick high priority even though it was registered second
    assert resolved == high_adapter
    high_priority_resolver.create_adapter.assert_called_once()
    low_priority_resolver.create_adapter.assert_not_called()


def test_singleton_registry_instance():
    """Ensure that the exported model_registry is a singleton instance of ModelRegistry."""
    from verger.core.models.model_registry import ModelRegistry

    assert isinstance(model_registry, ModelRegistry)
