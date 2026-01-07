from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from app.graphql.resolvers.venue import query as venue_query, venue
from app.graphql.resolvers.room import query as room_query, room
from app.graphql.resolvers.schedule import query as schedule_query, schedule
from app.graphql.resolvers.schedule import mutation as schedule_mutation

type_defs = load_schema_from_path("app/graphql/schema.graphql")

schema = make_executable_schema(
    type_defs,
    venue_query,
    room_query,
    schedule_query,
    schedule_mutation,
    venue,
    room,
    schedule
)

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))