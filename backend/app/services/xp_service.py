"""XP calculation and bonus awards (spec §13)."""

from __future__ import annotations

from decimal import Decimal

XP_BY_DIFFICULTY: dict[str, int] = {
    "basic": 10,
    "intermediate": 20,
    "advanced": 30,
}
HINT_PENALTY = 2
DAILY_GOAL_BONUS = 25
REVISION_SESSION_BONUS = 15
MODULE_MILESTONE_BONUS = 100
STREAK_7_BONUS = 50
STREAK_30_BONUS = 200


def base_xp_for_difficulty(difficulty: str, xp_reward: int | None = None) -> int:
    """First correct submission XP; prefer question xp_reward when set."""
    if xp_reward and xp_reward > 0:
        return xp_reward
    return XP_BY_DIFFICULTY.get(difficulty, 10)


def hint_penalty(hints_used: int) -> int:
    return HINT_PENALTY * max(0, hints_used)


def module_complete_bonus(old_pct: Decimal | float, new_pct: Decimal | float) -> int:
    if float(old_pct) < 100 and float(new_pct) >= 100:
        return MODULE_MILESTONE_BONUS
    return 0


def streak_milestone_bonus(old_streak: int, new_streak: int) -> int:
    bonus = 0
    if old_streak < 7 <= new_streak:
        bonus += STREAK_7_BONUS
    if old_streak < 30 <= new_streak:
        bonus += STREAK_30_BONUS
    return bonus
