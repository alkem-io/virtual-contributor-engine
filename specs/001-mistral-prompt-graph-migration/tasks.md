# Tasks: Migrate to Mistral Platform and Add Prompt Graph Support

**Input**: Design documents from `/specs/001-mistral-prompt-graph-migration/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete)
**Status**: All tasks completed (retroactive documentation)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dependency and Python version updates

- [x] T001 Update `pyproject.toml`: bump python to ^3.12, version to 0.8.0
- [x] T002 [P] Add `langchain-mistralai ^1.1.0` dependency
- [x] T003 [P] Add `langgraph ^1.0.4` dependency
- [x] T004 [P] Add `json-schema-to-pydantic ^0.4.3` dependency
- [x] T005 [P] Bump `chromadb-client` from 0.6.2 to ^1.5.0
- [x] T006 Regenerate `poetry.lock`

**Checkpoint**: Dependencies resolved, project builds

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Configuration and model initialization changes that all stories depend on

- [x] T007 [US1] Update `config.py`: remove all Azure env vars, add Mistral platform and embeddings vars
- [x] T008 [US1] Update `models.py`: replace AzureChatOpenAI with ChatMistralAI for `mistral_small`
- [x] T009 [US3] Update `models.py`: replace AzureOpenAIEmbeddings with OpenAIEmbeddings for `embeddings`
- [x] T010 [US5] Update `setup_logger.py`: remove file handler and `LOCAL_PATH` dependency
- [x] T011 [US5] Update `chromadb_client.py`: switch from BasicAuth to TokenAuth

**Checkpoint**: Library initializes with new config, models load correctly

---

## Phase 3: User Story 1 - Use Mistral Platform Directly (Priority: P1)

**Goal**: Replace Azure-hosted Mistral with native Mistral SDK

- [x] T012 [US1] Update `__init__.py`: replace `mistral_medium`, `mistral_large`, `openai_embeddings` exports with `mistral_small`, `embeddings`

**Checkpoint**: Consuming services can import `mistral_small` and use it for LLM calls

---

## Phase 4: User Story 2 - Define and Execute Prompt Graphs (Priority: P1)

**Goal**: New prompt graph module for JSON-defined AI workflows

- [x] T013 [P] [US2] Create `prompt_graph/edge.py`: Edge model with from/to aliases and optional condition
- [x] T014 [P] [US2] Create `prompt_graph/json_graph_parser.py`: `_transform_schema` + `parse_json_graph` for JSON schema to Pydantic conversion
- [x] T015 [P] [US2] Create `prompt_graph/state.py`: State class with `build_state_model`, `update`, `get`
- [x] T016 [US2] Create `prompt_graph/node.py`: Node with prompt templating, output validation, execution (depends on T014)
- [x] T017 [US2] Create `prompt_graph/prompt_graph.py`: PromptGraph with `from_dict`, `validate_graph`, `compile` (depends on T013, T015, T016)
- [x] T018 [US2] Create `prompt_graph/__init__.py`: export Edge, PromptGraph, Node, State, parse_json_graph
- [x] T019 [US2] Update `__init__.py`: add `PromptGraph` and `parse_json_graph` to package exports

**Checkpoint**: PromptGraph can be instantiated from JSON and compiled into a runnable LangGraph

---

## Phase 5: User Story 3 - Generic Embeddings Provider (Priority: P2)

**Goal**: Support any OpenAI-compatible embeddings endpoint

Covered by T009 (Phase 2). No additional tasks needed.

**Checkpoint**: Embeddings work with any OpenAI-compatible endpoint

---

## Phase 6: User Story 4 - ChromaDB Utility Functions (Priority: P2)

**Goal**: Provide query, combine, and ingest utilities for ChromaDB

- [x] T020 [US4] Create `chromadb_utils.py`: `query_documents()`, `combine_query_results()`, `ingest_documents()` with graceful degradation
- [x] T021 [US4] Update `__init__.py`: add chromadb utility functions to package exports
- [x] T022 [P] [US4] Update `utils.py`: make `combine_documents` accept both Document objects and plain strings

**Checkpoint**: Documents can be ingested and queried via utility functions

---

## Phase 7: User Story 5 - Simplified Configuration and Logging (Priority: P3)

**Goal**: Clean env vars and stdout-only logging

Covered by T007, T010, T011 (Phase 2). Additional tasks:

- [x] T023 [US5] Update `events/input.py`: make `body_of_knowledge_id` optional
- [x] T024 [P] [US5] Update `utils.py`: add `history_as_conversation()` and `history_as_dict()`
- [x] T025 [US5] Update `__init__.py`: add new utility functions to package exports

**Checkpoint**: Library runs with simplified config, logs to stdout only

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (deps must be installed)
- **US1 (Phase 3)**: Depends on Phase 2 (config + models must be updated)
- **US2 (Phase 4)**: Depends on Phase 1 only (new module, no config deps)
- **US3 (Phase 5)**: Covered by Phase 2
- **US4 (Phase 6)**: Depends on Phase 2 (needs embeddings initialized)
- **US5 (Phase 7)**: Partially covered by Phase 2; remaining tasks independent

### Parallel Opportunities

- T002, T003, T004, T005 can all run in parallel (independent dependency additions)
- T013, T014, T015 can all run in parallel (independent prompt graph models)
- T020, T022, T024 can all run in parallel (independent utility additions)

---

## Notes

- All tasks marked [x] — implementation is complete
- This is a retroactive task breakdown of work done in commits `8460f9e` and `efec74b`
- Total: 25 tasks across 7 phases
