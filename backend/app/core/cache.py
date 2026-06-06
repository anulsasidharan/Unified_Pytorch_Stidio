"""Redis JSON cache helpers for read-heavy API routes."""

import json
from collections.abc import Awaitable, Callable
from typing import Any

from app.core.redis_client import get_redis

JsonLoader = Callable[[], Awaitable[Any]]


async def get_json_cached(key: str, ttl_seconds: int, loader: JsonLoader) -> Any:
    redis = await get_redis()
    cached = await redis.get(key)
    if cached is not None:
        return json.loads(cached)
    value = await loader()
    await redis.setex(key, ttl_seconds, json.dumps(value))
    return value


async def invalidate_prefix(prefix: str) -> None:
    redis = await get_redis()
    async for key in redis.scan_iter(match=f"{prefix}*"):
        await redis.delete(key)
