import os

import pytest


@pytest.fixture
def mock_user_project(tmp_path):
    """
    Fixture to create a temporary 'user project' directory.
    This is used across core tests to simulate user environment.
    """
    project_dir = tmp_path / "user_ai_app"
    project_dir.mkdir()

    # 1. Create a verger.toml
    verger_content = """
env_file = ".env.test"

[prompts]
system = "prompts:SYSTEM_PROMPT"
user = "prompts:USER_PROMPT"

[models]
simple = "models:my_model"
"""
    (project_dir / "verger.toml").write_text(verger_content)

    # 2. Create a prompts.py file
    prompts_content = """
SYSTEM_PROMPT = "You are a helpful assistant."
USER_PROMPT = "Explain quantum physics."
"""
    (project_dir / "prompts.py").write_text(prompts_content)

    # 3. Create an .env.test file
    env_content = "OPENAI_API_KEY=sk-test-key"
    (project_dir / ".env.test").write_text(env_content)

    # Save current CWD and switch to the mock project
    old_cwd = os.getcwd()
    os.chdir(project_dir)

    yield project_dir

    # Cleanup: restore CWD
    os.chdir(old_cwd)
