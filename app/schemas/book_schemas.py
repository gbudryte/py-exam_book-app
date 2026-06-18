from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.schemas.user_schemas import UserBase, UserResponse
from typing import Optional
import re


class BookBase(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    author: str = Field(min_length=3, max_length=55)
    category_id: int
    rating: int = Field(ge=1, le=5)

    @field_validator("name")
    @classmethod
    def ensure_name_is_letters_or_digits(cls, value: str):
        if not any(char.isalnum() for char in value):
            raise ValueError("Book name should contain letters or numbers")
        return value
    
    @field_validator("author")
    @classmethod
    def ensure_name_is_without_spec_symbols(cls, value: str):
        if re.search(r'[^a-zA-Z0-9 ]', value):
            raise ValueError('author_name must not contain special characters')
        return value
    

class BookCreate(BookBase):
    pass

class BookPublicResponse(BookBase):
    created_by: UserBase
    created_at: datetime
    modified_at: Optional[datetime] = None

class BookAdminResponse(BookPublicResponse):
    created_by: UserResponse

class BookPublicUpdate(BookBase):
    modified_at: datetime

class BookAdminUpdate(BookAdminResponse):
    modified_at: datetime




