"""Validate required environment variables at startup (production)."""

from __future__ import annotations

import logging
import sys

from app.config import Settings

logger = logging.getLogger(__name__)

INSECURE_SECRET_VALUES = {
    "change-me-in-production-min-32-chars",
    "change-me-in-docker-use-a-long-random-string",
    "your-secret-key",
    "change-me",
}


def validate_settings(settings: Settings) -> list[str]:
    """Return list of validation errors (empty if OK)."""
    errors: list[str] = []

    if settings.app_env == "production":
        if not settings.secret_key or len(settings.secret_key) < 32:
            errors.append("SECRET_KEY must be at least 32 characters in production")
        elif settings.secret_key.lower() in INSECURE_SECRET_VALUES:
            errors.append("SECRET_KEY must not use a default/example value in production")

        if not settings.database_url or "localhost" in settings.database_url:
            errors.append("DATABASE_URL must point to a managed database in production")

        if not settings.redis_url:
            errors.append("REDIS_URL is required in production")

        has_tutor = bool(settings.openai_api_key.strip() or settings.anthropic_api_key.strip())
        if not has_tutor:
            logger.warning(
                "No OPENAI_API_KEY or ANTHROPIC_API_KEY set — tutor will use offline fallback"
            )

    return errors


def enforce_production_env(settings: Settings) -> None:
    errors = validate_settings(settings)
    if errors:
        for err in errors:
            logger.error("ENV validation: %s", err)
        sys.exit(1)
