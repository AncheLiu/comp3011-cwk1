from sqlalchemy.orm import Session

from app.models.hero import Hero
from app.models.item import Item


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


def seed_items(client) -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Item(id=1, name="Toxic Bullets", class_name="item_1", item_type="weapon"),
                Item(id=2, name="Ricochet", class_name="item_2", item_type="weapon"),
                Item(id=3, name="Leech", class_name="item_3", item_type="vitality"),
                Item(id=4, name="Metal Skin", class_name="item_4", item_type="vitality"),
            ]
        )
        db.commit()
    finally:
        db.close()


def build_payload() -> dict:
    return {
        "title": "Afterburn Rush Build",
        "hero_id": 1,
        "author_name": "student",
        "playstyle_tag": "damage_over_time",
        "description": "Focus on sustained burn damage",
        "notes": "Use against squishy teams",
        "source_community_build_id": 1013,
        "items": [
            {
                "item_id": 1,
                "category_name": "Early Game",
                "display_order": 1,
                "is_optional": False,
                "annotation": "Start here",
            },
            {
                "item_id": 2,
                "category_name": "Core",
                "display_order": 2,
                "is_optional": False,
                "annotation": "Mid-game spike",
            },
        ],
        "abilities": [
            {
                "ability_id": 1593133799,
                "display_order": 1,
                "annotation": "First point",
            },
            {
                "ability_id": 491391007,
                "display_order": 2,
                "annotation": "Second point",
            },
        ],
    }


def test_create_custom_build(client) -> None:
    seed_hero(client)
    seed_items(client)

    response = client.post("/custom-builds", json=build_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Afterburn Rush Build"
    assert body["hero_id"] == 1
    assert body["hero_name"] == "Infernus"
    assert body["source_community_build_id"] == 1013
    assert len(body["items"]) == 2
    assert body["items"][0]["item_name"] == "Toxic Bullets"
    assert len(body["abilities"]) == 2


def test_list_custom_builds(client) -> None:
    seed_hero(client)
    seed_items(client)

    client.post("/custom-builds", json=build_payload())

    response = client.get("/custom-builds")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["item_count"] == 2
    assert body[0]["ability_count"] == 2


def test_get_custom_build_by_id(client) -> None:
    seed_hero(client)
    seed_items(client)

    create_response = client.post("/custom-builds", json=build_payload())
    build_id = create_response.json()["id"]

    response = client.get(f"/custom-builds/{build_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == build_id
    assert body["items"][1]["item_name"] == "Ricochet"


def test_create_custom_build_rejects_unknown_hero(client) -> None:
    seed_items(client)

    response = client.post("/custom-builds", json=build_payload())

    assert response.status_code == 404


def test_create_custom_build_rejects_unknown_item(client) -> None:
    seed_hero(client)
    payload = build_payload()
    payload["items"][0]["item_id"] = 999

    response = client.post("/custom-builds", json=payload)

    assert response.status_code == 404


def test_update_custom_build(client) -> None:
    seed_hero(client)
    seed_items(client)

    create_response = client.post("/custom-builds", json=build_payload())
    build_id = create_response.json()["id"]

    payload = build_payload()
    payload["title"] = "Updated Build"
    payload["playstyle_tag"] = "late_game"
    payload["items"] = [
        {
            "item_id": 4,
            "category_name": "Defense",
            "display_order": 1,
            "is_optional": True,
            "annotation": "Situational defense",
        }
    ]
    payload["abilities"] = [
        {
            "ability_id": 3516947824,
            "display_order": 1,
            "annotation": "New priority",
        }
    ]

    response = client.put(f"/custom-builds/{build_id}", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated Build"
    assert body["playstyle_tag"] == "late_game"
    assert len(body["items"]) == 1
    assert body["items"][0]["item_name"] == "Metal Skin"
    assert len(body["abilities"]) == 1


def test_delete_custom_build(client) -> None:
    seed_hero(client)
    seed_items(client)

    create_response = client.post("/custom-builds", json=build_payload())
    build_id = create_response.json()["id"]

    delete_response = client.delete(f"/custom-builds/{build_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Custom build deleted successfully"}

    get_response = client.get(f"/custom-builds/{build_id}")
    assert get_response.status_code == 404
