import requests

ROOM_SERVICE_URL = "http://room-service:8000/graphql"

def room_exists(room_id: int) -> bool:
    query = """
    query ($id: ID!) {
      room(id: $id) {
        id
      }
    }
    """

    try:
        response = requests.post(
            ROOM_SERVICE_URL,
            json={"query": query, "variables": {"id": room_id}},
            timeout=3
        )
        data = response.json()
        return data.get("data", {}).get("room") is not None
    except Exception:
        return False
