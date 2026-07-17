#cd C:\PythonWithMyBro\shift-booking
#poetry run uvicorn app.main:app --reload
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import rooms, bookings, slots  # Импортируем роутеры

app = FastAPI(
    title="Сервис бронирования переговорных",
    description="API для управления бронированиями в коворкинге",
    version="0.1.0"
)

# Подключаем роутеры
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(slots.router)

@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}

from app import models
Base.metadata.create_all(bind=engine)