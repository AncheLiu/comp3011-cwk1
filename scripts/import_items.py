import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.item import Item


ITEMS_URL = "https://assets.deadlock-api.com/v2/items"


def fetch_items() -> list[dict]:
    request = Request(ITEMS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def infer_item_type(payload: dict) -> str:
    if payload.get("type"):
        return str(payload["type"])
    if payload.get("ability_type"):
        return "ability"
    if payload.get("weapon_info"):
        return "weapon"
    return "unknown"


def map_item_record(payload: dict) -> dict:
    heroes = payload.get("heroes") or []
    hero_id = heroes[0] if heroes else payload.get("hero")

    return {
        "id": payload["id"],
        "name": payload["name"],
        "class_name": payload["class_name"],
        "item_type": infer_item_type(payload),
        "hero_id": hero_id,
        "image_url": payload.get("image"),
        "raw_json": json.dumps(payload),
    }


def upsert_items(records: list[dict]) -> tuple[int, int]:
    db = SessionLocal()
    created = 0
    updated = 0

    try:
        for payload in records:
            mapped = map_item_record(payload)
            existing = db.get(Item, mapped["id"])

            if existing is None:
                db.add(Item(**mapped))
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

    records = fetch_items()
    created, updated = upsert_items(records)

    print(f"Imported {len(records)} item records")
    print(f"Created: {created}")
    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
