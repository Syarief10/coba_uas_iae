from ariadne import MutationType
from app.database import SessionLocal
from app.models import Schedule, ScheduleStatus
from app.auth import require_admin
from app.room_client import room_exists
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import DateTime

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

@mutation.field("blockSchedule")
def resolve_block_schedule(_, info, input):
    db = SessionLocal()
    try:
        room_id = input["roomId"]

        start_time = datetime.fromisoformat(input["startTime"])
        end_time = datetime.fromisoformat(input["endTime"])

        schedules = db.query(Schedule).filter(
            Schedule.room_id == room_id,
            Schedule.status == ScheduleStatus.AVAILABLE,
            Schedule.start_time < end_time,
            Schedule.end_time > start_time
        ).all()

        if not schedules:
            return {
                "success": False,
                "message": "Tidak ada jadwal AVAILABLE yang bisa diblok"
            }

        for s in schedules:
            s.status = ScheduleStatus.BLOCKED

        db.commit()

        return {
            "success": True,
            "message": f"{len(schedules)} schedule berhasil diblok"
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        db.close()

