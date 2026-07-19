from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.auth import UserAuth, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(user: UserAuth, db: Session = Depends(get_db)):
    # 1. Ищем юзера в базе
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # 2. Проверяем существование и пароль
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Генерируем токен (кладем туда id и роль)
    access_token = create_access_token(
        data={"sub": str(db_user.id), "role": db_user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}