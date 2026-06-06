"""Anthropic API wrapper for Python tutor."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from anthropic import APIError, AsyncAnthropic, AuthenticationError

from app.config import get_settings
from app.services.chatbot import PYTHON_TUTOR_SYSTEM_PROMPT

EXERCISE_CONTEXT_TEMPLATE = """
## Current Exercise Context

**Module**: {module_name}
**Exercise**: {question_title}
**Difficulty**: {difficulty}
**Type**: {question_type}

**Problem Statement**:
{problem_statement}

**User's Current Code**:
```python
{user_code}
```

**Error / Issue** (if any):
{error_message}

Please help the user with this specific exercise.
""".strip()


def _usage_key(user_id: UUID) -> str:
    today = date.today().isoformat()
    return f"tutor:usage:{user_id}:{today}"


def _history_key(user_id: UUID) -> str:
    return f"tutor:history:{user_id}"


class TutorService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def get_usage(self, redis, user_id: UUID) -> dict[str, Any]:
        key = _usage_key(user_id)
        count = int(await redis.get(key) or 0)
        limit = self.settings.tutor_daily_limit_free
        return {
            "messages_today": count,
            "daily_limit": limit,
            "remaining": max(0, limit - count),
            "resets_at": f"{date.today().isoformat()}T23:59:59Z",
        }

    async def get_history(self, redis, user_id: UUID, limit: int = 50) -> list[dict]:
        raw = await redis.lrange(_history_key(user_id), 0, limit - 1)
        messages = []
        for item in reversed(raw):
            try:
                messages.append(json.loads(item))
            except json.JSONDecodeError:
                continue
        return messages

    async def clear_history(self, redis, user_id: UUID) -> None:
        await redis.delete(_history_key(user_id))

    def build_exercise_context(
        self,
        *,
        module_name: str,
        question_title: str,
        difficulty: str,
        question_type: str,
        problem_statement: str,
        user_code: str,
        error_message: str = "",
    ) -> str:
        return EXERCISE_CONTEXT_TEMPLATE.format(
            module_name=module_name,
            question_title=question_title,
            difficulty=difficulty,
            question_type=question_type,
            problem_statement=problem_statement,
            user_code=user_code or "# (empty)",
            error_message=error_message or "None reported",
        )

    async def chat(
        self,
        redis,
        user_id: UUID,
        message: str,
        *,
        exercise_context: str | None = None,
        history_limit: int = 10,
    ) -> dict[str, Any]:
        usage = await self.get_usage(redis, user_id)
        if usage["remaining"] <= 0:
            raise TutorRateLimitError(usage["messages_today"], usage["daily_limit"])

        prior = await self.get_history(redis, user_id, limit=history_limit)
        assistant_text = await self._complete(message, prior, exercise_context)

        user_msg = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        assistant_msg = {
            "role": "assistant",
            "content": assistant_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        pipe = redis.pipeline()
        key = _history_key(user_id)
        pipe.rpush(key, json.dumps(user_msg), json.dumps(assistant_msg))
        pipe.ltrim(key, -100, -1)
        usage_key = _usage_key(user_id)
        pipe.incr(usage_key)
        pipe.expire(usage_key, 86400)
        await pipe.execute()

        new_usage = await self.get_usage(redis, user_id)
        return {
            "message": assistant_msg,
            "usage": new_usage,
        }

    async def _complete(
        self,
        message: str,
        history: list[dict],
        exercise_context: str | None,
    ) -> str:
        system = PYTHON_TUTOR_SYSTEM_PROMPT
        if exercise_context:
            system = f"{system}\n\n{exercise_context}"

        messages: list[dict[str, str]] = []
        for item in history[-8:]:
            role = item.get("role")
            content = item.get("content", "")
            if role in ("user", "assistant"):
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": message})

        api_key = (self.settings.anthropic_api_key or "").strip()
        if api_key:
            try:
                client = AsyncAnthropic(api_key=api_key)
                response = await client.messages.create(
                    model=self.settings.tutor_model,
                    max_tokens=self.settings.tutor_max_tokens,
                    temperature=0.3,
                    system=system,
                    messages=messages,
                )
                parts = [block.text for block in response.content if hasattr(block, "text")]
                return "\n".join(parts) if parts else "I could not generate a response."
            except (AuthenticationError, APIError):
                if self.settings.app_env == "production":
                    raise
                return self._mock_response(message, exercise_context)

        return self._mock_response(message, exercise_context)

    def _mock_response(self, message: str, exercise_context: str | None) -> str:
        """Offline fallback when ANTHROPIC_API_KEY is unset (dev/CI)."""
        hint = (
            "**Python Tutor (offline mode)** — set `ANTHROPIC_API_KEY` for live responses.\n\n"
        )
        if exercise_context:
            hint += (
                "I see your exercise context. Read tracebacks bottom-up, check types with "
                "`type()` and `isinstance()`, and prefer Pythonic idioms over verbose loops.\n\n"
            )
        if "error" in message.lower() or "traceback" in message.lower():
            hint += (
                "**Debug tip:** The last line of a traceback names the exception. "
                "Fix the innermost cause first, then re-run.\n"
            )
        else:
            hint += (
                "Ask about syntax, data structures, functions, OOP, or debugging — "
                "I'll guide you with Python 3.11+ patterns.\n"
            )
        hint += "\n```python\n# Try printing types and values at each step\nprint(repr(value))\n```"
        return hint


class TutorRateLimitError(Exception):
    def __init__(self, used: int, limit: int) -> None:
        self.used = used
        self.limit = limit
        super().__init__(f"Daily tutor limit reached ({used}/{limit})")
