# Implementation Plan: Add Tests, CI Build, and CLAUDE.md

**Branch**: `002-tests-ci-claude-md` | **Date**: 2026-03-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-tests-ci-claude-md/spec.md`

## Summary

Add a pytest-based test suite achieving 90%+ code coverage across the
entire library, with all external services mocked. Configure a GitHub
Actions CI pipeline that runs linting (flake8), type checking (pyright),
and tests with coverage enforcement on every push and PR. Create a
CLAUDE.md file documenting project conventions for developer onboarding
and AI-assisted development.

## Technical Context

**Language/Version**: Python ^3.12, managed with Poetry
**Primary Dependencies**: pytest, pytest-asyncio, pytest-cov, unittest.mock (stdlib)
**Storage**: N/A
**Testing**: pytest + pytest-asyncio + pytest-cov (90% minimum coverage)
**Target Platform**: GitHub Actions (CI), Linux/macOS (local dev)
**Project Type**: Library (internal infrastructure)
**Performance Goals**: Test suite completes in under 60 seconds
**Constraints**: No external services or API keys required for tests
**Scale/Scope**: ~21 Python source files to cover across 4 packages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Async-First | PASS | Tests for async code use pytest-asyncio; no blocking patterns introduced |
| II. Graceful Degradation | PASS | Tests verify degradation behavior (None fallbacks) by mocking missing deps |
| III. Configuration-Driven | PASS | Test config uses env var overrides; no hardcoded values |
| IV. Minimal Public API | PASS | Tests are not part of the public API; no new exports |
| V. Observability | PASS | No changes to logging; tests verify log output where relevant |
| Testing (Dev Workflow) | PASS | pytest + pytest-asyncio, 90% coverage enforced in CI, no external services |

## Project Structure

### Documentation (this feature)

```text
specs/002-tests-ci-claude-md/
├── plan.md              # This file
├── research.md          # Technology decisions
├── quickstart.md        # How to run tests and CI
└── tasks.md             # Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
tests/
├── conftest.py              # Shared fixtures (mock env, mock LLM, mock chromadb)
├── test_config.py           # Env config loading and validation
├── test_models.py           # LLM and embeddings initialization with mocks
├── test_utils.py            # Utility functions (history, documents, tags)
├── test_chromadb_client.py  # ChromaDB client initialization
├── test_chromadb_utils.py   # Query, combine, ingest utilities
├── test_setup_logger.py     # Logger configuration
├── test_rabbitmq.py         # RabbitMQ client (async)
├── test_alkemio_vc_engine.py # Main engine (async)
├── events/
│   ├── test_input.py        # Input event parsing
│   ├── test_response.py     # Response event structure
│   ├── test_ingest.py       # Ingest website events
│   └── test_base.py         # Base model alias support
└── prompt_graph/
    ├── test_edge.py          # Edge model
    ├── test_node.py          # Node prompt formatting + output validation
    ├── test_state.py         # State model building
    ├── test_json_graph_parser.py  # Schema transform + parsing
    └── test_prompt_graph.py  # Graph construction, validation, compilation

.github/
└── workflows/
    └── ci.yml               # GitHub Actions CI pipeline

CLAUDE.md                    # Developer guide
pyproject.toml               # Updated: dev deps (pytest, pytest-asyncio, pytest-cov)
```

**Structure Decision**: Tests mirror the source package structure in a
top-level `tests/` directory. Each source module gets a corresponding
test file. The `conftest.py` provides shared fixtures for mocking
external services.

## Complexity Tracking

No constitution violations. No complexity justification needed.
