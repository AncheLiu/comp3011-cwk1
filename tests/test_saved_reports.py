from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant


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


def seed_match_data(client) -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Match(
                    id=3001,
                    start_time=datetime(2026, 3, 10, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=1800,
                    winning_team=0,
                ),
                Match(
                    id=3002,
                    start_time=datetime(2026, 3, 11, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=1900,
                    winning_team=1,
                ),
            ]
        )
        db.add_all(
            [
                MatchParticipant(
                    match_id=3001,
                    account_id=4001,
                    team=0,
                    hero_id=1,
                    match_result=1,
                    player_kills=10,
                    player_deaths=4,
                    player_assists=8,
                    net_worth=15000,
                ),
                MatchParticipant(
                    match_id=3002,
                    account_id=4002,
                    team=1,
                    hero_id=1,
                    match_result=1,
                    player_kills=6,
                    player_deaths=7,
                    player_assists=12,
                    net_worth=12000,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


def test_get_saved_report_result_for_hero_overview(client) -> None:
    seed_hero(client)
    seed_match_data(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Overview Result",
            "report_type": "hero_meta",
            "hero_id": 1,
        },
    )
    report_id = create_response.json()["id"]

    response = client.get(f"/saved-reports/{report_id}/result")

    assert response.status_code == 200
    assert response.json() == {
        "report_id": report_id,
        "name": "Overview Result",
        "report_type": "hero_meta",
        "result": {
            "hero_id": 1,
            "hero_name": "Infernus",
            "matches": 2,
            "wins": 2,
            "losses": 0,
            "win_rate": 100.0,
            "avg_kills": 8.0,
            "avg_deaths": 5.5,
            "avg_assists": 10.0,
            "avg_net_worth": 13500.0,
        },
    }


def test_get_saved_report_result_for_hero_trend(client) -> None:
    seed_hero(client)
    seed_match_data(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Trend Result",
            "report_type": "hero_trend",
            "hero_id": 1,
            "date_from": "2026-03-11",
            "date_to": "2026-03-11",
        },
    )
    report_id = create_response.json()["id"]

    response = client.get(f"/saved-reports/{report_id}/result")

    assert response.status_code == 200
    assert response.json() == {
        "report_id": report_id,
        "name": "Trend Result",
        "report_type": "hero_trend",
        "result": {
            "hero_id": 1,
            "hero_name": "Infernus",
            "bucket": "day",
            "points": [
                {
                    "date": "2026-03-11",
                    "matches": 1,
                    "wins": 1,
                    "losses": 0,
                    "win_rate": 100.0,
                    "avg_kills": 6.0,
                    "avg_deaths": 7.0,
                    "avg_assists": 12.0,
                }
            ],
        },
    }


def test_get_saved_report_result_rejects_unsupported_type(client) -> None:
    seed_hero(client)

    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Unsupported Result",
            "report_type": "synergy_report",
            "hero_id": 1,
        },
    )
    report_id = create_response.json()["id"]

    response = client.get(f"/saved-reports/{report_id}/result")

    assert response.status_code == 400


def test_get_saved_report_result_rejects_missing_hero_id(client) -> None:
    create_response = client.post(
        "/saved-reports",
        json={
            "name": "Missing Hero Result",
            "report_type": "hero_meta",
        },
    )
    report_id = create_response.json()["id"]

    response = client.get(f"/saved-reports/{report_id}/result")

    assert response.status_code == 400
