"""Phase 2 API tests — Colab generation and tutor (offline mock)."""

import uuid


def test_colab_generates_notebook_url(api_client) -> None:
    topics = api_client.get("/api/v1/topics").json()
    if not topics:
        return
    detail = api_client.get(f"/api/v1/topics/{topics[0]['slug']}").json()
    if not detail.get("questions"):
        return
    qid = detail["questions"][0]["id"]
    res = api_client.get(f"/api/v1/colab/{qid}")
    assert res.status_code == 200
    body = res.json()
    assert "colab_url" in body
    assert body["source"] in ("stored", "generated")


def test_tutor_requires_auth(api_client) -> None:
    res = api_client.post(
        "/api/v1/tutor/chat",
        json={"message": "Why is my tensor shape wrong?"},
    )
    assert res.status_code == 401


def test_tutor_chat_offline_mock(api_client) -> None:
    suffix = uuid.uuid4().hex[:8]
    email = f"tutor_{suffix}@example.com"
    reg = api_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": f"tutor_{suffix}",
            "password": "testpass123",
        },
    )
    assert reg.status_code in (200, 201)
    login = api_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "testpass123"},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    chat = api_client.post(
        "/api/v1/tutor/chat",
        headers=headers,
        json={"message": "Explain shape mismatch in Linear layer"},
    )
    assert chat.status_code == 200
    data = chat.json()
    assert data["message"]["role"] == "assistant"
    assert "shape" in data["message"]["content"].lower() or "PyTorch" in data["message"]["content"]

    usage = api_client.get("/api/v1/tutor/usage", headers=headers)
    assert usage.status_code == 200
    assert usage.json()["messages_today"] >= 1

    history = api_client.get("/api/v1/tutor/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()["messages"]) >= 2
