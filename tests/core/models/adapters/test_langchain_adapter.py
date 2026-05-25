from unittest.mock import AsyncMock, MagicMock

import pytest

from verger.core.models.adapters.langchain_adapter import LangChainAdapter, LangChainResolver


@pytest.mark.asyncio
async def test_langchain_adapter_invoke_basic():
    """Test basic invocation of LangChainAdapter."""
    mock_runnable = AsyncMock()
    mock_runnable.ainvoke.return_value = "Hello world"

    from verger.core.schema import MessageRole, VergerMessage

    messages = [VergerMessage(role=MessageRole.USER, content="Hi")]
    adapter = LangChainAdapter(mock_runnable)
    result = await adapter.invoke(messages)

    assert result.content == "Hello world"
    assert result.role == MessageRole.AI
    # Verify it was converted to LangChain format [("human", "Hi")]
    mock_runnable.ainvoke.assert_called_once_with([("human", "Hi")])


@pytest.mark.asyncio
async def test_langchain_adapter_invoke_with_content():
    """Test invocation where result has a .content attribute (like AIMessage)."""
    mock_runnable = AsyncMock()
    mock_result = MagicMock()
    mock_result.content = "Message content"
    mock_runnable.ainvoke.return_value = mock_result

    from verger.core.schema import MessageRole, VergerMessage

    messages = [VergerMessage(role=MessageRole.USER, content="Hi")]
    adapter = LangChainAdapter(mock_runnable)
    result = await adapter.invoke(messages)

    assert result.content == "Message content"
    assert result.role == MessageRole.AI


@pytest.mark.asyncio
async def test_langchain_adapter_bind_tools():
    """Test tool binding in LangChainAdapter."""
    mock_runnable = MagicMock()
    mock_bound_runnable = AsyncMock()
    mock_bound_runnable.ainvoke.return_value = "Tool result"
    mock_runnable.bind_tools.return_value = mock_bound_runnable

    from verger.core.schema import MessageRole, VergerMessage

    messages = [VergerMessage(role=MessageRole.USER, content="Use tools")]
    adapter = LangChainAdapter(mock_runnable)
    from typing import cast

    from verger.core.tools.tool_base import VergerTool

    tools = cast(list[VergerTool], [MagicMock()])
    result = await adapter.invoke(messages, tools=tools)

    assert result.content == "Tool result"
    assert result.role == MessageRole.AI
    mock_runnable.bind_tools.assert_called_once_with(tools)
    mock_bound_runnable.ainvoke.assert_called_once_with([("human", "Use tools")])


def test_langchain_resolver_can_handle():
    """Test LangChainResolver duck-typing detection."""
    resolver = LangChainResolver()

    # Mock an object that looks like a LangChain runnable
    class MockLangChainObject:
        def ainvoke(self):
            pass

    # Manually set the module to simulate a langchain class
    MockLangChainObject.__module__ = "langchain_core.runnables.base"

    obj = MockLangChainObject()
    assert resolver.can_handle(obj) is True

    # Object with ainvoke but NOT from langchain
    class OtherObject:
        def ainvoke(self):
            pass

    OtherObject.__module__ = "some_other_module"

    assert resolver.can_handle(OtherObject()) is False

    # Object from langchain but NO ainvoke
    class IncompleteObject:
        pass

    IncompleteObject.__module__ = "langchain.something"

    assert resolver.can_handle(IncompleteObject()) is False


def test_langchain_resolver_create_adapter():
    """Test adapter creation by the resolver."""
    resolver = LangChainResolver()
    obj = MagicMock()
    adapter = resolver.create_adapter(obj)
    assert isinstance(adapter, LangChainAdapter)
    assert adapter.runnable == obj
