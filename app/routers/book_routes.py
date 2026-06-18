from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.book_schemas import (
    BookCreate,
    BookAdminResponse,
    BookPublicResponse,
    BookUpdate,
)
from app.services.book_service import BookService
from app.models.models import UserRole, Book
from app.services.auth_service import AuthService
from app.models.models import User, Category


router = APIRouter(prefix="/books", tags=["Book entries"])


@router.post("", response_model=BookPublicResponse)
def create_new_book_entry(
    book_in: BookCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    """Naujos rezervacijos sukūrimas."""
    return BookService.create_book_entry(db, book_data=book_in, user_id=current_user.id)


@router.get("", response_model=List[BookPublicResponse])
def get_all_book_entries(
    db: Session = Depends(get_db),
    book_name: Optional[str] = Query(None, description="Search by Book name"),
    category_name: Optional[str] = Query(None, description="Filter by category"),
    sort_direction: Optional[str] = Query(
        None, description="Sort by rating (desc/asc)"
    ),
    user_id: Optional[int] = Query(
        None, description="ADMIN ONLY: Filter by creator user ID"
    ),
    current_user=Depends(AuthService.get_current_user),
):
    """
    Rezervacijų sąrašas su filtravimu ir rūšiavimu.
    """
    # Enforce Role-Based Logic
    if current_user.role == "ADMIN":
        target_user_id = user_id
    else:
        if user_id is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can filter entries by a specific user_id",
            )
        target_user_id = current_user.id

    books = BookService.get_books(
        db, book_name, category_name, sort_direction, target_user_id
    )
    return books


@router.get("/my-reservations", response_model=List[BookPublicResponse])
def get_my_book_entries(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
    book_name: Optional[str] = Query(None, description="Search by Book name"),
    category_name: Optional[str] = Query(None, description="Filter by categoty"),
    sort_direction: Optional[str] = Query(
        None, description="Sort by rating (desc/asc)"
    ),
):
    """
    Grąžina įaršus, skirtus TIK šiuo metu prisijungusiam vartotojui.
    """
    books = BookService.get_books(
        db, book_name, category_name, sort_direction, current_user.id
    )
    return books


@router.put("/{book_enrty_id}", response_model=BookPublicResponse)
def update_existing_reservation(
    entry_id: int,
    payload: BookUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    """Rezervacijos redagavimas (su teisių patikra)."""
    db_res = db.query(Book).filter(Book.id == entry_id).first()
    if not db_res:
        raise HTTPException(status_code=404, detail="Book entry not found")

    # Leidžiame redaguoti tik jei vartotojas yra Adminas ARBA tai yra paties user įrašas
    if (
        current_user.role != UserRole.ADMIN
        and db_res.created_by_user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="You do not have a permission to update this entry"
        )

    updated_res = BookService.update_reservation(db, entry_id, payload)
    return updated_res


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_reservation(
    entry_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db),
):
    """Rezervacijos šalinimas (su teisių patikra)."""
    db_res = db.query(Book).filter(Book.id == entry_id).first()
    if not db_res:
        raise HTTPException(status_code=404, detail="Įrašas nerastas.")

    if (
        current_user.role != UserRole.ADMIN
        and db_res.created_by_user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="You do not have a permission to delete this entry"
        )

    BookService.delete_book_entry(db, entry_id)
    return None
