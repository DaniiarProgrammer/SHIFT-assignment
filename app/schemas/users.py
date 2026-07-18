from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    role: str = Field(..., pattern="^(admin|employee)$") # Разрешаем только admin или employee
    