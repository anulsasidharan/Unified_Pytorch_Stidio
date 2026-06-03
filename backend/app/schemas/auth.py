from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: str | None
    avatar_url: str | None
    pytorch_level: str
    daily_goal: int
    streak_count: int
    longest_streak: int
    last_active_date: date | None
    total_xp: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    pytorch_level: str | None = None
    daily_goal: int | None = Field(default=None, ge=1, le=50)
