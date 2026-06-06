"""Question bank routes — list, filter, detail."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
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
    "Re-read the problem statement carefully before changing your approach.",
    "Add a print() call to inspect intermediate values at each step.",
    "Check the Python docs for the built-in function or method you are using.",
]


def _build_hints(question: Question) -> list[str]:
    if getattr(question, "hints", None):
        return list(question.hints)
    if question.constraints:
        return [question.constraints, *DEFAULT_HINTS[:2]]
    return DEFAULT_HINTS


@router.get("/search", response_model=list[QuestionListItem])
async def search_questions(
    q: str = Query(..., min_length=1, description="Search title, statement, or tags"),
    topic: str | None = Query(None, description="Topic slug filter"),
    difficulty: str | None = Query(None),
    question_type: str | None = Query(None, alias="type"),
    tag: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[QuestionListItem]:
    return await _list_questions_filtered(
        db,
        topic=topic,
        difficulty=difficulty,
        question_type=question_type,
        tag=tag,
        search=q,
        limit=limit,
    )


@router.get("", response_model=list[QuestionListItem])
async def list_questions(
    topic: str | None = Query(None, description="Topic slug filter"),
    difficulty: str | None = Query(None),
    question_type: str | None = Query(None, alias="type"),
    tag: str | None = Query(None),
    q: str | None = Query(None, description="Search title, statement, or tags"),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[QuestionListItem]:
    return await _list_questions_filtered(
        db,
        topic=topic,
        difficulty=difficulty,
        question_type=question_type,
        tag=tag,
        search=q,
        limit=limit,
    )


async def _list_questions_filtered(
    db: AsyncSession,
    *,
    topic: str | None,
    difficulty: str | None,
    question_type: str | None,
    tag: str | None,
    search: str | None,
    limit: int,
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
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                Question.title.ilike(pattern),
                Question.problem_statement.ilike(pattern),
                Question.slug.ilike(pattern),
                func.coalesce(func.array_to_string(Question.tags, ","), "").ilike(pattern),
            )
        )

    stmt = stmt.order_by(Topic.order_index, Question.id).limit(limit)
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
        select(Question, Topic.slug, Topic.name)
        .join(Topic, Question.topic_id == Topic.id)
        .where(Question.id == question_id, Question.is_published.is_(True))
    )
    row = result.one_or_none()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    question, topic_slug, topic_name = row
    return QuestionDetail(
        id=question.id,
        topic_id=question.topic_id,
        topic_slug=topic_slug,
        topic_name=topic_name,
        title=question.title,
        slug=question.slug,
        difficulty=question.difficulty,
        question_type=question.question_type,
        problem_statement=question.problem_statement,
        constraints=question.constraints,
        starter_code=question.starter_code,
        expected_output=question.expected_output,
        expected_output_type=getattr(question, "expected_output_type", "exact") or "exact",
        expected_output_shape=question.expected_output_shape,
        run_in_browser=getattr(question, "run_in_browser", True),
        pep8_required=getattr(question, "pep8_required", False),
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
