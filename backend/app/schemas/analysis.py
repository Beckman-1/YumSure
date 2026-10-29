from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class IngredientAnalysisRequest(BaseModel):
    ingredients_text: str
    product_name: Optional[str] = "Custom Product"
    nutriments: Optional[Dict[str, Any]] = Field(default_factory=dict)
    user_id: Optional[str] = "default"

class IngredientAnalysisResponse(BaseModel):
    product_name: str
    truthin_score: int
    health_flag: str
    flag_reasons: List[str]
    personalized_alerts: List[str]
    allergens: List[str]
    additives: List[Dict[str, Any]]
    is_vegetarian: bool
    has_palm_oil: bool
