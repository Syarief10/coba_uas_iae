from ariadne import QueryType, ObjectType
from app.services.venue_client import get_venues, get_venue
from app.services.room_client import rooms_by_venue

query = QueryType()
venue = ObjectType("Venue")

@query.field("venues")
def resolve_venues(_, info):
    return get_venues()

@query.field("venue")
def resolve_venue(_, info, id):
    return get_venue(id)

@venue.field("rooms")
def resolve_venue_rooms(obj, info):
    return rooms_by_venue(obj["id"])
