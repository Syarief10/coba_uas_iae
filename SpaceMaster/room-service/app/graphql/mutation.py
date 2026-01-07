from ariadne import MutationType
from app.database import SessionLocal
from app.models import Room
from app.auth import require_admin_from_context, AuthError
from app.services.venue_client import fetch_venue, VenueServiceError
from graphql import GraphQLError

mutation = MutationType()


@mutation.field("createRoom")
def create_room(_, info, data):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        raise GraphQLError(
            message=str(e),
            extensions={"code": "UNAUTHORIZED", "http": {"status": 401}}
        )

    # VALIDASI VENUE KE VENUE-SERVICE
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
            venue_id=int(data["venueId"])
        )

        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    finally:
        db.close()
@mutation.field("updateRoom")
def update_room(_, info, data):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        raise GraphQLError(
            message=str(e),
            extensions={"code": "UNAUTHORIZED", "http": {"status": 401}}
        )

    db = SessionLocal()
    try:
        room = db.get(Room, int(data["id"]))
        if not room:
            raise GraphQLError(
                message="Room tidak ditemukan",
                extensions={"code": "NOT_FOUND", "http": {"status": 404}}
            )

        if "name" in data and data["name"] is not None:
            room.name = data["name"]

        if "capacity" in data and data["capacity"] is not None:
            room.capacity = data["capacity"]

        db.commit()
        db.refresh(room)
        return room

    finally:
        db.close()


@mutation.field("deleteRoom")
def delete_room(_, info, id):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        raise GraphQLError(
            message=str(e),
            extensions={"code": "UNAUTHORIZED", "http": {"status": 401}}
        )

    db = SessionLocal()
    try:
        room = db.get(Room, int(id))
        if not room:
            raise GraphQLError(
                message="Room tidak ditemukan",
                extensions={"code": "NOT_FOUND", "http": {"status": 404}}
            )

        db.delete(room)
        db.commit()
        return True

    finally:
        db.close()
