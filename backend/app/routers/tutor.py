"""AI tutor chat routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.redis_client import get_redis
from app.database import get_db
from app.deps import get_current_user
from app.models.question import Question
from app.models.user import User
from app.schemas.tutor import TutorChatRequest, TutorChatResponse, TutorMessageOut, TutorUsageOut
from app.services.tutor_service import TutorRateLimitError, TutorService

router = APIRouter(prefix="/tutor", tags=["tutor"])
tutor_service = TutorService()


@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(
    body: TutorChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TutorChatResponse:
    redis = await get_redis()
    exercise_context = None

    if body.question_id is not None:
        result = await db.execute(
            select(Question)
            .options(joinedload(Question.topic))
            .where(Question.id == body.question_id)
        )
        question = result.scalar_one_or_none()
        if question is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        module_name = question.topic.name if question.topic else "Unknown"
        exercise_context = tutor_service.build_exercise_context(
            module_name=module_name,
            question_title=question.title,
            difficulty=question.difficulty,
            question_type=question.question_type,
            problem_statement=question.problem_statement,
            user_code=body.user_code or question.starter_code or "",
            error_message=body.error_message or "",
        )

    try:
        result = await tutor_service.chat(
            redis,
            user.id,
            body.message,
            exercise_context=exercise_context,
        )
    except TutorRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Daily tutor message limit reached",
                "messages_today": exc.used,
                "daily_limit": exc.limit,
            },
        ) from exc

    msg = result["message"]
    usage = result["usage"]
    return TutorChatResponse(
        message=TutorMessageOut(**msg),
        usage=TutorUsageOut(**usage),
    )


@router.get("/history")
async def tutor_history(
    user: User = Depends(get_current_user),
    limit: int = 50,
) -> dict:
    redis = await get_redis()
    messages = await tutor_service.get_history(redis, user.id, limit=min(limit, 50))
    return {"messages": messages}


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_tutor_history(user: User = Depends(get_current_user)) -> None:
    redis = await get_redis()
    await tutor_service.clear_history(redis, user.id)


@router.get("/usage", response_model=TutorUsageOut)
async def tutor_usage(user: User = Depends(get_current_user)) -> TutorUsageOut:
    redis = await get_redis()
    usage = await tutor_service.get_usage(redis, user.id)
    return TutorUsageOut(**usage)
