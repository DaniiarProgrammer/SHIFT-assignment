#cd C:\PythonWithMyBro\shift-booking
#poetry run uvicorn app.main:app --reload
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
def get_rooms():
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
    name: str = Field(..., min_length=1, max_length=50)
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


class RoomUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    capacity: int = Field(..., gt=0)

@app.put("/rooms/{room_id}")
def update_room(room_id: int, room_update: RoomUpdate):
    for room in rooms_db:
        if room["id"] == room_id:
            room["name"] = room_update.name
            room["capacity"] = room_update.capacity       
            return room
    raise HTTPException(status_code=404, detail="Не найдено")


# Слоты задаются заранее, их нельзя создавать через POST
slots_db = [
    {"id": 1, "start_time": "09:00", "end_time": "10:00"},
    {"id": 2, "start_time": "11:00", "end_time": "12:00"},
    {"id": 3, "start_time": "14:00", "end_time": "15:00"},
]

users_db = [
    {"id": 1, "username": "daniyar", "role": "admin"},
    {"id": 2, "username": "employee1", "role": "employee"}
]



@app.get("/slots")
def get_slots():
    return slots_db

class BookingCreate(BaseModel):
    room_id: int
    slot_id: int
    date: str
    user_id: int

bookings_db = []

@app.post("/bookings", status_code=201)
def create_booking(book: BookingCreate):
    if any(room["id"] == book.room_id for room in rooms_db) and any(slot["id"] == book.slot_id for slot in slots_db):
        for existing_booking in bookings_db:
            if (existing_booking["room_id"] == book.room_id and
                existing_booking["slot_id"] == book.slot_id and
                existing_booking["date"] == book.date):

                raise HTTPException(status_code=409, detail="Комната уже забронирована")


        new_id = max((a["id"] for a in bookings_db), default=0) + 1
        new_booking = {
            "id": new_id,
            "room_id": book.room_id,
            "slot_id": book.slot_id,
            "date": book.date,
            "user_id": book.user_id
        }

        bookings_db.append(new_booking)
        return new_booking
    
    else:
        raise HTTPException(status_code=404, detail="Комната или слот не найдены, нельзя забронировать")

@app.get("/bookings")
def get_bookings():
    """Проверка броней"""
    return bookings_db

def get_role(user_id):
    for user in users_db:
        if user["id"] == user_id:
            return user["role"]

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, current_user_id: int):

    target_booking = None
    for booking in bookings_db:
        if booking["id"] == booking_id:
            target_booking = booking
            break
    if target_booking is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    
    is_author = (target_booking["user_id"] == current_user_id)
    is_admin = (get_role(current_user_id) == "admin")
    if is_author == False and is_admin == False:
        raise HTTPException(status_code=403, detail="Нет прав для удаления")
    
    bookings_db.remove(target_booking)
