from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "pytorch-learning-studio"
    app_env: str = "development"
    app_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    secret_key: str = "change-me-in-production-min-32-chars"

    database_url: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio"
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    anthropic_api_key: str = ""
    tutor_model: str = "claude-sonnet-4-20250514"
    tutor_max_tokens: int = 2048
    tutor_daily_limit_free: int = 20

    aws_region: str = "ca-central-1"
    aws_s3_bucket: str = "pytorch-studio-assets"
    aws_cloudfront_url: str = "https://cdn.pytorch-studio.example.com"

    colab_notebook_base_url: str = "https://colab.research.google.com/notebook#"
    nbviewer_base_url: str = "https://nbviewer.org/url/"

    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 30

    @property
    def sync_database_url(self) -> str:
        """Sync URL for Alembic and seed scripts."""
        url = self.database_url
        if url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
