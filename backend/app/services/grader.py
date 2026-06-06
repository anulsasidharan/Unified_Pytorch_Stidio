"""Auto-grader for Python code output assertions."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass


@dataclass
class GradeResult:
    passed: bool
    actual: str
    expected: str
    diff: str | None = None


def generate_diff(actual: str, expected: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def run_custom_validator(actual: str, expected: str) -> bool:
    """Placeholder for custom validators stored on questions."""
    return actual.strip() == expected.strip()


def grade_submission(
    actual_output: str,
    expected_output: str,
    check_type: str = "exact",
) -> GradeResult:
    actual = actual_output.strip()
    expected = expected_output.strip()

    if check_type == "exact":
        passed = actual == expected
    elif check_type == "contains":
        passed = expected in actual
    elif check_type == "regex":
        passed = bool(re.fullmatch(expected, actual))
    elif check_type == "custom":
        passed = run_custom_validator(actual, expected)
    else:
        passed = actual == expected

    return GradeResult(
        passed=passed,
        actual=actual,
        expected=expected,
        diff=generate_diff(actual, expected) if not passed else None,
    )


def grade_batch(
    actual_outputs: list[str],
    test_cases: list[dict],
) -> tuple[list[dict], int]:
    results: list[dict] = []
    passed_count = 0

    for idx, case in enumerate(test_cases):
        expected = str(case.get("expected_output", ""))
        actual = actual_outputs[idx] if idx < len(actual_outputs) else ""
        grade = grade_submission(actual, expected, case.get("check_type", "exact"))
        if grade.passed:
            passed_count += 1
        results.append(
            {
                "passed": grade.passed,
                "actual_output": grade.actual,
                "error": None if grade.passed else grade.diff,
            }
        )

    total = len(test_cases) or 1
    score = round((passed_count / total) * 100)
    return results, score
