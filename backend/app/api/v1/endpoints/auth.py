import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user_profile import UserProfile
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, summary="Register a new user")
async def register_user(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    stmt = select(UserProfile).where(UserProfile.email == user_in.email.lower())
    existing = await db.execute(stmt)
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists."
        )

    user_id = str(uuid.uuid4())
    new_user = UserProfile(
        id=user_id,
        email=user_in.email.lower(),
        hashed_password=hash_password(user_in.password),
        name=user_in.name,
        dietary_preference=user_in.dietary_preference,
        health_goals=user_in.health_goals,
        allergies=user_in.allergies,
        avoid_additives=user_in.avoid_additives,
        avoid_palm_oil=user_in.avoid_palm_oil,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": user_id, "email": new_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/login", response_model=TokenResponse, summary="Login and retrieve access token")
async def login_user(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(UserProfile).where(UserProfile.email == login_in.email.lower())
    res = await db.execute(stmt)
    user = res.scalars().first()

    if not user or not user.hashed_password or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive."
        )

    token = create_access_token({"sub": user.id, "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse, summary="Get current authenticated user")
async def get_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user
