# Research: Add Tests, CI Build, and CLAUDE.md

**Date**: 2026-03-25
**Status**: Complete

## Decision 1: Test Framework

**Decision**: pytest + pytest-asyncio + pytest-cov

**Rationale**: pytest is the de facto Python test framework and is
already referenced in the constitution. pytest-asyncio handles the
async RabbitMQ and engine code. pytest-cov integrates coverage
reporting directly into the test run with `--cov-fail-under=90`.

**Alternatives considered**:
- unittest (stdlib): Rejected — more verbose, weaker fixture model,
  no built-in async support.
- nose2: Rejected — less maintained, no significant advantage over
  pytest for this project.

## Decision 2: Mocking Strategy

**Decision**: Use `unittest.mock` (stdlib) for all external service
mocking. Patch at the module level where services are imported.

**Rationale**: The library imports external clients at module load
time (`chromadb_client`, `embeddings`, `mistral_small`). These must
be patched before the module under test imports them, or patched via
`monkeypatch` / `mock.patch` on the specific module attribute.

Key mocking targets:
- `chromadb_client` → mock ChromaDB HTTP client
- `embeddings` → mock OpenAI embeddings model
- `mistral_small` → mock Mistral LLM
- `aio_pika.connect_robust` → mock RabbitMQ connection
- `pydantic-settings` env loading → use `monkeypatch.setenv`

**Alternatives considered**:
- pytest-mock: Adds a convenience wrapper but `unittest.mock` is
  sufficient and avoids an extra dependency.
- Test containers (real services): Rejected — violates FR-002 and
  constitution (no external services in tests).

## Decision 3: Coverage Tool and Threshold

**Decision**: pytest-cov with `--cov-fail-under=90` flag.

**Rationale**: pytest-cov wraps coverage.py and integrates into the
pytest run. The `--cov-fail-under` flag makes the test command
itself fail if coverage drops below 90%, which CI can enforce
without additional scripting.

**Alternatives considered**:
- coverage.py standalone: Works but requires a separate command;
  pytest-cov is more ergonomic.
- codecov/coveralls services: Optional future addition for PR
  annotations, but not needed for enforcement.

## Decision 4: CI Platform and Configuration

**Decision**: GitHub Actions with a single workflow file
`.github/workflows/ci.yml`.

**Rationale**: The repository is on GitHub. Actions is free for
open-source, requires no external service setup, and integrates
natively with PR status checks.

Pipeline steps:
1. Checkout code
2. Set up Python 3.12
3. Install Poetry and dependencies
4. Run `flake8` (lint)
5. Run `pyright` (type check)
6. Run `pytest --cov --cov-fail-under=90` (tests + coverage)

**Alternatives considered**:
- CircleCI / Travis CI: Rejected — extra service setup, GitHub
  Actions is simpler for a GitHub-hosted repo.
- Self-hosted runners: Rejected — unnecessary complexity for a
  library with no special hardware needs.

## Decision 5: Test Directory Structure

**Decision**: Top-level `tests/` directory mirroring the package
structure, with `conftest.py` for shared fixtures.

**Rationale**: Mirrors the source layout so test files are easy to
find. A single `conftest.py` provides reusable fixtures for mocked
external services (env vars, ChromaDB, LLM, embeddings).

Subdirectories `tests/events/` and `tests/prompt_graph/` mirror
the source subpackages.

**Alternatives considered**:
- Tests inside the package (alongside source files): Rejected —
  would ship test code with the library.
- Flat test directory (no subdirs): Rejected — 17+ test files in
  one directory would be hard to navigate.

## Decision 6: CLAUDE.md Structure

**Decision**: Follow the Claude Code conventions with sections for
project overview, common commands, architecture, and coding
conventions.

**Rationale**: CLAUDE.md is read by Claude Code at conversation
start to understand project context. It should be concise,
actionable, and focused on "how to work in this repo" rather than
user-facing documentation.

Key sections:
- Project description (one paragraph)
- Common commands (poetry install, test, lint, type check)
- Architecture overview (package structure, key modules)
- Coding conventions (commit style, branch strategy, testing rules)

**Alternatives considered**:
- README.md only: Rejected — README is for users/consumers;
  CLAUDE.md is for contributors and AI assistants.
- CONTRIBUTING.md: Could coexist, but CLAUDE.md is the priority
  per the spec.
