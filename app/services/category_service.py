from sqlalchemy.orm import Session
from app.models.models import Category
from app.schemas.category_schemas import CategoryCreate, CategoryAdminUpdate
from typing import Optional, Union
from datetime import datetime


class BookService:
    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate, user_id: int):
        db_category_data = category_data.model_dump()

        db_category_data["created_by_user_id"] = user_id

        db_category = Category(**db_category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        update_data: CategoryAdminUpdate,
        user_id: int,
    ) -> Optional[Category]:
        """Atnaujina kategorijos įrašo duomenis DB."""
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_catgory(db: Session, entry_id: int) -> bool:
        """Ištrina knygos įrašą iš DB."""
        db_category = db.query(Category).filter(Category.id == entry_id).first()
        if not db_category:
            return False

        db.delete(db_category)
        db.commit()
        return True

    @staticmethod
    def get_all_categories(db: Session):
        query = db.query(Category)
        query = query.order_by(Category.name.desc())

        return query
