from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant


def seed_hero(client, hero_id: int, name: str) -> None:
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


def seed_matches(client) -> None:
    seed_hero(client, 1, "Infernus")
    seed_hero(client, 52, "Wraith")

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Match(
                    id=5001,
                    start_time=datetime(2026, 3, 10, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="eu",
                    duration_seconds=1800,
                    winning_team=0,
                    net_worth_team_0=35000,
                    net_worth_team_1=30000,
                ),
                Match(
                    id=5002,
                    start_time=datetime(2026, 3, 11, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="na",
                    duration_seconds=1900,
                    winning_team=1,
                    net_worth_team_0=32000,
                    net_worth_team_1=36000,
                ),
            ]
        )
        db.add_all(
            [
                MatchParticipant(
                    match_id=5001,
                    account_id=9001,
                    team=0,
                    hero_id=1,
                    hero_level=30,
                    match_result=1,
                    player_kills=10,
                    player_deaths=4,
                    player_assists=8,
                    last_hits=120,
                    denies=2,
                    net_worth=15000,
                ),
                MatchParticipant(
                    match_id=5001,
                    account_id=9002,
                    team=1,
                    hero_id=52,
                    hero_level=29,
                    match_result=0,
                    player_kills=5,
                    player_deaths=7,
                    player_assists=6,
                    last_hits=110,
                    denies=1,
                    net_worth=14000,
                ),
                MatchParticipant(
                    match_id=5002,
                    account_id=9003,
                    team=1,
                    hero_id=1,
                    hero_level=31,
                    match_result=1,
                    player_kills=7,
                    player_deaths=5,
                    player_assists=10,
                    last_hits=130,
                    denies=3,
                    net_worth=16000,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


def test_list_matches_returns_all_matches(client) -> None:
    seed_matches(client)

    response = client.get("/matches")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["id"] == 5002
    assert body[1]["id"] == 5001


def test_list_matches_supports_hero_filter(client) -> None:
    seed_matches(client)

    response = client.get("/matches?hero_id=52")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == 5001


def test_list_matches_rejects_unknown_hero_filter(client) -> None:
    response = client.get("/matches?hero_id=999")

    assert response.status_code == 404


def test_list_matches_supports_inclusive_date_filters(client) -> None:
    seed_matches(client)

    response = client.get("/matches?date_from=2026-03-11&date_to=2026-03-11")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == 5002


def test_get_match_detail_returns_participants(client) -> None:
    seed_matches(client)

    response = client.get("/matches/5001")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 5001
    assert len(body["participants"]) == 2
    assert body["participants"][0]["hero_name"] == "Infernus"
    assert body["participants"][1]["hero_name"] == "Wraith"


def test_get_match_detail_rejects_unknown_match(client) -> None:
    response = client.get("/matches/9999")

    assert response.status_code == 404
