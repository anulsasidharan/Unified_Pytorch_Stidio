"""Google Colab notebook launch routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.question import Question
from app.services.colab_service import resolve_colab_url

router = APIRouter(prefix="/colab", tags=["colab"])


@router.get("/{question_id}")
async def get_colab_url(question_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(
        select(Question)
        .options(joinedload(Question.topic))
        .where(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    module_name = question.topic.name if question.topic else "PyTorch Studio"
    colab = resolve_colab_url(question, module_name)

    return {
        "question_id": question_id,
        "colab_url": colab.colab_url,
        "nbviewer_url": colab.nbviewer_url,
        "source": colab.source,
        "gpu_required": question.gpu_required,
        "message": None if colab.source == "stored" else "Notebook generated from exercise content",
    }


@router.post("/import")
async def import_notebook() -> dict:
    return {"status": "not_implemented", "message": "Notebook import ships in Phase 4"}
