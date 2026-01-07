import requests
from fastapi import HTTPException

ROOM_SERVICE_URL = "http://room-service:8000/graphql"


def room_exists(room_id: int) -> bool:
    """
    Validasi apakah room dengan ID tertentu tersedia di room-service
    """

    query = """
    query ($id: Int!) {
      room(id: $id) {
        id
      }
    }
    """

    variables = {"id": room_id}

    try:
        response = requests.post(
            ROOM_SERVICE_URL,
            json={
                "query": query,
                "variables": variables
            },
            timeout=5
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Room service tidak dapat dihubungi"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Response room service tidak valid"
        )

    result = response.json()

    if "errors" in result:
        return False

    room = result.get("data", {}).get("room")

    return room is not None
=======
    return room is not None3b4101e30ed42d2df569d73586ae52a1f6
