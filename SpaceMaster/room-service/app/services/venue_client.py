import requests

VENUE_SERVICE_URL = "http://venue-service:8000/graphql"

class VenueServiceError(Exception):
    pass

def fetch_venue(venue_id: int) -> dict | None:
    query = """
    query ($id: ID!) {
      venue(id: $id) {
        id
        name
      }
    }
    """

    try:
        r = requests.post(
            VENUE_SERVICE_URL,
            json={"query": query, "variables": {"id": venue_id}},
            timeout=3
        )
        r.raise_for_status()
        data = r.json()
        return data.get("data", {}).get("venue")
    except requests.RequestException:
        raise VenueServiceError("Venue Service unavailable")
