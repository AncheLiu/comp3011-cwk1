from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    class_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)
    hero_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("heroes.id"), nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
