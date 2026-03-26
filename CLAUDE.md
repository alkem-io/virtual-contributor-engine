# Alkemio Virtual Contributor Engine

Internal Python library for Alkemio's AI infrastructure. Handles RabbitMQ message processing, LLM/embeddings model initialization, ChromaDB vector operations, and JSON-configured LangGraph prompt workflows.

## Setup

```bash
poetry install
```

## Commands

```bash
# Run tests with coverage (90% minimum enforced)
poetry run pytest --cov=alkemio_virtual_contributor_engine --cov-fail-under=90 -v

# Lint
poetry run flake8 alkemio_virtual_contributor_engine/

# Type check
poetry run pyright alkemio_virtual_contributor_engine/
```

## Architecture

```
alkemio_virtual_contributor_engine/
├── alkemio_vc_engine.py     # Main engine: RabbitMQ message loop + handler dispatch
├── config.py                # Pydantic-settings env var config
├── models.py                # LLM (Mistral) and embeddings initialization
├── rabbitmq.py              # Async RabbitMQ client (aio-pika)
├── chromadb_client.py       # ChromaDB HTTP client setup
├── chromadb_utils.py        # Document query/ingest utilities
├── setup_logger.py          # JSON structured logger (stdout only)
├── utils.py                 # Text/history formatting helpers
├── events/                  # Pydantic models for message events
│   ├── input.py             # Input query event
│   ├── response.py          # LLM response event
│   ├── ingest_website.py    # Website ingestion event
│   └── ingest_website_result.py
└── prompt_graph/            # JSON-to-LangGraph workflow engine
    ├── prompt_graph.py      # Graph orchestrator (from_dict → compile → invoke)
    ├── node.py              # Processing node with prompt template + output schema
    ├── edge.py              # Directed edge between nodes
    ├── state.py             # Dynamic state model builder
    └── json_graph_parser.py # JSON schema → Pydantic model converter
```

## Key Patterns

- **Async-first**: RabbitMQ and engine use async/await via aio-pika
- **Graceful degradation**: All external deps (Mistral, embeddings, ChromaDB) fall back to None when unconfigured
- **Config via env vars**: All config through pydantic-settings; no hardcoded values
- **Explicit public API**: Only types/functions in `__init__.py __all__` are public

## Conventions

- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`)
- **Branches**: Feature branches off `develop`, merged via PR
- **Testing**: pytest + pytest-asyncio, 90% coverage minimum, no external services or API keys needed
- **Versioning**: Semver in `pyproject.toml` (MAJOR.MINOR.PATCH)
- **Linting**: flake8 must pass, pyright must pass
