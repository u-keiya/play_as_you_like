# Test Strategy

## 1. Overview

This document outlines the testing strategy for the "PlayAsYouLike" project. Our goal is to ensure high quality and reliability by employing a multi-layered testing approach, inspired by the "Test Pyramid" concept. Each layer has a distinct purpose, from fast, isolated unit tests to comprehensive end-to-end user scenario validations.

## 2. Test Layers

| Layer | Tool / Framework | Location | Purpose |
| :--- | :--- | :--- | :--- |
| **Acceptance (E2E)** | Gherkin (Cucumber/Behave) | `tests/e2e/` | **Validate user requirements (USDM)**. Simulates user behavior from the outside-in, ensuring the system delivers the expected value. |
| **Contract** | Schemathesis, Pytest | `tests/contract/` | **Verify API contracts**. Automatically validates that the API implementation adheres to the `openapi.yaml` specification, including WebSocket message schemas. |
| **Integration** | Pytest | `tests/integration/` | Test interactions between components (e.g., API server and database, service to service, **WebSocket communication**). |
| **Unit** | Pytest | `tests/unit/` | Test individual functions, methods, or classes in isolation. Fast feedback for developers. |

## 3. Coverage Targets

Our initial coverage goals are as follows. These will be measured and reported via our CI pipeline.

- **USDM Acceptance Criteria Coverage**: 100%
  - Every leaf-node requirement in `docs/02_requirements/usdm/` must have at least one corresponding Gherkin scenario in `tests/e2e/`.
- **API Contract Coverage**: 100%
  - All HTTP endpoints and methods defined in `openapi.yaml` will be tested by Schemathesis.
  - All WebSocket message schemas (e.g., `EffectPresetMessage`) will be validated via dedicated contract tests.
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
- **/ws/effectPreset**: A contract test will be created in `tests/contract/` to validate that messages pushed from the server conform to the `EffectPresetMessage` schema defined in `openapi.yaml`. This test will subscribe to the WebSocket and validate incoming messages against the schema.

## 6. Open Questions

- (Resolved) The schema for `/ws/effectPreset` is now defined in `openapi.yaml` as `EffectPresetMessage`.
- The specific parameters for each `presetId` (e.g., `hueShift` for `rainbow`) are listed as examples in `EffectPresetParams`. A more formal, machine-readable definition for each preset's parameters would further improve test accuracy and prevent invalid parameter combinations. This should be discussed with the design team.