from verger.core.tools.tool_base import ToolResolver, VergerTool


def test_tool_protocols():
    """Test that tool protocols are runtime checkable."""

    class ValidTool:
        @property
        def name(self):
            return "name"

        @property
        def description(self):
            return "desc"

        @property
        def args_schema(self):
            return {}

        async def run(self, **kwargs):
            return "ok"

    class ValidResolver:
        priority = 1

        def can_handle(self, obj):
            return True

        def create_adapter(self, obj):
            return ValidTool()

    assert isinstance(ValidTool(), VergerTool)
    assert isinstance(ValidResolver(), ToolResolver)
