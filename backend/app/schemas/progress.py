from pydantic import BaseModel


class ProgressTotals(BaseModel):
    questions_attempted: int = 0
    questions_solved: int = 0
    completion_pct: float = 0.0


class ModuleProgress(BaseModel):
    topic_id: int
    slug: str
    name: str
    icon: str | None = None
    color: str | None = None
    module_number: int
    total_questions: int
    questions_attempted: int = 0
    questions_solved: int = 0
    completion_pct: float = 0.0
    basic_solved: int = 0
    intermediate_solved: int = 0
    advanced_solved: int = 0


class ProgressSummary(BaseModel):
    modules: list[ModuleProgress]
    totals: ProgressTotals


class TopicProgressDetail(BaseModel):
    topic_id: int
    slug: str
    name: str
    total_questions: int
    questions_attempted: int = 0
    questions_solved: int = 0
    completion_pct: float = 0.0
    basic_solved: int = 0
    intermediate_solved: int = 0
    advanced_solved: int = 0
    total_time_spent_secs: int = 0
