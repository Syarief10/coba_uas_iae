from ariadne import QueryType, ObjectType
from graphql import GraphQLError
from app.database import SessionLocal
from app.models import Venue
from app.eventhub_client import get_events_by_venue

query = QueryType()
venue = ObjectType("Venue")

@query.field("venueEvents")
async def resolve_query_venue_events(_, info, venueId):
    events = await get_events_by_venue(venueId)
    return events or []

@venue.field("events")
async def resolve_venue_events_field(obj, info):
    try:
        events = await get_events_by_venue(int(obj.id))
        return events or []
    except Exception as e:
        print(f"[EventHub Error] {e}")
        return []            


@query.field("venues")
def resolve_venues(_, info):
    db = SessionLocal()
    try:
        return db.query(Venue).all()
    finally:
        db.close()


@query.field("venue")
def resolve_venue(_, info, id):
    db = SessionLocal()
    try:
        venue = db.get(Venue, id)

        if not venue:
            raise GraphQLError(
                message="Venue tidak tersedia",
                extensions={
                    "code": "NOT_FOUND",
                    "http": {"status": 404}
                }
            )

        return venue
    finally:
        db.close()
