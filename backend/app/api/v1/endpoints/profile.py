from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileResponse, UserProfileUpdate
from app.services.ingredient_engine import ALLERGEN_PATTERNS

router = APIRouter()

SUPPORTED_HEALTH_GOALS = [
    {"id": "diabetes_control", "name": "Diabetes & Blood Sugar Control", "description": "Alerts on added sugars (>5g), maltodextrin, and high glycemic ingredients."},
    {"id": "weight_loss", "name": "Weight Management & Fat Loss", "description": "Flags high calorie density (>400 kcal/100g) and excessive sugars/fats."},
    {"id": "low_sodium", "name": "Low Sodium / Hypertension", "description": "Flags products with excessive sodium (>400mg per 100g)."},
    {"id": "heart_healthy", "name": "Heart Health & Cholesterol", "description": "Warns against trans fats, high saturated fat, and palm oil."},
    {"id": "clean_eating", "name": "Clean Eating & Additive-Free", "description": "Highlights artificial preservatives, synthetic dyes, and flavor enhancers."}
]

@router.get("/allergens/list", response_model=List[str], summary="List supported allergen tags")
async def list_supported_allergens():
    return sorted(list(ALLERGEN_PATTERNS.keys()))

@router.get("/goals/list", response_model=List[Dict[str, str]], summary="List supported health goals")
async def list_supported_goals():
    return SUPPORTED_HEALTH_GOALS

@router.get("/me", response_model=UserProfileResponse, summary="Get authenticated user's profile")
async def get_my_profile(current_user: UserProfile = Depends(get_current_user)):
    """Only the authenticated user can access their own profile."""
    return current_user

@router.put("/me", response_model=UserProfileResponse, summary="Update authenticated user's profile")
async def update_my_profile(
    profile_in: UserProfileUpdate,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Only the authenticated user can update their own profile."""
    if profile_in.name is not None:
        current_user.name = profile_in.name
    if profile_in.dietary_preference is not None:
        current_user.dietary_preference = profile_in.dietary_preference
    if profile_in.health_goals is not None:
        current_user.health_goals = profile_in.health_goals
    if profile_in.allergies is not None:
        current_user.allergies = profile_in.allergies
    if profile_in.avoid_additives is not None:
        current_user.avoid_additives = profile_in.avoid_additives
    if profile_in.avoid_palm_oil is not None:
        current_user.avoid_palm_oil = profile_in.avoid_palm_oil

    await db.commit()
    await db.refresh(current_user)
    return current_user
