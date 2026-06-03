from pydantic import BaseModel, Field


class RevisionDueItem(BaseModel):
    question_id: int
    title: str
    difficulty: str
    topic_slug: str
    topic_name: str
    module_number: int
    next_review_date: str
    days_overdue: int
    ease_factor: float
    interval_days: int


class RevisionStats(BaseModel):
    queue_size: int
    due_today: int
    overdue: int


class ReviewSubmit(BaseModel):
    question_id: int
    rating: int = Field(ge=0, le=5)


class ReviewResultOut(BaseModel):
    question_id: int
    next_review_date: str
    interval_days: int
    ease_factor: float
    xp_bonus: int = 0
