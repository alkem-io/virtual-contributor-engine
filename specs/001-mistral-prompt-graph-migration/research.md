# Research: Migrate to Mistral Platform and Add Prompt Graph Support

**Date**: 2026-03-25
**Status**: Complete (retroactive)

## Decision 1: Mistral SDK Choice

**Decision**: Use `langchain-mistralai` (ChatMistralAI) instead of Azure-hosted Mistral via AzureChatOpenAI.

**Rationale**: The previous approach used AzureChatOpenAI as a workaround because Azure hosts Mistral models via an OpenAI-compatible API. This created an unnecessary Azure dependency and a confusing abstraction (using an "OpenAI" class for Mistral). The native `langchain-mistralai` package provides direct Mistral platform access with proper typing and features.

**Alternatives considered**:
- Keep AzureChatOpenAI wrapper: Rejected because it ties the library to Azure infrastructure and obscures which LLM provider is actually in use.
- Use raw Mistral SDK without LangChain: Rejected because the library already depends on LangChain for prompt templates and output parsing; using the LangChain integration maintains consistency.

## Decision 2: Model Consolidation (small only)

**Decision**: Export a single `mistral_small` model instead of `mistral_medium` and `mistral_large`.

**Rationale**: The Mistral platform model naming differs from Azure deployment naming. The consuming services currently only need one model tier. Additional models can be added later if needed.

**Alternatives considered**:
- Export multiple model tiers: Rejected as premature; no consuming service currently requires multiple tiers from this library.

## Decision 3: Embeddings Provider

**Decision**: Use `langchain-openai` OpenAIEmbeddings with configurable base URL instead of AzureOpenAIEmbeddings.

**Rationale**: OpenAIEmbeddings with a custom `openai_api_base` supports any OpenAI-compatible embeddings endpoint (Mistral, local models, etc.), making the library provider-agnostic. The `check_embedding_ctx_length=False` flag is set because the provider handles chunking.

**Alternatives considered**:
- Use MistralAIEmbeddings from langchain-mistralai: Rejected because the current embeddings provider may not be Mistral; a generic OpenAI-compatible client is more flexible.

## Decision 4: Prompt Graph Architecture

**Decision**: Build a PromptGraph module that parses JSON graph definitions into LangGraph StateGraph instances.

**Rationale**: Consuming services need to define multi-step AI workflows declaratively (via JSON config from the Alkemio platform) without writing Python orchestration code. LangGraph provides the execution engine; the prompt_graph module bridges JSON config to LangGraph.

**Alternatives considered**:
- LangChain SequentialChain: Rejected because it doesn't support branching, parallel nodes, or dynamic state.
- Custom execution engine: Rejected because LangGraph already provides state management, checkpointing, and graph compilation.

## Decision 5: JSON Schema to Pydantic Conversion

**Decision**: Use `json-schema-to-pydantic` library for converting JSON output schemas and state definitions into Pydantic models at runtime.

**Rationale**: Prompt graph nodes define their output structure as JSON schema. LangChain's PydanticOutputParser requires a Pydantic model class. The `json-schema-to-pydantic` library bridges this gap with a custom `_transform_schema` preprocessing step to handle the simplified schema format used in graph configs (list-based properties, optional flag).

**Alternatives considered**:
- Manual Pydantic model construction with `create_model()`: Rejected because it requires reimplementing JSON schema type mapping.
- datamodel-code-generator: Rejected because it generates source code files rather than runtime model classes.

## Decision 6: ChromaDB Authentication

**Decision**: Switch from BasicAuthClientProvider to TokenAuthClientProvider with Authorization header.

**Rationale**: The ChromaDB deployment has been updated to use token-based authentication. The `chromadb-client` package was also bumped from 0.6.2 to ^1.5.0 to support the newer auth patterns.

## Decision 7: Logging Simplification

**Decision**: Remove file-based logging, keep only stdout JSON logging.

**Rationale**: The `LOCAL_PATH` config for file logging was a holdover from local development. In containerized deployments, stdout logging is the standard pattern (collected by container runtime or log aggregator). Removing file logging also removes the `LOCAL_PATH` env var dependency.

## Decision 8: Python Version Bump

**Decision**: Require Python ^3.12 (up from ^3.11).

**Rationale**: The `langchain-mistralai` and updated `chromadb-client` packages require Python 3.12+. All consuming services already run 3.12+.
