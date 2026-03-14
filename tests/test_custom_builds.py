from sqlalchemy.orm import Session

from app.models.hero import Hero


def seed_hero(client, hero_id: int = 1) -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        hero = Hero(
            id=hero_id,
            name="Infernus",
            class_name="hero_inferno",
            hero_type="marksman",
            complexity=1,
            is_selectable=True,
        )
        db.add(hero)
        db.commit()
    finally:
        db.close()


def test_create_custom_build(client) -> None:
    seed_hero(client)

    response = client.post(
        "/custom-builds",
        json={
            "title": "Afterburn Rush Build",
            "hero_id": 1,
            "author_name": "student",
            "playstyle_tag": "damage_over_time",
            "description": "Focus on sustained burn damage",
            "items_json": [968099481, 2081037738],
            "ability_order_json": [1593133799, 491391007],
            "notes": "Use against squishy teams",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Afterburn Rush Build"
    assert body["hero_id"] == 1
    assert body["items_json"] == [968099481, 2081037738]


def test_list_custom_builds(client) -> None:
    seed_hero(client)

    client.post(
        "/custom-builds",
        json={
            "title": "Starter Build",
            "hero_id": 1,
            "author_name": "student",
            "items_json": [1, 2, 3],
        },
    )

    response = client.get("/custom-builds")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_custom_build_by_id(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/custom-builds",
        json={
            "title": "Lane Build",
            "hero_id": 1,
            "author_name": "student",
            "items_json": [10, 20],
        },
    )
    build_id = create_response.json()["id"]

    response = client.get(f"/custom-builds/{build_id}")

    assert response.status_code == 200
    assert response.json()["id"] == build_id


def test_create_custom_build_rejects_unknown_hero(client) -> None:
    response = client.post(
        "/custom-builds",
        json={
            "title": "Invalid Hero Build",
            "hero_id": 999,
            "author_name": "student",
            "items_json": [1],
        },
    )

    assert response.status_code == 404


def test_update_custom_build(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/custom-builds",
        json={
            "title": "Original Build",
            "hero_id": 1,
            "author_name": "student",
            "items_json": [1, 2],
        },
    )
    build_id = create_response.json()["id"]

    response = client.put(
        f"/custom-builds/{build_id}",
        json={
            "title": "Updated Build",
            "hero_id": 1,
            "author_name": "student",
            "playstyle_tag": "late_game",
            "description": "Updated description",
            "items_json": [5, 6, 7],
            "ability_order_json": [10, 20],
            "notes": "Updated notes",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated Build"
    assert body["items_json"] == [5, 6, 7]
    assert body["playstyle_tag"] == "late_game"


def test_delete_custom_build(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/custom-builds",
        json={
            "title": "Delete Me",
            "hero_id": 1,
            "author_name": "student",
            "items_json": [1],
        },
    )
    build_id = create_response.json()["id"]

    delete_response = client.delete(f"/custom-builds/{build_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Custom build deleted successfully"}

    get_response = client.get(f"/custom-builds/{build_id}")
    assert get_response.status_code == 404
