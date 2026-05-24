"""Pane for inspecting all configured AI models."""

import json

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Static, TextArea

from verger.core.config.schema import ModelConfig
from verger.tui.widgets.base import VergerTUIComponent


class ModelsPane(VergerTUIComponent):
    """
    A pane to list and inspect all configured AI models.
    """

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the models pane.

        Yields:
            The widgets that make up the pane.
        """
        model_names = sorted(self.config.models.keys())

        with Horizontal():
            with Vertical(id="model-list-container", classes="sidebar"):
                yield Label("[b]Models[/b]", classes="sidebar-title")
                with ListView(id="model-list"):
                    for name in model_names:
                        yield ListItem(Label(name), id=f"model-item-{name}")

            with Vertical(id="model-details", classes="details-view"):
                yield Label("Select a model to view details", id="model-details-placeholder")
                yield Label("[b]Reference:[/b]", classes="detail-label")
                yield Static("", id="model-ref-display", classes="detail-value")
                yield Label("[b]Configuration Parameters:[/b]", classes="detail-label")
                yield TextArea(id="model-params-display", read_only=True, classes="detail-textarea")

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle model selection from the list."""
        if not event.item or not event.item.id:
            return

        model_name = event.item.id.replace("model-item-", "")
        config_entry = self.config.models[model_name]

        # Update placeholder
        self.query_one("#model-details-placeholder").display = False

        if isinstance(config_entry, ModelConfig):
            ref = config_entry.ref
            params = config_entry.params
        else:
            ref = config_entry
            params = {}

        # Update displays
        self.query_one("#model-ref-display", Static).update(ref)

        # Format params as pretty JSON
        params_json = json.dumps(params, indent=2) if params else "{}"
        self.query_one("#model-params-display", TextArea).text = params_json
