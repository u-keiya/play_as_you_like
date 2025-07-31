# Test Strategy

## 1. Overview

This document outlines the testing strategy for the "PlayAsYouLike" project. Our goal is to ensure high quality and reliability by employing a multi-layered testing approach, inspired by the "Test Pyramid" concept. Each layer has a distinct purpose, from fast, isolated unit tests to comprehensive end-to-end user scenario validations.

## 2. Test Layers

| Layer | Tool / Framework | Location | Purpose |
| :--- | :--- | :--- | :--- |
| **Acceptance (E2E)** | Gherkin (Cucumber/Behave) | `tests/e2e/` | **Validate user requirements (USDM)**. Simulates user behavior from the outside-in, ensuring the system delivers the expected value. |
| **Contract** | Schemathesis | `tests/contract/` | **Verify API contracts**. Automatically validates that the API implementation adheres to the `openapi.yaml` specification, preventing breaking changes between consumer and provider. |
| **Integration** | Pytest | `tests/integration/` | Test interactions between components (e.g., API server and database, service to service, **WebSocket communication**). |
| **Unit** | Pytest | `tests/unit/` | Test individual functions, methods, or classes in isolation. Fast feedback for developers. |

## 3. Coverage Targets

Our initial coverage goals are as follows. These will be measured and reported via our CI pipeline.

- **USDM Acceptance Criteria Coverage**: 100%
  - Every leaf-node requirement in `docs/02_requirements/usdm/` must have at least one corresponding Gherkin scenario in `tests/e2e/`.
- **API Contract Coverage**: 100%
  - All HTTP endpoints and methods defined in `openapi.yaml` will be tested by Schemathesis. WebSocket endpoints require separate integration tests.
- **Code Coverage (Unit & Integration)**: > 80%
  - This is a target for the development team to maintain.

## 4. CI/CD Integration

All tests will be executed automatically on every pull request to the `develop` and `main` branches. A pull request cannot be merged unless all tests pass.

- **Linting**: Code style and quality checks.
- **Unit/Integration Tests**: Fast feedback loop.
- **Contract Tests**: Ensure API integrity.
- **Acceptance Tests**: Validate end-to-end functionality.

## 5. WebSocket Testing

Our strategy for testing WebSocket endpoints is as follows:

- **/ws/hit-judge**: An integration test will be implemented in `tests/integration/` to verify the connection lifecycle and the real-time message flow. This includes sending `PlayerInput` messages and asserting the reception of `HitResult` or `Warning` messages based on the specifications found in the sequence diagrams.
- **/ws/effectPreset**: Testing for this endpoint is currently blocked. The specific schema for the pushed `effectPreset {presetId, params}` message needs to be clarified in the design documents before a valid test can be created.

## 6. Open Questions

- The specific schema for messages pushed from the `/ws/effectPreset` endpoint (e.g., `effectPreset {presetId, params}`) needs to be defined in the design documents to enable test creation.