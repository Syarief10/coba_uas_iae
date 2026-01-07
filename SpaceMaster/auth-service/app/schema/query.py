from ariadne import QueryType

query = QueryType()


@query.field("health")
def resolve_health(_, info):
    return "auth-service ok"
