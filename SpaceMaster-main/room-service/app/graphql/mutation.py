from ariadne import MutationType
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import Room
from app.auth import require_admin_from_context, AuthError
from app.services.venue_client import fetch_venue, VenueServiceError
from graphql import GraphQLError

mutation = MutationType()
@mutation.field("createRoom")
def create_room(_, info, data):
    require_admin_from_context(info)

    # VALIDASI KE VENUE SERVICE
    try:
        venue = fetch_venue(data["venueId"])
        if not venue:
            raise GraphQLError(
                message="Venue not found",
                extensions={"code": "NOT_FOUND", "http": {"status": 404}}
            )
    except VenueServiceError:
        raise GraphQLError(
            message="Venue service unavailable",
            extensions={"code": "SERVICE_UNAVAILABLE", "http": {"status": 503}}
        )

    db = SessionLocal()
    try:
        room = Room(
            name=data["name"],
            capacity=data["capacity"],
            venue_id=data["venueId"]
        )
        db.add(room)
        db.commit()
        db.refresh(room)

        return {
            "id": room.id,
            "name": room.name,
            "capacity": room.capacity,
            "venueId": room.venue_id
        }

    finally:
        db.close()
