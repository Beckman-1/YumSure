import datetime
from datetime import timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    """
    Core Product entity recording raw product metadata and identity.
    Source nutrition facts and calculated analyses are linked via separate tables.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    brand = Column(String(255), nullable=True, index=True)
    category = Column(String(255), nullable=True, index=True)
    product_type = Column(String(64), default="food", nullable=False) # food | cosmetic
    image_url = Column(Text, nullable=True)
    
    ingredients_text = Column(Text, nullable=True)
    ingredients_list = Column(JSON, default=list) # Raw list of ingredients as declared
    
    # Data Provenance & Completeness
    source = Column(String(64), default="openfoodfacts", nullable=False) # openfoodfacts | openbeautyfacts | local_seed | user_contributed
    source_url = Column(Text, nullable=True)
    retrieved_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)
    data_completeness_score = Column(Float, default=0.0, nullable=False) # 0.0 to 100.0%
    verification_status = Column(String(32), default="COMMUNITY", nullable=False) # UNVERIFIED, COMMUNITY, OFFICIAL_MANUFACTURER

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), onupdate=lambda: datetime.datetime.now(timezone.utc), nullable=False)

    # Relationships
    nutrition_facts = relationship("NutritionFact", back_populates="product", cascade="all, delete-orphan", lazy="selectin")
    analyses = relationship("NutritionAnalysis", back_populates="product", cascade="all, delete-orphan", lazy="selectin")

    @property
    def latest_analysis(self):
        """Returns the most recent calculated nutrition analysis, if any."""
        if self.analyses:
            return sorted(self.analyses, key=lambda a: a.calculated_at, reverse=True)[0]
        return None

    def get_facts_dict(self) -> dict:
        """Returns source nutrition facts as a key-value dictionary, preserving None for missing nutrients."""
        return {fact.nutrient_name: fact.amount for fact in self.nutrition_facts}
