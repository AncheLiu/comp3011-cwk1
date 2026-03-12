from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    game_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    match_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    region_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    winning_team: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    net_worth_team_0: Mapped[int | None] = mapped_column(Integer, nullable=True)
    net_worth_team_1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    objectives_mask_team0: Mapped[int | None] = mapped_column(Integer, nullable=True)
    objectives_mask_team1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="deadlock_api")
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
