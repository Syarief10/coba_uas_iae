from ariadne import MutationType
from app.database import SessionLocal
from app.models import Schedule
from app.auth import require_admin
from app.room_client import room_exists
from fastapi import HTTPException

mutation = MutationType()


@mutation.field("createSchedule")
def create_schedule(_, info, data):
    require_admin(info)

    if not room_exists(data["roomId"]):
        raise HTTPException(status_code=404, detail="Room tidak tersedia")

    db = SessionLocal()
    try:
        schedule = Schedule(
            room_id=data["roomId"],
            start_time=data["startTime"],
            end_time=data["endTime"],
            status=data["status"]
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    finally:
        db.close()


@mutation.field("updateSchedule")
def update_schedule(_, info, id, data):
    require_admin(info)

    db = SessionLocal()
    try:
        schedule = db.get(Schedule, int(id))
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule tidak ditemukan")

        if "roomId" in data:
            if not room_exists(data["roomId"]):
                raise HTTPException(status_code=404, detail="Room tidak tersedia")
            schedule.room_id = data["roomId"]

        if "startTime" in data:
            schedule.start_time = data["startTime"]

        if "endTime" in data:
            schedule.end_time = data["endTime"]

        if "status" in data:
            schedule.status = data["status"]

        db.commit()
        db.refresh(schedule)
        return schedule
    finally:
        db.close()


@mutation.field("deleteSchedule")
def delete_schedule(_, info, id):
    require_admin(info)

    db = SessionLocal()
    try:
        schedule = db.get(Schedule, int(id))
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule tidak ditemukan")

        db.delete(schedule)
        db.commit()
        return True
    finally:
        db.close()
