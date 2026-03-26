# Data Model: Migrate to Mistral Platform and Add Prompt Graph Support

**Date**: 2026-03-25
**Status**: Complete (retroactive)

## New Entities

### PromptGraph

Orchestrates a directed acyclic graph of processing nodes for multi-step AI workflows.

| Field | Type | Description |
|-------|------|-------------|
| nodes | Dict[str, Node] | Graph nodes keyed by name |
| edges | List[Edge] | Directed connections between nodes |
| start_node | str | Entry point name (default: "START") |
| end_node | str | Exit point name (default: "END") |
| state_model | Type[BaseModel] | Dynamically-built Pydantic model for graph state |

**Relationships**: Contains Nodes and Edges. References a State model.

**Key behaviors**:
- `from_dict(data)`: Factory that parses JSON into a PromptGraph instance
- `validate_graph()`: Checks edge connectivity and returns errors
- `compile(llm, special_nodes)`: Produces a runnable LangGraph StateGraph

### Node

A single processing step that takes state input, runs an LLM prompt, and produces validated output.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Unique identifier |
| input_variables | List[str] | State variable names this node reads |
| prompt | str | Prompt template with `{variable}` placeholders |
| output_schema | Dict | JSON schema defining output structure |
| output_model | Type[BaseModel] | Pydantic model built from output_schema |

**Key behaviors**:
- `format_prompt(state)`: Substitutes state values into the prompt template
- `validate_output(data)`: Validates output against the output model
- `execute(state, llm_function)`: Runs the full prompt-validate cycle

### Edge

A directed connection between two nodes in the graph.

| Field | Type | Description |
|-------|------|-------------|
| from_node | str | Source node name (aliased from JSON "from") |
| to_node | str | Destination node name (aliased from JSON "to") |
| condition | Optional[str] | Optional condition for conditional routing |

### State

Dynamic Pydantic model that carries data through the graph during execution.

| Field | Type | Description |
|-------|------|-------------|
| (dynamic) | (from JSON schema) | Fields are built at runtime from the state schema |

**Key behaviors**:
- `build_state_model(schema)`: Creates a Pydantic model class from JSON schema
- `update(**kwargs)`: Returns a new state with updated fields
- `get(key, default)`: Retrieves a field value

## Modified Entities

### Env (config.py)

**Removed fields**:
- `openai_key` (AZURE_OPENAI_API_KEY)
- `openai_api_version` (OPENAI_API_VERSION)
- `openai_endpoint` (AZURE_OPENAI_ENDPOINT)
- `mistral_endpoint` (AZURE_MISTRAL_ENDPOINT)
- `mistral_key` (AZURE_MISTRAL_API_KEY)
- `mistral_model_name` (AZURE_MISTRAL_DEPLOYMENT_NAME)
- `mistral_large_model_name` (AZURE_MISTRAL_LARGE_DEPLOYMENT_NAME)
- `mistral_api_version` (AZURE_MISTRAL_API_VERSION)
- `local_path` (LOCAL_PATH)

**Added fields**:
- `embeddings_api_key` (EMBEDDINGS_API_KEY)
- `embeddings_endpoint` (EMBEDDINGS_ENDPOINT)
- `embeddings_model_name` (EMBEDDINGS_MODEL_NAME) — renamed alias from EMBEDDINGS_DEPLOYMENT_NAME
- `mistral_api_key` (MISTRAL_API_KEY)
- `mistral_small_model_name` (MISTRAL_SMALL_MODEL_NAME)

### Input (events/input.py)

**Modified field**:
- `body_of_knowledge_id`: Changed from required `str` to `Optional[str]` with default `None`

## JSON Graph Configuration Schema

The JSON structure consumed by `PromptGraph.from_dict()`:

```json
{
  "start": "START",
  "end": "END",
  "state": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "context": { "type": "string", "optional": true },
      "result": { "type": "string", "optional": true }
    }
  },
  "nodes": [
    {
      "name": "analyze",
      "input_variables": ["query", "context"],
      "prompt": "Analyze: {query}\nContext: {context}",
      "output": {
        "type": "object",
        "properties": {
          "analysis": { "type": "string" }
        }
      }
    }
  ],
  "edges": [
    { "from": "START", "to": "analyze" },
    { "from": "analyze", "to": "END" }
  ]
}
```

**Schema extensions** (handled by `_transform_schema`):
- Properties can be a list with `name` field (converted to dict)
- `optional: true` on a property converts type to `[type, "null"]`
