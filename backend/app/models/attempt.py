import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserAttempt(Base):
    __tablename__ = "user_attempts"
    __table_args__ = (
        CheckConstraint(
            "result IN ('correct', 'incorrect', 'partial', 'skipped')",
            name="ck_user_attempts_result",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    submitted_code: Mapped[str | None] = mapped_column(Text)
    result: Mapped[str | None] = mapped_column(String(20))
    runtime_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_secs: Mapped[int] = mapped_column(Integer, default=0)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")
