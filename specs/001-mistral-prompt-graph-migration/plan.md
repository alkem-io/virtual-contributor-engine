# Implementation Plan: Migrate to Mistral Platform and Add Prompt Graph Support

**Branch**: `migrate-to-mistral-platform-and-prompt-graph` | **Date**: 2026-03-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mistral-prompt-graph-migration/spec.md`

**Note**: This is a retroactive plan documenting an already-completed implementation.

## Summary

Migrate the library from Azure-hosted Mistral/OpenAI services to the native Mistral platform SDK and generic OpenAI-compatible embeddings. Add a new prompt graph module that compiles JSON workflow definitions into executable LangGraph state graphs. Provide ChromaDB utility functions and simplify configuration by removing all Azure-specific env vars.

## Technical Context

**Language/Version**: Python ^3.12, managed with Poetry
**Primary Dependencies**: langchain ^1.1.0, langchain-mistralai ^1.1.0, langchain-openai ^1.1.0, langgraph ^1.0.4, json-schema-to-pydantic ^0.4.3, aio-pika 9.5.7, chromadb-client ^1.5.0, pydantic-settings ^2.11.0
**Storage**: ChromaDB (HTTP client mode, token-based auth)
**Testing**: No test suite (flake8 + pyright for static analysis)
**Target Platform**: Linux server (containerized), consumed as a Python library
**Project Type**: Library (internal infrastructure)
**Performance Goals**: N/A (library; performance bound by LLM API latency)
**Constraints**: Must maintain graceful degradation for all external services
**Scale/Scope**: ~21 Python source files, consumed by multiple Alkemio AI services

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Async-First Event-Driven | PASS | RabbitMQ layer unchanged, remains async via aio-pika |
| II. Graceful Degradation | PASS | All new model init (mistral_small, embeddings) falls back to None with warning logs |
| III. Configuration-Driven | PASS | All new config via pydantic-settings env vars; prompt graphs defined as JSON |
| IV. Minimal Public API | PASS | New exports (PromptGraph, parse_json_graph, chromadb utils) explicitly listed in `__all__` |
| V. Observability | PASS | Structured JSON logging preserved; file handler removed (stdout only fits containers) |

## Project Structure

### Documentation (this feature)

```text
specs/001-mistral-prompt-graph-migration/
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Migration guide
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
alkemio_virtual_contributor_engine/
├── __init__.py              # Public API exports (updated)
├── alkemio_vc_engine.py     # Main engine (unchanged)
├── chromadb_client.py       # ChromaDB connection (updated: token auth)
├── chromadb_utils.py        # NEW: query/combine/ingest utilities
├── config.py                # Env config (updated: Mistral platform + embeddings)
├── models.py                # LLM/embeddings init (updated: Mistral SDK + OpenAI embeddings)
├── rabbitmq.py              # RabbitMQ client (unchanged)
├── setup_logger.py          # Logger (updated: removed file handler)
├── utils.py                 # Helpers (updated: new history formatters)
├── events/
│   ├── __init__.py
│   ├── base.py
│   ├── input.py             # Updated: body_of_knowledge_id optional
│   ├── response.py
│   ├── ingest_website.py
│   └── ingest_website_result.py
└── prompt_graph/            # NEW: entire module
    ├── __init__.py
    ├── prompt_graph.py      # PromptGraph orchestrator
    ├── node.py              # Node with prompt template + output schema
    ├── edge.py              # Directed edge between nodes
    ├── state.py             # Dynamic state model builder
    └── json_graph_parser.py # JSON schema to Pydantic converter
```

**Structure Decision**: Single package layout. The prompt_graph subpackage is the only new directory. All other changes are modifications to existing files.

## Complexity Tracking

No constitution violations. No complexity justification needed.
