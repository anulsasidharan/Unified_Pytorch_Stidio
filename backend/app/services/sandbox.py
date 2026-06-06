"""Server-side Python sandbox fallback for non-Pyodide exercises."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    returncode: int


def _set_resource_limits() -> None:
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024))
    except (ImportError, OSError, ValueError):
        pass


def run_python_sandbox(code: str, time_limit: float = 5.0) -> SandboxResult:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=time_limit,
            preexec_fn=_set_resource_limits if os.name != "nt" else None,
        )
        return SandboxResult(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
        )
    except subprocess.TimeoutExpired:
        return SandboxResult(stdout="", stderr="Time limit exceeded", returncode=-1)
    finally:
        os.unlink(tmp_path)
