from pydantic import BaseModel, Field


class TutorChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    question_id: int | None = None
    user_code: str | None = None
    error_message: str | None = None


class TutorMessageOut(BaseModel):
    role: str
    content: str
    timestamp: str


class TutorUsageOut(BaseModel):
    messages_today: int
    daily_limit: int
    remaining: int
    resets_at: str


class TutorChatResponse(BaseModel):
    message: TutorMessageOut
    usage: TutorUsageOut
