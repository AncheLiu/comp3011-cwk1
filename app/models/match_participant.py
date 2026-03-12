from sqlalchemy import BigInteger, ForeignKey, Integer, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MatchParticipant(Base):
    __tablename__ = "match_participants"
    __table_args__ = (UniqueConstraint("match_id", "account_id", name="uq_match_account"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("matches.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    team: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    hero_id: Mapped[int] = mapped_column(Integer, ForeignKey("heroes.id"), nullable=False)
    hero_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    match_result: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    player_kills: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    player_deaths: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    player_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_hits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    denies: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    net_worth: Mapped[int | None] = mapped_column(Integer, nullable=True)
    player_damage: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    damage_taken: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    boss_damage: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    creep_damage: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    neutral_damage: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    shots_hit: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    shots_missed: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
