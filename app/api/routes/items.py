from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemRead


router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    statement = select(Item).order_by(Item.name.asc())
    return list(db.scalars(statement).all())
