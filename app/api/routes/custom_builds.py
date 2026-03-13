import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.custom_build import CustomBuild
from app.models.hero import Hero
from app.schemas.custom_build import CustomBuildCreate, CustomBuildRead


router = APIRouter(prefix="/custom-builds", tags=["custom-builds"])


def _to_read_model(custom_build: CustomBuild) -> CustomBuildRead:
    return CustomBuildRead(
        id=custom_build.id,
        title=custom_build.title,
        hero_id=custom_build.hero_id,
        author_name=custom_build.author_name,
        playstyle_tag=custom_build.playstyle_tag,
        description=custom_build.description,
        items_json=json.loads(custom_build.items_json),
        ability_order_json=(
            json.loads(custom_build.ability_order_json) if custom_build.ability_order_json else None
        ),
        notes=custom_build.notes,
        created_at=custom_build.created_at,
        updated_at=custom_build.updated_at,
    )


@router.post("", response_model=CustomBuildRead, status_code=status.HTTP_201_CREATED)
def create_custom_build(payload: CustomBuildCreate, db: Session = Depends(get_db)) -> CustomBuildRead:
    hero = db.get(Hero, payload.hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {payload.hero_id} was not found.",
        )

    custom_build = CustomBuild(
        title=payload.title,
        hero_id=payload.hero_id,
        author_name=payload.author_name,
        playstyle_tag=payload.playstyle_tag,
        description=payload.description,
        items_json=json.dumps(payload.items_json),
        ability_order_json=(
            json.dumps(payload.ability_order_json) if payload.ability_order_json is not None else None
        ),
        notes=payload.notes,
    )
    db.add(custom_build)
    db.commit()
    db.refresh(custom_build)
    return _to_read_model(custom_build)


@router.get("", response_model=list[CustomBuildRead])
def list_custom_builds(db: Session = Depends(get_db)) -> list[CustomBuildRead]:
    statement = select(CustomBuild).order_by(CustomBuild.created_at.desc(), CustomBuild.id.desc())
    custom_builds = list(db.scalars(statement).all())
    return [_to_read_model(custom_build) for custom_build in custom_builds]


@router.get("/{build_id}", response_model=CustomBuildRead)
def get_custom_build(build_id: int, db: Session = Depends(get_db)) -> CustomBuildRead:
    custom_build = db.get(CustomBuild, build_id)
    if custom_build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custom build with id {build_id} was not found.",
        )
    return _to_read_model(custom_build)
