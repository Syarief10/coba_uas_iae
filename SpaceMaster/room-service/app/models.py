from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    venue_id: Mapped[int] = mapped_column(Integer, nullable=False)
