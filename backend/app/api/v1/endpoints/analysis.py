from fastapi import APIRouter, Depends
from typing import Optional

from app.core.security import get_optional_current_user
from app.models.user_profile import UserProfile
from app.schemas.analysis import IngredientAnalysisRequest
from app.schemas.assessment import AssessmentResult
from app.services.assessment_service import AssessmentService

router = APIRouter()

@router.post(
    "/ingredients",
    response_model=AssessmentResult,
    summary="Analyze ingredients text directly",
    description="Analyzes raw ingredient text (from OCR/label photos or manual entry), detecting additives, allergens, health flags, and personalized warnings."
)
async def analyze_ingredients(
    request: IngredientAnalysisRequest,
    current_user: Optional[UserProfile] = Depends(get_optional_current_user)
):
    user_profile_data = None
    if current_user:
        user_profile_data = {
            "allergies": current_user.allergies or [],
            "health_goals": current_user.health_goals or [],
            "dietary_preference": current_user.dietary_preference or "any",
            "avoid_additives": current_user.avoid_additives,
            "avoid_palm_oil": current_user.avoid_palm_oil
        }

    assessment = AssessmentService.calculate_assessment(
        nutrition_facts=request.nutriments or {},
        ingredients_text=request.ingredients_text,
        user_profile=user_profile_data
    )

    return assessment
