.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make setup-precommit - Install git hooks"
	@echo "  make format          - Format code with ruff"
	@echo "  make lint            - Lint code with ruff"
	@echo "  make type-check      - Run ty type checker"
	@echo "  make secure          - Scan for secrets"
	@echo "  make check-all       - Run all pre-commit hooks"
	@echo "  make test            - Run all tests"
	@echo "  make cz              - Create a conventional commit"

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
	uv run detect-secrets scan

.PHONY: check-all
check-all:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest

.PHONY: setup-precommit
setup-precommit:
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@echo ""
	@echo "Git hooks reinstalled!"

.PHONY: cz
cz:
	uv run cz commit
