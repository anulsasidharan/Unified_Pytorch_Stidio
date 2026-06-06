"""Code execution routes — server-side sandbox fallback and grading."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_optional_user
from app.models.question import Question
from app.models.user import User
from app.services.grader import grade_batch, grade_submission
from app.services.linter import lint_code
from app.services.sandbox import run_python_sandbox

router = APIRouter(prefix="/execute", tags=["execute"])


class ExecuteRequest(BaseModel):
    code: str
    question_id: int | None = None
    time_limit_ms: int = Field(default=5000, ge=100, le=30000)


class ExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    is_correct: bool | None = None
    execution_time_ms: int
    pep8_violations: list[dict]


class BatchTestCase(BaseModel):
    input: str = ""
    expected_output: str
    check_type: str = "exact"


class BatchExecuteRequest(BaseModel):
    code: str
    test_cases: list[BatchTestCase]


class BatchResultItem(BaseModel):
    passed: bool
    actual_output: str
    error: str | None = None


class BatchExecuteResponse(BaseModel):
    results: list[BatchResultItem]
    score: int


@router.post("", response_model=ExecuteResponse)
async def execute_code(
    body: ExecuteRequest,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> ExecuteResponse:
    time_limit = body.time_limit_ms / 1000.0
    started = time.perf_counter()
    sandbox = run_python_sandbox(body.code, time_limit=time_limit)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    lint = lint_code(body.code)

    is_correct: bool | None = None
    if body.question_id is not None:
        result = await db.execute(select(Question).where(Question.id == body.question_id))
        question = result.scalar_one_or_none()
        if question is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        if question.expected_output:
            check_type = getattr(question, "expected_output_type", None) or "exact"
            grade = grade_submission(sandbox.stdout, question.expected_output, check_type)
            is_correct = grade.passed
            if getattr(question, "pep8_required", False) and lint.score < 100:
                is_correct = False

    # Persist submission (best-effort — ignore if table not yet available)
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
                "user_id": str(user.id) if user else None,
                "question_id": body.question_id,
                "code": body.code,
                "stdout": sandbox.stdout,
                "stderr": sandbox.stderr,
                "is_correct": is_correct,
                "exec_ms": elapsed_ms,
                "pep8_score": lint.score,
            },
        )
        await db.commit()
    except Exception:
        await db.rollback()

    return ExecuteResponse(
        stdout=sandbox.stdout,
        stderr=sandbox.stderr,
        is_correct=is_correct,
        execution_time_ms=elapsed_ms,
        pep8_violations=lint.violations,
    )


@router.post("/batch", response_model=BatchExecuteResponse)
async def execute_batch(body: BatchExecuteRequest) -> BatchExecuteResponse:
    outputs: list[str] = []
    for case in body.test_cases:
        wrapped = f"{case.input}\n{body.code}" if case.input else body.code
        sandbox = run_python_sandbox(wrapped, time_limit=5.0)
        outputs.append(sandbox.stdout)

    cases = [tc.model_dump() for tc in body.test_cases]
    results, score = grade_batch(outputs, cases)
    return BatchExecuteResponse(
        results=[BatchResultItem(**item) for item in results],
        score=score,
    )
