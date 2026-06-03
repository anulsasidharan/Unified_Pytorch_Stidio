import uuid

import pytest


def _register_and_login(api_client) -> str:
    suffix = uuid.uuid4().hex[:8]
    email = f"phase3_{suffix}@example.com"
    password = "testpass123"
    reg = api_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": f"phase3_{suffix}",
            "password": password,
        },
    )
    assert reg.status_code in (200, 201)
    login = api_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


def _first_question_id(api_client) -> int | None:
    topics = api_client.get("/api/v1/topics").json()
    if not topics:
        return None
    detail = api_client.get(f"/api/v1/topics/{topics[0]['slug']}").json()
    questions = detail.get("questions") or []
    return questions[0]["id"] if questions else None


def test_progress_requires_auth(api_client) -> None:
    assert api_client.get("/api/v1/progress").status_code == 401


def test_tracker_dashboard_authenticated(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    res = api_client.get("/api/v1/tracker/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "today" in data
    assert "streak" in data
    assert "weekly" in data
    assert len(data["weekly"]) == 7


def test_progress_after_correct_attempt(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    qid = _first_question_id(api_client)
    if qid is None:
        pytest.skip("No seeded questions")

    submit = api_client.post(
        "/api/v1/attempts",
        headers=headers,
        json={
            "question_id": qid,
            "code": "x = 1",
            "result": "correct",
            "time_spent_secs": 60,
        },
    )
    assert submit.status_code == 201
    assert submit.json()["xp_earned"] > 0
    assert submit.json()["added_to_revision"] is True

    progress = api_client.get("/api/v1/progress", headers=headers)
    assert progress.status_code == 200
    assert progress.json()["totals"]["questions_solved"] >= 1

    stats = api_client.get("/api/v1/revision/stats", headers=headers)
    assert stats.status_code == 200
    assert stats.json()["queue_size"] >= 1


def test_revision_review_flow(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    qid = _first_question_id(api_client)
    if qid is None:
        pytest.skip("No seeded questions")

    api_client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"question_id": qid, "result": "correct", "time_spent_secs": 30},
    )

    due = api_client.get("/api/v1/revision/due", headers=headers)
    assert due.status_code == 200
    items = due.json()
    assert any(item["question_id"] == qid for item in items)

    review = api_client.post(
        "/api/v1/revision/review",
        headers=headers,
        json={"question_id": qid, "rating": 4},
    )
    assert review.status_code == 200
    assert "next_review_date" in review.json()


def test_heatmap_and_streak(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    heatmap = api_client.get("/api/v1/tracker/heatmap", headers=headers)
    assert heatmap.status_code == 200
    assert "cells" in heatmap.json()
    streak = api_client.get("/api/v1/tracker/streak", headers=headers)
    assert streak.status_code == 200
    assert "current" in streak.json()
