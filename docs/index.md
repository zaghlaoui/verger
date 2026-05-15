# Welcome to Verger

Verger is a framework-agnostic tool designed to help developers evaluate, test, and manage AI prompts and models directly from their codebase.

## Quick Start

Get up and running with Verger in three simple steps.

### 1. Install Verger
Install Verger in your project using `uv` (recommended) or `pip`:

```bash
uv add verger
# or
pip install verger
```

### 2. Configure your project
Add the `[tool.verger]` section to your `pyproject.toml` to define your prompts and models:

```toml
[tool.verger.prompts]
translator = "myapp.prompts:SYSTEM_MSG"

[tool.verger.models]
gpt4 = "myapp.agents:openai_model"
```

### 3. Launch the TUI
Run Verger to interact with your prompts and test your models:

```bash
verger tui
```

## Key Features

- **AST-Powered**: Reads prompts directly from your Python files without executing them.
- **Framework Agnostic**: Supports LangChain, PydanticAI, and native functions via a flexible Adapter pattern.
- **TUI First**: A modern Terminal UI for side-by-side comparison of model outputs.
- **Zero-Invasive**: Works with your existing project structure without requiring code changes.
