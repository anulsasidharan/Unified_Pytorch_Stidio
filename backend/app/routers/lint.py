"""PEP 8 linting API."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.linter import lint_code

router = APIRouter(prefix="/lint", tags=["lint"])


class LintRequest(BaseModel):
    code: str


class LintResponse(BaseModel):
    violations: list[dict]
    score: int


@router.post("", response_model=LintResponse)
async def lint(body: LintRequest) -> LintResponse:
    result = lint_code(body.code)
    return LintResponse(violations=result.violations, score=result.score)
