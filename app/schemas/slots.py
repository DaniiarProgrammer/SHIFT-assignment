from pydantic import BaseModel, Field

class SlotCreate(BaseModel):
    start_time: str = Field(..., pattern="^([0-1]?\d|2[0-3]):[0-5]\d$") # Формат HH:MM
    end_time: str = Field(..., pattern="^([0-1]?\d|2[0-3]):[0-5]\d$")