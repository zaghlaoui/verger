"""Pane for inspecting all configured prompts."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Static, TextArea

from verger.core.prompts import prompt_registry
from verger.tui.widgets.base import VergerTUIComponent
from verger.utils.imports import import_reference


class PromptsPane(VergerTUIComponent):
    """
    A pane to list and inspect all discovered prompts.
    """

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the prompts pane.

        Yields:
            The widgets that make up the pane.
        """
        prompt_names = sorted(self.config.prompts.keys())

        with Horizontal():
            with Vertical(id="prompt-list-container", classes="sidebar"):
                yield Label("[b]Prompts[/b]", classes="sidebar-title")
                with ListView(id="prompt-list"):
                    for name in prompt_names:
                        yield ListItem(Label(name), id=f"prompt-item-{name}")

            with Vertical(id="prompt-details", classes="details-view"):
                yield Label("Select a prompt to view details", id="prompt-details-placeholder")
                yield Label("[b]Reference:[/b]", classes="detail-label")
                yield Static("", id="prompt-ref-display", classes="detail-value")
                yield Label("[b]Variables:[/b]", classes="detail-label")
                yield Static("", id="prompt-vars-display", classes="detail-value")
                yield Label("[b]Template Content:[/b]", classes="detail-label")
                yield TextArea(
                    id="prompt-content-display", read_only=True, classes="detail-textarea"
                )

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle prompt selection from the list."""
        if not event.item or not event.item.id:
            return

        prompt_name = event.item.id.replace("prompt-item-", "")
        prompt_ref = self.config.prompts[prompt_name]

        try:
            # Update placeholder
            self.query_one("#prompt-details-placeholder").display = False

            # Resolve the prompt
            prompt_obj = import_reference(prompt_ref)
            prompt = prompt_registry.resolve(prompt_obj)

            # Update displays
            self.query_one("#prompt-ref-display", Static).update(prompt_ref)

            vars_str = ", ".join(sorted(prompt.get_variables())) or "None"
            self.query_one("#prompt-vars-display", Static).update(vars_str)

            self.query_one("#prompt-content-display", TextArea).text = prompt.get_text()

        except Exception as e:
            self.app_ref.notify(f"Error loading prompt details: {e}", severity="error")
