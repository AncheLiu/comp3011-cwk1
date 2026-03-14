from sqlalchemy.orm import Session

from app.models.hero import Hero
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
