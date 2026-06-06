"""Shared execution grading and submission persistence."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.models.user import User
from app.services.grader import grade_submission
from app.services.linter import LintResult, lint_code


def grade_question_output(
    question: Question,
    stdout: str,
    lint: LintResult,
) -> bool | None:
    if not question.expected_output:
        return None

    check_type = getattr(question, "expected_output_type", None) or "exact"
    grade = grade_submission(stdout, question.expected_output, check_type)
    is_correct = grade.passed
    if getattr(question, "pep8_required", False) and lint.score < 100:
        is_correct = False
    return is_correct


async def persist_code_submission(
    db: AsyncSession,
    *,
    user: User | None,
    question_id: int | None,
    code: str,
    stdout: str,
    stderr: str,
    is_correct: bool | None,
    execution_time_ms: int,
    pep8_score: int,
) -> None:
    """Best-effort insert into code_submissions; ignores missing table in dev."""
    try:
        await db.execute(
            text("""
                INSERT INTO code_submissions
                    (user_id, question_id, code, stdout, stderr, is_correct,
                     execution_time_ms, pep8_score)
                VALUES
                    (:user_id, :question_id, :code, :stdout, :stderr, :is_correct,
                     :exec_ms, :pep8_score)
            """),
            {
                "user_id": user.id if user else None,
                "question_id": question_id,
                "code": code,
                "stdout": stdout,
                "stderr": stderr,
                "is_correct": is_correct,
                "exec_ms": execution_time_ms,
                "pep8_score": pep8_score,
            },
        )
        await db.commit()
    except Exception:
        await db.rollback()
