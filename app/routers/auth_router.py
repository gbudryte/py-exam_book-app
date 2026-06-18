from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token_schemas import Token

router = APIRouter(prefix="/auth", tags=["Authentication & Profiles"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Naujo vartotojo registracija."""
    try:
        new_user = AuthService.register_user(db, user_data=user_in)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    
   
    token_payload = {
        "sub": str(user.id),  
        "role": user.role.value
    }
    

    access_token = AuthService.create_access_token(data=token_payload)
    
    return {"access_token": access_token, "token_type": "bearer"}