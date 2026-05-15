import sys
from verger.cli.app import app
from verger.core.bootstrap import setup_app
from verger.utils.logging import setup_logging


def main():
    """
    Entry point:
    1. Configure how we see logs.
    2. Initialize the core logic.
    3. Launch the UI.
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
