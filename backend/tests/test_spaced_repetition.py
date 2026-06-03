from datetime import date, timedelta

from app.services.spaced_repetition import calculate_next_review


def test_sm2_blackout_resets_interval() -> None:
    result = calculate_next_review(rating=0, ease_factor=2.5, interval_days=10, repetition_count=3)
    assert result.new_interval == 1
    assert result.new_repetition_count == 0
    assert result.new_ease_factor == 2.3


def test_sm2_good_second_review_six_days() -> None:
    result = calculate_next_review(rating=4, ease_factor=2.5, interval_days=1, repetition_count=1)
    assert result.new_repetition_count == 2
    assert result.new_interval == 6
    assert result.next_review_date == date.today() + timedelta(days=6)
