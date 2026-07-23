from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.users import UserCreate
from app.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    """Проверка пользователей"""
    users = db.query(User).all()
    return users    

@router.post("/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать пользователя"""
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, role=user.role, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user