<!--
Sync Impact Report
===================
- Version change: 1.0.0 → 1.1.0 (MINOR: materially expanded testing guidance)
- Modified sections:
  - Development Workflow > Testing: replaced placeholder guidance with
    mandatory pytest, 90% coverage threshold, and no-external-services rule
- Added sections: none
- Removed sections: none
- Templates requiring updates:
  - `.specify/templates/plan-template.md` — ✅ no updates needed
  - `.specify/templates/spec-template.md` — ✅ no updates needed
  - `.specify/templates/tasks-template.md` — ✅ no updates needed
- Follow-up TODOs: none
-->

# Alkemio Virtual Contributor Engine Constitution

## Core Principles

### I. Async-First Event-Driven Architecture

All message processing MUST use async/await patterns with
`aio-pika` for RabbitMQ communication. Message handlers
registered with the engine MUST be async callables. The engine
owns the connection lifecycle (connect, consume, publish) and
consumers MUST NOT manage RabbitMQ channels directly.

Rationale: The library is the messaging backbone for Alkemio's
AI services. Blocking calls would stall the event loop and
prevent concurrent message processing.

### II. Graceful Degradation

Every external dependency (Mistral API, OpenAI API, ChromaDB,
embeddings endpoint) MUST be initialized with fallback to
`None` when credentials or endpoints are missing. Callers MUST
be able to use a subset of the library's capabilities without
configuring every service. A warning log MUST be emitted for
each unavailable dependency at startup.

Rationale: Different consuming services need different subsets
of functionality. Forcing all credentials would block
deployment of services that only need, e.g., the prompt graph
without vector search.

### III. Configuration-Driven Design

All runtime configuration MUST flow through `pydantic-settings`
environment variables (with `.env` file support). Prompt
workflows MUST be defined as JSON graph configurations and
parsed into validated Pydantic models at runtime. No hardcoded
model names, endpoints, or queue names are permitted in library
code.

Rationale: As an internal infrastructure library consumed by
multiple services, configuration MUST be externalised so each
consumer can independently set its own model, queue, and
endpoint parameters.

### IV. Minimal Public API Surface

The package `__init__.py` MUST explicitly export only the types
and functions that consuming services need. Internal helpers,
parsers, and implementation details MUST NOT appear in the
public API. New public exports require deliberate review.

Rationale: Keeping the API surface small reduces coupling with
consuming services and makes version upgrades safer.

### V. Observability

All log output MUST use the structured JSON logger configured
in `setup_logger.py`. Log level MUST be controllable via the
`LOG_LEVEL` environment variable. Key lifecycle events (engine
start, message received, handler invoked, result published,
errors) MUST be logged at appropriate levels.

Rationale: In a distributed message-driven system, structured
logs are the primary debugging tool. Consistent JSON format
enables aggregation in centralised logging platforms.

## Technology Stack & Constraints

- **Language**: Python ^3.12, managed with Poetry
- **Messaging**: RabbitMQ via `aio-pika` (async AMQP)
- **Vector DB**: ChromaDB (HTTP client mode)
- **LLM providers**: Mistral (primary), OpenAI (secondary)
- **Orchestration**: LangChain + LangGraph for prompt graphs
- **Validation**: Pydantic v2 for all data models and config
- **License**: EUPL
- **Package type**: Library (not a standalone service). No
  Dockerfile or deployment config is included; consuming
  services provide their own.
- New direct dependencies MUST be justified and MUST NOT
  duplicate functionality already available through LangChain
  or existing deps.

## Development Workflow

- **Branch strategy**: Feature branches off `develop`, merged
  via pull request.
- **Linting**: `flake8` MUST pass with no errors before merge.
- **Type checking**: `pyright` MUST pass with no errors before
  merge.
- **Versioning**: MAJOR.MINOR.PATCH (semver). MAJOR for
  breaking API changes, MINOR for new features or modules,
  PATCH for bug fixes. Version is set in `pyproject.toml`.
- **Commit messages**: Use conventional commit prefixes
  (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
- **Testing**: Tests MUST use `pytest` with `pytest-asyncio` for
  async support. Code coverage MUST be at least 90% and is
  enforced in CI. Tests MUST NOT require external services or
  real API keys.

## Governance

This constitution defines the non-negotiable principles for the
Alkemio Virtual Contributor Engine library. All pull requests
and code reviews MUST verify compliance with these principles.

**Amendment procedure**:

1. Propose a change via pull request modifying this file.
2. Document the rationale for the change in the PR description.
3. At least one maintainer MUST approve the amendment.
4. Update the version footer according to semver rules
   (MAJOR for principle removals/redefinitions, MINOR for new
   principles or material expansions, PATCH for clarifications).

**Version**: 1.1.0 | **Ratified**: 2026-03-25 | **Last Amended**: 2026-03-25
