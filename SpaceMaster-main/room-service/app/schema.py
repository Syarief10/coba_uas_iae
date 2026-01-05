from pydantic import BaseModel

class RoomSchema(BaseModel):
    id: int
    name: str
    capacity: int
    venue_id: int
