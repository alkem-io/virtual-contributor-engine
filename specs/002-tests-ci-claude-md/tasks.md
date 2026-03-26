# Tasks: Add Tests, CI Build, and CLAUDE.md

**Input**: Design documents from `/specs/002-tests-ci-claude-md/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete)

**Tests**: Yes — this feature IS the test suite. All test tasks are implementation tasks.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Add test dependencies and create test directory structure

- [x] T001 Add `pytest`, `pytest-asyncio`, and `pytest-cov` to dev dependencies in `pyproject.toml`
- [x] T002 Create test directory structure: `tests/`, `tests/events/`, `tests/prompt_graph/`
- [x] T003 Create shared test fixtures in `tests/conftest.py` (mock env vars, mock chromadb_client, mock embeddings, mock mistral_small, mock aio-pika connection)

**Checkpoint**: `poetry install` succeeds, `poetry run pytest` runs with no tests collected

---

## Phase 2: User Story 1 - Automated Test Suite (Priority: P1)

**Goal**: Achieve 90%+ code coverage across all library source files

**Independent Test**: Run `poetry run pytest --cov=alkemio_virtual_contributor_engine --cov-fail-under=90` and confirm all tests pass with coverage >= 90%

### Core module tests

- [x] T004 [P] [US1] Write tests for config loading and validation in `tests/test_config.py` — test env var loading, defaults, optional fields, type validation
- [x] T005 [P] [US1] Write tests for model initialization in `tests/test_models.py` — test mistral_small and embeddings init with mocked deps, test graceful degradation to None
- [x] T006 [P] [US1] Write tests for utility functions in `tests/test_utils.py` — test get_language_by_code, combine_documents (strings and Document objects), clear_tags, entry_as_string, history_as_text, history_as_conversation, history_as_dict
- [x] T007 [P] [US1] Write tests for ChromaDB client initialization in `tests/test_chromadb_client.py` — test client creation with valid creds, test None when creds missing
- [x] T008 [P] [US1] Write tests for ChromaDB utilities in `tests/test_chromadb_utils.py` — test query_documents, combine_query_results, ingest_documents, test RuntimeError on missing infra, test empty results handling
- [x] T009 [P] [US1] Write tests for logger setup in `tests/test_setup_logger.py` — test JSON format, log level from env, stdout handler only

### Event model tests

- [x] T010 [P] [US1] Write tests for base model in `tests/events/test_base.py` — test alias support and serialization
- [x] T011 [P] [US1] Write tests for Input event in `tests/events/test_input.py` — test parsing with all fields, optional body_of_knowledge_id, history items, prompt_graph field
- [x] T012 [P] [US1] Write tests for Response event in `tests/events/test_response.py` — test serialization and field validation
- [x] T013 [P] [US1] Write tests for ingest events in `tests/events/test_ingest.py` — test IngestWebsite and IngestionResult models

### Prompt graph tests

- [x] T014 [P] [US1] Write tests for Edge model in `tests/prompt_graph/test_edge.py` — test from/to alias, repr
- [x] T015 [P] [US1] Write tests for json_graph_parser in `tests/prompt_graph/test_json_graph_parser.py` — test _transform_schema (list-to-dict properties, optional flag, array items), test parse_json_graph produces valid Pydantic model
- [x] T016 [P] [US1] Write tests for State in `tests/prompt_graph/test_state.py` — test build_state_model creates correct Pydantic model from JSON schema
- [x] T017 [P] [US1] Write tests for Node in `tests/prompt_graph/test_node.py` — test output model building, format_prompt with state, validate_output, missing variable errors
- [x] T018 [P] [US1] Write tests for PromptGraph in `tests/prompt_graph/test_prompt_graph.py` — test from_dict parsing, validate_graph (valid and invalid graphs), compile with mocked LLM and special_nodes

### Async module tests

- [x] T019 [US1] Write tests for RabbitMQ client in `tests/test_rabbitmq.py` — test connect, consume, publish with mocked aio-pika (async tests)
- [x] T020 [US1] Write tests for AlkemioVirtualContributorEngine in `tests/test_alkemio_vc_engine.py` — test handler registration, message routing, invoke_handler with mocked RabbitMQ (async tests)

### Coverage verification

- [x] T021 [US1] Run full test suite with coverage and verify 90%+ threshold: `poetry run pytest --cov=alkemio_virtual_contributor_engine --cov-fail-under=90 -v`

**Checkpoint**: All tests pass, coverage >= 90%, no external services needed

---

## Phase 3: User Story 2 - CI Pipeline (Priority: P1)

**Goal**: Automated CI that runs lint, type check, and tests on every push/PR

**Independent Test**: Push a commit and verify the GitHub Actions pipeline triggers and completes with lint, type check, and test steps

- [x] T022 [US2] Create GitHub Actions workflow in `.github/workflows/ci.yml` — checkout, setup Python 3.12, install Poetry + deps, run flake8, run pyright, run pytest with --cov-fail-under=90. Trigger on push and pull_request.
- [x] T023 [US2] Verify CI pipeline runs locally by simulating steps: `poetry run flake8 alkemio_virtual_contributor_engine/` and `poetry run pyright alkemio_virtual_contributor_engine/` and `poetry run pytest --cov=alkemio_virtual_contributor_engine --cov-fail-under=90`

**Checkpoint**: CI pipeline config exists, all steps pass locally

---

## Phase 4: User Story 3 - CLAUDE.md (Priority: P2)

**Goal**: Developer guide for onboarding and AI-assisted development

**Independent Test**: Read CLAUDE.md and confirm it covers project description, setup, commands, architecture, and conventions

- [x] T024 [US3] Write CLAUDE.md at repository root with sections: project description, setup instructions (`poetry install`), common commands (test, lint, type check), architecture overview (package structure, key modules, message flow), coding conventions (conventional commits, branch strategy, testing rules with 90% coverage)

**Checkpoint**: CLAUDE.md accurately reflects current project state

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T025 Fix any flake8 or pyright errors in test files
- [x] T026 Run full validation: lint + type check + tests + coverage in sequence
- [x] T027 Verify tests pass without any `.env` file present

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **US1 Tests (Phase 2)**: Depends on Phase 1 (conftest.py and deps)
- **US2 CI (Phase 3)**: Depends on Phase 2 (needs tests to exist)
- **US3 CLAUDE.md (Phase 4)**: Depends on Phase 2 and 3 (references test/CI commands)
- **Polish (Phase 5)**: Depends on all previous phases

### Parallel Opportunities

- T004–T018 can ALL run in parallel (independent test files, different source modules)
- T019 and T020 are sequential (async tests may share fixtures)
- T022 and T024 could run in parallel if Phase 2 is complete

### Within User Story 1

```bash
# All core module tests in parallel:
T004 test_config.py
T005 test_models.py
T006 test_utils.py
T007 test_chromadb_client.py
T008 test_chromadb_utils.py
T009 test_setup_logger.py

# All event tests in parallel:
T010 test_base.py
T011 test_input.py
T012 test_response.py
T013 test_ingest.py

# All prompt graph tests in parallel:
T014 test_edge.py
T015 test_json_graph_parser.py
T016 test_state.py
T017 test_node.py
T018 test_prompt_graph.py

# Async tests (sequential):
T019 test_rabbitmq.py
T020 test_alkemio_vc_engine.py

# Coverage gate:
T021 verify 90%+
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: All test files
3. **STOP and VALIDATE**: Run `pytest --cov --cov-fail-under=90`
4. If coverage < 90%, add more test cases to under-covered modules

### Incremental Delivery

1. Setup + US1 Tests → Verify 90% coverage locally
2. Add US2 CI → Push and verify pipeline runs green
3. Add US3 CLAUDE.md → Review for completeness
4. Polish → Final validation pass

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- T004–T018 are the bulk of the work and are fully parallelizable
- T021 is a gate — if coverage < 90%, go back and add tests
- Commit after each logical group (e.g., all event tests, all prompt graph tests)
