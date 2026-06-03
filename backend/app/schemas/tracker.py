from pydantic import BaseModel


class TodaySummary(BaseModel):
    exercises_done: int = 0
    exercises_correct: int = 0
    xp_earned: int = 0
    time_spent_secs: int = 0
    goal: int = 5
    goal_met: bool = False


class StreakData(BaseModel):
    current: int = 0
    longest: int = 0
    last_active: str | None = None


class WeeklyDay(BaseModel):
    date: str
    exercises_done: int = 0
    xp_earned: int = 0


class DifficultyBreakdown(BaseModel):
    basic: int = 0
    intermediate: int = 0
    advanced: int = 0


class XpTimelinePoint(BaseModel):
    date: str
    cumulative_xp: int


class DashboardOut(BaseModel):
    today: TodaySummary
    streak: StreakData
    weekly: list[WeeklyDay]
    xp_this_week: int = 0
    total_xp: int = 0
    revision_due_today: int = 0
    difficulty_breakdown: DifficultyBreakdown
    xp_timeline: list[XpTimelinePoint] = []


class HeatmapCell(BaseModel):
    date: str
    count: int
    level: int


class HeatmapOut(BaseModel):
    cells: list[HeatmapCell]
    start_date: str
    end_date: str


class ActivityHistoryItem(BaseModel):
    activity_date: str
    exercises_done: int
    exercises_correct: int
    xp_earned: int
    time_spent_secs: int
    goal_met: bool
    streak_day: int
    modules_touched: list[str] = []


class ActivityHistoryOut(BaseModel):
    items: list[ActivityHistoryItem]
    page: int
    limit: int
