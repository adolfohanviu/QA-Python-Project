"""AI-assisted failure triage for CI test runs.

Reads a JUnit XML report, correlates failed tests with observability log
events, asks Claude for a root-cause hypothesis per failure, and writes a
markdown summary (GitHub Actions step summary when available, stdout
otherwise). Diagnostic only: this script never fails the build, even on
an unexpected error - see AGENTS.md's "AI-assisted QA workflows" section.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import anthropic
from pydantic import BaseModel, Field, ValidationError

PROMPT_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "failure_triage.md"
DEFAULT_MODEL = "claude-opus-5"
MAX_FAILURES_DEFAULT = 5


class TriageResult(BaseModel):
    """Validated shape of a single triage response - kept in sync with
    prompts/failure_triage.md's documented output schema."""

    root_cause_hypothesis: str
    confidence: str = Field(pattern="^(low|medium|high)$")
    suspected_flaky: bool
    suggested_next_step: str


@dataclass
class FailureRecord:
    test_name: str
    error_text: str


def load_system_prompt() -> str:
    """Extract the '## System prompt' section from prompts/failure_triage.md."""
    text = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    start = text.index("## System prompt") + len("## System prompt")
    end = text.index("## User prompt template")
    return text[start:end].strip()


def _junit_test_name_to_nodeid(classname: str, name: str) -> str:
    """Reconstruct a pytest nodeid (e.g. 'tests/api/test_user_api.py::test_x' or
    '...::TestClass::test_x') from JUnit's dotted `classname`/`name`.

    This pytest install's junitxml output has no `file` attribute, and a dotted
    classname is ambiguous between package separators and a test class name
    (e.g. "tests.api.test_user_api.TestUserAPI"). Resolved against the
    filesystem: the longest dotted prefix that names a real .py file is the
    module; any remaining segments are the test class chain. Must run with the
    repository root as the working directory, same as the script's other
    relative paths (logs/qa-tests.log, triage-report.md).
    """
    parts = classname.split(".") if classname else []
    for split_at in range(len(parts), 0, -1):
        candidate = Path(*parts[:split_at]).with_suffix(".py")
        if candidate.exists():
            remainder = parts[split_at:]
            return "::".join([candidate.as_posix(), *remainder, name])

    # No dotted prefix matched a real file - best effort, flat identifier.
    return f"{classname}::{name}" if classname else name


def parse_junit_failures(junit_path: Path) -> list[FailureRecord]:
    """Extract failed/errored testcases from a JUnit XML report.

    Returns an empty list when the report doesn't exist - callers treat
    that the same as "nothing failed", not an error.
    """
    if not junit_path.exists():
        return []

    failures: list[FailureRecord] = []
    tree = ET.parse(junit_path)
    for testcase in tree.getroot().iter("testcase"):
        node = testcase.find("failure")
        if node is None:
            node = testcase.find("error")
        if node is None:
            continue

        test_name = _junit_test_name_to_nodeid(testcase.get("classname", ""), testcase.get("name", ""))
        error_text = (node.text or node.get("message") or "").strip()
        failures.append(FailureRecord(test_name=test_name, error_text=error_text[:4000]))

    return failures


def index_observability_events(log_path: Path) -> dict[str, list[dict[str, Any]]]:
    """Parse logs/qa-tests.log once and group events by test_name.

    Returns {} when the log file is absent (observability wasn't enabled for
    the run) or a line isn't valid JSON.
    """
    if not log_path.exists():
        return {}

    events_by_test: dict[str, list[dict[str, Any]]] = {}
    with log_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            test_name = event.get("test_name")
            if test_name:
                events_by_test.setdefault(test_name, []).append(event)

    return events_by_test


def build_user_prompt(failure: FailureRecord, events: list[dict[str, Any]]) -> str:
    return (
        "<test_failure>\n"
        f"test_name: {failure.test_name}\n"
        f"error:\n{failure.error_text}\n"
        "</test_failure>\n\n"
        f"<observability_events>\n{json.dumps(events, ensure_ascii=True)}\n"
        "</observability_events>"
    )


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response")
    return text[start : end + 1]


