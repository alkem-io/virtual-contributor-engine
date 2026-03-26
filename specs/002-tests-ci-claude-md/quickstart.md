# Quickstart: Tests, CI, and CLAUDE.md

**Date**: 2026-03-25

## Running Tests Locally

```bash
# Install dependencies (including dev deps)
poetry install

# Run tests with coverage
poetry run pytest --cov=alkemio_virtual_contributor_engine --cov-fail-under=90

# Run tests with verbose output
poetry run pytest -v

# Run a specific test file
poetry run pytest tests/test_utils.py

# Run a specific test
poetry run pytest tests/test_utils.py::test_get_language_by_code
```

## Running Linting and Type Checking

```bash
# Lint
poetry run flake8 alkemio_virtual_contributor_engine/

# Type check
poetry run pyright alkemio_virtual_contributor_engine/
```

## CI Pipeline

The CI pipeline (`.github/workflows/ci.yml`) runs automatically on:
- Every push to any branch
- Every pull request

It executes three steps in order:
1. **Lint** — flake8
2. **Type check** — pyright
3. **Test** — pytest with 90% coverage minimum

If any step fails, the pipeline fails and the PR cannot be merged.

No secrets or external services are required — all tests use mocks.

## Writing New Tests

1. Create a test file in `tests/` mirroring the source file location
2. Use fixtures from `conftest.py` for mocked services
3. Run `poetry run pytest --cov` to verify coverage stays above 90%
4. Async tests use the `@pytest.mark.asyncio` decorator

## CLAUDE.md

The `CLAUDE.md` file at the repository root provides project context
for developers and AI assistants. Update it when:
- New commands are added
- Project structure changes
- Conventions are updated
