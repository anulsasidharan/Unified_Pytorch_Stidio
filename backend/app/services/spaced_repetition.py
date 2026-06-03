"""SM-2 spaced repetition algorithm (spec §12)."""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ReviewResult:
    next_review_date: date
    new_interval: int
    new_ease_factor: float
    new_repetition_count: int


def calculate_next_review(
    rating: int,
    ease_factor: float,
    interval_days: int,
    repetition_count: int,
) -> ReviewResult:
    """
    SM-2 algorithm implementation.
    rating < 3: treat as blackout — reset to day 1
    """
    if rating < 3:
        new_interval = 1
        new_repetition_count = 0
        new_ease_factor = max(1.3, ease_factor - 0.2)
    else:
        new_repetition_count = repetition_count + 1
        new_ease_factor = ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        new_ease_factor = max(1.3, new_ease_factor)

        if new_repetition_count == 1:
            new_interval = 1
        elif new_repetition_count == 2:
            new_interval = 6
        else:
            new_interval = round(interval_days * new_ease_factor)

    next_review = date.today() + timedelta(days=new_interval)

    return ReviewResult(
        next_review_date=next_review,
        new_interval=new_interval,
        new_ease_factor=round(new_ease_factor, 2),
        new_repetition_count=new_repetition_count,
    )
