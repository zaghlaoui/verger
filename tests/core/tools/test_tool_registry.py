from unittest.mock import MagicMock

import pytest

from verger.core.exceptions import VergerResolutionError
from verger.core.tools import ToolResolver, VergerTool, tool_registry


def test_tool_registry_resolution_success():
    """Test that the registry can resolve an object using a registered resolver."""
    from verger.core.tools.tool_registry import ToolRegistry

    test_registry = ToolRegistry()

    mock_resolver = MagicMock(spec=ToolResolver)
    mock_resolver.can_handle.return_value = True
    mock_adapter = MagicMock(spec=VergerTool)
    mock_resolver.create_adapter.return_value = mock_adapter

    test_registry.register(mock_resolver)

    def test_func(x):
        return x

    obj = test_func
    resolved = test_registry.resolve(obj)

    assert resolved == mock_adapter
    mock_resolver.can_handle.assert_called_once_with(obj)
    mock_resolver.create_adapter.assert_called_once_with(obj)


def test_tool_registry_resolution_failure():
    """Test that the registry raises VergerResolutionError when no resolver matches."""
    from verger.core.tools.tool_registry import ToolRegistry

    test_registry = ToolRegistry()

    mock_resolver = MagicMock(spec=ToolResolver)
    mock_resolver.can_handle.return_value = False

    test_registry.register(mock_resolver)

    with pytest.raises(VergerResolutionError, match="No tool adapter found for object of type"):
        test_registry.resolve("unknown_obj")


def test_tool_registry_priority_sorting():
    """Test that the registry respects resolver priority."""
    from verger.core.tools.tool_registry import ToolRegistry

    test_registry = ToolRegistry()

    # Resolver 1: Generic (Low Priority)
    low_priority_resolver = MagicMock(spec=ToolResolver)
    low_priority_resolver.can_handle.return_value = True
    low_priority_resolver.priority = 100
    low_adapter = MagicMock(spec=VergerTool)
    low_priority_resolver.create_adapter.return_value = low_adapter

    # Resolver 2: Expert (High Priority)
    high_priority_resolver = MagicMock(spec=ToolResolver)
    high_priority_resolver.can_handle.return_value = True
    high_priority_resolver.priority = 10
    high_adapter = MagicMock(spec=VergerTool)
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
    """Ensure that the exported tool_registry is a singleton instance of ToolRegistry."""
    from verger.core.tools.tool_registry import ToolRegistry

    assert isinstance(tool_registry, ToolRegistry)
