import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    categories = relationship("Category", back_populates="created_by")

    books_created = relationship(
        "Book",
        back_populates="created_by",
        cascade="all, delete-orphan",
        foreign_keys="Book.created_by_user_id",
    )

    books_modified = relationship(
        "Book", back_populates="modified_by", foreign_keys="Book.modified_by_user_id"
    )


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    created_by_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

    created_by = relationship("User", back_populates="categories")
    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    author = Column(String(55), nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    description = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=True)
    created_by_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now())
    modified_by_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    modified_at = Column(TIMESTAMP, nullable=True)

    created_by = relationship(
        "User", back_populates="books_created", foreign_keys=[created_by_user_id]
    )
    modified_by = relationship(
        "User", back_populates="books_modified", foreign_keys=[modified_by_user_id]
    )
    category = relationship("Category", back_populates="books")
