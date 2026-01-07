from fastapi import FastAPI
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

from app.schema.query import query
from app.schema.mutation import mutation
from app.database import engine
from app.models import Base

type_defs = load_schema_from_path("app/schema/schema.graphql")

schema = make_executable_schema(type_defs, query, mutation)

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.mount("/graphql", GraphQL(schema, debug=True))