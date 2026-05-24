"""Pane for inspecting system status and environment health."""

import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, Static

from verger.tui.widgets.base import VergerTUIComponent


class StatusPane(VergerTUIComponent):
    """
    A pane to inspect the system configuration and environment variable status.
    """

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the status pane.

        Yields:
            The widgets that make up the pane.
        """
        with VerticalScroll(classes="details-view"):
            yield Label("[b]System Configuration[/b]", classes="detail-label")

            # Show CWD
            yield Label("Working Directory:", classes="detail-sublabel")
            yield Static(str(Path.cwd()), classes="detail-value")

            # Show Configuration Source
            yield Label("Configuration Source:", classes="detail-sublabel")
            yield Static(self.config.status.config_source, classes="detail-value")

            # Show Env File info
            env_file = self.config.env_file or ".env"
            yield Label(f"Environment File ({env_file}):", classes="detail-sublabel")
            env_path = Path.cwd() / env_file
            found_text = "[green]FOUND[/green]" if env_path.exists() else "[red]MISSING[/red]"
            yield Static(f"{env_path} ({found_text})", classes="detail-value")

            yield Label("\n[b]Environment Status[/b]", classes="detail-label")
            yield Label(
                "Currently set variables (values are hidden for security):",
                classes="text-muted",
            )

            # Show ALL loaded environment variables from the .env file + some standard ones
            monitored_keys = set(self.config.status.env_keys)

            # Add some standard ones if they are set in the environment
            standard_keys = [
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "GOOGLE_API_KEY",
                "MISTRAL_API_KEY",
                "COHERE_API_KEY",
                "VERGER_LOG",
            ]
            for key in standard_keys:
                if os.getenv(key):
                    monitored_keys.add(key)

            if not monitored_keys:
                yield Static(
                    "  No relevant environment variables detected.", classes="detail-value"
                )
            else:
                for key in sorted(monitored_keys):
                    is_set = os.getenv(key) is not None
                    status_text = "[green]SET[/green]" if is_set else "[yellow]NOT SET[/yellow]"
                    yield Static(f"  {key}: {status_text}", classes="detail-value")
