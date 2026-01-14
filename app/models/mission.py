from sqlalchemy import Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("spy_cats.id", ondelete="SET NULL"),
        nullable=True
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    cat = relationship("SpyCat", back_populates="mission")
    targets = relationship(
        "Target",
        back_populates="mission",
        cascade="all, delete-orphan"
    )


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int] = mapped_column(
        ForeignKey("missions.id", ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str] = mapped_column(String(120))
    notes: Mapped[str] = mapped_column(Text, default="")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
