"""PEP 8 linting via pycodestyle and pyflakes."""

from __future__ import annotations

import io
import os
import tempfile
from dataclasses import dataclass, field

import pycodestyle
import pyflakes.api
from pyflakes.reporter import Reporter


@dataclass
class LintResult:
    violations: list[dict] = field(default_factory=list)
    score: int = 100


class _ViolationCollector(pycodestyle.BaseReport):
    """Custom pycodestyle reporter that collects violations as dicts."""

    def __init__(self, options: pycodestyle.StyleGuide) -> None:
        super().__init__(options)
        self.collected: list[dict] = []

    def error(
        self,
        line_number: int,
        offset: int,
        text: str,
        check: object,
    ) -> str | None:
        code = super().error(line_number, offset, text, check)
        if code:
            self.collected.append(
                {
                    "line": line_number,
                    "col": offset + 1,
                    "code": code,
                    "message": text[5:].strip() if len(text) > 5 else text.strip(),
                }
            )
        return code


def lint_code(code: str) -> LintResult:
    violations: list[dict] = []

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name

    try:
        style_guide = pycodestyle.StyleGuide(reporter=_ViolationCollector)
        report: _ViolationCollector = style_guide.check_files([tmp_path])  # type: ignore[assignment]
        violations.extend(report.collected)
    except Exception:
        pass
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    # pyflakes static analysis
    try:
        pyflakes_output = io.StringIO()
        pyflakes_reporter = Reporter(pyflakes_output, pyflakes_output)
        pyflakes.api.check(code, "<stdin>", pyflakes_reporter)
        for line in pyflakes_output.getvalue().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("<stdin>:") is False:
                if stripped:
                    violations.append({"line": 1, "col": 0, "code": "F", "message": stripped})
                continue
            # Parse "<stdin>:line:col: message" format
            parts = stripped.split(":", 3)
            try:
                lnum = int(parts[1])
                col = int(parts[2].split()[0]) if len(parts) > 2 else 0
                msg = parts[3].strip() if len(parts) > 3 else stripped
            except (IndexError, ValueError):
                lnum, col, msg = 1, 0, stripped
            violations.append({"line": lnum, "col": col, "code": "F", "message": msg})
    except Exception:
        pass

    score = max(0, 100 - len(violations) * 5)
    return LintResult(violations=violations, score=score)