def request_triage(
    client: anthropic.Anthropic, model: str, system_prompt: str, user_prompt: str
) -> TriageResult:
    """Call Claude and validate its JSON response, retrying once on malformed output.

    max_tokens is sized with headroom for adaptive thinking (on by default on
    Opus-tier models, drawing from the same budget as the output) and effort
    is pinned to "low" - this is a fixed-shape JSON classification task, not
    reasoning-heavy work, so low effort avoids spending most of the budget on
    thinking before the model ever writes the JSON object.
    """
    last_error: Exception | None = None
    for _ in range(2):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                output_config={"effort": "low"},
            )
            text = "".join(block.text for block in response.content if block.type == "text")
            payload = json.loads(_extract_json_object(text))
            return TriageResult.model_validate(payload)
        except (anthropic.APIError, ValueError, ValidationError, json.JSONDecodeError) as exc:
            last_error = exc
            continue

    raise RuntimeError("triage response unavailable after retry") from last_error


def render_summary(results: list[tuple[FailureRecord, "TriageResult | None"]]) -> str:
    lines = ["## AI Failure Triage", ""]
    if not results:
        lines.append("No failed tests to triage.")
        return "\n".join(lines)

    for failure, result in results:
        lines.append(f"### `{failure.test_name}`")
        if result is None:
            lines.append("_Triage unavailable for this failure._")
        else:
            lines.append(f"- **Hypothesis:** {result.root_cause_hypothesis}")
            lines.append(f"- **Confidence:** {result.confidence}")
            lines.append(f"- **Suspected flaky:** {result.suspected_flaky}")
            lines.append(f"- **Suggested next step:** {result.suggested_next_step}")
        lines.append("")

    return "\n".join(lines)


def _run_triage(failures: list[FailureRecord], log_path: Path, model: str, api_key: str) -> str:
    """Everything that can fail (prompt loading, the API, parsing) lives here,
    isolated from main()'s try/except boundary - see main()'s docstring."""
    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = load_system_prompt()
    events_by_test = index_observability_events(log_path)

    results: list[tuple[FailureRecord, "TriageResult | None"]] = []
    for failure in failures:
        events = events_by_test.get(failure.test_name, [])
        user_prompt = build_user_prompt(failure, events)
        result: "TriageResult | None"
        try:
            result = request_triage(client, model, system_prompt, user_prompt)
        except RuntimeError as exc:
            print(f"AI failure triage: {exc}", file=sys.stderr)
            result = None
        results.append((failure, result))

    return render_summary(results)


def main() -> int:
    junit_path = Path(os.getenv("TRIAGE_JUNIT_XML", "test-results.xml"))
    log_path = Path(os.getenv("TRIAGE_LOG_FILE", "logs/qa-tests.log"))
    max_failures = int(os.getenv("TRIAGE_MAX_FAILURES", str(MAX_FAILURES_DEFAULT)))
    model = os.getenv("TRIAGE_MODEL", DEFAULT_MODEL)

    failures = parse_junit_failures(junit_path)[:max_failures]
    if not failures:
        print("AI failure triage: no failed tests found, nothing to do.")
        return 0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "AI failure triage: ANTHROPIC_API_KEY is not set (expected on forked-repo "
            "pull requests, where GitHub does not expose secrets) - skipping."
        )
        return 0

    # Triage is diagnostic, not a gate: any unexpected failure here (a bad
    # prompt-template edit, an SDK error class we didn't anticipate, ...)
    # must never fail the CI run that got us here in the first place.
    try:
        summary = _run_triage(failures, log_path, model, api_key)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"AI failure triage: unexpected error, skipping - {exc}", file=sys.stderr)
        return 0

    print(summary)
    Path("triage-report.md").write_text(summary, encoding="utf-8")

    step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(summary + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
