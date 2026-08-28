---
name: bdd-scenario-scaffold
description: "Trigger: BDD scenario, Gherkin feature, add a scenario, pytest-bdd. Scaffold a feature file, step definitions, and a stub page-object/API call."
license: Apache-2.0
metadata:
  author: "adolfohanviu"
  version: "1.0"
---

# BDD Scenario Scaffold

## Activation Contract

Asked to add a BDD/Gherkin scenario, or to cover a user story with `pytest-bdd`.

## Hard Rules

- Read one existing pair first - `tests/steps/test_login_bdd.py` (UI) or `test_user_api_bdd.py` (API) plus its `.feature` file - and match that exact structure; never invent a different one.
- Every new test module needs `@pytest.mark.bdd` plus a domain marker already declared in `pytest.ini` (`--strict-markers` rejects undeclared ones) - add the marker there first if none fits.
- Feature text stays business language: no selectors, no endpoints.

## Decision Gates

| Scenario type | Fixture / stub |
|---|---|
| UI behavior | `page` fixture, extend `tests/pageobjects/base_page.py` |
| API behavior | `APIClient` in `tests/api/api_client.py` |

## Execution Steps

1. Read the matching existing pair (see Hard Rules).
2. Write the `.feature` file in `tests/features/`.
3. Write step definitions in `tests/steps/`, wired to the right fixture and markers.
4. Stub just enough of the page-object/API call for the scenario to run.
5. Run `pytest tests/steps/<new_file>.py -v` and confirm it's discovered.

## Output Contract

A `.feature` file, a matching step-definitions file, and a minimal stub implementation - all runnable via pytest, none duplicating an existing page object or API method.

## References

- `tests/steps/test_login_bdd.py`, `tests/steps/test_user_api_bdd.py` - reference implementations.
- `pytest.ini` - marker registry.
