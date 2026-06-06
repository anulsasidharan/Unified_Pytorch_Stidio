from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    username: str
    xp: int
    exercises_solved: int = 0


class LeaderboardOut(BaseModel):
    period: str
    entries: list[LeaderboardEntry]
    updated_at: str
