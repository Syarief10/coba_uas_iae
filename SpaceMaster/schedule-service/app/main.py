from fastapi import FastAPI
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from app.database import Base, engine
from app.graphql.query import query, schedule
from app.graphql.mutation import mutation
from pathlib import Path

Base.metadata.create_all(bind=engine)

type_defs = Path("app/graphql/schema.graphql").read_text()

schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    schedule
)

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=False))

