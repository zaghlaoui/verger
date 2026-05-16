import ast
from pathlib import Path

from verger.core.prompts.base import PromptResolver, VergerPrompt


class NativeStringPrompt(VergerPrompt):
    """A prompt defined as a string variable in a Python file."""

    def __init__(self, ref: str, text: str, file_path: Path):
        self.ref = ref
        self.text = text
        self.file_path = file_path

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> str:
        return self.ref


class NativeStringResolver(PromptResolver):
    """
    Loads prompts from Python files using AST.
    Reference format: 'module.name:VARIABLE'
    """

    def can_handle(self, ref: str) -> bool:
        # Matches 'something:VARIABLE' and doesn't look like a file path
        return ":" in ref and not ref.endswith(".j2") and not ref.endswith(".txt")

    def load(self, ref: str) -> VergerPrompt:
        module_path_str, var_name = ref.split(":", 1)

        # In a real app, you'd translate 'module.name' to a file path.
        # For now, we assume the user provides a relative path like 'src/prompts:GREETING'
        # or we use importlib to find the file.

        # Simplified: Treat module_path_str as a direct file path if it ends in .py
        file_path = Path(f"{module_path_str.replace('.', '/')}.py")

        if not file_path.exists():
            raise FileNotFoundError(f"Could not find Python file for prompt: {file_path}")

        # Use AST to extract the string without executing the file
        content = file_path.read_text()
        tree = ast.parse(content)

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == var_name:
                        if isinstance(node.value, ast.Constant) and isinstance(
                            node.value.value, str
                        ):
                            return NativeStringPrompt(ref, node.value.value, file_path)

        raise ValueError(f"Variable '{var_name}' not found or is not a string in {file_path}")


def get_resolver() -> PromptResolver:
    return NativeStringResolver()
