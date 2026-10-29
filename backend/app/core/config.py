import os
from typing import List

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "TruthIn Backend API")
    VERSION: str = os.getenv("VERSION", "2.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/truthin_db"
    )
    SYNC_DATABASE_URL: str = os.getenv(
        "SYNC_DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/truthin_db"
    )
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")
    
    # Security & JWT Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "truthin_super_secret_jwt_key_change_in_production_98374")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # External APIs
    OPEN_FOOD_FACTS_API: str = os.getenv(
        "OPEN_FOOD_FACTS_API", 
        "https://world.openfoodfacts.org/api/v2"
    )
    OPEN_BEAUTY_FACTS_API: str = os.getenv(
        "OPEN_BEAUTY_FACTS_API", 
        "https://world.openbeautyfacts.org/api/v2"
    )
    USER_AGENT: str = os.getenv(
        "USER_AGENT", 
        "TruthIn-Clone/2.0 (contact: info@yumsure.app)"
    )
    
    # Cache & Freshness Settings
    STALE_AFTER_DAYS: int = int(os.getenv("STALE_AFTER_DAYS", "30"))
    NEGATIVE_CACHE_TTL_SEC: int = int(os.getenv("NEGATIVE_CACHE_TTL_SEC", "300")) # 5 mins
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

settings = Settings()
