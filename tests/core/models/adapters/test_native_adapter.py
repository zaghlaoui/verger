import pytest

from verger.core.models.adapters.native_adapter import NativeFunctionAdapter


@pytest.mark.asyncio
async def test_native_model_adapter_tools_async():
    """Test async native model with tools support."""

    async def async_model(prompt, tools=None):
        return f"Async result with {len(tools or [])} tools"

    from typing import cast

    from verger.core.tools.tool_base import VergerTool

    adapter = NativeFunctionAdapter(async_model)
    result = await adapter.invoke("test", tools=cast(list[VergerTool], [1, 2]))
    assert result == "Async result with 2 tools"


@pytest.mark.asyncio
async def test_native_model_adapter_tools_sync():
    """Test sync native model with tools support (missing branch in coverage)."""

    def sync_model(prompt, tools=None):
        return f"Sync result with {len(tools or [])} tools"

    from typing import cast

    from verger.core.tools.tool_base import VergerTool

    adapter = NativeFunctionAdapter(sync_model)
    result = await adapter.invoke("test", tools=cast(list[VergerTool], [1, 2, 3]))
    assert result == "Sync result with 3 tools"


@pytest.mark.asyncio
async def test_native_model_adapter_no_tools_async():
    """Test async native model without tools support."""

    async def async_model_no_tools(prompt):
        return "No tools here"

    from typing import cast

    from verger.core.tools.tool_base import VergerTool

    adapter = NativeFunctionAdapter(async_model_no_tools)
    result = await adapter.invoke("test", tools=cast(list[VergerTool], [1]))
    assert result == "No tools here"


@pytest.mark.asyncio
async def test_native_model_adapter_no_tools_sync():
    """Test sync native model without tools support."""

    def sync_model_no_tools(prompt):
        return "Sync no tools"

    from typing import cast

    from verger.core.tools.tool_base import VergerTool

    adapter = NativeFunctionAdapter(sync_model_no_tools)
    result = await adapter.invoke("test", tools=cast(list[VergerTool], [1]))
    assert result == "Sync no tools"
