from ariadne import QueryType
from graphql import GraphQLError
from app.database import SessionLocal
from app.models import Venue

query = QueryType()


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
