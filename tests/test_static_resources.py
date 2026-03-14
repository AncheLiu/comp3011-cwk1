from sqlalchemy.orm import Session

from app.models.hero import Hero
from app.models.item import Item


def seed_static_resources(client) -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add(
            Hero(
                id=1,
                name="Infernus",
                class_name="hero_inferno",
                role_text="Lights up enemies and watches them burn",
                playstyle_text="Damage over time hero",
                hero_type="marksman",
                complexity=1,
                image_small_url="https://example.com/infernus-sm.png",
                image_card_url="https://example.com/infernus-card.png",
                is_selectable=True,
            )
        )
        db.add(
            Item(
                id=100,
                name="Mystic Shot",
                class_name="upgrade_mystic_shot",
                item_type="ability",
                hero_id=None,
                image_url="https://example.com/mystic-shot.png",
            )
        )
        db.commit()
    finally:
        db.close()


def test_get_hero_by_id(client) -> None:
    seed_static_resources(client)

    response = client.get("/heroes/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Infernus"
    assert response.json()["hero_type"] == "marksman"


def test_get_hero_by_id_returns_404_for_unknown_hero(client) -> None:
    response = client.get("/heroes/999")

    assert response.status_code == 404


def test_list_items_returns_imported_items(client) -> None:
    seed_static_resources(client)

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Mystic Shot"
