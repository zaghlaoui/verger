"""Typer application defining the CLI commands for Verger."""

import typer

from verger.core.config.loader import get_config

# Initialize the Typer application
app = typer.Typer(
    name="verger",
    help="AI Prompt and Model Management",
    no_args_is_help=True,
)


@app.command()
def info():
    """Display information about Verger and the current configuration."""
    try:
        config = get_config()
        typer.secho("Verger Status: Ready", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"Prompts found: {len(config.prompts)}")
        typer.echo(f"Models found: {len(config.models)}")

        if config.prompts:
            typer.echo("\nPrompts:")
            for name in config.prompts:
                typer.echo(f"  - {name}")

        if config.models:
            typer.echo("\nModels:")
            for name in config.models:
                typer.echo(f"  - {name}")

    except Exception as e:
        typer.secho(f"Error loading config: {e}", fg=typer.colors.RED)


@app.command()
def list_prompts():
    """List all configured prompts."""
    config = get_config()
    if not config.prompts:
        typer.echo("No prompts configured.")
        return

    for name, ref in config.prompts.items():
        typer.echo(f"{name}: {ref}")


@app.command()
def tui():
    """Launch the Verger Terminal User Interface."""
    try:
        from verger.tui.app import launch_tui

        launch_tui()
    except ImportError:
        typer.secho(
            "Error: Textual is not installed. "
            "Please install it with 'pip install textual' or 'uv add textual'.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=1) from None
