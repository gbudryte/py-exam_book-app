from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.schemas.user_schemas import UserBase, UserResponse
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryAdminResponse(CategoryBase):
    created_by: UserBase
    created_at: datetime


class CategoryUserResponse(CategoryBase):
    pass


class CategoryAdminUpdate(CategoryCreate):
    name: Optional[str] = Field(min_length=2, max_length=50)
