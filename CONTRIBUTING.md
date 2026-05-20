# Contributing to Verger

Thank you for your interest in contributing to Verger! This guide will help you get started.

## 🚀 Quick Start

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/verger.git
cd verger
```

### 2. Set Up Development Environment

**Option 1: Using Make (Recommended)**
```bash
make setup     # Installs dependencies + git hooks
```

**Option 2: Using uv directly**
```bash
uv sync --group dev
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

Git hooks will run before every commit and check:

- ✅ Code formatting (Ruff)
- ✅ Linting issues (Ruff)
- ✅ Type checking (ty)
- ✅ Spelling (codespell)
- ✅ General hygiene (whitespace, line endings, etc.)
- ✅ Commit message format (Commitizen)
- ✅ Security issues (Bandit & Detect-secrets)
- ✅ Tests (pytest - runs on push)

## 📝 Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear and structured commit history. You can use `make cz` to help you craft a compliant commit message.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `ci`: CI/CD changes
- `build`: Build system changes

### Scope (Optional)

Use scope to specify which part of the codebase is affected:
- `core`, `cli`, `tui`, `config`, `models`, `prompts`, `tests`, `docs`

### Examples

```bash
# Good commits ✅
git commit -m "feat: add support for new model provider"
git commit -m "feat(cli): implement verbose logging flag"
git commit -m "fix: resolve config loader environment variable precedence"
git commit -m "fix(tui): handle window resize events correctly"
git commit -m "docs: update architecture overview"
git commit -m "refactor(core): simplify plugin registration"
git commit -m "test(core): add unit tests for prompt registry"
git commit -m "chore: upgrade textual to v8.2.6"

# Bad commits ❌
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "Updated files"
git commit -m "Fix bug"
```

### Breaking Changes

If your change breaks backward compatibility, add `BREAKING CHANGE:` in the footer:

```bash
git commit -m "feat(core): redesign plugin interface

BREAKING CHANGE: The plugin interface now requires an 'initialize' method."
```

## 🔍 Code Quality Standards

### Before Committing

Run these commands to ensure your code meets our standards:

```bash
# Format and fix auto-fixable issues
make format

# Check for remaining issues
make lint

# Run type checking
make type-check

# Run security checks
make secure

# Run tests
make test

# Or run all checks at once
make check-all
```

### Pre-commit Hooks

The pre-commit hooks will automatically run when you commit. If they fail:

1. **Review the errors** - The hooks will show what needs to be fixed
2. **Fix the issues** - Most formatting issues are auto-fixed
3. **Stage the changes** - `git add .`
4. **Commit again** - `git commit -m "your message"`

### Bypassing Hooks (Not Recommended)

Only in emergencies:
```bash
git commit --no-verify -m "emergency fix"
```

⚠️ **Warning**: CI will still check your code, so bypassing hooks locally doesn't help!

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/core/config/test_loader.py

# Run specific test
uv run pytest tests/core/config/test_loader.py::test_loader_env_override
```

### Writing Tests

- Place tests in the `tests/` directory mirroring the `src/` structure.
- Use descriptive test names: `test_should_load_config_from_env`
- We use `pytest` and `pytest-asyncio` for testing.

## 🔒 Security

- Never commit secrets, API keys, or credentials
- Use environment variables or `.env` files (which are ignored) for sensitive data
- Run `make secure` to check for secrets and common security issues
- Report security vulnerabilities privately to the maintainers

## 📋 Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation if needed

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add amazing feature"
# or use commitizen
make cz
```

The pre-commit hooks will run automatically.

### 4. Push to Your Fork

```bash
git push origin feat/your-feature-name
```

### 5. Open a Pull Request

- Use a clear, descriptive title following Conventional Commits format
- Describe what changes you made and why
- Reference any related issues
- Ensure all CI checks pass

### PR Title Format

Your PR title must follow Conventional Commits:

```
feat: add local model adapter
fix(cli): resolve configuration path error
docs: update setup guide for windows
```

### CI Checks

Your PR must pass:
- ✅ Code formatting (Ruff)
- ✅ Linting (Ruff)
- ✅ Type checking (ty)
- ✅ Security checks (Bandit & Detect-secrets)
- ✅ Tests (pytest)
- ✅ Conventional Commits validation

## 🛠️ Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feat/my-feature

# 3. Make changes and test
make format
make test

# 4. Commit (hooks run automatically or use make cz)
make cz

# 5. Push
git push origin feat/my-feature

# 6. Open PR on GitHub
```

### Keeping Your Fork Updated

```bash
# Add upstream remote (once)
git remote add upstream https://github.com/ZAGHLAOUI/verger.git

# Update your fork
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 📚 Code Style Guidelines

### Python

- Follow PEP 8 (enforced by Ruff)
- Use type hints for all functions
- Keep functions small and focused
- Use descriptive variable names
- Avoid comments unless necessary (code should be self-documenting)

### Documentation

- Update `README.md` for user-facing changes
- Update files in `docs/` if the architecture or guides change
- Use Google-style docstrings for public APIs

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try the latest version
3. Reproduce the bug consistently

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. ...
2. ...

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.12]
- Verger version: [e.g., 0.1.0]

**Additional context**
Any other relevant information.
```

## 💡 Feature Requests

We welcome feature requests! Please:
1. Check if it's already requested
2. Describe the use case
3. Explain why it would be valuable
4. Consider contributing the implementation

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## 🎉 Recognition

Contributors will be:
- Listed in our README
- Mentioned in release notes
- Part of our growing community

Thank you for contributing to Verger! 🚀
