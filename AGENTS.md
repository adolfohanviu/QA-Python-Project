# AGENTS.md

Instructions for AI coding agents (Claude Code, and any other AGENTS.md-compatible tool)
working in this repository. This file is the source of truth for setup, conventions, and
the AI-assisted workflow; `CLAUDE.md` only adds Claude Code-specific pointers on top of it.

## Project

Senior QA Platform Engineering portfolio: Python + Pytest + Playwright framework covering
UI/API automation, BDD (`pytest-bdd`), CI quality gates, JMeter performance testing,
Docker/Kubernetes deployment validation, LGTM observability, and AI-assisted QA workflows
(last section below).

## Setup & commands

- Python 3.11+, `pip install -r requirements.txt`, then `playwright install`.
- Run everything: `pytest -v`. By marker: `pytest -m smoke|regression|api|ui|bdd|unit -v`.
- Lint: `flake8 tests scripts` and
  `pylint tests/api tests/utils tests/steps scripts --disable=R,C --fail-under=8.5`.
  Both run in CI (`.github/workflows/quality-gates.yml`) and must pass before merge.
- One-command run: `scripts/run.ps1` (Windows) / `scripts/run.sh` (macOS/Linux) - headless
  run + Allure report on `localhost:4040`.

## Conventions

- Async Playwright throughout (`async_api`); page objects extend
  `tests/pageobjects/base_page.py`.
- Type hints on every function signature; docstrings use `Args:`/`Returns:` (Google
  style) - match `tests/conftest.py` and `tests/utils/observability.py` for house style.
- Test data lives in `tests/fixtures/*.json`, loaded via `Config.load_fixture`, never
  inlined.
- Mark every test with at least one marker declared in `pytest.ini`; add new markers
  there before using them (`--strict-markers` is on).
- Commit messages: short imperative subject, Conventional Commits prefix (`feat:`,
  `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `perf:`).
- Don't add a dependency, an abstraction, or a fallback for a scenario that can't happen
  here - this is a portfolio codebase where every file gets read, not just executed.

## AI-assisted QA workflows

AI usage here is a reviewable part of the engineering process, not a bullet point -
every claim below points at a real file:

- **`.claude/skills/flaky-test-triage/SKILL.md`** - a Claude Code skill that investigates
  a failing or flaky test: reruns it, correlates `logs/qa-tests.log` trace events with the
  failure, and produces a root-cause hypothesis using the shared prompt in
  `prompts/failure_triage.md`.
- **`.claude/skills/bdd-scenario-scaffold/SKILL.md`** - scaffolds a new Gherkin feature +
  `pytest-bdd` step file + API/page-object stub from a one-line description, following the
  conventions in `tests/steps/`.
- **`scripts/ai_failure_triage.py`** - the same triage logic, wired into CI
  (`.github/workflows/all-tests.yml`, step `if: failure()`): on a failed run it parses the
  JUnit report, correlates each failure with the observability log, asks Claude for a
  hypothesis per failed test (capped by `TRIAGE_MAX_FAILURES`, default 5, to bound cost),
  and writes the result to the GitHub Actions step summary and `triage-report.md`. It never
  fails the build - triage is diagnostic, not a gate - and skips cleanly (exit 0) when
  `ANTHROPIC_API_KEY` isn't available, which is the normal case for a pull request from a
  fork.
- **`prompts/failure_triage.md`** - the versioned prompt template both the skill and the
  CI script use, including the output JSON schema and an explicit SECURITY note on how
  untrusted log/error content is fenced and never treated as instructions.
- **`tests/unit/test_ai_failure_triage.py`** - covers the parsing/prompt-building/
  validation logic with no network call; the AI feature is held to the same test bar as
  the rest of the framework.

Calling the API in CI requires the `ANTHROPIC_API_KEY` repository secret. Without it,
everything above still works locally in Claude Code - the two skills run inside the
assistant's own session and need no key; only the CI step degrades to a no-op.
