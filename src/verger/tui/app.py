from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, ListItem, ListView

from verger.core.config.loader import get_config
from verger.core.prompts.registry import registry as prompt_registry


class VergerTUI(App):
    """A simple TUI to display loaded prompts."""

    TITLE = "Verger TUI"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(id="prompt-list")
        yield Footer()

    def on_mount(self) -> None:
        """Populate the list with prompts from the configuration."""
        config = get_config()
        list_view = self.query_one("#prompt-list", ListView)

        if not config.prompts:
            list_view.append(ListItem(Label("No prompts configured in pyproject.toml")))
            return

        for name, ref in config.prompts.items():
            try:
                # Attempt to resolve the prompt to show its current value
                prompt = prompt_registry.resolve(ref)
                content = prompt.get_text()
                # Truncate content for the list view
                preview = (content[:50] + "..") if len(content) > 50 else content
                label = f"[b]{name}[/b] ({ref})\n[i]{preview}[/i]"
            except Exception as e:
                label = f"[b]{name}[/b] ({ref})\n[red]Error: {e}[/red]"

            list_view.append(ListItem(Label(label)))


def launch_tui():
    """Entry point to launch the TUI."""
    app = VergerTUI()
    app.run()
