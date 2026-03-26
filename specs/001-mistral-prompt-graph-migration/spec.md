# Feature Specification: Migrate to Mistral Platform and Add Prompt Graph Support

**Feature Branch**: `001-mistral-prompt-graph-migration`
**Created**: 2026-03-25
**Status**: Draft
**Input**: Retroactive specification based on changes in `migrate-to-mistral-platform-and-prompt-graph` branch vs `develop`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use Mistral Platform Directly (Priority: P1)

As a consuming service developer, I want the engine library to connect to the Mistral platform directly (instead of through Azure), so that I can use Mistral models without an Azure dependency and benefit from the native Mistral SDK features.

**Why this priority**: This is the core migration. All existing consuming services rely on LLM model initialization, and switching from Azure-hosted Mistral to the native Mistral platform is a breaking change that must work before anything else.

**Independent Test**: Can be verified by initializing the library with a valid `MISTRAL_API_KEY` and `MISTRAL_SMALL_MODEL_NAME` and confirming that a Mistral model instance is returned and can process a prompt.

**Acceptance Scenarios**:

1. **Given** valid Mistral platform credentials are set in environment variables, **When** the library initializes, **Then** a working Mistral small model instance is available for use.
2. **Given** the Mistral API key is missing, **When** the library initializes, **Then** the Mistral model is set to `None` and a warning is logged (no crash).
3. **Given** a consuming service previously used Azure Mistral env vars (`AZURE_MISTRAL_*`), **When** they upgrade to this version, **Then** they MUST update to the new env vars (`MISTRAL_API_KEY`, `MISTRAL_SMALL_MODEL_NAME`).

---

### User Story 2 - Define and Execute Prompt Graphs from JSON (Priority: P1)

As a consuming service developer, I want to define multi-step AI workflows as JSON configurations and have the engine compile and execute them as LangGraph state graphs, so that I can build complex prompt chains without writing custom orchestration code.

**Why this priority**: The prompt graph system is a major new capability that enables consuming services to define sophisticated AI workflows declaratively. It is equally critical to the migration since it is the primary new feature in this release.

**Independent Test**: Can be verified by providing a JSON graph definition with nodes, edges, and state schema, compiling it with a mock or real LLM, and invoking it to confirm the output matches the expected state.

**Acceptance Scenarios**:

1. **Given** a valid JSON graph definition with nodes, edges, and state schema, **When** I call `PromptGraph.from_dict()` and then `compile()` with an LLM, **Then** a runnable LangGraph instance is returned.
2. **Given** a compiled prompt graph, **When** I invoke it with an initial state, **Then** it executes all nodes in the defined order and returns the final state with all output fields populated.
3. **Given** a graph definition with a node that has a custom "special" function (e.g., document retrieval), **When** I pass the function in the `special_nodes` parameter at compile time, **Then** that node uses the custom function instead of the standard LLM pipeline.
4. **Given** a graph definition with invalid edges (referencing non-existent nodes), **When** I call `validate_graph()`, **Then** it returns a list of specific error messages.

---

### User Story 3 - Use Generic Embeddings Provider (Priority: P2)

As a consuming service developer, I want the engine to support a generic OpenAI-compatible embeddings endpoint (instead of Azure OpenAI), so that I can use any embeddings provider that exposes an OpenAI-compatible API.

**Why this priority**: Embeddings are needed for vector search but are secondary to the core LLM migration and prompt graph functionality.

**Independent Test**: Can be verified by setting `EMBEDDINGS_API_KEY`, `EMBEDDINGS_ENDPOINT`, and `EMBEDDINGS_MODEL_NAME` and confirming that embedding and vector search operations work.

**Acceptance Scenarios**:

1. **Given** valid embeddings configuration, **When** the library initializes, **Then** an embeddings model instance is available.
2. **Given** embeddings configuration is missing, **When** the library initializes, **Then** embeddings are set to `None` and a warning is logged.
3. **Given** a working embeddings instance, **When** I call `query_documents()` with a query and collection name, **Then** it returns matching documents from ChromaDB.
4. **Given** a working embeddings instance and a list of documents, **When** I call `ingest_documents()`, **Then** documents are embedded and stored in ChromaDB in batches.

---

### User Story 4 - Query and Ingest ChromaDB Documents via Utility Functions (Priority: P2)

As a consuming service developer, I want convenient utility functions for querying and ingesting documents into ChromaDB, so that I do not need to write boilerplate embedding and collection management code in every consuming service.

**Why this priority**: These utilities reduce duplication across consuming services but depend on the embeddings provider (US3) being functional.

**Independent Test**: Can be verified by ingesting a set of test documents into a ChromaDB collection and then querying them to confirm results are returned and formatted correctly.

**Acceptance Scenarios**:

1. **Given** a ChromaDB instance and initialized embeddings, **When** I call `ingest_documents()` with a collection name and document list, **Then** existing collection data is replaced and new documents are embedded and stored.
2. **Given** documents ingested in a collection, **When** I call `query_documents()` with a search query, **Then** semantically relevant documents are returned.
3. **Given** query results, **When** I call `combine_query_results()`, **Then** documents are combined into a single formatted string with source indices.
4. **Given** ChromaDB or embeddings are not initialized, **When** I call any utility function, **Then** it logs an error and returns an empty result (no crash).

