from fastapi import APIRouter, HTTPException
from app.database import rooms_db, slots_db, bookings_db, users_db
from app.schemas.bookings import BookingCreate

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", status_code=201)
def create_booking(book: BookingCreate):
    """Создать бронь"""
    if not any(room["id"] == book.room_id for room in rooms_db):
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    if not any(slot["id"] == book.slot_id for slot in slots_db):
        raise HTTPException(status_code=404, detail="Слот не найден")

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
    
@router.get("/")
def get_bookings():
    """Проверка броней"""
    return bookings_db

def get_role(user_id):
    for user in users_db:
        if user["id"] == user_id:
            return user["role"]
        
@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, current_user_id: int):
    """Удалить бронь"""
    target_booking = None
    for booking in bookings_db:
        if booking["id"] == booking_id:
            target_booking = booking
            break
    if target_booking is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    
    is_author = (target_booking["user_id"] == current_user_id)
    is_admin = (get_role(current_user_id) == "admin")
    if not is_author and not is_admin:
        raise HTTPException(status_code=403, detail="Нет прав для удаления")
    
    bookings_db.remove(target_booking)

