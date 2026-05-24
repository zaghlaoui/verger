"""Configuration pane for model and prompt evaluation."""

from typing import Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Select, TextArea

from verger.core.prompts import prompt_registry
from verger.tui.widgets.base import VergerTUIComponent
from verger.utils.imports import import_reference


class ConfigPane(VergerTUIComponent):
    """
    A single configuration pane.

    Contains model selection, prompt preset selection, an editable prompt text area,
    and a display for the model's output.
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
        yield Label("Edit Prompt:", classes="pane-label")
        yield TextArea(id=f"prompt-text-{self.pane_id}", classes="pane-textarea")
        yield Label("Output:", classes="pane-label")
        yield TextArea(id=f"output-display-{self.pane_id}", classes="pane-output", read_only=True)

    def on_select_changed(self, event: Select.Changed) -> None:
        """
        Handle preset selection to populate the text area.

        Args:
            event: The selection change event.
        """
        if event.select.id == f"prompt-select-{self.pane_id}" and event.value != Select.BLANK:
            try:
                # Load the raw prompt object from the reference
                prompt_obj = import_reference(cast(str, event.value))
                # Resolve it to a VergerPrompt adapter to get its text
                prompt = prompt_registry.resolve(prompt_obj)

                # Update the text area
                text_area = self.query_one(f"#prompt-text-{self.pane_id}", TextArea)
                text_area.text = prompt.get_text()

            except Exception as e:
                self.app_ref.notify(f"Error loading preset: {e}", severity="error")

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """
        Notify the app to update shared variables when text area changes.

        Args:
            event: The text area change event.
        """
        # Using a small delay to avoid excessive parsing while typing
        self.app_ref.schedule_variable_update()
