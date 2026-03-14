from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant


def seed_hero(client, hero_id: int = 1, name: str = "Infernus") -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        hero = Hero(
            id=hero_id,
            name=name,
            class_name=f"hero_{hero_id}",
            hero_type="marksman",
            complexity=1,
            is_selectable=True,
        )
        db.add(hero)
        db.commit()
    finally:
        db.close()


def seed_match_participants_for_overview(client) -> None:
    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Match(
                    id=1001,
                    start_time=datetime(2026, 3, 10, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=1800,
                    winning_team=0,
                ),
                Match(
                    id=1002,
                    start_time=datetime(2026, 3, 11, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=1900,
                    winning_team=0,
                ),
            ]
        )
        db.add_all(
            [
                MatchParticipant(
                    match_id=1001,
                    account_id=2001,
                    team=0,
                    hero_id=1,
                    match_result=1,
                    player_kills=10,
                    player_deaths=4,
                    player_assists=8,
                    net_worth=15000,
                ),
                MatchParticipant(
                    match_id=1002,
                    account_id=2002,
                    team=1,
                    hero_id=1,
                    match_result=0,
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


def seed_matchups_data(client) -> None:
    seed_hero(client, hero_id=52, name="Wraith")
    seed_hero(client, hero_id=16, name="Kelvin")

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Match(
                    id=2001,
                    start_time=datetime(2026, 3, 12, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=2000,
                    winning_team=0,
                ),
                Match(
                    id=2002,
                    start_time=datetime(2026, 3, 13, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=2100,
                    winning_team=1,
                ),
            ]
        )
        db.add_all(
            [
                MatchParticipant(
                    match_id=2001,
                    account_id=3001,
                    team=0,
                    hero_id=1,
                    match_result=1,
                    player_kills=9,
                    player_deaths=3,
                    player_assists=11,
                    net_worth=17000,
                ),
                MatchParticipant(
                    match_id=2001,
                    account_id=3002,
                    team=1,
                    hero_id=52,
                    match_result=0,
                    player_kills=5,
                    player_deaths=7,
                    player_assists=8,
                    net_worth=14000,
                ),
                MatchParticipant(
                    match_id=2001,
                    account_id=3003,
                    team=1,
                    hero_id=16,
                    match_result=0,
                    player_kills=3,
                    player_deaths=8,
                    player_assists=5,
                    net_worth=13000,
                ),
                MatchParticipant(
                    match_id=2002,
                    account_id=3004,
                    team=0,
                    hero_id=1,
                    match_result=0,
                    player_kills=4,
                    player_deaths=8,
                    player_assists=7,
                    net_worth=13500,
                ),
                MatchParticipant(
                    match_id=2002,
                    account_id=3005,
                    team=1,
                    hero_id=52,
                    match_result=1,
                    player_kills=10,
                    player_deaths=4,
                    player_assists=9,
                    net_worth=18000,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


def seed_synergies_data(client) -> None:
    seed_hero(client, hero_id=16, name="Kelvin")
    seed_hero(client, hero_id=52, name="Wraith")

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add_all(
            [
                Match(
                    id=2101,
                    start_time=datetime(2026, 3, 12, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=2000,
                    winning_team=0,
                ),
                Match(
                    id=2102,
                    start_time=datetime(2026, 3, 13, 12, 0, tzinfo=UTC),
                    game_mode="1",
                    match_mode="1",
                    region_mode="unknown",
                    duration_seconds=2100,
                    winning_team=1,
                ),
            ]
        )
        db.add_all(
            [
                MatchParticipant(
                    match_id=2101,
                    account_id=3101,
                    team=0,
                    hero_id=1,
                    match_result=1,
                    player_kills=9,
                    player_deaths=3,
                    player_assists=11,
                    net_worth=17000,
                ),
                MatchParticipant(
                    match_id=2101,
                    account_id=3102,
                    team=0,
                    hero_id=16,
                    match_result=1,
                    player_kills=4,
                    player_deaths=5,
                    player_assists=14,
                    net_worth=14500,
                ),
                MatchParticipant(
                    match_id=2101,
                    account_id=3103,
                    team=1,
                    hero_id=52,
                    match_result=0,
                    player_kills=5,
                    player_deaths=7,
                    player_assists=8,
                    net_worth=14000,
                ),
                MatchParticipant(
                    match_id=2102,
                    account_id=3104,
                    team=1,
                    hero_id=1,
                    match_result=1,
                    player_kills=7,
                    player_deaths=5,
                    player_assists=10,
                    net_worth=16000,
                ),
                MatchParticipant(
                    match_id=2102,
                    account_id=3105,
                    team=1,
                    hero_id=52,
                    match_result=1,
                    player_kills=11,
                    player_deaths=4,
                    player_assists=9,
                    net_worth=18000,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


def test_hero_overview_returns_zero_values_when_no_match_data(client) -> None:
    seed_hero(client)

    response = client.get("/analytics/heroes/1/overview")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "matches": 0,
        "wins": 0,
        "losses": 0,
        "win_rate": 0.0,
        "avg_kills": 0.0,
        "avg_deaths": 0.0,
        "avg_assists": 0.0,
        "avg_net_worth": 0.0,
    }


def test_hero_overview_returns_aggregated_stats(client) -> None:
    seed_hero(client)
    seed_match_participants_for_overview(client)

    response = client.get("/analytics/heroes/1/overview")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "matches": 2,
        "wins": 1,
        "losses": 1,
        "win_rate": 50.0,
        "avg_kills": 8.0,
        "avg_deaths": 5.5,
        "avg_assists": 10.0,
        "avg_net_worth": 13500.0,
    }


def test_hero_overview_rejects_unknown_hero(client) -> None:
    response = client.get("/analytics/heroes/999/overview")

    assert response.status_code == 404


def test_hero_trend_returns_daily_points(client) -> None:
    seed_hero(client)
    seed_match_participants_for_overview(client)

    response = client.get("/analytics/heroes/1/trend")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "bucket": "day",
        "points": [
            {
                "date": "2026-03-10",
                "matches": 1,
                "wins": 1,
                "losses": 0,
                "win_rate": 100.0,
                "avg_kills": 10.0,
                "avg_deaths": 4.0,
                "avg_assists": 8.0,
            },
            {
                "date": "2026-03-11",
                "matches": 1,
                "wins": 0,
                "losses": 1,
                "win_rate": 0.0,
                "avg_kills": 6.0,
                "avg_deaths": 7.0,
                "avg_assists": 12.0,
            },
        ],
    }


def test_hero_trend_supports_date_filters(client) -> None:
    seed_hero(client)
    seed_match_participants_for_overview(client)

    response = client.get("/analytics/heroes/1/trend?date_from=2026-03-11&date_to=2026-03-11")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "bucket": "day",
        "points": [
            {
                "date": "2026-03-11",
                "matches": 1,
                "wins": 0,
                "losses": 1,
                "win_rate": 0.0,
                "avg_kills": 6.0,
                "avg_deaths": 7.0,
                "avg_assists": 12.0,
            }
        ],
    }


def test_hero_trend_rejects_unknown_hero(client) -> None:
    response = client.get("/analytics/heroes/999/trend")

    assert response.status_code == 404


def test_hero_matchups_returns_enemy_hero_summary(client) -> None:
    seed_hero(client)
    seed_matchups_data(client)

    response = client.get("/analytics/heroes/1/matchups")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "items": [
            {
                "enemy_hero_id": 52,
                "enemy_hero_name": "Wraith",
                "matches": 2,
                "wins": 1,
                "losses": 1,
                "win_rate": 50.0,
            },
            {
                "enemy_hero_id": 16,
                "enemy_hero_name": "Kelvin",
                "matches": 1,
                "wins": 1,
                "losses": 0,
                "win_rate": 100.0,
            },
        ],
    }


def test_hero_matchups_returns_empty_list_when_no_data(client) -> None:
    seed_hero(client)

    response = client.get("/analytics/heroes/1/matchups")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "items": [],
    }


def test_hero_matchups_rejects_unknown_hero(client) -> None:
    response = client.get("/analytics/heroes/999/matchups")

    assert response.status_code == 404


def test_hero_synergies_returns_ally_hero_summary(client) -> None:
    seed_hero(client)
    seed_synergies_data(client)

    response = client.get("/analytics/heroes/1/synergies")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "items": [
            {
                "ally_hero_id": 16,
                "ally_hero_name": "Kelvin",
                "matches": 1,
                "wins": 1,
                "losses": 0,
                "win_rate": 100.0,
            },
            {
                "ally_hero_id": 52,
                "ally_hero_name": "Wraith",
                "matches": 1,
                "wins": 1,
                "losses": 0,
                "win_rate": 100.0,
            },
        ],
    }


def test_hero_synergies_returns_empty_list_when_no_data(client) -> None:
    seed_hero(client)

    response = client.get("/analytics/heroes/1/synergies")

    assert response.status_code == 200
    assert response.json() == {
        "hero_id": 1,
        "hero_name": "Infernus",
        "items": [],
    }


def test_hero_synergies_rejects_unknown_hero(client) -> None:
    response = client.get("/analytics/heroes/999/synergies")

    assert response.status_code == 404


def test_hero_meta_returns_ranked_entries(client) -> None:
    seed_hero(client)
    seed_hero(client, hero_id=52, name="Wraith")
    seed_match_participants_for_overview(client)

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add(
            MatchParticipant(
                match_id=1001,
                account_id=2999,
                team=1,
                hero_id=52,
                match_result=0,
                player_kills=3,
                player_deaths=8,
                player_assists=4,
                net_worth=9000,
            )
        )
        db.commit()
    finally:
        db.close()

    response = client.get("/analytics/heroes/meta")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "hero_id": 1,
                "hero_name": "Infernus",
                "matches": 2,
                "wins": 1,
                "losses": 1,
                "win_rate": 50.0,
                "avg_kills": 8.0,
                "avg_deaths": 5.5,
                "avg_assists": 10.0,
            },
            {
                "hero_id": 52,
                "hero_name": "Wraith",
                "matches": 1,
                "wins": 0,
                "losses": 1,
                "win_rate": 0.0,
                "avg_kills": 3.0,
                "avg_deaths": 8.0,
                "avg_assists": 4.0,
            },
        ]
    }


def test_hero_meta_supports_sort_and_limit(client) -> None:
    seed_hero(client)
    seed_hero(client, hero_id=52, name="Wraith")
    seed_match_participants_for_overview(client)

    override = client.app.dependency_overrides
    dependency = next(iter(override.values()))
    db: Session = next(dependency())
    try:
        db.add(
            MatchParticipant(
                match_id=1001,
                account_id=2999,
                team=1,
                hero_id=52,
                match_result=1,
                player_kills=11,
                player_deaths=2,
                player_assists=6,
                net_worth=17000,
            )
        )
        db.commit()
    finally:
        db.close()

    response = client.get("/analytics/heroes/meta?sort_by=avg_kills&limit=1")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "hero_id": 52,
                "hero_name": "Wraith",
                "matches": 1,
                "wins": 1,
                "losses": 0,
                "win_rate": 100.0,
                "avg_kills": 11.0,
                "avg_deaths": 2.0,
                "avg_assists": 6.0,
            }
        ]
    }
