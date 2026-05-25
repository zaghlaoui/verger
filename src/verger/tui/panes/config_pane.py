"""Configuration pane for model and prompt evaluation."""

from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label, Select, TextArea

from verger.core.prompts import prompt_registry
from verger.core.schema import MessageRole
from verger.tui.widgets.base import VergerTUIComponent
from verger.tui.widgets.message_block import MessageBlock
from verger.utils.imports import import_reference


class ConfigPane(VergerTUIComponent):
    """
    A single configuration pane.

    Contains model selection, prompt preset selection, an editable list of
    message blocks, and a display for the model's output.
    """

    def __init__(self, pane_id: int, app_ref: Any, **kwargs: Any):
        """
        Initialize the configuration pane.

        Args:
            pane_id: Unique numerical ID for this pane.
            app_ref: Reference to the parent TUI application.
            **kwargs: Additional parameters for the container.
        """
        super().__init__(app_ref=app_ref, **kwargs)
        self.pane_id = pane_id
        self.border_title = f"Configuration {pane_id}"

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the configuration pane.

        Yields:
            The widgets that make up the pane.
        """
        model_options = [(name, name) for name in self.config.models.keys()]
        prompt_options = [(name, ref) for name, ref in self.config.prompts.items()]

        with Horizontal(classes="pane-selectors"):
            yield Select(
                model_options,
                prompt="Model",
                id=f"model-select-{self.pane_id}",
                classes="pane-select",
            )
            yield Select(
                prompt_options,
                prompt="Preset",
                id=f"prompt-select-{self.pane_id}",
                classes="pane-select",
            )

        yield Label("Conversation:", classes="pane-label")
        with VerticalScroll(id=f"messages-container-{self.pane_id}", classes="messages-scroll"):
            # Initial user message
            yield MessageBlock(role=MessageRole.USER)

        yield Button("+ Add Message", variant="success", id=f"add-msg-btn-{self.pane_id}")

        yield Label("Output:", classes="pane-label")
        yield TextArea(id=f"output-display-{self.pane_id}", classes="pane-output", read_only=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle adding a new message block."""
        if event.button.id == f"add-msg-btn-{self.pane_id}":
            container = self.query_one(f"#messages-container-{self.pane_id}", VerticalScroll)
            await container.mount(MessageBlock())
            self.app_ref.schedule_variable_update()

    async def on_select_changed(self, event: Select.Changed) -> None:
        """
        Handle preset selection to populate the message blocks.

        Args:
            event: The selection change event.
        """
        if event.select.id == f"prompt-select-{self.pane_id}" and event.value != Select.BLANK:
            try:
                # Load the raw prompt object from the reference
                prompt_obj = import_reference(cast(str, event.value))
                # Resolve it to a VergerPrompt adapter
                prompt = prompt_registry.resolve(prompt_obj)

                # Clear existing messages and mount new ones
                container = self.query_one(f"#messages-container-{self.pane_id}", VerticalScroll)
                await container.remove_children()

                messages = prompt.get_messages()
                for msg in messages:
                    await container.mount(MessageBlock(role=msg.role, content=msg.content))

                self.app_ref.schedule_variable_update()

            except Exception as e:
                self.app_ref.notify(f"Error loading preset: {e}", severity="error")

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """
        Notify the app to update shared variables when any message content changes.

        Args:
            event: The text area change event.
        """
        self.app_ref.schedule_variable_update()
