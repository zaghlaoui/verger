import pytest

from verger.core.engine import ExecutionEngine
from verger.core.plugins import load_plugins


@pytest.fixture(autouse=True)
def init_plugins():
    """Ensure plugins are loaded before each test."""
    load_plugins()


@pytest.mark.asyncio
async def test_engine_run_success(mock_user_project):
    """Test that ExecutionEngine can format and run a prompt object on a model object."""
    # The engine now expects RAW objects, not references.
    raw_prompt = "Hello, {name}! Welcome to {place}."

    def mock_model(prompt: str) -> str:
        return f"PROCESSED: {prompt}"

    engine = ExecutionEngine()
    result = await engine.run(
        model_obj=mock_model,
        prompt_obj=raw_prompt,
        variables={"name": "Karim", "place": "the Verger engine"},
    )

    assert result == "PROCESSED: Hello, Karim! Welcome to the Verger engine."


@pytest.mark.asyncio
async def test_engine_run_with_missing_variables(mock_user_project):
    """Test that it raises a KeyError if variables are missing in the prompt."""
    raw_prompt = "Hello, {name}!"
    engine = ExecutionEngine()

    with pytest.raises(KeyError):
        await engine.run(
            model_obj=lambda x: x,
            prompt_obj=raw_prompt,
            variables={},  # Missing 'name'
        )


@pytest.mark.asyncio
async def test_engine_run_with_tools(mock_user_project):
    """Test that tools are resolved and passed to the model function."""
    raw_prompt = "Use the tool."

    def tool_func(x: int) -> int:
        """A simple tool."""
        return x * 2

    def mock_model_with_tools(prompt: str, tools: list | None = None) -> str:
        if tools and len(tools) > 0:
            tool_name = tools[0].name
            return f"Model ran with tool: {tool_name}"
        return "Model ran without tools"

    engine = ExecutionEngine()
    result = await engine.run(
        model_obj=mock_model_with_tools,
        prompt_obj=raw_prompt,
        tools=[tool_func],
    )

    assert result == "Model ran with tool: tool_func"


def test_prompt_variable_discovery(mock_user_project):
    """Test that we can discover variables required by a prompt before running it."""
    from verger.core.prompts import prompt_registry

    raw_prompt = "Hello {name}, welcome to {city}. Today is {day}."
    prompt = prompt_registry.resolve(raw_prompt)
    variables = prompt.get_variables()

    assert variables == {"name", "city", "day"}
