import datetime
from datetime import timezone
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserProfile(Base):
    """
    User Account & Health Profile.
    Stores authentication credentials along with personal dietary preferences,
    health goals, and allergen watchlists for personalized product evaluation.
    """
    __tablename__ = "user_profiles"

    id = Column(String(64), primary_key=True) # UUID string or identifier
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    name = Column(String(128), default="User", nullable=False)
    
    # Dietary & Health Preferences
    dietary_preference = Column(String(64), default="any", nullable=False) # vegetarian, vegan, non-vegetarian, jain, any
    health_goals = Column(JSON, default=list, nullable=False) # ["diabetes_control", "weight_loss", "low_sodium", "heart_healthy", "clean_eating"]
    allergies = Column(JSON, default=list, nullable=False) # ["milk", "gluten", "peanuts", "soy", "eggs", "tree_nuts"]
    avoid_additives = Column(Boolean, default=True, nullable=False)
    avoid_palm_oil = Column(Boolean, default=False, nullable=False)
    
    # Account status & Timestamps
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), onupdate=lambda: datetime.datetime.now(timezone.utc), nullable=False)

    # Relationships
    scan_history = relationship("ScanHistory", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
