from pydantic import BaseModel, Field

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    capacity: int = Field(...,  gt=0)

class RoomUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    capacity: int = Field(..., gt=0)
