import json
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.community_build import CommunityBuild
from app.models.hero import Hero


def seed_hero(client, hero_id: int = 1, name: str = "Infernus") -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add(
            Hero(
                id=hero_id,
                name=name,
                class_name=f"hero_{hero_id}",
                hero_type="marksman",
                complexity=1,
                is_selectable=True,
            )
        )
        db.commit()
    finally:
        db.close()


def seed_community_builds(client) -> None:
    seed_hero(client)

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                CommunityBuild(
                    hero_build_id=1013,
                    hero_id=1,
                    author_account_id=29436163,
                    name="Zieth Infernus",
                    description="Example build",
                    language=0,
                    version=21,
                    last_updated_timestamp=datetime(2026, 3, 10, 12, 0, tzinfo=UTC),
                    favorites_count=100,
                    tags_json=json.dumps([1, 2]),
                    details_json=json.dumps({"mod_categories": []}),
                ),
                CommunityBuild(
                    hero_build_id=1014,
                    hero_id=1,
                    author_account_id=29436164,
                    name="Late Game Infernus",
                    description="Another build",
                    language=0,
                    version=7,
                    last_updated_timestamp=datetime(2026, 3, 9, 12, 0, tzinfo=UTC),
                    favorites_count=50,
                    tags_json=json.dumps([]),
                    details_json=json.dumps({"mod_categories": ["core"]}),
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


def test_list_community_builds_returns_ranked_builds(client) -> None:
    seed_community_builds(client)

    response = client.get("/community-builds")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["hero_build_id"] == 1013
    assert body[1]["hero_build_id"] == 1014


def test_list_community_builds_supports_hero_filter(client) -> None:
    seed_community_builds(client)

    response = client.get("/community-builds?hero_id=1")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_community_builds_rejects_unknown_hero(client) -> None:
    response = client.get("/community-builds?hero_id=999")

    assert response.status_code == 404


def test_get_community_build_returns_details(client) -> None:
    seed_community_builds(client)

    response = client.get("/community-builds/1")

    assert response.status_code == 200
    body = response.json()
    assert body["hero_build_id"] == 1013
    assert body["tags_json"] == [1, 2]
    assert body["details_json"] == {"mod_categories": []}


def test_get_community_build_rejects_unknown_id(client) -> None:
    response = client.get("/community-builds/999")

    assert response.status_code == 404
