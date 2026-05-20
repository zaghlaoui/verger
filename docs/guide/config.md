# Configuration Guide

Verger is designed to be "Zero-Invasive." You don't need to change your code; you just tell Verger where to look in your configuration file.

## Configuration Files

Verger looks for configuration in the following order:

1.  **`VERGER_CONFIG` environment variable**: Path to a specific TOML file.
2.  **`verger.toml`**: A standalone configuration file in your project root.
3.  **`pyproject.toml`**: The `[tool.verger]` section in your project's standard configuration file.

### `verger.toml` example

You can put your configuration in a dedicated file:

```toml
env_file = ".env"

[prompts]
system_msg = "src/agents/prompts:SYSTEM_PROMPT"

[models]
gpt4_agent = { ref = "src.agents.main:agent" }
```

### `pyproject.toml` example

Alternatively, add a `[tool.verger]` section to your `pyproject.toml`:

```toml
[tool.verger]
env_file = ".env"

[tool.verger.prompts]
system_msg = "src/agents/prompts:SYSTEM_PROMPT"

[tool.verger.models]
gpt4_agent = { ref = "src.agents.main:agent" }
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
