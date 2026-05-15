# Contributing to Verger

We love contributions! Whether you're fixing a bug, adding a new model adapter, or improving the TUI.

## Development Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-repo/verger.git
   cd verger
   ```

2. **Install dependencies**:
   We use `uv` for lightning-fast dependency management.
   ```bash
   uv sync
   ```

3. **Run the CLI in dev mode**:
   ```bash
   uv run ver info
   ```

## Adding a New Model Adapter

To add support for a new framework (e.g., LlamaIndex):
1. Create a new resolver in `src/verger/core/models/adapters/`.
2. Implement the `ModelResolver` and `VergerModel` protocols.
3. Register your resolver in `pyproject.toml` under `[project.entry-points."verger.models.resolvers"]`.

## Testing

Run tests using pytest:
```bash
uv run pytest
```
