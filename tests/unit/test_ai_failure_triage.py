"""Unit tests for scripts/ai_failure_triage.py.

No network calls - request_triage()/main() (the only functions that touch the
Anthropic API) are exercised elsewhere only through manual/CI runs. Everything
here covers the pure parsing, correlation, and prompt-building logic.
"""

import json
from pathlib import Path

import pytest

from scripts.ai_failure_triage import (
    FailureRecord,
    TriageResult,
    _extract_json_object,
    _junit_test_name_to_nodeid,
    build_user_prompt,
    index_observability_events,
    load_system_prompt,
    parse_junit_failures,
    render_summary,
)

pytestmark = pytest.mark.unit

JUNIT_XML = """<?xml version="1.0"?>
<testsuite>
  <testcase classname="tests.api.test_user_api" name="test_create_user" time="0.1">
    <failure message="AssertionError: expected 201, got 500">Traceback...</failure>
  </testcase>
  <testcase classname="tests.api.test_user_api.TestUserAPI" name="test_get_user" time="0.1">
    <failure message="AssertionError">boom</failure>
  </testcase>
  <testcase classname="tests.api.test_user_api" name="test_passing" time="0.1"/>
</testsuite>
"""


def test_junit_test_name_to_nodeid_for_module_level_test() -> None:
    nodeid = _junit_test_name_to_nodeid("tests.api.test_user_api", "test_create_user")
    assert nodeid == "tests/api/test_user_api.py::test_create_user"


def test_junit_test_name_to_nodeid_for_class_based_test() -> None:
    nodeid = _junit_test_name_to_nodeid("tests.api.test_user_api.TestUserAPI", "test_get_user")
    assert nodeid == "tests/api/test_user_api.py::TestUserAPI::test_get_user"


def test_junit_test_name_to_nodeid_falls_back_when_no_file_matches() -> None:
    nodeid = _junit_test_name_to_nodeid("not.a.real.module", "test_x")
    assert nodeid == "not.a.real.module::test_x"


def test_parse_junit_failures_extracts_only_failed_cases_and_matches_pytest_nodeid() -> None:
    junit_path = Path("test-results-fixture.xml")
    junit_path.write_text(JUNIT_XML, encoding="utf-8")
    try:
        failures = parse_junit_failures(junit_path)
    finally:
        junit_path.unlink()

    assert len(failures) == 2
    assert failures[0].test_name == "tests/api/test_user_api.py::test_create_user"
    assert failures[1].test_name == "tests/api/test_user_api.py::TestUserAPI::test_get_user"
    assert "Traceback" in failures[0].error_text


def test_parse_junit_failures_returns_empty_when_file_missing(tmp_path: Path) -> None:
    assert parse_junit_failures(tmp_path / "missing.xml") == []


def test_index_observability_events_groups_by_test_name(tmp_path: Path) -> None:
    log_path = tmp_path / "qa-tests.log"
    log_path.write_text(
        "\n".join(
            [
                json.dumps({"event": "test_start", "test_name": "a"}),
                json.dumps({"event": "test_end", "test_name": "a"}),
                json.dumps({"event": "test_start", "test_name": "b"}),
                "not json",
                "",
            ]
        ),
        encoding="utf-8",
    )

    index = index_observability_events(log_path)

    assert [e["event"] for e in index["a"]] == ["test_start", "test_end"]
    assert len(index["b"]) == 1


def test_index_observability_events_returns_empty_when_file_missing() -> None:
    assert index_observability_events(Path("does/not/exist.log")) == {}


def test_build_user_prompt_wraps_untrusted_data_in_tags() -> None:
    failure = FailureRecord(test_name="t", error_text="boom")
    prompt = build_user_prompt(failure, [{"event": "test_start"}])

    assert "<test_failure>" in prompt
    assert "<observability_events>" in prompt
    assert "boom" in prompt


def test_extract_json_object_pulls_object_out_of_surrounding_text() -> None:
    text = 'Here is the result:\n{"a": 1}\nThanks.'
    assert _extract_json_object(text) == '{"a": 1}'


def test_extract_json_object_raises_when_no_object_present() -> None:
    with pytest.raises(ValueError):
        _extract_json_object("no json here")


def test_load_system_prompt_extracts_only_the_system_section() -> None:
    prompt = load_system_prompt()

    assert "SECURITY" in prompt
    assert "## User prompt template" not in prompt


def test_render_summary_reports_unavailable_triage() -> None:
    failure = FailureRecord(test_name="t", error_text="boom")
    summary = render_summary([(failure, None)])

    assert "Triage unavailable" in summary


def test_render_summary_reports_hypothesis() -> None:
    failure = FailureRecord(test_name="t", error_text="boom")
    result = TriageResult(
        root_cause_hypothesis="Flaky selector timing",
        confidence="medium",
        suspected_flaky=True,
        suggested_next_step="Add explicit wait",
    )
    summary = render_summary([(failure, result)])

    assert "Flaky selector timing" in summary
    assert "medium" in summary


def test_run_triage_never_raises_when_prompt_template_is_malformed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """main()'s try/except boundary only helps if the failure it's meant to
    catch actually reaches it - this proves _run_triage raises instead of
    swallowing errors itself, so that boundary is load-bearing, not dead code.
    """
    import scripts.ai_failure_triage as triage_module

    broken_prompt = tmp_path / "broken.md"
    broken_prompt.write_text("no headings here at all", encoding="utf-8")
    monkeypatch.setattr(triage_module, "PROMPT_TEMPLATE_PATH", broken_prompt)

    with pytest.raises(ValueError):
        triage_module._run_triage(
            [FailureRecord(test_name="t", error_text="boom")],
            tmp_path / "missing.log",
            "claude-opus-5",
            "fake-key",
        )
