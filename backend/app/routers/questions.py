"""Question bank routes — list, filter, detail."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user, get_optional_user
from app.models.attempt import UserAttempt
from app.models.question import Question, Solution, TestCase
from app.models.topic import Topic
from app.models.user import User
from app.schemas.questions import QuestionDetail, QuestionListItem, SolutionOut, TestCaseOut

router = APIRouter(prefix="/questions", tags=["questions"])

DEFAULT_HINTS = [
    "Re-read the problem constraints before changing your approach.",
    "Print tensor `.shape` and `.dtype` at each step to debug mismatches.",
    "Check the PyTorch docs for the function signature you are using.",
]


def _build_hints(question: Question) -> list[str]:
    if question.constraints:
        return [question.constraints, *DEFAULT_HINTS[:2]]
    return DEFAULT_HINTS


@router.get("", response_model=list[QuestionListItem])
async def list_questions(
    topic: str | None = Query(None, description="Topic slug filter"),
    difficulty: str | None = Query(None),
    question_type: str | None = Query(None, alias="type"),
    tag: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[QuestionListItem]:
    stmt = (
        select(Question, Topic.slug)
        .join(Topic, Question.topic_id == Topic.id)
        .where(Question.is_published.is_(True), Topic.is_active.is_(True))
    )
    if topic:
        stmt = stmt.where(Topic.slug == topic)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)
    if question_type:
        stmt = stmt.where(Question.question_type == question_type)
    if tag:
        stmt = stmt.where(Question.tags.contains([tag]))

    stmt = stmt.order_by(Topic.order_index, Question.id)
    result = await db.execute(stmt)
    rows = result.all()

    return [
        QuestionListItem(
            id=q.id,
            topic_id=q.topic_id,
            topic_slug=slug,
            title=q.title,
            slug=q.slug,
            difficulty=q.difficulty,
            question_type=q.question_type,
            xp_reward=q.xp_reward,
            time_estimate_mins=q.time_estimate_mins,
            gpu_required=q.gpu_required,
            tags=q.tags,
        )
        for q, slug in rows
    ]


@router.get("/bookmarked", response_model=list[QuestionListItem])
async def bookmarked_questions(
    _user: User = Depends(get_current_user),
) -> list[QuestionListItem]:
    return []


@router.get("/{question_id}", response_model=QuestionDetail)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)) -> QuestionDetail:
    result = await db.execute(
        select(Question, Topic.slug)
        .join(Topic, Question.topic_id == Topic.id)
        .where(Question.id == question_id, Question.is_published.is_(True))
    )
    row = result.one_or_none()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    question, topic_slug = row
    return QuestionDetail(
        id=question.id,
        topic_id=question.topic_id,
        topic_slug=topic_slug,
        title=question.title,
        slug=question.slug,
        difficulty=question.difficulty,
        question_type=question.question_type,
        problem_statement=question.problem_statement,
        constraints=question.constraints,
        starter_code=question.starter_code,
        expected_output_shape=question.expected_output_shape,
        gpu_required=question.gpu_required,
        colab_link=question.colab_link or None,
        pytorch_version=question.pytorch_version,
        tags=question.tags,
        xp_reward=question.xp_reward,
        time_estimate_mins=question.time_estimate_mins,
        hints=_build_hints(question),
    )


@router.get("/{question_id}/test-cases", response_model=list[TestCaseOut])
async def get_test_cases(question_id: int, db: AsyncSession = Depends(get_db)) -> list[TestCaseOut]:
    result = await db.execute(
        select(TestCase)
        .where(TestCase.question_id == question_id, TestCase.is_hidden.is_(False))
        .order_by(TestCase.order_index)
    )
    return list(result.scalars().all())


@router.get("/{question_id}/solution", response_model=list[SolutionOut])
async def get_solution(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> list[SolutionOut]:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")

    count = (await db.execute(
        select(func.count())
        .select_from(UserAttempt)
        .where(UserAttempt.user_id == user.id, UserAttempt.question_id == question_id)
    )).scalar_one()
    if count < 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete at least one attempt before viewing the solution",
        )

    result = await db.execute(
        select(Solution)
        .where(Solution.question_id == question_id)
        .order_by(Solution.order_index)
    )
    solutions = list(result.scalars().all())
    if not solutions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No solution published")
    return solutions


@router.post("/{question_id}/bookmark", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_bookmark(
    question_id: int,
    _user: User = Depends(get_current_user),
) -> None:
    pass
