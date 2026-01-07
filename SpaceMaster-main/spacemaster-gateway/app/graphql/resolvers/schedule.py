from ariadne import QueryType, ObjectType, MutationType
from app.services.schedule_client import (
    get_schedules,
    available_slots,
    block_schedule
)
from app.services.room_client import get_room

query = QueryType()
mutation = MutationType()
schedule = ObjectType("Schedule")

@query.field("schedules")
def resolve_schedules(_, info):
    return get_schedules()

@schedule.field("room")
def resolve_schedule_room(obj, info):
    return get_room(obj["roomId"])

@query.field("availableSlots")
def resolve_available_slots(_, info, roomId, startDate, endDate):
    return available_slots(roomId, startDate, endDate)

@mutation.field("blockSchedule")
def resolve_block_schedule(_, info, input):
    return block_schedule(
        room_id=input["roomId"],
        start_time=input["startTime"],
        end_time=input["endTime"]
    )
