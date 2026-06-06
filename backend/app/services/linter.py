"""PEP 8 linting via pycodestyle and pyflakes."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass

import pycodestyle
import pyflakes.api
from pyflakes.reporter import Reporter


@dataclass
class LintResult:
    violations: list[dict]
    score: int


def lint_code(code: str) -> LintResult:
    violations: list[dict] = []

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name

    try:
        style_guide = pycodestyle.StyleGuide(quiet=True)
        report = style_guide.check_files([tmp_path])
        for error in report.messages:
            violations.append(
                {
                    "line": error.row,
                    "col": error.col,
                    "code": error.code,
                    "message": error.text,
                }
            )
    finally:
        os.unlink(tmp_path)

    pyflakes_output = __import__("io").StringIO()
    pyflakes_reporter = Reporter(pyflakes_output, pyflakes_output)
    pyflakes.api.check(code, "stdin", pyflakes_reporter)
    for line in pyflakes_output.getvalue().splitlines():
        if not line.strip():
            continue
        violations.append(
            {
                "line": 1,
                "col": 0,
                "code": "F",
                "message": line.strip(),
            }
        )

    score = max(0, 100 - len(violations) * 5)
    return LintResult(violations=violations, score=score)
