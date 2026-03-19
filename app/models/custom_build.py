from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CustomBuild(Base):
    __tablename__ = "custom_builds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    hero_id: Mapped[int] = mapped_column(Integer, ForeignKey("heroes.id"), nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    playstyle_tag: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_community_build_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    items = relationship(
        "CustomBuildItem",
        back_populates="build",
        cascade="all, delete-orphan",
        order_by="CustomBuildItem.display_order",
    )
    abilities = relationship(
        "CustomBuildAbility",
        back_populates="build",
        cascade="all, delete-orphan",
        order_by="CustomBuildAbility.display_order",
    )
