from decimal import Decimal

from pydantic import BaseModel


class TopicProgressSummary(BaseModel):
    questions_attempted: int = 0
    questions_solved: int = 0
    completion_pct: float = 0.0


class TopicListItem(BaseModel):
    id: int
    module_number: int
    name: str
    slug: str
    description: str | None
    icon: str | None
    color: str | None
    total_questions: int
    progress: TopicProgressSummary | None = None

    model_config = {"from_attributes": True}


class QuestionSummary(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: str
    question_type: str
    xp_reward: int
    time_estimate_mins: int
    gpu_required: bool
    tags: list[str] | None = None
    solved: bool = False

    model_config = {"from_attributes": True}


class TopicDetail(TopicListItem):
    questions: list[QuestionSummary] = []
