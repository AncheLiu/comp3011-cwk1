from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hero import Hero
from app.schemas.hero import HeroRead


router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("", response_model=list[HeroRead])
def list_heroes(db: Session = Depends(get_db)) -> list[Hero]:
    statement = select(Hero).order_by(Hero.name.asc())
    return list(db.scalars(statement).all())
