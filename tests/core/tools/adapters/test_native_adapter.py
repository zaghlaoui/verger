import pytest

from verger.core.tools.adapters.native_adapter import NativeToolAdapter, NativeToolResolver


def test_native_tool_adapter_sync():
    """Test the NativeToolAdapter with a synchronous function."""

    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    adapter = NativeToolAdapter(add)
    assert adapter.name == "add"
    assert adapter.description == "Add two numbers."

    schema = adapter.args_schema
    assert schema["type"] == "object"
    assert "a" in schema["properties"]
    assert "b" in schema["properties"]

    import asyncio

    result = asyncio.run(adapter.run(a=1, b=2))
    assert result == 3


@pytest.mark.asyncio
async def test_native_tool_adapter_async():
    """Test the NativeToolAdapter with an asynchronous function."""

    async def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    adapter = NativeToolAdapter(multiply)
    assert adapter.name == "multiply"

    result = await adapter.run(a=3, b=4)
    assert result == 12


def test_native_tool_resolver():
    """Test that the NativeToolResolver correctly identifies callables."""
    resolver = NativeToolResolver()

    def my_func():
        pass

    assert resolver.can_handle(my_func) is True
    assert resolver.can_handle(lambda x: x) is True
    assert resolver.can_handle("not a func") is False
    assert resolver.can_handle(int) is False  # Classes are callables but usually not tools

    adapter = resolver.create_adapter(my_func)
    assert isinstance(adapter, NativeToolAdapter)
