from verger.core.models.model_base import ModelResolver, VergerModel


def test_model_protocols():
    """Test that model protocols are runtime checkable."""

    class ValidModel:
        async def invoke(self, prompt, tools=None, **kwargs):
            return "ok"

    class ValidResolver:
        priority = 1

        def can_handle(self, obj):
            return True

        def create_adapter(self, obj):
            return ValidModel()

    assert isinstance(ValidModel(), VergerModel)
    assert isinstance(ValidResolver(), ModelResolver)
