"""Main entry point for the Verger application."""

import sys

from verger.cli.app import app
from verger.core.bootstrap import setup_app
from verger.utils.logging import setup_logging


def main() -> None:
    """
    Main execution routine for Verger.

    This function coordinates the startup sequence:
    1. Configures logging.
    2. Initializes the core engine (config, plugins).
    3. Launches the Typer command-line interface.
    """
    try:
        # Configuration of logs happens at the APP level, not the CORE level.
        setup_logging()

        # Initialize core (plugins, config, etc.)
        setup_app()

        # Launch Typer
        app()

    except Exception as e:
        print(f"Error during startup: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