---

### User Story 5 - Simplified Configuration and Logging (Priority: P3)

As a consuming service developer, I want a cleaner environment variable configuration (no Azure-specific vars) and stdout-only logging (no file logging), so that the library is simpler to configure and fits containerized deployment patterns.

**Why this priority**: Configuration cleanup and logging simplification are housekeeping improvements that support the migration but are not independently valuable features.

**Independent Test**: Can be verified by checking that the library starts with only the new env var names and that all log output goes to stdout in JSON format.

**Acceptance Scenarios**:

1. **Given** the new env var names (`MISTRAL_API_KEY`, `EMBEDDINGS_API_KEY`, etc.), **When** the library initializes, **Then** configuration is loaded correctly.
2. **Given** old Azure env var names (`AZURE_MISTRAL_*`, `AZURE_OPENAI_*`), **When** the library initializes, **Then** they are NOT recognized (breaking change).
3. **Given** any log event, **When** it is emitted, **Then** it is written to stdout in JSON format only (no file logging).
4. **Given** the `LOCAL_PATH` env var, **When** the library initializes, **Then** it is ignored (removed from config).

---

### Edge Cases

- What happens when a prompt graph JSON has nodes with no edges connecting them? The graph validation MUST detect disconnected nodes.
- What happens when a prompt graph node's output schema is malformed JSON? The node initialization MUST raise a clear error.
- What happens when a document being ingested is missing the required `documentId` metadata field? The ingest function MUST raise a `ValueError` with a descriptive message.
- What happens when ChromaDB token auth credentials are invalid? The client initialization MUST handle the error gracefully.
- What happens when a prompt graph node references state variables that do not exist? The node execution MUST raise a `ValueError` listing the missing variables.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Library MUST use the native Mistral SDK for LLM interactions instead of Azure-hosted OpenAI-compatible endpoints.
- **FR-002**: Library MUST support a single Mistral model (`mistral_small`) configurable via `MISTRAL_API_KEY` and `MISTRAL_SMALL_MODEL_NAME` environment variables.
- **FR-003**: Library MUST remove all Azure-specific configuration (`AZURE_MISTRAL_*`, `AZURE_OPENAI_*`, `OPENAI_API_VERSION`).
- **FR-004**: Library MUST support generic OpenAI-compatible embeddings via `EMBEDDINGS_API_KEY`, `EMBEDDINGS_ENDPOINT`, and `EMBEDDINGS_MODEL_NAME`.
- **FR-005**: Library MUST provide a `PromptGraph` capability that parses JSON graph definitions into executable state graphs.
- **FR-006**: Prompt graph nodes MUST support prompt templates with variable substitution from graph state.
- **FR-007**: Prompt graph nodes MUST validate their output against a schema-derived structured model.
- **FR-008**: Prompt graph compilation MUST accept optional `special_nodes` for custom node processing functions.
- **FR-009**: Library MUST provide `query_documents()`, `combine_query_results()`, and `ingest_documents()` utility functions for vector database operations.
- **FR-010**: All external service dependencies (Mistral, embeddings, ChromaDB) MUST degrade gracefully to `None` when credentials are missing.
- **FR-011**: Library MUST use token-based authentication for the vector database instead of basic authentication.
- **FR-012**: Library MUST log only to stdout (no file-based logging).
- **FR-013**: Library MUST require Python 3.12 or higher.
- **FR-014**: The `body_of_knowledge_id` field in input events MUST be optional.
- **FR-015**: Library MUST provide `history_as_conversation()` and `history_as_dict()` utility functions for message history formatting.

### Key Entities

- **PromptGraph**: A directed graph of processing nodes connected by edges, with a typed state model. Created from JSON, compiled with an LLM into a runnable graph instance.
- **Node**: A single processing step in the graph. Has a name, input variables, prompt template, and output schema. Can be an LLM node or a special-function node.
- **Edge**: A directed connection between two nodes (including START and END virtual nodes). Supports optional conditions.
- **State**: A dynamically-generated typed model that carries data through the graph as nodes read and write fields.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Consuming services can initialize an LLM model using only Mistral platform credentials (no Azure dependency required).
- **SC-002**: A multi-step AI workflow defined as JSON can be compiled and executed end-to-end, producing validated structured output.
- **SC-003**: Documents can be ingested into and queried from a vector database using the library's utility functions without writing any embedding logic in consuming services.
- **SC-004**: The library initializes successfully when only a subset of external service credentials are provided, with clear warning logs for unavailable services.
- **SC-005**: All consuming services can migrate by updating environment variable names and dependency version, with no code changes beyond import names. See the [migration guide](./quickstart.md) for step-by-step instructions.

## Assumptions

- Consuming services have access to the Mistral platform API (not only Azure-hosted Mistral).
- The vector database deployment supports token-based authentication (replacing basic auth).
- All consuming services run Python 3.12 or higher.
- The `mistral_medium` and `mistral_large` model exports are replaced by `mistral_small`. Consuming services must update their imports per the [migration guide](./quickstart.md).
- Consuming services that used `openai_embeddings` will migrate to the new `embeddings` export name.
- This is a breaking change release (0.7.0 to 0.8.0) and consuming services accept the migration cost.
