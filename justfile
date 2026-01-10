@_default:
    just --list --unsorted

# Install development dependencies
install:
    uv sync --extra dev
    uv run pre-commit install

# Run checkers
check:
    uv run ruff check copier tests
    uv run ruff format --check copier tests
    uv run pyrefly check
    uv run pyproject-fmt --check pyproject.toml
    uv run rumdl check .

# Run formatters
format:
    uv run ruff format tests
    uv run pyproject-fmt pyproject.toml
    uv run rumdl check --fix .

# Run all tests
test:
    uv run pytest --template .

# Run integration tests only
test-integration:
    uv run pytest tests --ignore=tests/e2e --template .

# Run end-to-end tests only
test-e2e:
    uv run pytest tests/e2e --template .

# Run continuous integration (check + test)
ci:
    just check
    just test