from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hero import Hero
from app.schemas.hero import HeroDetailRead, HeroRead


router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("", response_model=list[HeroRead])
def list_heroes(db: Session = Depends(get_db)) -> list[Hero]:
    statement = select(Hero).order_by(Hero.name.asc())
    return list(db.scalars(statement).all())


@router.get("/{hero_id}", response_model=HeroDetailRead)
def get_hero(hero_id: int, db: Session = Depends(get_db)) -> Hero:
    hero = db.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} was not found.",
        )
    return hero
