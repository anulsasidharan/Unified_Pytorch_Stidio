"""JWT auth routes — register, login, logout, refresh, GET/PUT /auth/me."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_client import get_redis
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    parse_user_id_from_token,
    verify_password,
)
from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfile,
    UserProfileUpdate,
)

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_PREFIX = "refresh:"


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    existing = await db.execute(
        select(User).where((User.email == body.email) | (User.username == body.username))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username taken")

    user = User(
        email=body.email.lower(),
        username=body.username,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == body.email.lower()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest) -> TokenResponse:
    redis = await get_redis()
    if await redis.get(f"{REFRESH_PREFIX}{body.refresh_token}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    try:
        user_id = parse_user_id_from_token(body.refresh_token, expected_type="refresh")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    return TokenResponse(
        access_token=create_access_token(str(user_id)),
        refresh_token=create_refresh_token(str(user_id)),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: RefreshRequest,
    _user: User = Depends(get_current_user),
) -> None:
    redis = await get_redis()
    from app.config import get_settings

    settings = get_settings()
    ttl = settings.jwt_refresh_token_expire_days * 86400
    await redis.setex(f"{REFRESH_PREFIX}{body.refresh_token}", ttl, "1")


@router.get("/me", response_model=UserProfile)
async def get_me(user: User = Depends(get_current_user)) -> User:
    return user


@router.put("/me", response_model=UserProfile)
async def update_me(
    body: UserProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    if body.full_name is not None:
        user.full_name = body.full_name
    if body.pytorch_level is not None:
        user.pytorch_level = body.pytorch_level
    if body.daily_goal is not None:
        user.daily_goal = body.daily_goal
    await db.commit()
    await db.refresh(user)
    return user
