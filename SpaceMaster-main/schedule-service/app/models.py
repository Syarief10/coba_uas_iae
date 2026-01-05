from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class ScheduleStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    BLOCKED = "BLOCKED"
    MAINTENANCE = "MAINTENANCE"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ScheduleStatus] = mapped_column(
        Enum(ScheduleStatus),
        nullable=False
    )
