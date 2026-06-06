"""Unit tests for the Python Live Execution Engine (Phase 2)."""

from app.services.grader import grade_batch, grade_submission
from app.services.linter import lint_code
from app.services.sandbox import run_python_sandbox


def test_grader_exact_match() -> None:
    result = grade_submission("Hello\nWorld", "Hello\nWorld", "exact")
    assert result.passed is True
    assert result.diff is None


def test_grader_exact_mismatch_generates_diff() -> None:
    result = grade_submission("foo", "bar", "exact")
    assert result.passed is False
    assert result.diff is not None
    assert "expected" in result.diff


def test_grader_contains_mode() -> None:
    assert grade_submission("The answer is 42", "42", "contains").passed is True
    assert grade_submission("no match", "42", "contains").passed is False


def test_grader_regex_mode() -> None:
    assert grade_submission("abc123", r"[a-z]+\d+", "regex").passed is True
    assert grade_submission("123", r"[a-z]+\d+", "regex").passed is False


def test_grader_batch_score() -> None:
    results, score = grade_batch(
        ["1", "2", "wrong"],
        [
            {"expected_output": "1"},
            {"expected_output": "2"},
            {"expected_output": "3"},
        ],
    )
    assert len(results) == 3
    assert results[0]["passed"] is True
    assert results[2]["passed"] is False
    assert score == 67


def test_linter_clean_code_scores_high() -> None:
    result = lint_code("x = 1\nprint(x)\n")
    assert result.score >= 90
    assert isinstance(result.violations, list)


def test_linter_flags_pep8_violation() -> None:
    result = lint_code("x=1\n")
    assert len(result.violations) >= 1
    assert result.score < 100


def test_sandbox_runs_print() -> None:
    result = run_python_sandbox("print('sandbox-ok')", time_limit=5.0)
    assert result.returncode == 0
    assert "sandbox-ok" in result.stdout


def test_sandbox_timeout() -> None:
    result = run_python_sandbox("import time\ntime.sleep(30)", time_limit=0.2)
    assert result.returncode == -1
    assert "Time limit exceeded" in result.stderr


def test_execute_endpoint_runs_code(api_client) -> None:
    res = api_client.post(
        "/api/v1/execute",
        json={"code": "print(2 + 2)"},
    )
    assert res.status_code == 200
    body = res.json()
    assert "4" in body["stdout"]
    assert body["execution_time_ms"] >= 0
    assert isinstance(body["pep8_violations"], list)


def test_execute_grade_only_mode(api_client) -> None:
    res = api_client.post(
        "/api/v1/execute",
        json={
            "code": "print('hi')",
            "stdout": "hi",
            "stderr": "",
            "execution_time_ms": 42,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["stdout"] == "hi"
    assert body["execution_time_ms"] == 42


def test_execute_batch_endpoint(api_client) -> None:
    res = api_client.post(
        "/api/v1/execute/batch",
        json={
            "code": "print('a')",
            "test_cases": [
                {"expected_output": "a"},
                {"expected_output": "a", "check_type": "contains"},
            ],
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["score"] == 100
    assert all(item["passed"] for item in body["results"])


def test_lint_endpoint(api_client) -> None:
    res = api_client.post(
        "/api/v1/lint",
        json={"code": "x=1\n"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["score"] < 100
    assert len(body["violations"]) >= 1
