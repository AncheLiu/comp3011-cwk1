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


def test_create_saved_report(client) -> None:
    seed_hero(client)

    response = client.post(
        "/saved-reports",
        json={
            "name": "Infernus Europe Meta Report",
            "report_type": "hero_meta",
            "hero_id": 1,
            "region_mode": "europe",
            "rank_min": 7,
            "rank_max": 11,
            "date_from": "2026-02-01",
            "date_to": "2026-03-01",
            "filters_json": {"min_matches": 50},
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Infernus Europe Meta Report"
    assert body["hero_id"] == 1
    assert body["filters_json"] == {"min_matches": 50}


def test_list_saved_reports(client) -> None:
    seed_hero(client)

    client.post(
        "/saved-reports",
        json={
            "name": "Overview Report",
            "report_type": "hero_meta",
            "hero_id": 1,
        },
    )

    response = client.get("/saved-reports")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_saved_report_by_id(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Trend Report",
            "report_type": "trend",
            "hero_id": 1,
        },
    )
    report_id = create_response.json()["id"]

    response = client.get(f"/saved-reports/{report_id}")

    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_create_saved_report_rejects_unknown_hero(client) -> None:
    response = client.post(
        "/saved-reports",
        json={
            "name": "Unknown Hero Report",
            "report_type": "hero_meta",
            "hero_id": 999,
        },
    )

    assert response.status_code == 404


def test_update_saved_report(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Original Report",
            "report_type": "hero_meta",
            "hero_id": 1,
        },
    )
    report_id = create_response.json()["id"]

    response = client.patch(
        f"/saved-reports/{report_id}",
        json={
            "name": "Updated Report",
            "region_mode": "europe",
            "rank_min": 8,
            "filters_json": {"min_matches": 100},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Updated Report"
    assert body["region_mode"] == "europe"
    assert body["rank_min"] == 8
    assert body["filters_json"] == {"min_matches": 100}


def test_delete_saved_report(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Delete Report",
            "report_type": "hero_meta",
            "hero_id": 1,
        },
    )
    report_id = create_response.json()["id"]

    delete_response = client.delete(f"/saved-reports/{report_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Saved report deleted successfully"}

    get_response = client.get(f"/saved-reports/{report_id}")
    assert get_response.status_code == 404
