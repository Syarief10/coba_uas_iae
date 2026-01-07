from ariadne import QueryType, ObjectType
from app.database import SessionLocal
from datetime import datetime, timedelta
from app.models import Schedule, ScheduleStatus

query = QueryType()
schedule = ObjectType("Schedule")

@query.field("schedules")
def resolve_schedules(_, info):
    db = SessionLocal()
    try:
        return db.query(Schedule).all()
    finally:
        db.close()

@schedule.field("roomId")
def resolve_room_id(obj, *_):
    return obj.room_id

@schedule.field("startTime")
def resolve_start_time(obj, *_):
    return obj.start_time

@schedule.field("endTime")
def resolve_end_time(obj, *_):
    return obj.end_time

@schedule.field("status")
def resolve_status(obj, *_):
    return obj.status.value

@query.field("availableSlots")
def resolve_available_slots(_, info, roomId, startDate, endDate):
    db = SessionLocal()
    try:
        start = datetime.fromisoformat(startDate)
        end = datetime.fromisoformat(endDate)

        schedules = (
            db.query(Schedule)
            .filter(
                Schedule.room_id == roomId,
                Schedule.start_time >= start.isoformat(),
                Schedule.end_time <= end.isoformat(),
                Schedule.status != ScheduleStatus.AVAILABLE
            )
            .all()
        )

        blocked = [
            (s.start_time, s.end_time)
            for s in schedules
            if s.status != ScheduleStatus.AVAILABLE
        ]

        slots = []
        current = start

        for b_start, b_end in sorted(blocked):
            if current < datetime.fromisoformat(b_start):
                slots.append({
                    "startTime": current.isoformat(),
                    "endTime": b_start
                })
            current = max(current, datetime.fromisoformat(b_end))

        if current < end:
            slots.append({
                "startTime": current.isoformat(),
                "endTime": end.isoformat()
            })

        return slots
    finally:
        db.close()