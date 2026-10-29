from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.user_profile import UserProfile
from app.models.scan_history import ScanHistory
from app.schemas.assessment import ProductAssessmentResponse
from app.services.barcode_resolver import BarcodeResolver

router = APIRouter()

@router.get(
    "/{barcode}",
    response_model=ProductAssessmentResponse,
    summary="Scan and analyze barcode",
    description="Resolves any food or cosmetic product barcode using check-digit validation, multi-source resolution, and versioned TruthIn assessment."
)
async def scan_barcode(
    barcode: str,
    category_hint: Optional[str] = Query(None, description="Optional hint (e.g. 'food' or 'cosmetic') for source routing"),
    current_user: Optional[UserProfile] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Barcode Format & Check-Digit Validation
    is_valid, clean_barcode, err = BarcodeResolver.validate_barcode(barcode)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "INVALID_BARCODE",
                "message": err,
                "barcode": barcode
            }
        )

    # 2. Extract User Profile context for personalized alerts (if authenticated)
    user_profile_data = None
    if current_user:
        user_profile_data = {
            "allergies": current_user.allergies or [],
            "health_goals": current_user.health_goals or [],
            "dietary_preference": current_user.dietary_preference or "any",
            "avoid_additives": current_user.avoid_additives,
            "avoid_palm_oil": current_user.avoid_palm_oil
        }

    # 3. Resolve Barcode multi-source
    product_dict = await BarcodeResolver.resolve_barcode(
        clean_barcode, db, user_profile=user_profile_data, category_hint=category_hint
    )
    
    if not product_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PRODUCT_NOT_FOUND",
                "message": f"Barcode '{clean_barcode}' could not be resolved from local cache or verified global product registries.",
                "barcode": clean_barcode,
                "suggestion": "You can contribute this product via POST /api/v1/products or submit its ingredients label via POST /api/v1/analysis/ingredients"
            }
        )

    # 4. If user is authenticated, record scan in their private scan history
    if current_user:
        try:
            history_entry = ScanHistory(
                user_id=current_user.id,
                product_id=product_dict.get("id"),
                barcode=product_dict["barcode"],
                product_name=product_dict["name"],
                brand=product_dict.get("brand"),
                image_url=product_dict.get("image_url"),
                health_flag=product_dict["assessment"]["health_flag"],
                truthin_score=product_dict["assessment"]["truthin_score"]
            )
            db.add(history_entry)
            await db.commit()
        except Exception:
            pass

    return product_dict
