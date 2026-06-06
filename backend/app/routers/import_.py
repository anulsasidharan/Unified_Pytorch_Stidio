"""External question import and custom question routes."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.deps import get_current_user, get_optional_user
from app.models.question import CustomQuestion
from app.models.topic import Topic
from app.models.user import User
from app.schemas.import_ import (
    CustomQuestionOut,
    CustomQuestionUpdate,
    ImportHistoryEntry,
    ImportResponse,
    ImportResultItem,
    JsonImportRequest,
    ManualImportRequest,
    NotebookImportRequest,
)
from app.services.import_service import (
    ImportRowResult,
    ImportValidationError,
    ParsedQuestion,
    build_import_history,
    custom_question_to_dict,
    extract_notebook_fields,
    fetch_notebook_json,
    list_custom_questions,
    parse_csv_content,
    parse_json_payload,
    parse_py_content,
    persist_custom_questions,
    resolve_topic_id,
)

router = APIRouter(tags=["import"])


def _build_import_response(
    import_source: str,
    results: list,
    preview: bool,
    saved: list[CustomQuestion] | None = None,
    slug_map: dict[int, str] | None = None,
) -> ImportResponse:
    items = [
        ImportResultItem(
            title=r.title,
            status=r.status,
            id=r.question_id,
            error=r.error,
        )
        for _, r in results
    ]
    created = sum(1 for i in items if i.status == "created")
    failed = sum(1 for i in items if i.status == "failed")
    questions_out = None
    if saved and slug_map is not None:
        questions_out = [
            CustomQuestionOut(**custom_question_to_dict(q, slug_map.get(q.topic_id)))
            for q in saved
        ]
    return ImportResponse(
        import_source=import_source,
        total=len(items),
        created=created,
        failed=failed,
        preview=preview,
        items=items,
        questions=questions_out,
    )


@router.post("/import/manual", response_model=ImportResponse)
async def import_manual(
    body: ManualImportRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImportResponse:
    try:
        item = ParsedQuestion(
            title=body.title.strip(),
            topic_slug=body.topic_slug,
            difficulty=body.difficulty,
            problem_statement=body.problem_statement.strip(),
            solution_code=body.solution_code,
            colab_link=body.colab_link,
            tags=body.tags,
        )
        if body.preview:
            return _build_import_response(
                "manual",
                [(None, ImportRowResult(title=item.title, status="preview"))],
                preview=True,
            )
        results = await persist_custom_questions(
            db, user, [item], "manual", is_shared=body.is_shared
        )
        saved = [r[0] for r in results if r[0] is not None]
        slug_map = {}
        if saved and saved[0].topic_id:
            t = await db.get(Topic, saved[0].topic_id)
            if t:
                slug_map[t.id] = t.slug
        return _build_import_response("manual", results, False, saved, slug_map)
    except ImportValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/import/json", response_model=ImportResponse)
async def import_json(
    body: JsonImportRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImportResponse:
    try:
        items = parse_json_payload({"questions": body.questions})
        if body.preview:
            preview_results = [(None, ImportRowResult(title=i.title, status="preview")) for i in items]
            return _build_import_response("json", preview_results, preview=True)
        results = await persist_custom_questions(db, user, items, "json")
        saved = [r[0] for r in results if r[0] is not None]
        slug_map = await _topic_slug_map(db, saved)
        return _build_import_response("json", results, False, saved, slug_map)
    except ImportValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/import/csv", response_model=ImportResponse)
async def import_csv(
    file: UploadFile = File(...),
    preview: bool = False,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImportResponse:
    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CSV must be UTF-8 encoded"
        ) from exc

    try:
        items = parse_csv_content(text)
        if preview:
            preview_results = [(None, ImportRowResult(title=i.title, status="preview")) for i in items]
            return _build_import_response("csv", preview_results, preview=True)
        results = await persist_custom_questions(db, user, items, "csv")
        saved = [r[0] for r in results if r[0] is not None]
        slug_map = await _topic_slug_map(db, saved)
        return _build_import_response("csv", results, False, saved, slug_map)
    except ImportValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/import/py", response_model=ImportResponse)
async def import_py(
    file: UploadFile = File(...),
    preview: bool = False,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImportResponse:
    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=".py file must be UTF-8 encoded"
        ) from exc

    try:
        items = parse_py_content(text)
        if preview:
            preview_results = [(None, ImportRowResult(title=i.title, status="preview")) for i in items]
            return _build_import_response("py", preview_results, preview=True)
        results = await persist_custom_questions(db, user, items, "py")
        saved = [r[0] for r in results if r[0] is not None]
        slug_map = await _topic_slug_map(db, saved)
        return _build_import_response("py", results, False, saved, slug_map)
    except ImportValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/import/notebook", response_model=ImportResponse)
async def import_notebook(
    body: NotebookImportRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImportResponse:
    try:
        nb_json = await fetch_notebook_json(body.url)
        parsed = extract_notebook_fields(nb_json, fallback_title=body.title)
        if body.topic_slug:
            parsed.topic_slug = body.topic_slug

        if body.preview:
            return _build_import_response(
                "notebook",
                [(None, ImportRowResult(title=parsed.title, status="preview"))],
                preview=True,
            )

        results = await persist_custom_questions(
            db,
            user,
            [parsed],
            "notebook",
            is_shared=body.is_shared,
            colab_link_override=body.url,
        )
        saved = [r[0] for r in results if r[0] is not None]
        slug_map = await _topic_slug_map(db, saved)
        return _build_import_response("notebook", results, False, saved, slug_map)
    except ImportValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/import/history", response_model=list[ImportHistoryEntry])
async def import_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ImportHistoryEntry]:
    entries = await build_import_history(db, user.id)
    return [ImportHistoryEntry(**e) for e in entries]


async def _topic_slug_map(db: AsyncSession, questions: list[CustomQuestion]) -> dict[int, str]:
    ids = {q.topic_id for q in questions if q.topic_id}
    if not ids:
        return {}
    result = await db.execute(select(Topic.id, Topic.slug).where(Topic.id.in_(ids)))
    return {tid: slug for tid, slug in result.all()}


@router.get("/custom-questions", response_model=list[CustomQuestionOut])
async def get_custom_questions(
    mine: bool = False,
    community: bool = False,
    user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
) -> list[CustomQuestionOut]:
    if mine and user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    rows = await list_custom_questions(
        db, user, mine_only=mine, community_only=community
    )
    return [CustomQuestionOut(**r) for r in rows]


@router.get("/custom-questions/{question_id}", response_model=CustomQuestionOut)
async def get_custom_question(
    question_id: int,
    user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
) -> CustomQuestionOut:
    result = await db.execute(
        select(CustomQuestion)
        .options(joinedload(CustomQuestion.user))
        .where(CustomQuestion.id == question_id)
    )
    q = result.scalar_one_or_none()
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if not q.is_shared and (user is None or q.user_id != user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    slug = None
    if q.topic_id:
        topic = await db.get(Topic, q.topic_id)
        slug = topic.slug if topic else None
    return CustomQuestionOut(
        **custom_question_to_dict(
            q, topic_slug=slug, author_username=q.user.username if q.user else None
        )
    )


@router.put("/custom-questions/{question_id}", response_model=CustomQuestionOut)
async def update_custom_question(
    question_id: int,
    body: CustomQuestionUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CustomQuestionOut:
    result = await db.execute(
        select(CustomQuestion).where(
            CustomQuestion.id == question_id, CustomQuestion.user_id == user.id
        )
    )
    q = result.scalar_one_or_none()
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    if body.title is not None:
        q.title = body.title
    if body.problem_statement is not None:
        q.problem_statement = body.problem_statement
    if body.solution_code is not None:
        q.solution_code = body.solution_code
    if body.colab_link is not None:
        q.colab_link = body.colab_link
    if body.tags is not None:
        q.tags = body.tags
    if body.difficulty is not None:
        q.difficulty = body.difficulty
    if body.is_shared is not None:
        q.is_shared = body.is_shared
    if body.topic_slug is not None:
        q.topic_id = await resolve_topic_id(db, body.topic_slug)

    await db.commit()
    await db.refresh(q)
    slug = None
    if q.topic_id:
        topic = await db.get(Topic, q.topic_id)
        slug = topic.slug if topic else None
    return CustomQuestionOut(**custom_question_to_dict(q, topic_slug=slug))


@router.delete("/custom-questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_question(
    question_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(CustomQuestion).where(
            CustomQuestion.id == question_id, CustomQuestion.user_id == user.id
        )
    )
    q = result.scalar_one_or_none()
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    await db.delete(q)
    await db.commit()
