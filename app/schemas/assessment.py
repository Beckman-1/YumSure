from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class NutrientFactItem(BaseModel):
    nutrient_name: str
    amount: Optional[float] = None
    unit: str = "g"
    per_amount: float = 100.0
    per_unit: str = "g"
    reference_basis: str = "per_100g"
    provenance_source: str = "openfoodfacts"
    verification_status: str = "COMMUNITY"

    model_config = {"from_attributes": True}

class AssessmentResult(BaseModel):
    truthin_score: int
    health_flag: str # GREEN, YELLOW, RED
    rule_version: str = "2026.1"
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None
    flag_reasons: List[str] = Field(default_factory=list)
    personalized_alerts: List[str] = Field(default_factory=list)
    detected_allergens: List[str] = Field(default_factory=list)
    detected_additives: List[Dict[str, Any]] = Field(default_factory=list)
    nutrient_breakdown: Dict[str, Any] = Field(default_factory=dict)
    is_vegetarian: bool = True
    has_palm_oil: bool = False
    data_completeness_score: float = 0.0

    model_config = {"from_attributes": True}

class ProductAssessmentResponse(BaseModel):
    id: Optional[int] = None
    barcode: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    product_type: str = "food"
    image_url: Optional[str] = None
    ingredients_text: Optional[str] = None
    
    # Provenance & Completeness
    source: str = "openfoodfacts"
    source_url: Optional[str] = None
    retrieved_at: Optional[str] = None
    data_completeness_score: float = 0.0
    verification_status: str = "COMMUNITY"
    
    # Source Nutrition Facts (None preserved for missing nutrients)
    nutrition_facts: Dict[str, Optional[float]] = Field(default_factory=dict)
    
    # Versioned Assessment
    assessment: AssessmentResult

    model_config = {"from_attributes": True}
