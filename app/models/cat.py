from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SpyCat(Base):
    __tablename__ = "spy_cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(120), nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    mission = relationship("Mission", back_populates="cat", uselist=False)
