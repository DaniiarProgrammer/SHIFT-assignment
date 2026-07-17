from fastapi import APIRouter, HTTPException
from app.database import slots_db

router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/")
def get_slots():
    return slots_db
