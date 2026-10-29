from fastapi import APIRouter
from app.api.v1.endpoints import auth, scanner, products, analysis, profile, history

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(scanner.router, prefix="/scanner", tags=["Barcode Scanner"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Ingredient Analysis"])
api_router.include_router(profile.router, prefix="/profile", tags=["User Health Profile"])
api_router.include_router(history.router, prefix="/history", tags=["Scan History"])
