from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    email: str
    username: str
    full_name: str | None
    avatar_url: str | None
    python_level: str = Field(validation_alias="pytorch_level")
    daily_goal: int
    streak_count: int
    longest_streak: int
    last_active_date: date | None
    total_xp: int
    created_at: datetime


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    full_name: str | None = None
    python_level: str | None = Field(default=None, validation_alias="pytorch_level")
    daily_goal: int | None = Field(default=None, ge=1, le=50)
