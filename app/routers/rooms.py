from fastapi import APIRouter, HTTPException
from app.database import rooms_db
from app.schemas.rooms import RoomCreate, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/")
def get_rooms():
    """Проверка комнат"""
    return rooms_db

@router.get("/{room_id}")
def get_room(room_id: int):
    """Получить комнату по ID"""
    for room in rooms_db:
        if room["id"] == room_id:
            return room
                
    raise HTTPException(status_code=404, detail="Комната не найдена")

@router.post("/", status_code=201)
def create_room(room: RoomCreate):
    """Создать комнату"""
    new_id = max((r["id"] for r in rooms_db), default=0) + 1
    room_dict = {
        "id": new_id,
        "name": room.name,
        "capacity": room.capacity,
        }

    rooms_db.append(room_dict)
    return room_dict

@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int):
    """Удалить комнату"""
    for i, room in enumerate(rooms_db):
        if room["id"] == room_id:
            rooms_db.pop(i) #Удалить элемент по индексу
            return
    raise HTTPException(status_code=404, detail="Не найдено")

@router.put("/{room_id}")
def update_room(room_id: int, room_update: RoomUpdate):
    """Обновить комнату"""
    for room in rooms_db:
        if room["id"] == room_id:
            room["name"] = room_update.name
            room["capacity"] = room_update.capacity       
            return room
    raise HTTPException(status_code=404, detail="Не найдено")