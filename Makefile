.DEFAULT_GOAL := help

.PHONY: help
help:
	@printf "🚀 Verger Development Tools\n\n"
	@printf "🛠️  Setup & Maintenance:\n"
	@printf "  make setup           - Install dev dependencies and configure git hooks\n"
	@printf "  make setup-precommit - Reinstall git hooks\n"
	@printf "  make dep-check       - Check for dependency issues (deptry)\n\n"
	@printf "🧹 Formatting & Linting:\n"
	@printf "  make format          - Format code and fix auto-fixable issues (ruff)\n"
	@printf "  make lint            - Check for linting issues (ruff)\n"
	@printf "  make type-check      - Run static type analysis (ty)\n"
	@printf "  make refurb          - Suggest code modernizations (refurb)\n\n"
	@printf "🧪 Testing & Quality:\n"
	@printf "  make test            - Run tests quickly without coverage\n"
	@printf "  make test-cov        - Run tests with strict coverage enforcement\n"
	@printf "  make dead-code       - Find unused code (vulture)\n"
	@printf "  make quality         - Run all quality checks at once\n"
	@printf "  make pre-commit      - Run all pre-commit hooks on all files\n\n"
	@printf "📝 Documentation:\n"
	@printf "  make doc-check       - Check docstring coverage (interrogate)\n"
	@printf "  make doc-verbose     - List all missing docstrings\n"
	@printf "  make docs-build      - Run strict documentation build (mkdocs)\n\n"
	@printf "🛡️  Security:\n"
	@printf "  make secure          - Scan for secrets and vulnerabilities\n\n"
	@printf "✍️  Git Workflow:\n"
	@printf "  make cz              - Create a conventional commit\n"

.PHONY: setup
setup:
	@printf "📦 --- Installing development dependencies ---\n"
	uv sync --group dev
	$(MAKE) setup-precommit
	@printf "✨ Setup complete!\n"

.PHONY: format
format:
	@printf "🧹 --- Formatting code (Ruff) ---\n"
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: lint
lint:
	@printf "🔍 --- Linting code (Ruff) ---\n"
	uv run ruff check .

.PHONY: type-check
type-check:
	@printf "🏷️ --- Running Type Analysis (Ty) ---\n"
	uv run ty check

.PHONY: refurb
refurb:
	@printf "🔧 --- Running Refurb (Modernization) ---\n"
	bash -c "export MYPYPATH=src && uv run refurb src/verger --python-version 3.12"

.PHONY: secure
secure:
	@printf "🔐 --- Scanning for Secrets ---\n"
	uv run detect-secrets scan
	@printf "\n🛡️ --- Scanning for Security Vulnerabilities (Bandit) ---\n"
	uv run bandit -r src -s B101 -l

.PHONY: pre-commit
pre-commit:
	@printf "🪝 --- Running All Pre-commit Hooks ---\n"
	uv run pre-commit run --all-files

.PHONY: test
test:
	@printf "🧪 --- Running Tests (Fast) ---\n"
	uv run pytest --no-cov

.PHONY: test-cov
test-cov:
	@printf "📊 --- Running Tests with Coverage (Strict) ---\n"
	uv run pytest

.PHONY: doc-check
doc-check:
	@printf "📝 --- Checking Docstring Coverage (Interrogate) ---\n"
	uv run interrogate src/verger

.PHONY: doc-verbose
doc-verbose:
	@printf "📖 --- Listing All Missing Docstrings ---\n"
	uv run interrogate -v src/verger

.PHONY: docs-build
docs-build:
	@printf "📚 --- Running Strict MkDocs Build ---\n"
	uv run mkdocs build --strict

.PHONY: dead-code
dead-code:
	@printf "💀 --- Finding Dead Code (Vulture) ---\n"
	uv run vulture src/verger

.PHONY: dep-check
dep-check:
	@printf "📦 --- Checking Dependency Health (Deptry) ---\n"
	uv run deptry .

.PHONY: quality
quality: lint type-check test-cov doc-check dead-code dep-check refurb docs-build
	@printf "🏆 All quality checks passed!\n"

.PHONY: setup-precommit
setup-precommit:
	@printf "🪝 --- Configuring git hooks ---\n"
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@printf "\n✅ Git hooks reinstalled!\n"

.PHONY: cz
cz:
	@printf "✍️ --- Creating a Conventional Commit ---\n"
	uv run cz commit
