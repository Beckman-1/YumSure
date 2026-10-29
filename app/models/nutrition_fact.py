import datetime
from datetime import timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class NutritionFact(Base):
    """
    Source nutrition facts recorded directly from product labels or upstream registries.
    Stored independently from any calculated scores or health assessments.
    CRITICAL RULE: Missing values must remain None (NULL), never converted to 0.0.
    """
    __tablename__ = "nutrition_facts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    
    nutrient_name = Column(String(64), nullable=False, index=True) 
    # e.g. "sugars", "sodium", "fat", "saturated_fat", "proteins", "fiber", "energy_kcal", "carbohydrates", "salt"
    
    amount = Column(Float, nullable=True) # None indicates unrecorded/missing data
    unit = Column(String(16), default="g", nullable=False) # "g", "mg", "kcal", "kJ", "mcg"
    
    per_amount = Column(Float, default=100.0, nullable=False) # e.g. 100.0
    per_unit = Column(String(16), default="g", nullable=False) # "g", "ml", "serving"
    reference_basis = Column(String(32), default="per_100g", nullable=False) # "per_100g", "per_serving"
    serving_size = Column(String(64), nullable=True) # e.g. "30g" or "1 packet (70g)"
    
    provenance_source = Column(String(64), default="openfoodfacts", nullable=False)
    retrieved_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)
    verification_status = Column(String(32), default="COMMUNITY", nullable=False) # UNVERIFIED, COMMUNITY, OFFICIAL_MANUFACTURER

    # Relationship
    product = relationship("Product", back_populates="nutrition_facts")
