"""Configuration pane for model and prompt evaluation."""

from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label, Select, TextArea

from verger.core.lab import lab_service
from verger.core.prompts import prompt_registry
from verger.core.schema import MessageRole
from verger.tui.widgets.base import VergerTUIComponent
from verger.tui.widgets.message_block import MessageBlock
from verger.tui.widgets.snapshot_modal import SnapshotModal
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

        with Horizontal(classes="pane-actions"):
            yield Button("Save Snapshot", variant="primary", id=f"save-snap-btn-{self.pane_id}")

        yield Label("Output:", classes="pane-label")
        yield TextArea(id=f"output-display-{self.pane_id}", classes="pane-output", read_only=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == f"add-msg-btn-{self.pane_id}":
            container = self.query_one(f"#messages-container-{self.pane_id}", VerticalScroll)
            await container.mount(MessageBlock())
            self.app_ref.schedule_variable_update()
        elif event.button.id == f"save-snap-btn-{self.pane_id}":
            await self._action_save_snapshot()

    async def _action_save_snapshot(self) -> None:
        """Collect messages and prompt for metadata to save a snapshot."""
        # 1. Identify the anchor name (preset name or a default)
        prompt_select = self.query_one(f"#prompt-select-{self.pane_id}", Select)
        if prompt_select.value == Select.BLANK:
            anchor = f"playground-{self.pane_id}"
        else:
            # We don't have direct access to the display name easily, so we use value
            # which is the reference, but we want a cleaner anchor name.
            # For now, we'll try to find the label in the options.
            anchor = "unknown"
            for label, value in prompt_select._options:
                if value == prompt_select.value:
                    anchor = str(label)
                    break

        # 2. Open modal for metadata
        def handle_modal_result(data: dict[str, str]) -> None:
            """
            Process the metadata from the modal and save the snapshot.

            Args:
                data: The metadata dictionary from the modal.
            """
            if not data:
                return

            try:
                # 3. Collect messages
                message_blocks = list(self.query(MessageBlock))
                messages = [block.get_message_data() for block in message_blocks]

                # 4. Save via LabService
                tags_list = [t.strip() for t in data["tags"].split(",") if t.strip()]
                lab_service.prompts.capture_snapshot(
                    anchor=anchor,
                    messages=messages,
                    author=data["author"],
                    description=data["description"] or None,
                    tags=tags_list,
                )
                self.app.notify(f"Snapshot saved for '{anchor}'", severity="information")
            except Exception as e:
                self.app.notify(f"Failed to save snapshot: {e}", severity="error")

        self.app.push_screen(SnapshotModal(anchor_name=anchor), handle_modal_result)

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
