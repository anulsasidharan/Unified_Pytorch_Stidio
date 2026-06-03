import uuid

import pytest


def _register_and_login(api_client) -> str:
    suffix = uuid.uuid4().hex[:8]
    email = f"phase4_{suffix}@example.com"
    password = "testpass123"
    reg = api_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": f"phase4_{suffix}",
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


def test_import_manual_and_community(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}

    res = api_client.post(
        "/api/v1/import/manual",
        headers=headers,
        json={
            "title": "Custom L2 Norm",
            "topic_slug": "tensors",
            "difficulty": "intermediate",
            "problem_statement": "Implement L2 norm without torch.norm",
            "solution_code": "import torch\nx = torch.randn(3, 4)",
            "tags": ["custom"],
            "is_shared": True,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["created"] == 1
    assert data["import_source"] == "manual"
    qid = data["items"][0]["id"]
    assert qid is not None

    mine = api_client.get("/api/v1/custom-questions?mine=true", headers=headers)
    assert mine.status_code == 200
    assert any(q["id"] == qid for q in mine.json())

    community = api_client.get("/api/v1/custom-questions?community=true")
    assert community.status_code == 200
    assert any(q["id"] == qid for q in community.json())

    history = api_client.get("/api/v1/import/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) >= 1


def test_import_json_preview(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}

    preview = api_client.post(
        "/api/v1/import/json",
        headers=headers,
        json={
            "preview": True,
            "questions": [
                {
                    "title": "BatchNorm Scratch",
                    "topic_slug": "nn-module",
                    "difficulty": "advanced",
                    "problem_statement": "Implement BatchNorm1d from scratch",
                    "starter_code": "import torch",
                }
            ],
        },
    )
    assert preview.status_code == 200
    assert preview.json()["preview"] is True
    assert preview.json()["created"] == 0

    save = api_client.post(
        "/api/v1/import/json",
        headers=headers,
        json={
            "questions": [
                {
                    "title": "BatchNorm Scratch",
                    "topic_slug": "nn-module",
                    "difficulty": "advanced",
                    "problem_statement": "Implement BatchNorm1d from scratch",
                    "starter_code": "import torch",
                }
            ],
        },
    )
    assert save.status_code == 200
    assert save.json()["created"] == 1


def test_import_csv(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}
    csv_body = (
        "title,topic_slug,difficulty,problem_statement,starter_code,tags\n"
        '"CSV Exercise","tensors","basic","Sum a tensor","import torch\n# code","csv,test"\n'
    )
    res = api_client.post(
        "/api/v1/import/csv",
        headers=headers,
        files={"file": ("questions.csv", csv_body, "text/csv")},
    )
    assert res.status_code == 200
    assert res.json()["created"] == 1


def test_notes_crud(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}

    topics = api_client.get("/api/v1/topics").json()
    if not topics:
        pytest.skip("No topics seeded")
    topic_id = topics[0]["id"]

    create = api_client.post(
        "/api/v1/notes",
        headers=headers,
        json={
            "topic_id": topic_id,
            "content": "Remember broadcasting rules",
            "note_type": "insight",
            "tags": ["broadcasting"],
        },
    )
    assert create.status_code == 201
    note_id = create.json()["id"]

    listed = api_client.get(f"/api/v1/notes?topic_id={topic_id}", headers=headers)
    assert listed.status_code == 200
    assert any(n["id"] == note_id for n in listed.json())

    updated = api_client.put(
        f"/api/v1/notes/{note_id}",
        headers=headers,
        json={"content": "Updated insight on broadcasting"},
    )
    assert updated.status_code == 200
    assert "Updated" in updated.json()["content"]

    deleted = api_client.delete(f"/api/v1/notes/{note_id}", headers=headers)
    assert deleted.status_code == 204


def test_custom_question_update_delete(api_client) -> None:
    token = _register_and_login(api_client)
    headers = {"Authorization": f"Bearer {token}"}

    created = api_client.post(
        "/api/v1/import/manual",
        headers=headers,
        json={
            "title": "To Update",
            "problem_statement": "Original statement",
            "is_shared": False,
        },
    )
    qid = created.json()["items"][0]["id"]

    updated = api_client.put(
        f"/api/v1/custom-questions/{qid}",
        headers=headers,
        json={"title": "Updated Title", "is_shared": True},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated Title"
    assert updated.json()["is_shared"] is True

    deleted = api_client.delete(f"/api/v1/custom-questions/{qid}", headers=headers)
    assert deleted.status_code == 204
