from fastapi import APIRouter, HTTPException, Depends
from app.schemas.bookings import BookingCreate
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking, User
from app.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", status_code=201)
def create_booking(book: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Создать бронь""" 
    existing_booking = db.query(Booking).filter(
        Booking.room_id == book.room_id,
        Booking.slot_id == book.slot_id,
        Booking.date == book.date
    ).first()
    if existing_booking:
        raise HTTPException(status_code=409, detail="Комната уже забронирована")
    db_booking = Booking(room_id=book.room_id, slot_id=book.slot_id, date=book.date, user_id=current_user.id ) 
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/")
def get_bookings(db: Session = Depends(get_db)):
    """Проверка броней"""
    bookings = db.query(Booking).all()
    return bookings
        
@router.delete("/{booking_id}", status_code=204)
def delete_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    """Удалить бронь"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    
    is_author = (booking.user_id == current_user.id)
    is_admin = (current_user.role == "admin")
    if not is_author and not is_admin:
        raise HTTPException(status_code=403, detail="Нет прав для удаления")
    
    db.delete(booking)
    db.commit()
    return
