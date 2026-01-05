from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from app.graphql.query import query
from app.graphql.mutation import mutation
from app.database import engine
from app.models import Base

type_defs = load_schema_from_path("app/graphql/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.mount(
    "/graphql",
    GraphQL(
        schema,
        debug=True,
        context_value=lambda request: {"request": request}
    )
)
