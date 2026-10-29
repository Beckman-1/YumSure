from typing import List, Optional
from pydantic import BaseModel, Field

class UserProfileBase(BaseModel):
    name: Optional[str] = "User"
    dietary_preference: Optional[str] = "any" # vegetarian, vegan, non-vegetarian, jain, any
    health_goals: List[str] = Field(default_factory=list) # diabetes_control, weight_loss, low_sodium, heart_healthy
    allergies: List[str] = Field(default_factory=list) # milk, gluten, peanuts, soy, eggs, tree_nuts
    avoid_additives: bool = True
    avoid_palm_oil: bool = False

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: str

    model_config = {"from_attributes": True}
