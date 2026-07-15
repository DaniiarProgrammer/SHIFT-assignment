#cd C:\PythonWithMyBro\shift-booking

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import HTTPException


rooms_db = []

# Создаём приложение FastAPI
app = FastAPI(
    title="Сервис бронирования переговорных",
    description="API для управления бронированиями в коворкинге",
    version="0.1.0"
)

# Простой health check endpoint
@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}

@app.get("/rooms")
def rooms_check():
    """Проверка комнат"""
    return rooms_db

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    """Получить комнату по ID"""
    for room in rooms_db:
        if room["id"] == room_id:
            return room
                
    raise HTTPException(status_code=404, detail="Комната не найдена")


class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50) #Бот, поможешь, у меня Field не определено Pylance и в общем не работает, может надо какой то модуль установить или ещё что-то?
    capacity: int = Field(...,  gt=0)

@app.post("/rooms", status_code=201)
def create_room(room: RoomCreate):
    new_id = max((r["id"] for r in rooms_db), default=0) + 1
    room_dict = {
        "id": new_id,
        "name": room.name,
        "capacity": room.capacity,
        }

    rooms_db.append(room_dict)
    return room_dict

@app.delete("/rooms/{room_id}", status_code=204)
def delete_room(room_id: int):
    for i, room in enumerate(rooms_db):
        if room["id"] == room_id:
            rooms_db.pop(i) #Удалить элемент по индексу
            return
    raise HTTPException(status_code=404, detail="Не найдено")



