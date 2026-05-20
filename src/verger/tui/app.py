import asyncio
import string
from typing import cast

from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label, Select, TextArea

from verger.core.config.loader import get_config
from verger.core.engine import ExecutionEngine
from verger.core.prompts import prompt_registry
from verger.utils.imports import import_reference


class ConfigPane(Vertical):
    """A single configuration pane containing model select,
    prompt preset, editable prompt, and output."""

    def __init__(self, pane_id: int, app_ref: "VergerTUI", **kwargs):
        super().__init__(**kwargs)
        self.pane_id = pane_id
        self.app_ref = app_ref
        self.border_title = f"Configuration {pane_id}"

    def compose(self) -> ComposeResult:
        model_options = [(name, name) for name in self.app_ref.config.models.keys()]
        prompt_options = [(name, ref) for name, ref in self.app_ref.config.prompts.items()]

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
        """Handle preset selection to populate the text area."""
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
        """When the text area changes, tell the main app to update the shared variables."""
        # Using a small delay to avoid excessive parsing while typing
        self.app_ref.schedule_variable_update()


class VergerTUI(App):
    """
    Verger Terminal User Interface.
    Side-by-side evaluation of prompts and models.
    """

    TITLE = "Verger: The AI Weaver"
    CSS = """
    Screen {
        layout: vertical;
    }

    #top-half {
        height: 1fr;
        min-height: 15;
        border-bottom: solid $primary;
    }

    #panes-container {
        height: 100%;
    }

    ConfigPane {
        width: 45;
        height: 100%;
        border: solid green;
        margin: 0 1;
        padding: 0;
    }

    .pane-selectors {
        height: 3;
        margin: 0;
        padding: 0;
    }

    .pane-select {
        width: 1fr;
        height: 3;
        margin: 0;
        padding: 0;
    }

    .pane-label {
        height: 1;
        margin: 0 0 0 1;
        padding: 0;
        color: $text-muted;
    }

    .pane-textarea {
        height: 1fr;
        margin: 0;
        padding: 0;
    }

    .pane-output {
        height: 1fr;
        margin: 0;
        padding: 0;
    }

    #add-pane-container {
        width: 25;
        height: 100%;
        border: dashed $success;
        align: center middle;
        margin: 0 1;
        padding: 0;
    }

    #bottom-half {
        height: auto;
        max-height: 30%;
        padding: 0 1;
    }

    .input-row {
        height: 3;
        margin: 0;
    }

    .input-label {
        width: 15;
        content-align: right middle;
        margin-right: 1;
    }

    #action-buttons {
        height: 3;
        margin: 0;
        padding: 0;
    }

    #run-btn {
        width: 1fr;
        height: 3;
        margin: 0 1 0 0;
    }

    #add-pane-btn-bottom {
        width: 20;
        height: 3;
        margin: 0;
    }

    #status-label {
        color: $text-muted;
        height: 1;
        margin: 0 0 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run_engine", "Run All"),
        ("a", "add_pane_action", "Add Pane"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = ExecutionEngine()
        self.config = get_config()
        self.pane_count = 0
        self._update_timer = None

    def compose(self) -> ComposeResult:
        yield Header()

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

        yield Footer()

    async def on_mount(self) -> None:
        """Add the first pane by default."""
        await self.add_pane()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ("add-pane-btn", "add-pane-btn-bottom"):
            await self.add_pane()
        elif event.button.id == "run-btn":
            await self.action_run_engine()

    async def action_add_pane_action(self) -> None:
        await self.add_pane()

    async def add_pane(self) -> None:
        """Dynamically add a new configuration pane."""
        self.pane_count += 1
        container = self.query_one("#panes-container", HorizontalScroll)
        add_btn_container = self.query_one("#add-pane-container")

        # Mount the new pane right before the add button
        await container.mount(ConfigPane(self.pane_count, self), before=add_btn_container)

    def schedule_variable_update(self) -> None:
        """Debounce variable updates so we don't re-render on every keystroke."""
        if self._update_timer is not None:
            self._update_timer.stop()
        self._update_timer = self.set_timer(0.5, self._extract_and_update_variables)

    async def _extract_and_update_variables(self) -> None:
        """Extracts variables from all active panes and updates the shared input list."""
        all_variables = set()
        formatter = string.Formatter()

        # Parse text from all text areas
        for text_area in self.query(TextArea):
            text = text_area.text
            if text:
                try:
                    variables = {
                        field_name
                        for _, field_name, _, _ in formatter.parse(text)
                        if field_name is not None
                    }
                    all_variables.update(variables)
                except ValueError:
                    # Ignore format string errors while typing
                    pass

        await self._render_variable_inputs(all_variables)

    async def _render_variable_inputs(self, variables: set[str]) -> None:
        """Updates the variable input widgets, preserving existing values."""
        container = self.query_one("#variable-inputs", VerticalScroll)

        # Save existing values
        existing_values = {}
        for input_widget in container.query(Input):
            if input_widget.id:
                var_name = input_widget.id.replace("var-", "")
                existing_values[var_name] = input_widget.value

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
                    Input(value=value, placeholder=f"Enter value for {var}", id=f"var-{var}"),
                    classes="input-row",
                )
            )

    async def action_run_engine(self) -> None:
        """Runs all active configurations concurrently."""
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
        tasks = []
        for pane in panes:
            tasks.append(self._run_single_pane(pane, variables))

        # Run all panes concurrently
        await asyncio.gather(*tasks)

        status_label.update("[green]All runs completed![/green]")

    async def _run_single_pane(self, pane: ConfigPane, variables: dict[str, str]) -> None:
        """Executes a single pane's configuration."""
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


def launch_tui():
    """Launch the Verger TUI. Core setup is assumed to be handled by the caller (main.py)."""
    app = VergerTUI()
    app.run()
