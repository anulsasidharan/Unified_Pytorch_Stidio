import uuid


def test_topics_list(api_client) -> None:
    response = api_client.get("/api/v1/topics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "slug" in data[0]
        assert "module_number" in data[0]
        module_numbers = [t["module_number"] for t in data]
        assert len(module_numbers) == len(set(module_numbers)), (
            "duplicate module_number in /topics — run python -m seeds.dedupe_topics"
        )


def test_auth_register_and_me(api_client) -> None:
    suffix = uuid.uuid4().hex[:8]
    email = f"phase1_{suffix}@example.com"
    reg = api_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": f"phase1_{suffix}",
            "password": "testpass123",
            "full_name": "Phase One",
        },
    )
    assert reg.status_code in (200, 201)
    login = api_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "testpass123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    me = api_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == email


def test_colab_stub(api_client) -> None:
    topics = api_client.get("/api/v1/topics").json()
    if not topics:
        return
    detail = api_client.get(f"/api/v1/topics/{topics[0]['slug']}").json()
    if not detail.get("questions"):
        return
    qid = detail["questions"][0]["id"]
    res = api_client.get(f"/api/v1/colab/{qid}")
    assert res.status_code == 200
    assert "colab_url" in res.json()
