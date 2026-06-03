"""Topic/module routes — list and detail by slug."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_optional_user
from app.models.attempt import UserAttempt
from app.models.progress import UserProgress
from app.models.question import Question
from app.models.topic import Topic
from app.models.user import User
from app.schemas.topics import QuestionSummary, TopicDetail, TopicListItem, TopicProgressSummary

router = APIRouter(prefix="/topics", tags=["topics"])


def _progress_summary(progress: UserProgress | None) -> TopicProgressSummary | None:
    if progress is None:
        return None
    return TopicProgressSummary(
        questions_attempted=progress.questions_attempted,
        questions_solved=progress.questions_solved,
        completion_pct=float(progress.completion_pct or Decimal("0")),
    )


async def _get_topic_by_slug(slug: str, db: AsyncSession) -> Topic:
    result = await db.execute(select(Topic).where(Topic.slug == slug, Topic.is_active.is_(True)))
    topic = result.scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return topic


@router.get("", response_model=list[TopicListItem])
async def list_topics(
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> list[TopicListItem]:
    result = await db.execute(
        select(Topic).where(Topic.is_active.is_(True)).order_by(Topic.order_index)
    )
    topics = result.scalars().all()

    progress_map: dict[int, UserProgress] = {}
    if user:
        prog_result = await db.execute(
            select(UserProgress).where(UserProgress.user_id == user.id)
        )
        progress_map = {p.topic_id: p for p in prog_result.scalars().all()}

    return [
        TopicListItem(
            id=t.id,
            module_number=t.module_number,
            name=t.name,
            slug=t.slug,
            description=t.description,
            icon=t.icon,
            color=t.color,
            total_questions=t.total_questions,
            progress=_progress_summary(progress_map.get(t.id)),
        )
        for t in topics
    ]


@router.get("/{slug}", response_model=TopicDetail)
async def get_topic(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> TopicDetail:
    topic = await _get_topic_by_slug(slug, db)

    questions_result = await db.execute(
        select(Question)
        .where(Question.topic_id == topic.id, Question.is_published.is_(True))
        .order_by(Question.id)
    )
    questions = questions_result.scalars().all()

    solved_ids: set[int] = set()
    if user and questions:
        solved_result = await db.execute(
            select(UserAttempt.question_id)
            .where(
                UserAttempt.user_id == user.id,
                UserAttempt.result == "correct",
                UserAttempt.question_id.in_([q.id for q in questions]),
            )
            .distinct()
        )
        solved_ids = set(solved_result.scalars().all())

    progress = None
    if user:
        prog_result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user.id,
                UserProgress.topic_id == topic.id,
            )
        )
        progress = _progress_summary(prog_result.scalar_one_or_none())

    return TopicDetail(
        id=topic.id,
        module_number=topic.module_number,
        name=topic.name,
        slug=topic.slug,
        description=topic.description,
        icon=topic.icon,
        color=topic.color,
        total_questions=topic.total_questions,
        progress=progress,
        questions=[
            QuestionSummary(
                id=q.id,
                title=q.title,
                slug=q.slug,
                difficulty=q.difficulty,
                question_type=q.question_type,
                xp_reward=q.xp_reward,
                time_estimate_mins=q.time_estimate_mins,
                gpu_required=q.gpu_required,
                tags=q.tags,
                solved=q.id in solved_ids,
            )
            for q in questions
        ],
    )


@router.get("/{slug}/progress", response_model=TopicProgressSummary)
async def get_topic_progress(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> TopicProgressSummary:
    if user is None:
        return TopicProgressSummary()

    topic = await _get_topic_by_slug(slug, db)
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.topic_id == topic.id,
        )
    )
    progress = result.scalar_one_or_none()
    return _progress_summary(progress) or TopicProgressSummary()
