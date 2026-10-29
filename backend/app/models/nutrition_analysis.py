import datetime
from datetime import timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class NutritionAnalysis(Base):
    """
    Calculated assessments evaluated against a specific, versioned set of scoring rules.
    Retains historical assessments and allows auditing when scoring policies evolve.
    """
    __tablename__ = "nutrition_analyses"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    
    rule_version = Column(String(32), default="2026.1", nullable=False, index=True)
    
    truthin_score = Column(Integer, nullable=False) # 0 to 100
    health_flag = Column(String(32), nullable=False) # GREEN, YELLOW, RED
    nutriscore_grade = Column(String(4), nullable=True) # a, b, c, d, e
    nova_group = Column(Integer, nullable=True) # 1, 2, 3, 4
    
    flag_reasons = Column(JSON, default=list, nullable=False)
    nutrient_breakdown = Column(JSON, default=dict, nullable=False)
    detected_allergens = Column(JSON, default=list, nullable=False)
    detected_additives = Column(JSON, default=list, nullable=False)
    
    is_vegetarian = Column(Boolean, default=True, nullable=False)
    has_palm_oil = Column(Boolean, default=False, nullable=False)
    
    calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)

    # Relationship
    product = relationship("Product", back_populates="analyses")
