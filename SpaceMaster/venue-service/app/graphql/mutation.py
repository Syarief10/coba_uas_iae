from ariadne import MutationType
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import Venue
from app.auth import require_admin_from_context, AuthError

mutation = MutationType()


@mutation.field("createVenue")
def create_venue(_, info, data):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        return {
            "success": False,
            "message": str(e),
            "venue": None
        }

    db = SessionLocal()
    try:
        exists = db.query(Venue).filter(Venue.name == data["name"]).first()
        if exists:
            return {
                "success": False,
                "message": "Venue name already exists",
                "venue": None
            }

        venue = Venue(**data)
        db.add(venue)
        db.commit()
        db.refresh(venue)

        return {
            "success": True,
            "message": "Venue created successfully",
            "venue": venue
        }

    except IntegrityError:
        db.rollback()
        return {
            "success": False,
            "message": "Venue name must be unique",
            "venue": None
        }
    finally:
        db.close()


@mutation.field("updateVenue")
def update_venue(_, info, id, data):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        return {
            "success": False,
            "message": str(e),
            "venue": None
        }

    db = SessionLocal()
    try:
        venue = db.get(Venue, id)
        if not venue:
            return {
                "success": False,
                "message": "Venue not found",
                "venue": None
            }

        for k, v in data.items():
            setattr(venue, k, v)

        db.commit()
        db.refresh(venue)

        return {
            "success": True,
            "message": "Venue updated successfully",
            "venue": venue
        }
    finally:
        db.close()


@mutation.field("deleteVenue")
def delete_venue(_, info, id):
    try:
        require_admin_from_context(info)
    except AuthError as e:
        return {
            "success": False,
            "message": str(e)
        }

    db = SessionLocal()
    try:
        venue = db.get(Venue, id)
        if not venue:
            return {
                "success": False,
                "message": "Venue not found"
            }

        db.delete(venue)
        db.commit()

        return {
            "success": True,
            "message": "Venue deleted successfully"
        }
    finally:
        db.close()