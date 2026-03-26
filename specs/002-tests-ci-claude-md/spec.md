# Feature Specification: Add Tests, CI Build, and CLAUDE.md

**Feature Branch**: `002-tests-ci-claude-md`
**Created**: 2026-03-25
**Status**: Draft
**Input**: User description: "add tests, configure CI build and create CLAUDE.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Test Suite (Priority: P1)

As a library maintainer, I want an automated test suite that
covers the library's core modules, so that I can catch
regressions before they reach consuming services and review
contributions with confidence.

**Why this priority**: The library currently has zero tests.
Without tests, every change is a leap of faith. This is the
foundation that CI and all future development depends on.

**Independent Test**: Can be verified by running the test suite
locally and confirming that all tests pass with clear
pass/fail output.

**Acceptance Scenarios**:

1. **Given** the library source code, **When** a developer runs
   the test command, **Then** all unit tests execute and report
   pass/fail results within 60 seconds.
2. **Given** a module with external dependencies (Mistral API,
   ChromaDB, RabbitMQ), **When** the tests run without those
   services available, **Then** tests for that module still pass
   by using appropriate test isolation (mocks/stubs).
3. **Given** the prompt graph module, **When** tests run,
   **Then** graph parsing, node prompt formatting, output
   validation, and graph compilation are all verified.
4. **Given** the configuration module, **When** tests run with
   specific environment variables set, **Then** the config
   correctly loads and validates those values.
5. **Given** the utility functions, **When** tests run,
   **Then** all helper functions (history formatting, document
   combining, tag clearing) produce correct output.

---

### User Story 2 - Continuous Integration Pipeline (Priority: P1)

As a library maintainer, I want an automated CI pipeline that
runs on every push and pull request, so that broken code is
caught before it is merged and the team has confidence in the
main branch's stability.

**Why this priority**: Equally critical to tests — without CI,
tests only run when developers remember to run them locally.
CI enforces quality gates automatically.

**Independent Test**: Can be verified by pushing a commit to a
feature branch and confirming that the CI pipeline triggers,
runs linting, type checking, and tests, and reports the
result on the pull request.

**Acceptance Scenarios**:

1. **Given** a push to any branch, **When** the CI pipeline
   triggers, **Then** it runs linting, type checking, and the
   full test suite.
2. **Given** a pull request, **When** CI completes, **Then**
   the pass/fail status is visible on the PR before merge.
3. **Given** a linting or type checking failure, **When** CI
   runs, **Then** the pipeline fails with a clear error message
   identifying the issue.
4. **Given** a test failure, **When** CI runs, **Then** the
   pipeline fails and reports which tests failed.
5. **Given** the pipeline configuration, **When** reviewed,
   **Then** it does NOT require real API keys or external
   services to run (tests use mocks).

---

### User Story 3 - CLAUDE.md Developer Guide (Priority: P2)

As a developer (human or AI assistant) working on this library
for the first time, I want a CLAUDE.md file in the repository
root that describes the project conventions, architecture, and
common commands, so that I can contribute effectively without
tribal knowledge.

**Why this priority**: Valuable for onboarding and AI-assisted
development, but the library functions without it. Depends on
US1 and US2 being defined first so the guide can reference
test and CI commands.

**Independent Test**: Can be verified by reading the file and
confirming it contains project description, setup instructions,
common commands, architecture overview, and coding conventions.

**Acceptance Scenarios**:

1. **Given** a new developer opens the repository, **When** they
   read CLAUDE.md, **Then** they understand the project's
   purpose, structure, and how to run tests and linting.
2. **Given** an AI coding assistant is given a task in this repo,
   **When** it reads CLAUDE.md, **Then** it has enough context
   to follow project conventions (commit style, code style,
   module organization).
3. **Given** the CLAUDE.md file, **When** reviewed, **Then** it
   accurately reflects the current project structure, commands,
   and conventions.

---

### Edge Cases

- What happens when a developer runs tests without any `.env`
  file present? Tests MUST still pass (no dependency on local
  environment configuration).
- What happens when CI runs on a fork without repository
  secrets configured? The pipeline MUST still succeed for
  linting, type checking, and unit tests.
- What happens when a new module is added without tests? The CI
  pipeline MUST fail if overall coverage drops below 90%.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST have a test suite that achieves
  at least 90% code coverage across the entire library.
- **FR-002**: Tests MUST run without requiring external services
  (RabbitMQ, ChromaDB, Mistral API) or real API keys.
- **FR-003**: Tests MUST be runnable with a single command from
  the repository root.
- **FR-004**: The CI pipeline MUST run automatically on every
  push and pull request.
- **FR-005**: The CI pipeline MUST execute linting, type
  checking, and the full test suite as separate steps.
- **FR-006**: The CI pipeline MUST fail if any step (lint, type
  check, tests) fails.
- **FR-006a**: The CI pipeline MUST fail if code coverage drops
  below 90%.
- **FR-007**: The CI pipeline MUST NOT require external service
  credentials or secrets to run.
- **FR-008**: A CLAUDE.md file MUST exist at the repository root
  containing: project description, setup instructions, common
  commands (test, lint, type check), architecture overview, and
  coding conventions.
- **FR-009**: CLAUDE.md MUST document the commit message
  convention (conventional commits).
- **FR-010**: CLAUDE.md MUST document the branch strategy
  (feature branches off develop).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The test suite achieves at least 90% code coverage
  across all library source files.
- **SC-002**: The full test suite runs and passes in under 60
  seconds without any external services.
- **SC-003**: Every pull request shows a CI status check that
  includes lint, type check, and test results before merge.
- **SC-004**: A new developer can set up the project and run
  tests successfully by following only the instructions in
  CLAUDE.md, without additional guidance.
- **SC-005**: The CI pipeline runs end-to-end (from trigger to
  status report) in under 5 minutes.

## Assumptions

- The CI platform is GitHub Actions (the repository is hosted
  on GitHub).
- Test isolation uses mocking/stubbing for external services
  rather than running real service containers in CI.
- Code coverage reporting is mandatory with a 90% minimum
  threshold enforced in CI.
- CLAUDE.md follows the conventions expected by Claude Code
  (the AI coding assistant), which reads this file for project
  context.
- The test suite will use pytest with pytest-asyncio for async
  test support, consistent with the constitution's testing
  guidance.
