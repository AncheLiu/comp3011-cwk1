from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CommunityBuild(Base):
    __tablename__ = "community_builds"
    __table_args__ = (UniqueConstraint("hero_build_id", "version", name="uq_hero_build_version"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hero_build_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    hero_id: Mapped[int] = mapped_column(Integer, nullable=False)
    author_account_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[int | None] = mapped_column(Integer, nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_updated_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    publish_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    favorites_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tags_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    details_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
