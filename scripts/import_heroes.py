import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.hero import Hero


HEROES_URL = "https://assets.deadlock-api.com/v2/heroes"


def fetch_heroes() -> list[dict]:
    request = Request(HEROES_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def map_hero_record(payload: dict) -> dict:
    description = payload.get("description") or {}
    images = payload.get("images") or {}

    return {
        "id": payload["id"],
        "name": payload["name"],
        "class_name": payload["class_name"],
        "role_text": description.get("role"),
        "playstyle_text": description.get("playstyle"),
        "hero_type": payload.get("hero_type"),
        "complexity": payload.get("complexity"),
        "image_small_url": images.get("icon_image_small"),
        "image_card_url": images.get("icon_hero_card"),
        "is_selectable": payload.get("player_selectable", True),
        "raw_json": json.dumps(payload),
    }


def upsert_heroes(records: list[dict]) -> tuple[int, int]:
    db = SessionLocal()
    created = 0
    updated = 0

    try:
        for payload in records:
            mapped = map_hero_record(payload)
            existing = db.get(Hero, mapped["id"])

            if existing is None:
                db.add(Hero(**mapped))
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


def main() -> None:
    Base.metadata.create_all(bind=engine)

    records = fetch_heroes()
    created, updated = upsert_heroes(records)

    print(f"Imported {len(records)} hero records")
    print(f"Created: {created}")
    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
