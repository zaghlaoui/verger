.DEFAULT_GOAL := help

.PHONY: help
help:
	@printf "🚀 Available commands:\n"
	@printf "  make setup           - 🛠️  Install dev dependencies and configure git hooks\n"
	@printf "  make setup-precommit - 🪝  Install git hooks\n"
	@printf "  make format          - 🧹  Format code with ruff\n"
	@printf "  make lint            - 🔍  Lint code with ruff\n"
	@printf "  make type-check      - 🏷️  Run ty type checker\n"
	@printf "  make secure          - 🛡️  Scan for secrets\n"
	@printf "  make check-all       - ✅  Run all pre-commit hooks\n"
	@printf "  make test            - 🧪  Run all tests\n"
	@printf "  make test-cov        - 📊  Run tests with coverage report\n"
	@printf "  make doc-check       - 📝  Check docstring coverage (interrogate)\n"
	@printf "  make doc-verbose     - 📖  List all missing docstrings (interrogate -v)\n"
	@printf "  make dead-code       - 💀  Find unused code (vulture)\n"
	@printf "  make dep-check       - 📦  Check for dependency issues (deptry)\n"
	@printf "  make quality         - 🏆  Run all quality checks at once\n"
	@printf "  make cz              - ✍️  Create a conventional commit\n"

.PHONY: setup
setup:
	@printf "📦 Installing development dependencies...\n"
	uv sync --group dev
	$(MAKE) setup-precommit
	@printf "✨ Setup complete!\n"

.PHONY: format
format:
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: type-check
type-check:
	uv run ty check

.PHONY: secure
secure:
	@printf "🔐 --- Scanning for Secrets ---\n"
	uv run detect-secrets scan
	@printf "\n🛡️ --- Scanning for Security Vulnerabilities (Bandit) ---\n"
	uv run bandit -r src -s B101 -l

.PHONY: check-all
check-all:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest

.PHONY: test-cov
test-cov:
	uv run pytest --cov=src/verger --cov-report=term-missing

.PHONY: doc-check
doc-check:
	uv run interrogate src/verger

.PHONY: doc-verbose
doc-verbose:
	uv run interrogate -v src/verger

.PHONY: dead-code
dead-code:
	uv run vulture src/verger

.PHONY: dep-check
dep-check:
	uv run deptry .

.PHONY: quality
quality: lint type-check test-cov doc-check dead-code dep-check
	@printf "✨ All quality checks passed!\n"

.PHONY: setup-precommit
setup-precommit:
	@printf "🔧 Configuring git hooks...\n"
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@printf "\n✅ Git hooks reinstalled!\n"

.PHONY: cz
cz:
	uv run cz commit
