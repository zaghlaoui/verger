"""Widget for a single message block in the TUI."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Select, TextArea

from verger.core.schema import MessageRole


class MessageBlock(Vertical):
    """
    A widget representing a single message in a conversation.
    Includes a role selector, content editor, and a delete button.
    """

    DEFAULT_CSS = """
    MessageBlock {
        height: auto;
        border: solid $accent;
        margin: 1 0;
        padding: 0;
    }

    .message-header {
        height: 3;
        background: $boost;
        padding: 0 1;
    }

    .role-select {
        width: 1fr;
    }

    .delete-btn {
        width: 4;
        min-width: 4;
        margin-left: 1;
    }

    .message-content {
        height: 5;
        min-height: 3;
    }
    """

    def __init__(self, role: MessageRole = MessageRole.USER, content: str = "", **kwargs):
        super().__init__(**kwargs)
        self.initial_role = role
        self.initial_content = content

    def compose(self) -> ComposeResult:
        """Build the message block UI."""
        roles = [(role.value.upper(), role.value) for role in MessageRole]

        with Horizontal(classes="message-header"):
            yield Select(roles, value=self.initial_role, classes="role-select", allow_blank=False)
            yield Button("X", variant="error", classes="delete-btn", id="delete-msg-btn")

        yield TextArea(self.initial_content, classes="message-content")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle deletion of this message block."""
        if event.button.id == "delete-msg-btn":
            self.remove()

    def get_message_data(self) -> dict:
        """Extract the current role and content from the widgets."""
        role = self.query_one(Select).value
        content = self.query_one(TextArea).text
        return {"role": role, "content": content}
