# Architecture Overview

Verger is built on three main layers to ensure it remains fast, extensible, and easy to maintain.

## 1. The Core (The Brain)
The core handles the "heavy lifting" of the application. It is completely independent of the UI.
- **Registry Pattern**: All model and prompt support is loaded dynamically.
- **Adapters**: We wrap external libraries (like LangChain) in a unified `VergerModel` interface.
- **AST Loader**: We use Python's `ast` module to surgically read and write prompts in your source code.

## 2. The CLI (The Voice)
Built with **Typer**, the CLI provides a fast way to interact with your prompts and models from the command line.
- Commands: `ver prompts list`, `ver run`, etc.

## 3. The TUI (The Face)
Built with **Textual**, the TUI provides a rich, interactive environment for evaluating AI responses side-by-side.

---

## Data Flow

1. **Bootstrap**: System loads `.env` and discovers plugins via Entry Points.
2. **Discovery**: User code is scanned (via AST for prompts, via Import for models).
3. **Execution**: The `Runner` executes prompts against models using async adapters.
