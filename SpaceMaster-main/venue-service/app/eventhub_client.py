import httpx

EVENTHUB_URL = "https://45b1ddc77aa4.ngrok-free.app/event/graphql"

async def get_events_by_venue(venue_id: int):
    query = """
    query ($venueId: Int!) {
      eventsByVenue(venueId: $venueId) {
        id
        title
        startTime
        endTime
        status
        roomId
      }
    }
    """

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(
            EVENTHUB_URL,
            json={
                "query": query,
                "variables": {"venueId": venue_id}
            }
        )

        res.raise_for_status()
        return res.json()["data"]["eventsByVenue"]
