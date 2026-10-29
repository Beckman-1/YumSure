from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel

class ScanHistoryItem(BaseModel):
    id: int
    user_id: str
    barcode: str
    product_name: str
    brand: Optional[str] = None
    image_url: Optional[str] = None
    health_flag: str
    truthin_score: int
    is_favorite: bool
    scanned_at: Optional[Union[datetime, str]] = None

    model_config = {"from_attributes": True}

class FavoriteToggleRequest(BaseModel):
    is_favorite: bool
