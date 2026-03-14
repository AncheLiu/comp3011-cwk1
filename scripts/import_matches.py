import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import sys
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.hero import Hero
from app.models.match import Match
from app.models.match_participant import MatchParticipant


RECENT_MATCHES_URL = "https://api.deadlock-api.com/v1/matches/recently-fetched"
MATCH_METADATA_URL = "https://api.deadlock-api.com/v1/matches/{match_id}/metadata"


def fetch_json(url: str) -> list[dict] | dict:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_recent_matches(limit: int) -> list[dict]:
    payload = fetch_json(RECENT_MATCHES_URL)
    finished_matches = [record for record in payload if record.get("game_mode") == 1]
    return finished_matches[:limit]


def fetch_match_metadata(match_id: int) -> dict:
    return fetch_json(MATCH_METADATA_URL.format(match_id=match_id))


def to_datetime(timestamp: int | None) -> datetime:
    if not timestamp:
        return datetime.now(UTC)
    return datetime.fromtimestamp(timestamp, tz=UTC)


def latest_stats(player_payload: dict) -> dict:
    stats = player_payload.get("stats") or []
    if not stats:
        return {}
    return stats[-1]


def map_match(summary_payload: dict, metadata_payload: dict) -> dict:
    match_info = metadata_payload.get("match_info") or {}
    players = match_info.get("players") or []
    team_zero_net_worth = sum(
        int(player.get("net_worth") or 0) for player in players if player.get("team") == 0
    )
    team_one_net_worth = sum(
        int(player.get("net_worth") or 0) for player in players if player.get("team") == 1
    )

    return {
        "id": summary_payload["match_id"],
        "start_time": to_datetime(match_info.get("start_time") or summary_payload.get("start_time")),
        "game_mode": str(match_info.get("game_mode") or summary_payload.get("game_mode") or "unknown"),
        "match_mode": str(
            match_info.get("match_mode") or summary_payload.get("match_mode") or "unknown"
        ),
        "region_mode": str(match_info.get("region_mode") or "unknown"),
        "duration_seconds": match_info.get("duration_s") or summary_payload.get("duration_s"),
        "winning_team": match_info.get("winning_team"),
        "net_worth_team_0": team_zero_net_worth,
        "net_worth_team_1": team_one_net_worth,
        "objectives_mask_team0": match_info.get("objectives_mask_team0"),
        "objectives_mask_team1": match_info.get("objectives_mask_team1"),
        "source": "deadlock_api",
        "ingested_at": datetime.now(UTC),
    }


def map_participant(match_id: int, winning_team: int | None, player_payload: dict) -> dict:
    final_stats = latest_stats(player_payload)
    player_team = player_payload.get("team")

    if winning_team is None or player_team is None:
        match_result = None
    else:
        match_result = 1 if int(player_team) == int(winning_team) else 0

    return {
        "match_id": match_id,
        "account_id": player_payload["account_id"],
        "team": player_team,
        "hero_id": player_payload["hero_id"],
        "hero_level": player_payload.get("level"),
        "match_result": match_result,
        "player_kills": int(player_payload.get("kills") or 0),
        "player_deaths": int(player_payload.get("deaths") or 0),
        "player_assists": int(player_payload.get("assists") or 0),
        "last_hits": int(player_payload.get("last_hits") or 0),
        "denies": int(player_payload.get("denies") or 0),
        "net_worth": player_payload.get("net_worth"),
        "player_damage": final_stats.get("player_damage"),
        "damage_taken": final_stats.get("player_damage_taken"),
        "boss_damage": final_stats.get("boss_damage"),
        "creep_damage": final_stats.get("creep_damage"),
        "neutral_damage": final_stats.get("neutral_damage"),
        "shots_hit": final_stats.get("shots_hit"),
        "shots_missed": final_stats.get("shots_missed"),
    }


def upsert_match_data(limit: int) -> tuple[int, int, int]:
    db = SessionLocal()
    created_matches = 0
    created_participants = 0
    skipped_matches = 0

    try:
        recent_matches = fetch_recent_matches(limit)

        for summary_payload in recent_matches:
            metadata_payload = fetch_match_metadata(summary_payload["match_id"])
            match_info = metadata_payload.get("match_info") or {}
            players = match_info.get("players") or []

            hero_ids = {player.get("hero_id") for player in players if player.get("hero_id") is not None}
            existing_hero_ids = {
                hero_id
                for (hero_id,) in db.query(Hero.id).filter(Hero.id.in_(hero_ids)).all()
            }
            missing_hero_ids = hero_ids - existing_hero_ids
            if missing_hero_ids:
                skipped_matches += 1
                print(
                    f"Skipped match {summary_payload['match_id']} because heroes are missing: "
                    f"{sorted(missing_hero_ids)}"
                )
                continue

            mapped_match = map_match(summary_payload, metadata_payload)
            existing_match = db.get(Match, mapped_match["id"])
            if existing_match is None:
                db.add(Match(**mapped_match))
                created_matches += 1
            else:
                for field, value in mapped_match.items():
                    setattr(existing_match, field, value)

            for player_payload in players:
                mapped_participant = map_participant(
                    match_id=summary_payload["match_id"],
                    winning_team=mapped_match["winning_team"],
                    player_payload=player_payload,
                )
                existing_participant = (
                    db.query(MatchParticipant)
                    .filter(
                        MatchParticipant.match_id == mapped_participant["match_id"],
                        MatchParticipant.account_id == mapped_participant["account_id"],
                    )
                    .one_or_none()
                )

                if existing_participant is None:
                    db.add(MatchParticipant(**mapped_participant))
                    created_participants += 1
                    continue

                for field, value in mapped_participant.items():
                    setattr(existing_participant, field, value)

        db.commit()
        return created_matches, created_participants, skipped_matches
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a small batch of recent finished Deadlock matches into the local database."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of recent finished matches to import. Default: 5",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    Base.metadata.create_all(bind=engine)

    created_matches, created_participants, skipped_matches = upsert_match_data(args.limit)
    print(f"Processed up to {args.limit} recent matches")
    print(f"Created or updated matches: {created_matches}")
    print(f"Created or updated participants: {created_participants}")
    print(f"Skipped matches: {skipped_matches}")


if __name__ == "__main__":
    main()
