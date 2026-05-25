"""Pane for inspecting all configured prompts and their history."""

from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Label, ListItem, ListView, Static, TextArea, Tree

from verger.core.lab import lab_service
from verger.core.prompts import prompt_registry
from verger.tui.widgets.base import VergerTUIComponent
from verger.utils.imports import import_reference


class PromptsPane(VergerTUIComponent):
    """
    A pane to list and inspect all discovered prompts, including their version history.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the prompts pane.

        Args:
            *args: Positional arguments for the component.
            **kwargs: Keyword arguments for the component.
        """
        super().__init__(*args, **kwargs)
        self.selected_prompt_name: str = ""
        """The name of the currently selected prompt in the sidebar."""

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
                with VerticalScroll(id="prompt-info-container"):
                    yield Label("Select a prompt to view details", id="prompt-details-placeholder")

                    yield Label("[b]Current Source (Code)[/b]", classes="detail-label")
                    yield Label("[b]Reference:[/b]", classes="detail-sublabel")
                    yield Static("", id="prompt-ref-display", classes="detail-value")
                    yield Label("[b]Variables:[/b]", classes="detail-sublabel")
                    yield Static("", id="prompt-vars-display", classes="detail-value")

                    yield Label("[b]Version History (Lab)[/b]", classes="detail-label")
                    yield Tree("History", id="prompt-history-tree")

                    yield Label("[b]Content Preview[/b]", classes="detail-label")
                    yield TextArea(
                        id="prompt-content-display", read_only=True, classes="detail-textarea"
                    )

                    yield Button("Load Selected Version", variant="primary", id="load-version-btn")

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """
        Handle prompt selection from the list.

        Args:
            event: The list view highlighting event.
        """
        if not event.item or not event.item.id:
            return

        prompt_name = event.item.id.replace("prompt-item-", "")
        self.selected_prompt_name = prompt_name
        prompt_ref = self.config.prompts[prompt_name]

        try:
            # Update placeholder
            self.query_one("#prompt-details-placeholder").display = False

            # Resolve the prompt from code
            prompt_obj = import_reference(prompt_ref)
            prompt = prompt_registry.resolve(prompt_obj)

            # Update code-based displays
            self.query_one("#prompt-ref-display", Static).update(prompt_ref)
            vars_str = ", ".join(sorted(prompt.get_variables())) or "None"
            self.query_one("#prompt-vars-display", Static).update(vars_str)

            # Update History Tree
            tree = self.query_one("#prompt-history-tree", Tree)
            tree.clear()
            tree.root.label = f"History: {prompt_name}"

            history = lab_service.prompts.get_history(prompt_name)
            if not history:
                tree.root.add_leaf("No snapshots found in Lab.")
            else:
                for entry in history:
                    # Format a nice label for the history node
                    date_str = entry["created_at"].strftime("%Y-%m-%d %H:%M")
                    label = f"{entry['hash'][:7]} - {entry['author']} ({date_str})"
                    if entry["description"]:
                        label += f": {entry['description']}"

                    node = tree.root.add_leaf(label)
                    node.data = entry["hash"]

            # Initial preview shows the code version
            messages = prompt.get_messages()
            self._update_preview(messages)

        except Exception as e:
            self.app_ref.notify(f"Error loading prompt details: {e}", severity="error")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """
        Preview the content of a selected history node.

        Args:
            event: The tree node selection event.
        """
        commit_hash = cast(str | None, event.node.data)
        if not commit_hash:
            return

        try:
            snapshot = lab_service.prompts.load_snapshot(self.selected_prompt_name, commit_hash)
            self._update_preview(snapshot.messages)
        except Exception as e:
            self.app_ref.notify(f"Error loading snapshot preview: {e}", severity="error")

    def _update_preview(self, messages: list) -> None:
        """
        Helper to update the content preview text area.

        Args:
            messages: The list of VergerMessage objects to display.
        """
        display_text = ""
        for msg in messages:
            display_text += f"--- {msg.role.upper()} ---\n{msg.content}\n\n"
        self.query_one("#prompt-content-display", TextArea).text = display_text.strip()
