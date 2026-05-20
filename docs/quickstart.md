# Quick Start

Get up and running with Verger in three simple steps.

### 1. Install Verger
If you are using **uv** (recommended):
```bash
uv add --dev verger
```

If you prefer **pip**:
```bash
pip install verger
```

### 2. Configure your project
Create a `verger.toml` file in your project root to configure your models, prompts, and tools. This file tells Verger where to find your AI resources within your Python codebase.

**verger.toml**
```toml
[prompts]
translator = "myapp.prompts:SYSTEM_MSG"

[models]
gpt4 = "myapp.agents:openai_model"

[tools]
search_tool = "myapp.tools:web_search"
```

If you prefer to keep all your configuration in one place, you can use `pyproject.toml` instead by adding a `[tool.verger]` section:

**pyproject.toml**
```toml
[tool.verger.prompts]
translator = "myapp.prompts:SYSTEM_MSG"

[tool.verger.models]
gpt4 = "myapp.agents:openai_model"

[tool.verger.tools]
search_tool = "myapp.tools:web_search"
```

### 3. Launch the TUI
Run Verger to interact with your prompts and test your models:

```bash
uv run verger tui
```
