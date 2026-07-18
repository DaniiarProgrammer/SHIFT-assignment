from fastapi import APIRouter, HTTPException, Depends
from app.schemas.rooms import RoomCreate, RoomUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Room


router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/")
def get_rooms(db: Session = Depends(get_db)):
    """Проверка комнат"""
    rooms = db.query(Room).all()
    return rooms

@router.get("/{room_id}")
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Получить комнату по ID"""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:                
        raise HTTPException(status_code=404, detail="Комната не найдена")
    return room

@router.post("/", status_code=201)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """Создать комнату"""

    db_room = Room(name=room.name, capacity=room.capacity)

    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room

@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Удалить комнату"""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    db.delete(room)
    db.commit()
    return

@router.put("/{room_id}")
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
    """Обновить комнату"""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Не найдено")
    room.name = room_update.name
    room.capacity = room_update.capacity

    db.commit()
    db.refresh(room)
    return room