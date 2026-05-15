.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make format        - Format code with ruff"
	@echo "  make lint          - Lint code with ruff"

.PHONY: format
format:
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: lint
lint:
	uv run ruff check .

