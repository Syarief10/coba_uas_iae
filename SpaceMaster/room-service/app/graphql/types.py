from ariadne import ObjectType

room = ObjectType("Room")

@room.field("venueId")
def resolve_room_venue_id(obj, *_):
    return obj.venue_id