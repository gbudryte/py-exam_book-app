from sqlalchemy.orm import Session
from app.models.models import Book
from app.schemas.book_schemas import (
    BookCreate,
    BookPublicUpdate,
    BookAdminUpdate,
)
from typing import Optional, Union
from datetime import datetime


class BookService:
    @staticmethod
    def create_book_entry(db: Session, book_data: BookCreate, user_id: int):
        db_book_data = book_data.model_dump()

        db_book_data["created_by_user_id"] = user_id

        db_book = Book(**db_book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)

        return db_book

    @staticmethod
    def update_book_entry(
        db: Session,
        entry_id: int,
        update_data: Union[BookAdminUpdate, BookPublicUpdate],
        user_id: int,
    ) -> Optional[Book]:
        """Atnaujina knygos įrašo duomenis DB."""
        db_book = db.query(Book).filter(Book.id == entry_id).first()
        if not db_book:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(db_book, key, value)

        db_book["modified_at"] = datetime.now()
        db_book["modified_by_user_id"] = user_id

        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book_entry(db: Session, entry_id: int) -> bool:
        """Ištrina knygos įrašą iš DB."""
        db_book = db.query(Book).filter(Book.id == entry_id).first()
        if not db_book:
            return False

        db.delete(db_book)
        db.commit()
        return True

    def get_books_by_category(db: Session, category_name):
        query = db.query(Book)
        if category_name:
            query = query.filter(Book.category.name == category_name)
        return query

    def sort_books_by_rating(db: Session, direction):
        query = db.query(Book)
        if direction.lower() == "acs":
            query = query.order_by(Book.rating.asc())
        else:
            query = query.order_by(Book.rating.desc())
