from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slot
from app.schemas.slots import SlotCreate

router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/")
def get_slots(db: Session = Depends(get_db)):
    """Проверка слотов"""
    slots = db.query(Slot).all()
    return slots

@router.post("/", status_code=201)
def create_slot(slot: SlotCreate, db: Session = Depends(get_db)):
    """Создать слот"""
    db_slot = Slot(start_time=slot.start_time, end_time=slot.end_time)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot
