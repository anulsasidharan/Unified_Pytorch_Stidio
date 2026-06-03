import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_user_progress"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    questions_attempted: Mapped[int] = mapped_column(Integer, default=0)
    questions_solved: Mapped[int] = mapped_column(Integer, default=0)
    basic_solved: Mapped[int] = mapped_column(Integer, default=0)
    intermediate_solved: Mapped[int] = mapped_column(Integer, default=0)
    advanced_solved: Mapped[int] = mapped_column(Integer, default=0)
    total_time_spent_secs: Mapped[int] = mapped_column(Integer, default=0)
    completion_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"))
    last_attempted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user = relationship("User", back_populates="progress")
    topic = relationship("Topic", back_populates="progress")
