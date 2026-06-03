"""Phase 5 API tests — search and question filters."""


def test_questions_search_requires_query(api_client) -> None:
    res = api_client.get("/api/v1/questions/search")
    assert res.status_code == 422


def test_questions_search_by_keyword(api_client) -> None:
    res = api_client.get("/api/v1/questions/search", params={"q": "tensor", "limit": 10})
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    if body:
        assert "title" in body[0]
        assert "topic_slug" in body[0]


def test_questions_list_with_filters(api_client) -> None:
    res = api_client.get(
        "/api/v1/questions",
        params={"difficulty": "basic", "type": "code_completion", "limit": 5},
    )
    assert res.status_code == 200
    for item in res.json():
        assert item["difficulty"] == "basic"
        assert item["question_type"] == "code_completion"


def test_questions_list_text_search(api_client) -> None:
    res = api_client.get("/api/v1/questions", params={"q": "LSTM", "limit": 20})
    assert res.status_code == 200
    assert isinstance(res.json(), list)
