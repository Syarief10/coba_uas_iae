from ariadne import QueryType
from graphql import GraphQLError
from app.database import SessionLocal
from app.models import Room

query = QueryType()

@query.field("roomsByVenue")
def resolve_rooms_by_venue(_, info, venueId):
    db = SessionLocal()
    try:
        return db.query(Room).filter(Room.venue_id == venueId).all()
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
