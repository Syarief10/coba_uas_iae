from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, UniqueConstraint
from .database import Base

class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (
        UniqueConstraint("name", name="uq_venue_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
