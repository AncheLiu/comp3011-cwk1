from sqlalchemy import BigInteger, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CustomBuildAbility(Base):
    __tablename__ = "custom_build_abilities"
    __table_args__ = (UniqueConstraint("build_id", "display_order", name="uq_build_ability_order"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    build_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("custom_builds.id"), nullable=False)
    ability_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    annotation: Mapped[str | None] = mapped_column(Text, nullable=True)

    build = relationship("CustomBuild", back_populates="abilities")
