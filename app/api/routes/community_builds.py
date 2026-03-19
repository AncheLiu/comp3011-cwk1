import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.community_build import CommunityBuild
from app.models.custom_build import CustomBuild
from app.models.custom_build_ability import CustomBuildAbility
from app.models.custom_build_item import CustomBuildItem
from app.models.hero import Hero
from app.models.item import Item
from app.schemas.custom_build import CustomBuildRead
from app.schemas.community_build import CommunityBuildDetailRead, CommunityBuildRead


router = APIRouter(prefix="/community-builds", tags=["community-builds"])


def _parse_item_rows(details_json: dict, items_by_id: dict[int, Item]) -> list[CustomBuildItem]:
    rows: list[CustomBuildItem] = []
    display_order = 1

    for category in details_json.get("mod_categories") or []:
        if not isinstance(category, dict):
            continue

        category_name = category.get("name")
        mods = category.get("mods") or []
        for mod in mods:
            if not isinstance(mod, dict):
                continue

            item_id = mod.get("ability_id")
            if item_id is None or item_id not in items_by_id:
                continue

            rows.append(
                CustomBuildItem(
                    item_id=item_id,
                    category_name=category_name,
                    display_order=display_order,
                    is_optional=bool(category.get("optional") or False),
                    annotation=mod.get("annotation"),
                )
            )
            display_order += 1

    return rows


def _parse_ability_rows(details_json: dict) -> list[CustomBuildAbility]:
    rows: list[CustomBuildAbility] = []
    display_order = 1

    ability_order = details_json.get("ability_order") or {}
    currency_changes = ability_order.get("currency_changes") or []
    for change in currency_changes:
        if not isinstance(change, dict):
            continue

        ability_id = change.get("ability_id")
        if ability_id is None:
            continue

        rows.append(
            CustomBuildAbility(
                ability_id=ability_id,
                display_order=display_order,
                annotation=change.get("annotation"),
            )
        )
        display_order += 1

    return rows


def _to_custom_build_read(custom_build: CustomBuild, hero_name: str, items_by_id: dict[int, Item]) -> CustomBuildRead:
    return CustomBuildRead(
        id=custom_build.id,
        title=custom_build.title,
        hero_id=custom_build.hero_id,
        hero_name=hero_name,
        author_name=custom_build.author_name,
        playstyle_tag=custom_build.playstyle_tag,
        description=custom_build.description,
        notes=custom_build.notes,
        source_community_build_id=custom_build.source_community_build_id,
        items=[
            {
                "id": item.id,
                "item_id": item.item_id,
                "item_name": items_by_id[item.item_id].name if item.item_id in items_by_id else str(item.item_id),
                "item_type": items_by_id[item.item_id].item_type if item.item_id in items_by_id else "unknown",
                "category_name": item.category_name,
                "display_order": item.display_order,
                "is_optional": item.is_optional,
                "annotation": item.annotation,
            }
            for item in custom_build.items
        ],
        abilities=[
            {
                "id": ability.id,
                "ability_id": ability.ability_id,
                "display_order": ability.display_order,
                "annotation": ability.annotation,
            }
            for ability in custom_build.abilities
        ],
        created_at=custom_build.created_at,
        updated_at=custom_build.updated_at,
    )


@router.get(
    "",
    response_model=list[CommunityBuildRead],
    summary="List imported community builds",
    description="Returns community builds imported from public Deadlock sources, optionally filtered to a single hero.",
    responses={404: {"description": "Requested hero was not found."}},
)
def list_community_builds(
    hero_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CommunityBuildRead]:
    statement = select(CommunityBuild)

    if hero_id is not None:
        hero = db.get(Hero, hero_id)
        if hero is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hero with id {hero_id} was not found.",
            )
        statement = statement.where(CommunityBuild.hero_id == hero_id)

    statement = statement.order_by(
        CommunityBuild.favorites_count.desc().nullslast(),
        CommunityBuild.id.desc(),
    )
    builds = list(db.scalars(statement).all())
    return [CommunityBuildRead.model_validate(build) for build in builds]


@router.get(
    "/{build_id}",
    response_model=CommunityBuildDetailRead,
    summary="Get a community build",
    description="Returns the stored community build snapshot, including tags and the raw imported build details payload.",
    responses={404: {"description": "Community build was not found."}},
)
def get_community_build(build_id: int, db: Session = Depends(get_db)) -> CommunityBuildDetailRead:
    build = db.get(CommunityBuild, build_id)
    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Community build with id {build_id} was not found.",
        )

    return CommunityBuildDetailRead(
        id=build.id,
        hero_build_id=build.hero_build_id,
        hero_id=build.hero_id,
        author_account_id=build.author_account_id,
        name=build.name,
        description=build.description,
        language=build.language,
        version=build.version,
        last_updated_timestamp=build.last_updated_timestamp,
        publish_timestamp=build.publish_timestamp,
        favorites_count=build.favorites_count,
        tags_json=json.loads(build.tags_json) if build.tags_json else None,
        details_json=json.loads(build.details_json),
    )


@router.post(
    "/{build_id}/clone-to-custom",
    response_model=CustomBuildRead,
    status_code=status.HTTP_201_CREATED,
    summary="Clone a community build into a custom build",
    description=(
        "Creates an editable custom build draft from an imported community build. "
        "The endpoint copies the hero and description, stores the source community build id, "
        "extracts item rows from mod categories, and extracts ability progression from the imported ability order."
    ),
    responses={
        201: {"description": "Custom build draft created successfully."},
        404: {"description": "Community build or referenced hero was not found."},
    },
)
def clone_community_build_to_custom(build_id: int, db: Session = Depends(get_db)) -> CustomBuildRead:
    build = db.get(CommunityBuild, build_id)
    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Community build with id {build_id} was not found.",
        )

    hero = db.get(Hero, build.hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {build.hero_id} was not found.",
        )

    details_json = json.loads(build.details_json)
    item_ids = []
    for category in details_json.get("mod_categories") or []:
        if not isinstance(category, dict):
            continue
        for mod in category.get("mods") or []:
            if isinstance(mod, dict) and mod.get("ability_id") is not None:
                item_ids.append(mod["ability_id"])

    items = db.query(Item).filter(Item.id.in_(item_ids)).all() if item_ids else []
    items_by_id = {item.id: item for item in items}

    custom_build = CustomBuild(
        title=f"{build.name} (Custom Copy)",
        hero_id=build.hero_id,
        author_name="student",
        playstyle_tag=None,
        description=build.description,
        notes="Cloned from imported community build.",
        source_community_build_id=build.hero_build_id,
    )
    custom_build.items = _parse_item_rows(details_json, items_by_id)
    custom_build.abilities = _parse_ability_rows(details_json)

    db.add(custom_build)
    db.commit()
    db.refresh(custom_build)

    refreshed_items = {item.id: item for item in db.query(Item).filter(Item.id.in_([row.item_id for row in custom_build.items])).all()} if custom_build.items else {}
    return _to_custom_build_read(custom_build, hero.name, refreshed_items)
