import os
import requests
from graphql import GraphQLError

SCHEDULE_URL = os.getenv(
    "SCHEDULE_SERVICE_URL",
    "http://schedule-service:8000/graphql"
)

TIMEOUT = 5


def schedules_by_room(room_id):
    room_id = int(room_id)

    query = """
    query {
      schedules {
        id
        roomId
        startTime
        endTime
        status
      }
    }
    """

    try:
        r = requests.post(
            SCHEDULE_URL,
            json={"query": query},
            timeout=TIMEOUT
        )
        r.raise_for_status()
        result = r.json()
    except requests.RequestException:
        raise GraphQLError("Schedule service unavailable")

    if result.get("errors"):
        raise GraphQLError(result["errors"][0]["message"])

    schedules = result.get("data", {}).get("schedules", [])
    return [s for s in schedules if s["roomId"] == room_id]


def get_schedules():
    query = """
    query {
      schedules {
        id
        roomId
        startTime
        endTime
        status
      }
    }
    """

    try:
        r = requests.post(
            SCHEDULE_URL,
            json={"query": query},
            timeout=TIMEOUT
        )
        r.raise_for_status()
        result = r.json()
    except requests.RequestException:
        raise GraphQLError("Schedule service unavailable")

    if result.get("errors"):
        raise GraphQLError(result["errors"][0]["message"])

    return result.get("data", {}).get("schedules", [])


def available_slots(room_id, start_date, end_date):
    query = """
    query($roomId: Int!, $startDate: String!, $endDate: String!) {
      availableSlots(
        roomId: $roomId
        startDate: $startDate
        endDate: $endDate
      ) {
        startTime
        endTime
      }
    }
    """

    try:
        r = requests.post(
            SCHEDULE_URL,
            json={
                "query": query,
                "variables": {
                    "roomId": int(room_id),
                    "startDate": start_date,
                    "endDate": end_date
                }
            },
            timeout=TIMEOUT
        )
        r.raise_for_status()
        result = r.json()
    except requests.RequestException:
        raise GraphQLError("Schedule service unavailable")

    if result.get("errors"):
        raise GraphQLError(result["errors"][0]["message"])

    return result.get("data", {}).get("availableSlots", [])


def block_schedule(room_id, start_time, end_time):
    query = """
    mutation($input: BlockScheduleInput!) {
      blockSchedule(input: $input) {
        success
        message
      }
    }
    """

    variables = {
        "input": {
            "roomId": int(room_id),
            "startTime": start_time,
            "endTime": end_time
        }
    }

    try:
        r = requests.post(
            SCHEDULE_URL,
            json={"query": query, "variables": variables},
            timeout=TIMEOUT
        )
        r.raise_for_status()
        result = r.json()
    except requests.RequestException:
        return {
            "success": False,
            "message": "Schedule service unavailable"
        }

    if result.get("errors"):
        return {
            "success": False,
            "message": result["errors"][0]["message"]
        }

    return result.get("data", {}).get("blockSchedule", {
        "success": False,
        "message": "Unknown error"
    })
