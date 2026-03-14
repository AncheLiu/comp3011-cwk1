import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.community_build import CommunityBuild
from app.models.hero import Hero


BUILDS_URL = "https://api.deadlock-api.com/v1/builds"


def fetch_json(url: str) -> list[dict] | dict:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def build_url(hero_id: int) -> str:
    return f"{BUILDS_URL}?{urlencode({'hero_id': hero_id})}"


def fetch_builds_for_hero(hero_id: int) -> list[dict]:
    return fetch_json(build_url(hero_id))


def to_datetime(timestamp: int | None) -> datetime | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, tz=UTC)


def upsert_builds(hero_ids: list[int], per_hero_limit: int) -> tuple[int, int]:
    db = SessionLocal()
    created = 0
    updated = 0

    try:
        for hero_id in hero_ids:
            payloads = fetch_builds_for_hero(hero_id)[:per_hero_limit]
            for payload in payloads:
                hero_build = payload.get("hero_build") or {}
                details = hero_build.get("details") or {}
                mapped = {
                    "hero_build_id": hero_build["hero_build_id"],
                    "hero_id": hero_build["hero_id"],
                    "author_account_id": hero_build.get("author_account_id"),
                    "name": hero_build["name"],
                    "description": hero_build.get("description"),
                    "language": hero_build.get("language"),
                    "version": hero_build.get("version"),
                    "last_updated_timestamp": to_datetime(hero_build.get("last_updated_timestamp")),
                    "publish_timestamp": to_datetime(hero_build.get("publish_timestamp")),
                    "favorites_count": payload.get("num_favorites"),
                    "tags_json": json.dumps(hero_build.get("tags") or []),
                    "details_json": json.dumps(details),
                }

                existing = (
                    db.query(CommunityBuild)
                    .filter(
                        CommunityBuild.hero_build_id == mapped["hero_build_id"],
                        CommunityBuild.version == mapped["version"],
                    )
                    .one_or_none()
                )

                if existing is None:
                    db.add(CommunityBuild(**mapped))
                    created += 1
                    continue

                for field, value in mapped.items():
                    setattr(existing, field, value)
                updated += 1

        db.commit()
        return created, updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import community build snapshots for a subset of heroes."
    )
    parser.add_argument(
        "--hero-limit",
        type=int,
        default=3,
        help="Number of heroes to import builds for. Default: 3",
    )
    parser.add_argument(
        "--per-hero-limit",
        type=int,
        default=5,
        help="Number of builds to import per hero. Default: 5",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        hero_ids = [hero_id for (hero_id,) in db.query(Hero.id).order_by(Hero.id.asc()).limit(args.hero_limit)]
    finally:
        db.close()

    created, updated = upsert_builds(hero_ids, args.per_hero_limit)
    print(f"Imported community builds for {len(hero_ids)} heroes")
    print(f"Created: {created}")
    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
