"""Google Colab notebook launch routes (Phase 1 stub)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models.question import Question

router = APIRouter(prefix="/colab", tags=["colab"])
settings = get_settings()


@router.get("/{question_id}")
async def get_colab_url(question_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    if question.colab_link:
        url = question.colab_link
        source = "stored"
    else:
        url = (
            f"{settings.colab_notebook_base_url}"
            "create=true&hl=en#scrollTo=stub"
            f"&question_id={question_id}"
        )
        source = "generated_stub"

    return {
        "question_id": question_id,
        "colab_url": url,
        "nbviewer_url": None,
        "source": source,
        "message": "Full notebook generation ships in Phase 2",
    }


@router.post("/import")
async def import_notebook() -> dict:
    return {"status": "not_implemented", "message": "Notebook import ships in Phase 4"}
