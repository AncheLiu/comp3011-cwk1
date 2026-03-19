from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CustomBuildItem(Base):
    __tablename__ = "custom_build_items"
    __table_args__ = (UniqueConstraint("build_id", "display_order", name="uq_build_item_order"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    build_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("custom_builds.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("items.id"), nullable=False)
    category_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_optional: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    annotation: Mapped[str | None] = mapped_column(Text, nullable=True)

    build = relationship("CustomBuild", back_populates="items")
