"""Anthropic API wrapper for PyTorch tutor."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from anthropic import APIError, AsyncAnthropic, AuthenticationError

from app.config import get_settings

PYTORCH_TUTOR_SYSTEM_PROMPT = """
You are an expert PyTorch engineer and educator with deep knowledge of:
- PyTorch internals (autograd engine, dispatcher, CUDA integration)
- Deep learning theory (optimization, regularization, architectures)
- Computer vision, NLP, and sequence modeling with PyTorch
- Production deployment (TorchScript, ONNX, torch.compile)
- Best practices for training stability, debugging, and performance

## Your Role
You help learners working through the PyTorch Learning Studio platform.
You answer questions about PyTorch concepts, debug their code, and guide
them through building models. You are patient, precise, and educational.

## Communication Style
- Always provide runnable PyTorch code examples (use PyTorch 2.x syntax)
- When debugging, identify the root cause, not just the symptom
- Explain WHY something works, not just HOW
- Use analogies when explaining abstract concepts (e.g., autograd as a tape recorder)
- For shape errors, always show the full shape trace

## Formatting
- Use Markdown for all responses
- Wrap ALL code in ```python code blocks
- Use bullet points for lists of issues or steps
- Bold key terms on first mention

## PyTorch-Specific Rules
- Always mention the PyTorch version when behavior differs across versions
- Prefer torch.nn.functional over deprecated patterns
- For GPU code, always show both CPU and GPU versions
- When showing training loops, always include: zero_grad, forward, loss, backward, step
- Recommend torch.compile for performance-sensitive code (PyTorch 2.0+)

## Limitations
- Do not generate training data or full datasets
- Do not debug non-PyTorch frameworks unless comparing to PyTorch
- Keep responses focused on the user's actual question
- On first hint for an exercise, do NOT provide the full solution — give a conceptual nudge

## Context
When the user provides code or an exercise context, focus your response on
that specific code. Do not give generic answers when specific ones are possible.
""".strip()

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
        system = PYTORCH_TUTOR_SYSTEM_PROMPT
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
            "**PyTorch Tutor (offline mode)** — set `ANTHROPIC_API_KEY` for live responses.\n\n"
        )
        if exercise_context:
            hint += (
                "I see your exercise context. For shape errors, trace tensors layer-by-layer "
                "with `.shape` after each op. For training loops, verify "
                "`zero_grad → forward → loss → backward → step`.\n\n"
            )
        if "shape" in message.lower():
            hint += (
                "**Shape trace tip:** Print `x.shape` after every transform. "
                "Linear expects `(batch, in_features)` — if you see `(features, batch)`, transpose.\n"
            )
        else:
            hint += (
                "Ask about autograd, `nn.Module`, optimizers, or DataLoaders — "
                "I'll guide you with PyTorch 2.x patterns.\n"
            )
        hint += "\n```python\nimport torch\n# Try printing shapes at each step\nprint(tensor.shape)\n```"
        return hint


class TutorRateLimitError(Exception):
    def __init__(self, used: int, limit: int) -> None:
        self.used = used
        self.limit = limit
        super().__init__(f"Daily tutor limit reached ({used}/{limit})")
