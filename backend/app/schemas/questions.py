from pydantic import BaseModel


class TestCaseOut(BaseModel):
    id: int
    input_data: dict
    expected_output: dict
    explanation: str | None
    is_hidden: bool
    order_index: int

    model_config = {"from_attributes": True}


class QuestionListItem(BaseModel):
    id: int
    topic_id: int
    topic_slug: str | None = None
    title: str
    slug: str
    difficulty: str
    question_type: str
    xp_reward: int
    time_estimate_mins: int
    gpu_required: bool
    tags: list[str] | None = None

    model_config = {"from_attributes": True}


class QuestionDetail(BaseModel):
    id: int
    topic_id: int
    topic_slug: str
    topic_name: str | None = None
    title: str
    slug: str
    difficulty: str
    question_type: str
    problem_statement: str
    constraints: str | None
    starter_code: str | None
    expected_output: str | None = None
    expected_output_type: str = "exact"
    expected_output_shape: str | None
    run_in_browser: bool = True
    pep8_required: bool = False
    gpu_required: bool
    colab_link: str | None
    pytorch_version: str
    tags: list[str] | None
    xp_reward: int
    time_estimate_mins: int
    hints: list[str] = []

    model_config = {"from_attributes": True}


class SolutionOut(BaseModel):
    id: int
    title: str
    code: str
    explanation: str | None
    is_optimal: bool
    order_index: int

    model_config = {"from_attributes": True}


class AttemptSubmit(BaseModel):
    question_id: int
    code: str | None = None
    result: str
    time_spent_secs: int = 0
    hints_used: int = 0


class AttemptResponse(BaseModel):
    id: int
    result: str
    xp_earned: int = 0
    runtime_ms: int | None = None
    error_message: str | None = None
    added_to_revision: bool = False
    message: str = "Attempt recorded"
