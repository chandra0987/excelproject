from fastapi import APIRouter, HTTPException, status

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_users_collection
from app.models import UserModel
from app.schemas import (
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
async def register(payload: UserRegister):
    """Create a new user account with a hashed password."""
    users = get_users_collection()

    # Check if username or email already exists
    existing = await users.find_one(
        {"$or": [{"username": payload.username}, {"email": payload.email}]}
    )
    if existing:
        field = "username" if existing["username"] == payload.username else "email"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with this {field} already exists.",
        )

    user_doc = UserModel(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    result = await users.insert_one(user_doc.to_mongo())
    user_doc.id = str(result.inserted_id)
    return user_doc


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate a user and return a JWT token",
)
async def login(payload: UserLogin):
    """Authenticate with email and password, returns a bearer JWT token."""
    users = get_users_collection()

    user_data = await users.find_one({"email": payload.email})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserModel.from_mongo(user_data)

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated.",
        )

    access_token = create_access_token(
        data={"sub": user.id, "username": user.username}
    )
    return TokenResponse(access_token=access_token)
