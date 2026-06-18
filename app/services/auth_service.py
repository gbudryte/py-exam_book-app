import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from app.models.models import User
from app.schemas.user_schemas import UserCreate
from app.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import hashlib

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
)
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Užkoduoja atvirą slaptažodį į hash tekstą."""
        # 1. Force generate a SHA-256 string (64 characters total)
        pre_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # 2. Pass it directly into the context
        return pwd_context.hash(pre_hashed)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Patikrina, ar prisijungimo metu įvestas slaptažodis sutampa su esančiu DB."""
        # 1. Re-hash the login attempt password with SHA-256
        pre_hashed = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

        # 2. Verify against the database hash
        return pwd_context.verify(pre_hashed, hashed_password)

    @classmethod
    def register_user(cls, db: Session, user_data: UserCreate) -> User:
        """Verslo logika naujo vartotojo registracijai."""

        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("User with this email alresdy exists")

        hashed_pwd = cls.hash_password(user_data.password)

        db_user = User(
            name=user_data.name, email=user_data.email, password_hash=hashed_pwd
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Sugeneruoja JWT žetoną su galiojimo laiku."""
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    def authenticate_user(cls, db: Session, email: str, password: str) -> User:
        """Patikrina el. paštą ir slaptažodį. Jei viskas gerai - grąžina User objektą."""
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not cls.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        return user

    @staticmethod
    def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
    ) -> User:
        """
        Iškoduoja JWT žetoną ir grąžina duomenų bazės User objektą.
        Jei žetonas blogas ar pasibaigęs -> iškart išmeta HTTP 401 klaidą.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Log-in expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise credentials_exception

        except jwt.PyJWTError:
            raise credentials_exception
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception

        return user
