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
async def test_engine_run_no_variables(mock_user_project):
    """Test engine run when no variables are provided (raw prompt)."""
    raw_prompt = "This is a plain prompt."

    engine = ExecutionEngine()
    result = await engine.run(model_obj=lambda x: f"GOT: {x}", prompt_obj=raw_prompt)

    assert result == "GOT: This is a plain prompt."


def test_prompt_variable_discovery(mock_user_project):
    """Test that we can discover variables required by a prompt before running it."""
    from verger.core.prompts.registry import registry as prompt_registry

    raw_prompt = "Hello {name}, welcome to {city}. Today is {day}."
    prompt = prompt_registry.resolve(raw_prompt)
    variables = prompt.get_variables()

    assert variables == {"name", "city", "day"}
