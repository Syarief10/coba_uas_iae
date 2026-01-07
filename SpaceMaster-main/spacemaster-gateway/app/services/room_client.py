import os
import requests
from graphql import GraphQLError

ROOM_URL = os.getenv(
    "ROOM_SERVICE_URL",
    "http://room-service:8000/graphql"
)

TIMEOUT = 5

def rooms_by_venue(venue_id):
    query = """
    query ($venueId: ID!) {
      roomsByVenue(venueId: $venueId) {
        id
        name
        capacity
        venueId
      }
    }
    """

    try:
        response = requests.post(
            ROOM_URL,
            json={
                "query": query,
                "variables": {"venueId": venue_id}
            },
            timeout=TIMEOUT
        )
    except requests.RequestException:
        raise GraphQLError(
            "Room service unavailable",
            extensions={"code": "SERVICE_UNAVAILABLE"}
        )

    if response.status_code != 200:
        raise GraphQLError(
            "Failed to contact room service",
            extensions={"code": "BAD_GATEWAY"}
        )

    result = response.json()

    if result.get("errors"):
        raise GraphQLError(
            result["errors"][0]["message"],
            extensions={"code": "ROOM_SERVICE_ERROR"}
        )

    data = result.get("data")
    if not data or data.get("roomsByVenue") is None:
        return []

    return data["roomsByVenue"]

def get_room(room_id):
    query = """
    query($id: ID!) {
      room(id: $id) {
        id
        name
        capacity
        venueId
      }
    }
    """
    r = requests.post(
        ROOM_URL,
        json={"query": query, "variables": {"id": room_id}}
    )
    return r.json()["data"]["room"]