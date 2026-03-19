from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.custom_build import CustomBuild
from app.models.custom_build_ability import CustomBuildAbility
from app.models.custom_build_item import CustomBuildItem
from app.models.hero import Hero
from app.models.item import Item
from app.schemas.custom_build import (
    CustomBuildAbilityRead,
    CustomBuildCreate,
    CustomBuildItemRead,
    CustomBuildListRead,
    CustomBuildRead,
)


router = APIRouter(prefix="/custom-builds", tags=["custom-builds"])


def _get_existing_hero(hero_id: int, db: Session) -> Hero:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )
    return hero


def _validate_items(payload: CustomBuildCreate, db: Session) -> dict[int, Item]:
    item_ids = [item_payload.item_id for item_payload in payload.items]
    if not item_ids:
        return {}

    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    items_by_id = {item.id: item for item in items}

    missing_ids = [item_id for item_id in item_ids if item_id not in items_by_id]
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {missing_ids[0]} was not found.",
        )

    return items_by_id


def _statement_with_related() -> select:
    return select(CustomBuild).options(
        selectinload(CustomBuild.items),
        selectinload(CustomBuild.abilities),
    )


def _to_detail_read_model(custom_build: CustomBuild, hero_name: str, items_by_id: dict[int, Item]) -> CustomBuildRead:
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
            CustomBuildItemRead(
                id=item.id,
                item_id=item.item_id,
                item_name=items_by_id[item.item_id].name if item.item_id in items_by_id else str(item.item_id),
                item_type=items_by_id[item.item_id].item_type if item.item_id in items_by_id else "unknown",
                category_name=item.category_name,
                display_order=item.display_order,
                is_optional=item.is_optional,
                annotation=item.annotation,
            )
            for item in custom_build.items
        ],
        abilities=[
            CustomBuildAbilityRead(
                id=ability.id,
                ability_id=ability.ability_id,
                display_order=ability.display_order,
                annotation=ability.annotation,
            )
            for ability in custom_build.abilities
        ],
        created_at=custom_build.created_at,
        updated_at=custom_build.updated_at,
    )


def _populate_build_children(custom_build: CustomBuild, payload: CustomBuildCreate) -> None:
    custom_build.items = [
        CustomBuildItem(
            item_id=item_payload.item_id,
            category_name=item_payload.category_name,
            display_order=item_payload.display_order,
            is_optional=item_payload.is_optional,
            annotation=item_payload.annotation,
        )
        for item_payload in payload.items
    ]
    custom_build.abilities = [
        CustomBuildAbility(
            ability_id=ability_payload.ability_id,
            display_order=ability_payload.display_order,
            annotation=ability_payload.annotation,
        )
        for ability_payload in payload.abilities
    ]


@router.post("", response_model=CustomBuildRead, status_code=status.HTTP_201_CREATED)
def create_custom_build(payload: CustomBuildCreate, db: Session = Depends(get_db)) -> CustomBuildRead:
    hero = _get_existing_hero(payload.hero_id, db)
    items_by_id = _validate_items(payload, db)

    custom_build = CustomBuild(
        title=payload.title,
        hero_id=payload.hero_id,
        author_name=payload.author_name,
        playstyle_tag=payload.playstyle_tag,
        description=payload.description,
        notes=payload.notes,
        source_community_build_id=payload.source_community_build_id,
    )
    _populate_build_children(custom_build, payload)

    db.add(custom_build)
    db.commit()
    db.refresh(custom_build)

    return _to_detail_read_model(custom_build, hero.name, items_by_id)


@router.get("", response_model=list[CustomBuildListRead])
def list_custom_builds(db: Session = Depends(get_db)) -> list[CustomBuildListRead]:
    statement = _statement_with_related().order_by(CustomBuild.created_at.desc(), CustomBuild.id.desc())
    custom_builds = list(db.scalars(statement).all())

    hero_ids = {custom_build.hero_id for custom_build in custom_builds}
    heroes = {
        hero.id: hero.name for hero in db.query(Hero).filter(Hero.id.in_(hero_ids)).all()
    } if hero_ids else {}

    return [
        CustomBuildListRead(
            id=custom_build.id,
            title=custom_build.title,
            hero_id=custom_build.hero_id,
            hero_name=heroes.get(custom_build.hero_id, ""),
            author_name=custom_build.author_name,
            playstyle_tag=custom_build.playstyle_tag,
            source_community_build_id=custom_build.source_community_build_id,
            item_count=len(custom_build.items),
            ability_count=len(custom_build.abilities),
            created_at=custom_build.created_at,
            updated_at=custom_build.updated_at,
        )
        for custom_build in custom_builds
    ]


@router.get("/{build_id}", response_model=CustomBuildRead)
def get_custom_build(build_id: int, db: Session = Depends(get_db)) -> CustomBuildRead:
    statement = _statement_with_related().where(CustomBuild.id == build_id)
    custom_build = db.scalars(statement).one_or_none()
    if custom_build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custom build with id {build_id} was not found.",
        )

    hero = _get_existing_hero(custom_build.hero_id, db)
    item_ids = [item.item_id for item in custom_build.items]
    items_by_id = {
        item.id: item for item in db.query(Item).filter(Item.id.in_(item_ids)).all()
    } if item_ids else {}

    return _to_detail_read_model(custom_build, hero.name, items_by_id)


@router.put("/{build_id}", response_model=CustomBuildRead)
def update_custom_build(
    build_id: int, payload: CustomBuildCreate, db: Session = Depends(get_db)
) -> CustomBuildRead:
    statement = _statement_with_related().where(CustomBuild.id == build_id)
    custom_build = db.scalars(statement).one_or_none()
    if custom_build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custom build with id {build_id} was not found.",
        )

    hero = _get_existing_hero(payload.hero_id, db)
    items_by_id = _validate_items(payload, db)

    custom_build.title = payload.title
    custom_build.hero_id = payload.hero_id
    custom_build.author_name = payload.author_name
    custom_build.playstyle_tag = payload.playstyle_tag
    custom_build.description = payload.description
    custom_build.notes = payload.notes
    custom_build.source_community_build_id = payload.source_community_build_id
    db.query(CustomBuildItem).filter(CustomBuildItem.build_id == custom_build.id).delete()
    db.query(CustomBuildAbility).filter(CustomBuildAbility.build_id == custom_build.id).delete()
    db.flush()

    custom_build.items = [
        CustomBuildItem(
            item_id=item_payload.item_id,
            category_name=item_payload.category_name,
            display_order=item_payload.display_order,
            is_optional=item_payload.is_optional,
            annotation=item_payload.annotation,
        )
        for item_payload in payload.items
    ]
    custom_build.abilities = [
        CustomBuildAbility(
            ability_id=ability_payload.ability_id,
            display_order=ability_payload.display_order,
            annotation=ability_payload.annotation,
        )
        for ability_payload in payload.abilities
    ]
    db.flush()

    db.commit()
    db.refresh(custom_build)

    return _to_detail_read_model(custom_build, hero.name, items_by_id)


@router.delete("/{build_id}", status_code=status.HTTP_200_OK)
def delete_custom_build(build_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    custom_build = db.get(CustomBuild, build_id)
    if custom_build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custom build with id {build_id} was not found.",
        )

    db.delete(custom_build)
    db.commit()
    return {"message": "Custom build deleted successfully"}
