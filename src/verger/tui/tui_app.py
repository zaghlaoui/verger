"""
Verger Terminal User Interface.

Main application module for the Verger TUI.
"""

import asyncio
import string
from pathlib import Path
from typing import Any, cast

from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Select,
    TabbedContent,
    TabPane,
    TextArea,
)

from verger.core.config.loader import get_config
from verger.core.engine import ExecutionEngine
from verger.tui.panes.config_pane import ConfigPane
from verger.tui.panes.models_pane import ModelsPane
from verger.tui.panes.prompts_pane import PromptsPane
from verger.tui.panes.tools_pane import ToolsPane
from verger.utils.imports import import_reference


class VergerTUI(App):
    """
    Verger Terminal User Interface.

    Main application that manages multiple configuration panes and shared
    variable inputs for side-by-side evaluation.
    """

    TITLE = "Verger: The AI Weaver"
    CSS_PATH = Path(__file__).parent / "styles" / "main.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run_engine", "Run All"),
        ("a", "add_pane_action", "Add Pane"),
    ]

    def __init__(self, **kwargs: Any):
        """
        Initialize the Verger TUI.

        Args:
            **kwargs: Additional parameters for the App.
        """
        super().__init__(**kwargs)
        self.engine = ExecutionEngine()
        self.config = get_config()
        self.pane_count = 0
        self._update_timer = None

    def compose(self) -> ComposeResult:
        """
        Build the UI structure for the main application.

        Yields:
            The widgets that make up the interface.
        """
        yield Header()

        with TabbedContent():
            with TabPane("Playground", id="tab-playground"):
                # TOP HALF: Horizontal Scroll for Configuration Panes
                with Vertical(id="top-half"):
                    with HorizontalScroll(id="panes-container"):
                        # We will mount panes here dynamically
                        with Vertical(id="add-pane-container"):
                            yield Label("Add another\nconfiguration pane", id="add-pane-label")
                            yield Button("+ Add Pane", id="add-pane-btn", variant="success")

                # BOTTOM HALF: Shared Variables and Run Button
                with Vertical(id="bottom-half"):
                    yield Label("[b]Shared Variables[/b]")
                    yield VerticalScroll(id="variable-inputs")
                    with Horizontal(id="action-buttons"):
                        yield Button("Run All Configurations (r)", variant="primary", id="run-btn")
                        yield Button("+ Add Pane (a)", id="add-pane-btn-bottom", variant="success")
                    yield Label("", id="status-label")

            with TabPane("Prompts", id="tab-prompts"):
                yield PromptsPane(app_ref=self)

            with TabPane("Models", id="tab-models"):
                yield ModelsPane(app_ref=self)

            with TabPane("Tools", id="tab-tools"):
                yield ToolsPane(app_ref=self)

        yield Footer()

    async def on_mount(self) -> None:
        """Handle the application mount event."""
        await self.add_pane()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle all button press events.

        Args:
            event: The button pressed event.
        """
        if event.button.id in ("add-pane-btn", "add-pane-btn-bottom"):
            await self.add_pane()
        elif event.button.id == "run-btn":
            await self.action_run_engine()

    async def action_add_pane_action(self) -> None:
        """Action for adding a new configuration pane via key binding."""
        await self.add_pane()

    async def add_pane(self) -> None:
        """Dynamically add a new configuration pane."""
        self.pane_count += 1
        container = self.query_one("#panes-container", HorizontalScroll)
        add_btn_container = self.query_one("#add-pane-container")

        # Mount the new pane right before the add button
        await container.mount(ConfigPane(self.pane_count, self), before=add_btn_container)

    def schedule_variable_update(self) -> None:
        """Debounce variable updates to prevent excessive parsing while typing."""
        if self._update_timer is not None:
            self._update_timer.stop()
        self._update_timer = self.set_timer(0.5, self._extract_and_update_variables)

    async def _extract_and_update_variables(self) -> None:
        """Extract variables from all active panes and update the shared input list."""
        all_variables = set()
        formatter = string.Formatter()

        # Parse text from all text areas
        for text_area in self.query(TextArea):
            text = text_area.text
            if text:
                from contextlib import suppress

                with suppress(ValueError):
                    variables = {
                        field_name
                        for _, field_name, _, _ in formatter.parse(text)
                        if field_name is not None
                    }
                    all_variables.update(variables)

        await self._render_variable_inputs(all_variables)

    async def _render_variable_inputs(self, variables: set[str]) -> None:
        """
        Update the variable input widgets, preserving existing values.

        Args:
            variables: The set of variable names detected in the prompts.
        """
        container = self.query_one("#variable-inputs", VerticalScroll)

        # Save existing values
        existing_values = {
            input_widget.id.replace("var-", ""): input_widget.value
            for input_widget in container.query(Input)
            if input_widget.id
        }

        await container.remove_children()

        if not variables:
            await container.mount(
                Label("No variables detected in current prompts.", classes="text-muted")
            )
            return

        for var in sorted(variables):
            value = existing_values.get(var, "")
            await container.mount(
                Horizontal(
                    Label(f"{var}:", classes="input-label"),
                    Input(
                        value=value,
                        placeholder=f"Enter value for {var}",
                        id=f"var-{var}",
                    ),
                    classes="input-row",
                )
            )

    async def action_run_engine(self) -> None:
        """Run all active configurations concurrently."""
        status_label = self.query_one("#status-label", Label)

        # Collect shared variables
        variables = {}
        for input_widget in self.query("#variable-inputs Input"):
            input_widget = cast(Input, input_widget)
            if input_widget.id:
                var_name = input_widget.id.replace("var-", "")
                variables[var_name] = input_widget.value

        status_label.update("[yellow]Running configurations...[/yellow]")

        panes = list(self.query(ConfigPane))
        if not panes:
            status_label.update("[red]No configurations to run.[/red]")
            return

        # Prepare tasks for concurrent execution
        tasks = [self._run_single_pane(pane, variables) for pane in panes]

        # Run all panes concurrently
        await asyncio.gather(*tasks)

        status_label.update("[green]All runs completed![/green]")

    async def _run_single_pane(self, pane: ConfigPane, variables: dict[str, str]) -> None:
        """
        Execute a single pane's configuration.

        Args:
            pane: The ConfigPane to run.
            variables: Shared variables for formatting the prompt.
        """
        model_select = pane.query_one(f"#model-select-{pane.pane_id}", Select)
        text_area = pane.query_one(f"#prompt-text-{pane.pane_id}", TextArea)
        output_display = pane.query_one(f"#output-display-{pane.pane_id}", TextArea)

        if model_select.value == Select.BLANK:
            output_display.text = "Please select a model."
            return

        raw_prompt_text = text_area.text
        if not raw_prompt_text:
            output_display.text = "Prompt is empty."
            return

        output_display.text = "Waiting for model..."

        try:
            model_name = cast(str, model_select.value)
            model_ref = self.config.get_model_ref(model_name)

            # Dynamically load the model object
            model_obj = import_reference(model_ref)

            # Since the user might have edited the text area, we treat the
            # text area content ITSELF as the raw prompt object (a string).
            # We don't use the prompt reference here.
            prompt_obj = raw_prompt_text

            # Run engine
            result = await self.engine.run(
                model_obj=model_obj,
                prompt_obj=prompt_obj,
                variables=variables,
            )
            output_display.text = result
        except Exception as e:
            output_display.text = f"Error: {e}"


def launch_tui() -> None:
    """Launch the Verger TUI. Core setup is assumed to be handled by the caller."""
    app = VergerTUI()
    app.run()
