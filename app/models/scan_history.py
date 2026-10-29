import datetime
from datetime import timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScanHistory(Base):
    """
    User-specific scan log.
    Ensures users can access only their own records.
    """
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("user_profiles.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    
    barcode = Column(String(64), index=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    image_url = Column(Text, nullable=True)
    health_flag = Column(String(32), default="YELLOW", nullable=False)
    truthin_score = Column(Integer, default=50, nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)
    scanned_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc), nullable=False)

    # Relationship
    user = relationship("UserProfile", back_populates="scan_history")
