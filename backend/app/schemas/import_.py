"""Pydantic schemas for import and custom questions."""

from datetime import datetime

from pydantic import BaseModel, Field


class ManualImportRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    topic_slug: str | None = None
    difficulty: str | None = "intermediate"
    problem_statement: str = Field(..., min_length=1)
    solution_code: str | None = None
    colab_link: str | None = None
    tags: list[str] | None = None
    is_shared: bool = False
    preview: bool = False


class JsonImportRequest(BaseModel):
    questions: list[dict]
    preview: bool = False


class NotebookImportRequest(BaseModel):
    url: str = Field(..., min_length=10)
    topic_slug: str | None = None
    title: str | None = None
    is_shared: bool = False
    preview: bool = False


class CustomQuestionOut(BaseModel):
    id: int
    title: str
    topic_id: int | None
    topic_slug: str | None = None
    difficulty: str | None
    problem_statement: str
    solution_code: str | None
    colab_link: str | None
    tags: list[str] | None
    is_shared: bool
    import_source: str | None
    created_at: datetime
    author_username: str | None = None

    model_config = {"from_attributes": True}


class CustomQuestionUpdate(BaseModel):
    title: str | None = None
    topic_slug: str | None = None
    difficulty: str | None = None
    problem_statement: str | None = None
    solution_code: str | None = None
    colab_link: str | None = None
    tags: list[str] | None = None
    is_shared: bool | None = None


class ImportResultItem(BaseModel):
    title: str
    status: str
    id: int | None = None
    error: str | None = None


class ImportResponse(BaseModel):
    import_source: str
    total: int
    created: int
    failed: int
    preview: bool
    items: list[ImportResultItem]
    questions: list[CustomQuestionOut] | None = None


class ImportHistoryEntry(BaseModel):
    import_source: str
    imported_at: datetime
    questions_count: int
    status: str


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)
    question_id: int | None = None
    topic_id: int | None = None
    note_type: str = "personal"
    tags: list[str] | None = None


class NoteUpdate(BaseModel):
    content: str | None = None
    note_type: str | None = None
    tags: list[str] | None = None


class NoteOut(BaseModel):
    id: int
    question_id: int | None
    topic_id: int | None
    content: str
    note_type: str
    tags: list[str] | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
