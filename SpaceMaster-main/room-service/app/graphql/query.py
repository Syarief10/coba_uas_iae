from ariadne import QueryType, ObjectType
from graphql import GraphQLError
from app.database import SessionLocal
from app.models import Room

query = QueryType()
room = ObjectType("Room")

@query.field("roomsByVenue")
def resolve_rooms_by_venue(_, info, venueId):
    db = SessionLocal()
    try:
        return db.query(Room).filter(Room.venue_id == int(venueId)).all()
    finally:
        db.close()

@query.field("room")
def resolve_room(_, info, id):
    db = SessionLocal()
    try:
        room = db.get(Room, id)
        if not room:
            raise GraphQLError(
                message="Room tidak ditemukan",
                extensions={
                    "code": "NOT_FOUND",
                    "http": {"status": 404}
                }
            )
        return room
    finally:
        db.close()

@room.field("venueId")
def resolve_venue_id(obj, *_):
    return obj.venue_id