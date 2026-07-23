from pydantic import BaseModel

class BookingCreate(BaseModel):
    room_id: int
    slot_id: int
    date: str
