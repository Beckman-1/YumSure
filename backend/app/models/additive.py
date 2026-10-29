from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Additive(Base):
    __tablename__ = "additives"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False) # e.g. "INS 621", "E150d"
    name = Column(String(255), nullable=False)
    category = Column(String(128), nullable=False) # Flavor Enhancer, Preservative, Sweetener, Color
    hazard_level = Column(String(32), default="SAFE") # SAFE, CAUTION, AVOID
    description = Column(Text, nullable=True)
    health_concerns = Column(Text, nullable=True)
