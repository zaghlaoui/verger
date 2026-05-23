# Verger: AI Agent Project Memory

> **System Prompt Addendum**: This file is the source of truth for all AI agents working on Verger. It defines the architecture, standards, and conventions that must be strictly followed.

## 🎯 Overview
**Verger** is a framework-agnostic tool for evaluating AI prompts and models. It allows developers to define and compare different AI configurations (models, prompts, and eventually tools) through a central configuration file and an interactive TUI.

---

## 🏗 Architecture
Verger follows a strict three-tier decoupled architecture centered around a configuration-driven resolution system.

### 1. Core Layer (`src/verger/core/`)
- **Bootstrap Phase**: Sequential initialization via `bootstrap.py` (`.env` → `config` → `plugins`).
- **Configuration Loader**: Reads from `verger.toml` or `pyproject.toml`. Users define named references to models and prompts here.
- **Registry Pattern**: Centralized hubs for Models and Prompts (`model_registry.py`, `prompt_registry.py`).
- **Adapter Pattern**: Frameworks (LangChain, etc.) and native objects are wrapped in unified interfaces (`VergerModel`, `VergerPrompt`).
- **Plugin System**: Auto-scanning of `adapters/` directories via `pkgutil` for discovery of resolvers.

### 2. CLI Layer (`src/verger/cli/`)
- Built with **Typer**. Handles configuration inspection and TUI launch.

### 3. TUI Layer (`src/verger/tui/`)
- Built with **Textual**. Provides a side-by-side evaluation environment with reactive variable detection based on `string.Formatter`.

---

## 🔍 Code Quality Standards (The "Strict Gates")
We maintain a "Max Quality" baseline. Every commit is gated by 14+ automated checks.

### 1. Testing & Coverage
- **Enforcement**: `pytest` runs on every commit.
- **Baseline**: Minimum **48.5%** test coverage required (enforced by `pytest-cov`).
- **Fast Loop**: `make test` (no coverage) for development; `make test-cov` for verification.

### 2. Documentation
- **Coverage**: **100% docstring coverage** required (enforced by `interrogate`).
- **Integrity**: `mkdocs build --strict` must pass (no broken API references).

### 3. Static Analysis
- **Modernization**: `refurb` suggests modern Python idioms.
- **Dead Code**: `vulture` find unused code (respecting framework entry points).
- **Dependencies**: `deptry` validates `pyproject.toml` against actual imports.

---

## 📖 Documentation Style Guidelines
All documentation must follow the **Google Style** and match the precision of `model_registry.py`.

### 1. Module Level
Every file must start with a high-level docstring describing its specific purpose.

### 2. Class Level
Summary line followed by a detailed paragraph explaining the class's role in the system.

### 3. Method Level
Must include:
- **Summary**: Brief description of the action.
- **Args**: Typed list of parameters.
- **Returns**: Description of the return value and type.
- **Raises**: Explicit list of possible exceptions.

**Example Pattern:**
```python
def example_method(self, value: str) -> bool:
    """
    Brief summary of the method.

    Detailed explanation of logic or side effects.

    Args:
        value: The input string to process.

    Returns:
        True if processing succeeded, False otherwise.

    Raises:
        ValueError: If value is empty.
    """
```

---

## 🛠 Development Workflow
1.  **Work**: Make changes in `src/`.
2.  **Verify**: Run `make quality` (runs all 8 core checks).
3.  **Commit**: Use `make cz` or `git commit` to trigger the 14 pre-commit hooks.
4.  **Style**: Use **Conventional Commits** (`feat:`, `fix:`, `refactor:`, `docs:`, `build:`, `chore:`).

---

## 🚦 Current State & Milestones
- [x] Core Architecture & Registries.
- [x] Multi-provider Adapter System (Native, LangChain).
- [x] Configuration Loader (TOML/Pyproject).
- [x] Terminal User Interface (TUI) with side-by-side comparison.
- [x] Strict Quality Pipeline (Pre-commit hooks).
- [x] 100% Docstring Coverage.
- [ ] Tool Plugins & Registry (Not yet implemented).
- [ ] Comprehensive CLI Test Suite (Coverage Gap).
- [ ] TUI Unit/Integration Tests.
