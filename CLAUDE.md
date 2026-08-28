# CLAUDE.md

Claude Code-specific notes for this repository. Read `AGENTS.md` first - it's the
canonical, tool-agnostic source for setup, conventions, and the AI-assisted workflow
section. This file only adds what's specific to working here through Claude Code.

## Skills

Two project skills live in `.claude/skills/`:

- `flaky-test-triage` - invoke when a test is failing intermittently or you're asked to
  investigate a failure; it reuses `prompts/failure_triage.md`, the same prompt the CI
  script runs.
- `bdd-scenario-scaffold` - invoke when asked to add a new BDD scenario; it scaffolds the
  `.feature` file, the `pytest-bdd` step definitions, and a stub page-object/API call
  following the existing `tests/steps/` pattern instead of writing them from scratch.

## Before committing

Run `flake8 tests scripts` and
`pylint tests/api tests/utils tests/steps scripts --disable=R,C --fail-under=8.5` locally -
both are hard gates in CI (`quality-gates.yml`) and a PR won't pass otherwise.

## Working on `scripts/ai_failure_triage.py` or `prompts/failure_triage.md`

These two files stay in sync by hand: the script's `load_system_prompt()` parses the
"## System prompt" section out of the markdown file at runtime by locating that heading
and the next one, so renaming or reordering those headings breaks it silently. Run
`tests/unit/test_ai_failure_triage.py` after touching either file.
