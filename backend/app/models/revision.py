import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RevisionQueue(Base):
    __tablename__ = "revision_queue"
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_revision_queue"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    ease_factor: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=Decimal("2.50"))
    interval_days: Mapped[int] = mapped_column(Integer, default=1)
    repetition_count: Mapped[int] = mapped_column(Integer, default=0)
    next_review_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_result: Mapped[str | None] = mapped_column(String(20))

    user = relationship("User", back_populates="revision_items")
    question = relationship("Question", back_populates="revision_items")
