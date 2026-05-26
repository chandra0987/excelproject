from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas import (
    MessageResponse,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Create a new user account with a hashed password."""
    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter(
            or_(User.username == payload.username, User.email == payload.email)
        )
        .first()
    )
    if existing_user:
        field = "username" if existing_user.username == payload.username else "email"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with this {field} already exists.",
        )

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate a user and return a JWT token",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with username and password, returns a bearer JWT token."""
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated.",
        )

    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return TokenResponse(access_token=access_token)
