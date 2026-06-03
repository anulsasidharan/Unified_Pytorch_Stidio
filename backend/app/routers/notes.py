"""User notes CRUD routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.question import UserNote
from app.models.user import User
from app.schemas.import_ import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

VALID_NOTE_TYPES = {"personal", "insight", "gotcha"}


@router.get("", response_model=list[NoteOut])
async def list_notes(
    question_id: int | None = Query(None),
    topic_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[NoteOut]:
    stmt = select(UserNote).where(UserNote.user_id == user.id)
    if question_id is not None:
        stmt = stmt.where(UserNote.question_id == question_id)
    if topic_id is not None:
        stmt = stmt.where(UserNote.topic_id == topic_id)
    stmt = stmt.order_by(UserNote.updated_at.desc())
    result = await db.execute(stmt)
    return [NoteOut.model_validate(n) for n in result.scalars().all()]


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    body: NoteCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteOut:
    if body.question_id is None and body.topic_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either question_id or topic_id is required",
        )
    if body.note_type not in VALID_NOTE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"note_type must be one of: {', '.join(sorted(VALID_NOTE_TYPES))}",
        )

    note = UserNote(
        user_id=user.id,
        question_id=body.question_id,
        topic_id=body.topic_id,
        content=body.content.strip(),
        note_type=body.note_type,
        tags=body.tags,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return NoteOut.model_validate(note)


@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    body: NoteUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteOut:
    result = await db.execute(
        select(UserNote).where(UserNote.id == note_id, UserNote.user_id == user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if body.content is not None:
        note.content = body.content.strip()
    if body.note_type is not None:
        if body.note_type not in VALID_NOTE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"note_type must be one of: {', '.join(sorted(VALID_NOTE_TYPES))}",
            )
        note.note_type = body.note_type
    if body.tags is not None:
        note.tags = body.tags

    await db.commit()
    await db.refresh(note)
    return NoteOut.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(UserNote).where(UserNote.id == note_id, UserNote.user_id == user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    await db.delete(note)
    await db.commit()
