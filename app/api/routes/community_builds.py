import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.community_build import CommunityBuild
from app.models.hero import Hero
from app.schemas.community_build import CommunityBuildDetailRead, CommunityBuildRead


router = APIRouter(prefix="/community-builds", tags=["community-builds"])


@router.get("", response_model=list[CommunityBuildRead])
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


@router.get("/{build_id}", response_model=CommunityBuildDetailRead)
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
