from ariadne import QueryType, ObjectType
from app.database import SessionLocal
from app.models import Schedule

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
