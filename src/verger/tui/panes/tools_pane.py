"""Pane for inspecting all configured AI tools."""

import json

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Static, TextArea

from verger.core.tools import tool_registry
from verger.tui.widgets.base import VergerTUIComponent
from verger.utils.imports import import_reference


class ToolsPane(VergerTUIComponent):
    """
    A pane to list and inspect all configured AI tools.
    """

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the tools pane.

        Yields:
            The widgets that make up the pane.
        """
        tool_names = sorted(self.config.tools.keys())

        with Horizontal():
            with Vertical(id="tool-list-container", classes="sidebar"):
                yield Label("[b]Tools[/b]", classes="sidebar-title")
                with ListView(id="tool-list"):
                    for name in tool_names:
                        yield ListItem(Label(name), id=f"tool-item-{name}")

            with Vertical(id="tool-details", classes="details-view"):
                yield Label("Select a tool to view details", id="tool-details-placeholder")
                yield Label("[b]Name:[/b]", classes="detail-label")
                yield Static("", id="tool-name-display", classes="detail-value")
                yield Label("[b]Description:[/b]", classes="detail-label")
                yield Static("", id="tool-desc-display", classes="detail-value")
                yield Label("[b]Arguments Schema:[/b]", classes="detail-label")
                yield TextArea(id="tool-schema-display", read_only=True, classes="detail-textarea")

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle tool selection from the list."""
        if not event.item or not event.item.id:
            return

        tool_key = event.item.id.replace("tool-item-", "")
        tool_ref = self.config.tools[tool_key]

        try:
            # Update placeholder
            self.query_one("#tool-details-placeholder").display = False

            # Resolve the tool
            tool_obj = import_reference(tool_ref)
            tool = tool_registry.resolve(tool_obj)

            # Update displays
            self.query_one("#tool-name-display", Static).update(tool.name)
            self.query_one("#tool-desc-display", Static).update(tool.description)

            # Format schema as pretty JSON
            schema_json = json.dumps(tool.args_schema, indent=2)
            self.query_one("#tool-schema-display", TextArea).text = schema_json

        except Exception as e:
            self.app_ref.notify(f"Error loading tool details: {e}", severity="error")
