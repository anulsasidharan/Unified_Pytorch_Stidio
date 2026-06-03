"""Submission and attempt history routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.attempt import UserAttempt
from app.models.question import Question
from app.models.user import User
from app.schemas.questions import AttemptResponse, AttemptSubmit
from app.services.progress_service import process_attempt_submission

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("", response_model=AttemptResponse, status_code=201)
async def submit_attempt(
    body: AttemptSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptResponse:
    result = await db.execute(select(Question).where(Question.id == body.question_id))
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    count_result = await db.execute(
        select(func.count())
        .select_from(UserAttempt)
        .where(UserAttempt.user_id == user.id, UserAttempt.question_id == body.question_id)
    )
    attempt_number = count_result.scalar_one() + 1

    side_effects = await process_attempt_submission(
        db,
        user,
        question,
        result=body.result,
        hints_used=body.hints_used,
        time_spent_secs=body.time_spent_secs,
    )

    attempt = UserAttempt(
        user_id=user.id,
        question_id=body.question_id,
        submitted_code=body.code,
        result=body.result,
        time_spent_secs=body.time_spent_secs,
        hints_used=body.hints_used,
        attempt_number=attempt_number,
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)

    return AttemptResponse(
        id=attempt.id,
        result=body.result,
        xp_earned=side_effects["xp_earned"],
        added_to_revision=side_effects["added_to_revision"],
        message="Attempt recorded",
    )


@router.get("")
async def list_attempts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    offset = (page - 1) * limit
    result = await db.execute(
        select(UserAttempt)
        .where(UserAttempt.user_id == user.id)
        .order_by(UserAttempt.attempted_at.desc())
        .offset(offset)
        .limit(limit)
    )
    attempts = result.scalars().all()
    return {
        "items": [
            {
                "id": a.id,
                "question_id": a.question_id,
                "result": a.result,
                "time_spent_secs": a.time_spent_secs,
                "attempt_number": a.attempt_number,
                "attempted_at": a.attempted_at.isoformat(),
            }
            for a in attempts
        ],
        "page": page,
        "limit": limit,
    }


@router.get("/question/{question_id}")
async def attempts_for_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict]:
    result = await db.execute(
        select(UserAttempt)
        .where(UserAttempt.user_id == user.id, UserAttempt.question_id == question_id)
        .order_by(UserAttempt.attempted_at.desc())
    )
    return [
        {
            "id": a.id,
            "result": a.result,
            "submitted_code": a.submitted_code,
            "time_spent_secs": a.time_spent_secs,
            "attempt_number": a.attempt_number,
            "attempted_at": a.attempted_at.isoformat(),
        }
        for a in result.scalars().all()
    ]
