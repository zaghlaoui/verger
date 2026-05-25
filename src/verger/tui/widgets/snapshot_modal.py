"""Modal screen for capturing snapshot metadata."""

from typing import Any

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SnapshotModal(ModalScreen[dict[str, str]]):
    """
    A modal screen to collect description and tags for a snapshot.
    """

    anchor_name: str
    """The name of the prompt anchor being versioned."""

    DEFAULT_CSS = """
    SnapshotModal {
        align: center middle;
    }

    #snapshot-dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-columns: 1fr 2fr;
        padding: 0 1;
        width: 60;
        height: auto;
        border: thick $primary 80%;
        background: $surface;
    }

    #snapshot-title {
        column-span: 2;
        height: 3;
        width: 100%;
        content-align: center middle;
        text-style: bold;
        background: $primary;
        color: $text;
    }

    .modal-label {
        content-align: right middle;
        height: 3;
    }

    .modal-input {
        width: 100%;
    }

    #modal-buttons {
        column-span: 2;
        height: 5;
        align: center middle;
    }

    .modal-btn {
        width: 15;
        margin: 0 1;
    }
    """

    def __init__(self, anchor_name: str, **kwargs: Any):
        """
        Initialize the modal.

        Args:
            anchor_name: The name of the prompt anchor.
            **kwargs: Additional parameters for the Screen.
        """
        super().__init__(**kwargs)
        self.anchor_name = anchor_name

    def compose(self) -> ComposeResult:
        """
        Build the modal UI structure.

        Yields:
            The widgets that make up the modal.
        """
        with Grid(id="snapshot-dialog"):
            yield Label(f"Save Snapshot: {self.anchor_name}", id="snapshot-title")

            yield Label("Author:", classes="modal-label")
            yield Input(placeholder="Your Name", id="snapshot-author", classes="modal-input")

            yield Label("Description:", classes="modal-label")
            yield Input(placeholder="What changed?", id="snapshot-desc", classes="modal-input")

            yield Label("Tags:", classes="modal-label")
            yield Input(
                placeholder="e.g. stable, experimental", id="snapshot-tags", classes="modal-input"
            )

            with Horizontal(id="modal-buttons"):
                yield Button("Cancel", variant="default", id="cancel-btn", classes="modal-btn")
                yield Button("Save", variant="primary", id="save-btn", classes="modal-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button clicks in the modal.

        Args:
            event: The button pressed event.
        """
        if event.button.id == "cancel-btn":
            self.dismiss({})
        elif event.button.id == "save-btn":
            author = self.query_one("#snapshot-author", Input).value
            description = self.query_one("#snapshot-desc", Input).value
            tags = self.query_one("#snapshot-tags", Input).value

            if not author:
                self.app.notify("Author is required", severity="error")
                return

            self.dismiss({"author": author, "description": description, "tags": tags})
