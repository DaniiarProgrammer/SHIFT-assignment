from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    capacity = Column(Integer, nullable=False)

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column(String(10))
    end_time = Column(String(10))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique = True)
    role = Column(String(20))

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    date = Column(String(10))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)