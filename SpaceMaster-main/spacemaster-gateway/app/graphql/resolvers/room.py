from ariadne import QueryType, ObjectType
from app.services.room_client import rooms_by_venue, get_room
from app.services.schedule_client import schedules_by_room
from app.services.venue_client import get_venue

query = QueryType()
room = ObjectType("Room")

@query.field("roomsByVenue")
def resolve_rooms_by_venue(_, info, venueId):
    return rooms_by_venue(venueId)

@query.field("room")
def resolve_room(_, info, id):
    return get_room(id)

@room.field("schedules")
def resolve_room_schedules(obj, info):
    return schedules_by_room(obj["id"])

@room.field("venue")
def resolve_room_venue(obj, info):
    return get_venue(obj["venueId"])