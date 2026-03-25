# Migration Guide: v0.7.0 to v0.8.0

**Date**: 2026-03-25

## Overview

Version 0.8.0 migrates from Azure-hosted Mistral/OpenAI to the native Mistral platform and adds prompt graph support. This is a **breaking change** release.

## Prerequisites

- Python 3.12+ (bumped from 3.11)
- Mistral platform API key (replaces Azure Mistral credentials)
- OpenAI-compatible embeddings endpoint (replaces Azure OpenAI)
- ChromaDB with token-based authentication (replaces basic auth)

## Step 1: Update Dependencies

```bash
# In your consuming service
poetry add alkemio-virtual-contributor-engine@^0.8.0
```

## Step 2: Update Environment Variables

### Removed Variables (delete these)

```bash
# Azure Mistral (all removed)
AZURE_MISTRAL_ENDPOINT
AZURE_MISTRAL_API_KEY
AZURE_MISTRAL_DEPLOYMENT_NAME
AZURE_MISTRAL_LARGE_DEPLOYMENT_NAME
AZURE_MISTRAL_API_VERSION

# Azure OpenAI (all removed)
AZURE_OPENAI_API_KEY
AZURE_OPENAI_ENDPOINT
OPENAI_API_VERSION
EMBEDDINGS_DEPLOYMENT_NAME

# Other removed
LOCAL_PATH
```

### New Variables (add these)

```bash
# Mistral platform
MISTRAL_API_KEY=your-mistral-platform-key
MISTRAL_SMALL_MODEL_NAME=mistral-small-latest

# Embeddings (any OpenAI-compatible endpoint)
EMBEDDINGS_API_KEY=your-embeddings-key
EMBEDDINGS_ENDPOINT=https://your-embeddings-endpoint
EMBEDDINGS_MODEL_NAME=your-embedding-model

# Unchanged
RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, etc.
VECTOR_DB_HOST, VECTOR_DB_PORT, VECTOR_DB_CREDENTIALS
LOG_LEVEL
```

## Step 3: Update Imports

```python
# Before (v0.7.0)
from alkemio_virtual_contributor_engine import (
    mistral_medium,
    mistral_large,
    openai_embeddings,
)

# After (v0.8.0)
from alkemio_virtual_contributor_engine import (
    mistral_small,
    embeddings,
)
```

### New Exports Available

```python
from alkemio_virtual_contributor_engine import (
    # Prompt graph
    PromptGraph,
    parse_json_graph,

    # ChromaDB utilities
    query_documents,
    combine_query_results,
    ingest_documents,

    # History formatters
    history_as_conversation,
    history_as_dict,
)
```

## Step 4: Update ChromaDB Credentials

ChromaDB now uses token-based auth instead of basic auth. Ensure your `VECTOR_DB_CREDENTIALS` value is a valid token (not a username:password pair).

## Step 5: Using the Prompt Graph (New Feature)

```python
from alkemio_virtual_contributor_engine import PromptGraph, mistral_small

# Define a graph as JSON (typically from Alkemio platform config)
graph_config = {
    "start": "START",
    "end": "END",
    "state": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "result": {"type": "string", "optional": True}
        }
    },
    "nodes": [
        {
            "name": "respond",
            "input_variables": ["query"],
            "prompt": "Answer this: {query}",
            "output": {
                "type": "object",
                "properties": {
                    "result": {"type": "string"}
                }
            }
        }
    ],
    "edges": [
        {"from": "START", "to": "respond"},
        {"from": "respond", "to": "END"}
    ]
}

# Parse, compile, and execute
graph = PromptGraph.from_dict(graph_config)
compiled = graph.compile(llm=mistral_small)
result = compiled.invoke({"query": "What is Alkemio?"})
```

## Step 6: Using ChromaDB Utilities (New Feature)

```python
from alkemio_virtual_contributor_engine import (
    query_documents,
    combine_query_results,
    ingest_documents,
)
from langchain_core.documents import Document

# Ingest documents
docs = [
    Document(
        page_content="Some text",
        metadata={"documentId": "doc-1"}
    )
]
ingest_documents("my-collection", docs)

# Query documents
results = query_documents("search query", "my-collection", num_docs=4)
combined = combine_query_results(results)
```

## Breaking Wire-Format Changes

- **`bodyOfKnowledgeID` is now optional** in the `Input` event model. It defaults to `None` when not present in the incoming message. If your consuming service assumes `input.body_of_knowledge_id` is always a `str`, add a `None` check before using it.

## Removed Functionality

- File-based logging (`app.log`) — all output now goes to stdout only
- `LOCAL_PATH` configuration
- `mistral_medium` and `mistral_large` model exports
- `openai_embeddings` export (replaced by `embeddings`)
- All Azure-specific configuration
