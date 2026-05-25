from verger.core.prompts.prompt_base import PromptResolver, VergerPrompt


def test_prompt_protocols():
    """Test that prompt protocols are runtime checkable."""

    class ValidPrompt:
        def get_messages(self):
            return []

        def get_id(self):
            return "id"

        def format(self, **kwargs):
            return []

        def get_variables(self):
            return set()

    class ValidResolver:
        priority = 1

        def can_handle(self, obj):
            return True

        def create_adapter(self, obj):
            return ValidPrompt()

    assert isinstance(ValidPrompt(), VergerPrompt)
    assert isinstance(ValidResolver(), PromptResolver)
