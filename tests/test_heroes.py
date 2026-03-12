from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_heroes_returns_empty_list_by_default() -> None:
    response = client.get("/heroes")

    assert response.status_code == 200
    assert response.json() == []
