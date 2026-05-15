# Verger Project Memory

## Overview
**Verger** is a framework-agnostic tool for evaluating AI prompts and models directly from a Python codebase. It uses static analysis (AST) for prompts and dynamic loading for models, providing a side-by-side comparison TUI.

## 🏗 Architecture
Verger follows a strict three-tier architecture to ensure modularity and extensibility.

### 1. Core Layer (`src/verger/core/`)
The "Brain" of the application, completely decoupled from any UI.
- **Bootstrap Phase**: Sequential initialization (`.env` → `config` → `plugins`).
- **Registry Pattern**: Centralized registries for both Models and Prompts.
- **Adapter Pattern**: Frameworks (LangChain, PydanticAI) are wrapped in unified interfaces (`VergerModel`, `VergerPrompt`).
- **Plugin System**: Uses **Auto-Scanning** via `pkgutil` to discover all resolvers in the `adapters/` directories. This allows for zero-config extension by simply adding a new file.
- **AST Loader**: Uses `ast` to read/write string variables in source code without execution.

### 2. CLI Layer (`src/verger/cli/`)
Built with **Typer**.
- Provides commands for listing, running, and managing prompts/models.
- Uses `@app.callback()` to trigger the Core bootstrap.

### 3. TUI Layer (`src/verger/tui/`)
Built with **Textual**.
- Interactive environment for real-time prompt editing and side-by-side model evaluation.

---

## 🛠 Design Decisions & Patterns
- **Framework Agnostic**: Do not make LangChain a first-class citizen. Use adapters to remain compatible with any future LLM framework.
- **Duck-Typing Resolvers**: Resolvers (like `LangChainResolver`) check object structures/module names to avoid importing heavy dependencies into the Verger core.
- **Async First**: All model invocations are `async` to support parallel evaluation.
- **UV for Dev**: Use `uv` for dependency management and `uv run` for execution.

---

## 🚦 Current State
- [x] Project scaffolding and directory structure.
- [x] Core Bootstrap and Plugin Discovery system.
- [x] Model Registry and Native/LangChain Adapters.
- [x] Prompt Registry and AST-based Native String Resolver.
- [x] MkDocs documentation skeleton (Material theme).
- [ ] Configuration Loader (parsing `pyproject.toml`).
- [ ] Model Loader (dynamic import logic).
- [ ] Runner Engine (execution logic).
- [ ] TUI Implementation.

## 📖 Conventions
- **Imports**: Use absolute imports (`from verger.core...`).
- **Testing**: Use `pytest`. Add tests for every new resolver.
- **Documentation**: All public logic should be reflected in `docs/`.
- **Coding Style**: Strict adherence to `ruff` formatting and linting.
