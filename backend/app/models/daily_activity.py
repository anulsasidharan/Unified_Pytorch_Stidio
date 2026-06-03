import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, TEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DailyActivity(Base):
    __tablename__ = "daily_activity"
    __table_args__ = (
        UniqueConstraint("user_id", "activity_date", name="uq_daily_activity"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    exercises_done: Mapped[int] = mapped_column(Integer, default=0)
    exercises_correct: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_secs: Mapped[int] = mapped_column(Integer, default=0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    modules_touched: Mapped[list[str] | None] = mapped_column(ARRAY(TEXT))
    streak_day: Mapped[int] = mapped_column(Integer, default=0)
    goal_met: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="daily_activities")
