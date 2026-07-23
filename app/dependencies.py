from jose import JWTError
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from app.auth import decode_access_token

# Создаём "парсер" токенов
# tokenUrl="/auth/login" — это URL, куда клиент отправляет логин/пароль
# Swagger использует этот URL для кнопки Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """Извлекает текущего пользователя из JTW-токена"""
    try:
        payload = decode_access_token(token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise ValueError("No sub in token")
        user_id = int(user_id_str)
    except (ValueError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )        

    # Ищем пользователя в базе
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Возвращаем объект пользователя
    return user