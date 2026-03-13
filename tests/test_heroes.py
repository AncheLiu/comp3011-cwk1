def test_list_heroes_returns_empty_list_by_default(client) -> None:
    response = client.get("/heroes")

    assert response.status_code == 200
    assert response.json() == []
