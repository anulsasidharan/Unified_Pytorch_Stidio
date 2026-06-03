import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint(
            "difficulty IN ('basic', 'intermediate', 'advanced')",
            name="ck_questions_difficulty",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[str | None] = mapped_column(Text)
    starter_code: Mapped[str | None] = mapped_column(Text)
    expected_output: Mapped[str | None] = mapped_column(Text)
    expected_output_shape: Mapped[str | None] = mapped_column(String(200))
    pytorch_version: Mapped[str] = mapped_column(String(20), default="2.x")
    gpu_required: Mapped[bool] = mapped_column(Boolean, default=False)
    colab_link: Mapped[str | None] = mapped_column(String(1000))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    xp_reward: Mapped[int] = mapped_column(Integer, default=10)
    time_estimate_mins: Mapped[int] = mapped_column(Integer, default=15)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(100), default="internal")
    source_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    topic = relationship("Topic", back_populates="questions")
    solutions = relationship("Solution", back_populates="question")
    test_cases = relationship("TestCase", back_populates="question")
    attempts = relationship("UserAttempt", back_populates="question")
    revision_items = relationship("RevisionQueue", back_populates="question")
    notes = relationship("UserNote", back_populates="question")


class Solution(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(20), default="python")
    explanation: Mapped[str | None] = mapped_column(Text)
    time_complexity: Mapped[str | None] = mapped_column(String(100))
    space_complexity: Mapped[str | None] = mapped_column(String(100))
    is_optimal: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    question = relationship("Question", back_populates="solutions")


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    input_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    expected_output: Mapped[dict] = mapped_column(JSONB, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer, default=1)

    question = relationship("Question", back_populates="test_cases")


class UserNote(Base):
    __tablename__ = "user_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("questions.id")
    )
    topic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("topics.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    note_type: Mapped[str] = mapped_column(String(20), default="personal")
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="notes")
    question = relationship("Question", back_populates="notes")


class CustomQuestion(Base):
    __tablename__ = "custom_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("topics.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    difficulty: Mapped[str | None] = mapped_column(String(20))
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    solution_code: Mapped[str | None] = mapped_column(Text)
    colab_link: Mapped[str | None] = mapped_column(String(1000))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    is_shared: Mapped[bool] = mapped_column(Boolean, default=False)
    import_source: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="custom_questions")
