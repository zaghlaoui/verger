# CLI Usage

Verger provides a set of commands to interact with your AI assets directly from the terminal.

## Commands

### `verger info`
Check if Verger is correctly installed and displays the count of found prompts and models in your project.

### `verger list-prompts`
List all prompts defined in your `pyproject.toml` along with their references.

### `verger tui`
Launch the full interactive experience. The TUI allows you to:
- **View Prompts**: See all your configured prompts in one place.
- **Live Preview**: See the actual text of your prompts extracted via AST.
- **Side-by-Side Comparison**: (Upcoming) Compare how different models respond to the same prompt.

## Global Options

### `VERGER_LOG=DEBUG`
Set this environment variable to see detailed logs about plugin discovery and configuration loading.

```bash
VERGER_LOG=DEBUG verger info
```
