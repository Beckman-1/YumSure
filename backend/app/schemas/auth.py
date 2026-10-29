from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = "User"
    dietary_preference: str = "any"
    health_goals: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    avoid_additives: bool = True
    avoid_palm_oil: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    name: str
    dietary_preference: str
    health_goals: List[str]
    allergies: List[str]
    avoid_additives: bool
    avoid_palm_oil: bool
    is_active: bool

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
