from pydantic import BaseModel, EmailStr, Field
from app.models.models import UserRole


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=55)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=100)


class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True
