from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from database import SessionLocal, User

router = APIRouter()

# ==========================
# JWT CONFIG
# ==========================
SECRET_KEY = "CHANGE_THIS_TO_A_SECURE_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================
# MODELS
# ==========================
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================
# HELPERS
# ==========================
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================
# REGISTER
# ==========================
@router.post("/register", response_model=Token)
def register(user: UserCreate):
    session = SessionLocal()

    existing = session.query(User).filter(User.email == user.email).first()
    if existing:
        session.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    session.close()

    token = create_access_token({"sub": db_user.email})
    return Token(access_token=token)


# ==========================
# LOGIN
# ==========================
@router.post("/login", response_model=Token)
def login(user: UserLogin):
    session = SessionLocal()
    db_user = session.query(User).filter(User.email == user.email).first()
    session.close()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return Token(access_token=token)
