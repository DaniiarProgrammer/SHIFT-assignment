from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



rooms_db = []
slots_db = [
    {"id": 1, "start_time": "09:00", "end_time": "10:00"},
    {"id": 2, "start_time": "11:00", "end_time": "12:00"},
    {"id": 3, "start_time": "14:00", "end_time": "15:00"},
]

users_db = [
    {"id": 1, "username": "daniyar", "role": "admin"},
    {"id": 2, "username": "employee1", "role": "employee"}
]
bookings_db = []
