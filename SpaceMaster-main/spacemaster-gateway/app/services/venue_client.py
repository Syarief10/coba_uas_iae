import os
import requests
from graphql import GraphQLError

VENUE_URL = os.getenv(
    "VENUE_SERVICE_URL",
    "http://venue-service:8000/graphql"
)

TIMEOUT = 5


def get_venues():
    query = """
    query {
      venues {
        id
        name
        city
        address
        description
      }
    }
    """

    try:
        response = requests.post(
            VENUE_URL,
            json={"query": query},
            timeout=TIMEOUT
        )
    except requests.RequestException:
        raise GraphQLError(
            "Venue service unavailable",
            extensions={"code": "SERVICE_UNAVAILABLE"}
        )

    result = response.json()

    if result.get("errors"):
        raise GraphQLError(
            result["errors"][0]["message"],
            extensions={"code": "VENUE_SERVICE_ERROR"}
        )

    return result.get("data", {}).get("venues", [])


def get_venue(venue_id):
    query = """
    query ($id: ID!) {
      venue(id: $id) {
        id
        name
        city
        address
        description
      }
    }
    """

    try:
        response = requests.post(
            VENUE_URL,
            json={
                "query": query,
                "variables": {"id": venue_id}
            },
            timeout=TIMEOUT
        )
    except requests.RequestException:
        raise GraphQLError(
            "Venue service unavailable",
            extensions={"code": "SERVICE_UNAVAILABLE"}
        )

    result = response.json()

    if result.get("errors"):
        raise GraphQLError(
            result["errors"][0]["message"],
            extensions={"code": "VENUE_SERVICE_ERROR"}
        )

    venue = result.get("data", {}).get("venue")

    if not venue:
        raise GraphQLError(
            "Venue not found",
            extensions={"code": "NOT_FOUND"}
        )

    return venue
