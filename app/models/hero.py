from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Hero(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    class_name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    role_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    playstyle_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    hero_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    complexity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_small_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_card_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_selectable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
