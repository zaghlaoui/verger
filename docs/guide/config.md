# Configuration Guide

Verger is designed to be "Zero-Invasive." You don't need to change your code; you just tell Verger where to look in your `pyproject.toml`.

## The `[tool.verger]` Section

Add this section to your project's `pyproject.toml` to start using Verger.

```toml
[tool.verger]
# Optional: path to your .env file
env_file = ".env"

[tool.verger.prompts]
# format: name = "path/to/file:VARIABLE_NAME"
# or: name = "module.name:VARIABLE_NAME"
system_msg = "src/agents/prompts:SYSTEM_PROMPT"
user_msg = "src/agents/prompts:USER_PROMPT"

[tool.verger.models]
# format: name = { ref = "module:object" }
# Verger automatically detects if it's LangChain, PydanticAI, or a function.
gpt4_agent = { ref = "src.agents.main:agent" }
experimental_chain = { ref = "src.chains.translator:chain" }
mock_model = { ref = "tests.mocks:dummy_llm" }
```

## How Discovery Works

### Prompts
Verger uses **AST (Static Analysis)** to read prompts. This means:
1. It finds the file you pointed to.
2. It looks for the variable name.
3. It extracts the string value **without running your code**.

### Models
Verger uses **Dynamic Imports** for models.
1. It imports the module and gets the object.
2. It passes the object through our **Registry**.
3. It automatically wraps it in the correct **Adapter** (e.g., LangChain Adapter).
