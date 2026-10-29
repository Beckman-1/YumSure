from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AdditiveDetail(BaseModel):
    code: str
    name: str
    category: str
    hazard: str
    concerns: Optional[str] = None

class ProductBase(BaseModel):
    barcode: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    product_type: str = "food"
    image_url: Optional[str] = None
    ingredients_text: Optional[str] = None
    nutriments: Dict[str, Any] = Field(default_factory=dict)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: Optional[int] = None
    ingredients_list: List[Any] = Field(default_factory=list)
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None
    truthin_score: int
    health_flag: str
    flag_reasons: List[str] = Field(default_factory=list)
    personalized_alerts: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    additives: List[Dict[str, Any]] = Field(default_factory=list)
    is_vegetarian: bool = True
    has_palm_oil: bool = False
    source: str = "local"
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}

class ProductAlternative(BaseModel):
    id: int
    barcode: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    truthin_score: int
    health_flag: str
    score_improvement: int
    flag_reasons: List[str] = Field(default_factory=list)
