"""Module-level routes — end-of-module projects."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user, get_optional_user
from app.models.topic import Topic
from app.models.user import User
from app.schemas.modules import (
    ModuleProjectResponse,
    ProjectSpec,
    ProjectSubmissionOut,
    ProjectSubmitRequest,
    ProjectSubmitResponse,
)
from app.services.project_service import get_project_spec, get_user_submission, upsert_submission

router = APIRouter(prefix="/modules", tags=["modules"])


async def _load_topic(db: AsyncSession, slug: str) -> Topic:
    result = await db.execute(
        select(Topic).where(Topic.slug == slug, Topic.is_active.is_(True))
    )
    topic = result.scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return topic


def _submission_out(sub) -> ProjectSubmissionOut:
    return ProjectSubmissionOut(
        code=sub.code,
        score=sub.score,
        is_passed=sub.is_passed,
        feedback=sub.feedback,
        pep8_score=sub.pep8_score,
        stdout=sub.stdout,
        stderr=sub.stderr,
        submitted_at=sub.submitted_at.isoformat(),
    )


@router.get("/{slug}/project", response_model=ModuleProjectResponse)
async def get_module_project(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> ModuleProjectResponse:
    topic = await _load_topic(db, slug)
    spec_data = get_project_spec(slug, topic.name)
    if spec_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No project defined for this module",
        )

    submission = None
    if user is not None:
        sub = await get_user_submission(db, user.id, topic.id)
        if sub is not None:
            submission = _submission_out(sub)

    return ModuleProjectResponse(spec=ProjectSpec(**spec_data), submission=submission)


@router.post("/{slug}/project", response_model=ProjectSubmitResponse)
async def submit_module_project(
    slug: str,
    body: ProjectSubmitRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProjectSubmitResponse:
    topic = await _load_topic(db, slug)
    spec_data = get_project_spec(slug, topic.name)
    if spec_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No project defined for this module",
        )

    submission = await upsert_submission(db, user.id, topic, body.code)
    return ProjectSubmitResponse(
        score=submission.score,
        is_passed=submission.is_passed,
        feedback=submission.feedback,
        pep8_score=submission.pep8_score,
        stdout=submission.stdout,
        stderr=submission.stderr,
    )
