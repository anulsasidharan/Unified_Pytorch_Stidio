from pydantic import BaseModel, Field


class ProjectSpec(BaseModel):
    slug: str
    module_name: str
    title: str
    description: str
    starter_code: str
    requirements: list[str]


class ProjectSubmissionOut(BaseModel):
    code: str
    score: int
    is_passed: bool
    feedback: str | None
    pep8_score: int | None
    stdout: str | None
    stderr: str | None
    submitted_at: str

    model_config = {"from_attributes": True}


class ModuleProjectResponse(BaseModel):
    spec: ProjectSpec
    submission: ProjectSubmissionOut | None = None


class ProjectSubmitRequest(BaseModel):
    code: str = Field(..., min_length=1)


class ProjectSubmitResponse(BaseModel):
    score: int
    is_passed: bool
    feedback: str | None
    pep8_score: int | None
    stdout: str | None
    stderr: str | None
